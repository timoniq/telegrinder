import dataclasses
import typing
from collections import defaultdict

from fntypes.option import Some
from fntypes.result import Error, Ok, Result

from telegrinder.bot.dispatch.context import Context
from telegrinder.modules import logger
from telegrinder.node.base import (
    AnyNode,
    ComposeError,
    IsNode,
    Name,
    NodeClass,
    NodeScope,
    as_node,
    unwrap_node,
)
from telegrinder.tools.aio import maybe_awaitable
from telegrinder.tools.fullname import fullname
from telegrinder.tools.global_context.builtin_context import TelegrinderContext
from telegrinder.tools.magic import bundle, get_func_annotations, join_dicts

type AsyncGenerator = typing.AsyncGenerator[typing.Any, None]
type Impls = dict[type[typing.Any], type[typing.Any]]

CONTEXT_STORE_NODES_KEY: typing.Final[str] = "_node_ctx"
GLOBAL_VALUE_KEY: typing.Final[str] = "_value"
NODE_SCOPE_KEY: typing.Final[str] = "scope"


def get_scope(node: IsNode, /) -> NodeScope | None:
    return getattr(node, NODE_SCOPE_KEY, None)


def get_impls(
    compose_function: typing.Callable[..., typing.Any],
    impls: Impls,
    /,
) -> dict[str, typing.Any]:
    return {
        key: impls[tp]
        for key, annotation in get_func_annotations(compose_function).items()
        if typing.get_origin(annotation) is type
        and (typing.get_origin(tp := typing.get_args(annotation)[0]) or tp) in impls
    }


async def compose_node(
    node: IsNode,
    linked: dict[type[typing.Any], typing.Any],
    data: dict[type[typing.Any], typing.Any] | None = None,
    impls: Impls | None = None,
) -> "NodeSession":
    subnodes = node.get_subnodes()
    compose_bundle = bundle(node.compose, join_dicts(subnodes, linked), bundle_kwargs=True)
    kwargs = compose_bundle.kwargs.copy()

    if data:
        compose_type_bundle = bundle(node.compose, data, typebundle=True)
        kwargs |= compose_type_bundle.kwargs

    if impls:
        compose_impls_bundle = bundle(node.compose, get_impls(node.compose, impls))
        kwargs |= compose_impls_bundle.kwargs

    compose_result = node.compose(**kwargs)
    if node.is_generator():
        generator = typing.cast("AsyncGenerator", compose_result)
        value = await generator.asend(None)
    else:
        generator = None
        value = await maybe_awaitable(compose_result)

    return NodeSession(node, value, subnodes={}, generator=generator)


async def compose_nodes(
    nodes: typing.Mapping[str, AnyNode],
    ctx: Context,
    data: dict[type[typing.Any], typing.Any] | None = None,
    impls: Impls | None = None,
) -> Result["NodeCollection", ComposeError]:
    logger.debug("Composing nodes ({})...", ", ".join(f"{k}: {fullname(v)}" for k, v in nodes.items()))

    impls = impls or CONTEXT.composer.unwrap().selected_impls
    data = {Context: ctx} | (data or {})
    parent_nodes = dict[IsNode, NodeSession]()
    event_nodes: dict[IsNode, NodeSession] = ctx.get_or_set(CONTEXT_STORE_NODES_KEY, {})
    unwrapped_nodes = {(key, n := (as_node(node)), node): unwrap_node(n) for key, node in nodes.items()}

    for (parent_node_name, parent_node_t, parent_original_type), linked_nodes in unwrapped_nodes.items():
        local_nodes = dict[IsNode, NodeSession]()
        subnodes = {}
        data[Name] = parent_node_name
        data[NodeClass] = parent_original_type

        for node_t in linked_nodes:
            node_t = as_node(node_t)
            scope = get_scope(node_t)

            if scope is NodeScope.PER_EVENT and node_t in event_nodes:
                local_nodes[node_t] = event_nodes[node_t]
                continue
            elif scope is NodeScope.GLOBAL and hasattr(node_t, GLOBAL_VALUE_KEY):
                local_nodes[node_t] = NodeSession(node_t, getattr(node_t, GLOBAL_VALUE_KEY), {})
                continue

            subnodes |= {
                k: session.value for k, session in (local_nodes | event_nodes).items() if k not in subnodes
            }
            try:
                local_nodes[node_t] = await compose_node(node_t, linked=subnodes, data=data, impls=impls)
            except ComposeError as exc:
                for t, local_node in local_nodes.items():
                    if get_scope(t) is NodeScope.PER_CALL:
                        await local_node.close()
                return Error(ComposeError(f"Cannot compose {fullname(node_t)}, error: {exc.message!r}"))

            if scope is NodeScope.PER_EVENT:
                event_nodes[node_t] = local_nodes[node_t]
            elif scope is NodeScope.GLOBAL:
                setattr(node_t, GLOBAL_VALUE_KEY, local_nodes[node_t].value)

        parent_nodes[parent_node_t] = local_nodes[parent_node_t]

    return Ok(NodeCollection({k: parent_nodes[t] for k, t, _ in unwrapped_nodes}))


