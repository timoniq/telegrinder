import types
import typing
from collections import defaultdict
from functools import cached_property

from fntypes.library.monad.option import Some
from fntypes.library.monad.result import Error, Ok, Result

from telegrinder.bot.dispatch.context import Context
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
from telegrinder.node.context import get_global_session, set_global_session
from telegrinder.node.scope import get_scope
from telegrinder.node.session import NodeSession, close_sessions
from telegrinder.tools.aio import Generator, maybe_awaitable, next_generator
from telegrinder.tools.fullname import fullname
from telegrinder.tools.global_context.builtin_context import TelegrinderContext
from telegrinder.tools.magic import bundle, get_func_annotations, join_dicts

type ComposeGenerator = Generator[typing.Any, typing.Any, typing.Any]
type Impls = dict[type[typing.Any], type[typing.Any]]

CONTEXT_STORE_NODES_KEY: typing.Final[str] = "_node_ctx"
GLOBAL_VALUE_KEY: typing.Final[str] = "_value"
TELEGRINDER_CONTEXT: typing.Final[TelegrinderContext] = TelegrinderContext()


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
    compose = bundle(node.compose, join_dicts(subnodes, linked), bundle_kwargs=True)

    if data:
        compose &= bundle(node.compose, data, typebundle=True)

    if impls:
        compose &= bundle(node.compose, get_impls(node.compose, impls))

    result = compose()
    if node.is_generator():
        generator = typing.cast("ComposeGenerator", result)
        value = await next_generator(generator)
    else:
        generator = None
        value = await maybe_awaitable(result)

    return NodeSession(node, value, generator)


async def compose_nodes(
    nodes: typing.Mapping[str, AnyNode],
    ctx: Context,
    data: dict[type[typing.Any], typing.Any] | None = None,
    impls: Impls | None = None,
) -> Result["NodeCollection", ComposeError]:
    impls = impls or TELEGRINDER_CONTEXT.composer.unwrap().selected_impls
    data = {Context: ctx} | (data or {})
    parent_nodes = dict[IsNode, NodeSession]()
    event_nodes: dict[IsNode, NodeSession] = ctx.get_or_set(CONTEXT_STORE_NODES_KEY, {})
    unwrapped_nodes = {(key, n := (as_node(node)), node): unwrap_node(n) for key, node in nodes.items()}

    for (parent_node_name, parent_node_t, parent_original_type), linked_nodes in unwrapped_nodes.items():
        data.update({Name: parent_node_name, NodeClass: parent_original_type})

        local_nodes = LocalNodeCollection()
        subnodes = dict[typing.Any, typing.Any]()

        for node_t in linked_nodes:
            node_t = as_node(node_t)
            scope = get_scope(node_t)

            if scope is NodeScope.PER_EVENT and node_t in event_nodes:
                local_nodes[node_t] = event_nodes[node_t]
                continue

            if scope is NodeScope.GLOBAL and (global_session := get_global_session(node_t)) is not None:
                local_nodes[node_t] = global_session
                continue

            subnodes |= {
                k: session.value for k, session in (local_nodes | event_nodes).items() if k not in subnodes
            }
            try:
                session = await local_nodes.set_session(
                    node_t,
                    await compose_node(node_t, linked=subnodes, data=data, impls=impls),
                    scope,
                )
            except ComposeError as error:
                await close_sessions(local_nodes)
                return Error(ComposeError(f"Cannot compose node `{fullname(node_t)}`, error: {error.message!r}"))

            if scope is NodeScope.PER_EVENT:
                event_nodes[node_t] = session
            elif scope is NodeScope.GLOBAL:
                set_global_session(node_t, session)

        parent_session = local_nodes.pop(parent_node_t)
        parent_session.subsessions |= local_nodes
        parent_nodes[parent_node_t] = parent_session

    return Ok(NodeCollection(sessions={k: parent_nodes[t] for k, t, _ in unwrapped_nodes}))


class LocalNodeCollection(dict[IsNode, NodeSession]):
    def __init__(self) -> None:
        super().__init__()

    async def set_session(
        self,
        node: IsNode,
        session: NodeSession,
        scope: NodeScope,
        /,
    ) -> NodeSession:
        # Close old per call session when rewriting with new one
        if node in self and scope is NodeScope.PER_CALL:
            await self[node].close()

        self[node] = session
        return session


class NodeCollection:
    def __init__(self, sessions: dict[str, NodeSession]) -> None:
        self.sessions = sessions

    def __repr__(self) -> str:
        return "<{}: sessions={!r}>".format(type(self).__name__, self.sessions)

    @cached_property
    def values(self) -> types.MappingProxyType[str, typing.Any]:
        return types.MappingProxyType({name: session.value for name, session in self.sessions.items()})

    async def close_all(
        self,
        with_value: typing.Any | None = None,
        scopes: tuple[NodeScope, ...] = (NodeScope.PER_CALL,),
    ) -> None:
        await close_sessions(
            {session.node: session for session in self.sessions.values()},
            scopes=scopes,
            with_value=with_value,
            reverse=False,  # Do not reverse the order of sessions, because the order in NodeCollection is already correct
        )


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

        self.selected_impls[for_type] = impl

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


TELEGRINDER_CONTEXT.composer = Some(Composer())


__all__ = ("Composer", "NodeCollection", "compose_node", "compose_nodes")