@dataclasses.dataclass(slots=True, repr=False)
class NodeSession:
    node: IsNode | None
    value: typing.Any
    subnodes: dict[str, typing.Self]
    generator: typing.AsyncGenerator[typing.Any, typing.Any | None] | None = None

    def __repr__(self) -> str:
        return f"<{type(self).__name__}: {self.value!r}" + (" (ACTIVE)>" if self.generator else ">")

    async def close(
        self,
        with_value: typing.Any | None = None,
        scopes: tuple[NodeScope, ...] = (NodeScope.PER_CALL,),
    ) -> None:
        if self.node is not None and get_scope(self.node) not in scopes:
            return

        for subnode in self.subnodes.values():
            await subnode.close(scopes=scopes)

        if self.generator is None:
            return
        try:
            logger.debug("Closing session for node {}...", fullname(self.node))
            await self.generator.asend(with_value)
        except StopAsyncIteration:
            self.generator = None


class NodeCollection:
    __slots__ = ("sessions", "_values")

    def __init__(self, sessions: dict[str, NodeSession]) -> None:
        self.sessions = sessions
        self._values: dict[str, typing.Any] = {}

    def __repr__(self) -> str:
        return "<{}: sessions={!r}>".format(self.__class__.__name__, self.sessions)

    @property
    def values(self) -> dict[str, typing.Any]:
        if self._values.keys() == self.sessions.keys():
            return self._values

        for name, session in self.sessions.items():
            if name not in self._values:
                self._values[name] = session.value

        return self._values

    async def close_all(
        self,
        with_value: typing.Any | None = None,
        scopes: tuple[NodeScope, ...] = (NodeScope.PER_CALL,),
    ) -> None:
        for session in self.sessions.values():
            await session.close(with_value, scopes=scopes)


class Composer:
    impls: dict[type[typing.Any], set[typing.Any]]
    selected_impls: Impls

    def __init__(self) -> None:
        self.impls = defaultdict(set)
        self.selected_impls = dict()

    def __setitem__(self, for_type: typing.Any, impl: type[typing.Any], /) -> None:
        for_type = typing.get_origin(for_type) or for_type

        if for_type not in self.impls:
            raise LookupError(f"No impls defined for type of `{fullname(for_type)}`.")

        if (typing.get_origin(impl) or impl) not in self.impls[for_type]:
            raise LookupError(f"Impl `{fullname(impl)}` is not defined for type of `{fullname(for_type)}`.")

        self.selected_impls[typing.get_origin(for_type) or for_type] = impl

    def impl[T](self, for_type: typing.Any, /) -> typing.Callable[[type[T]], type[T]]:
        def decorator(impl: type[T], /) -> type[T]:
            self.impls[typing.get_origin(for_type) or for_type].add(impl)
            return impl

        return decorator

    async def compose_nodes(
        self,
        nodes: typing.Mapping[str, AnyNode],
        ctx: Context,
        data: dict[type[typing.Any], typing.Any] | None = None,
    ) -> Result[NodeCollection, ComposeError]:
        return await compose_nodes(nodes, ctx, data, self.selected_impls)


CONTEXT = TelegrinderContext()
CONTEXT.composer = Some(Composer())


__all__ = ("NodeCollection", "NodeSession", "compose_node", "compose_nodes")
