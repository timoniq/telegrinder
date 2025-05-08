import dataclasses
import typing

from fntypes.result import Error, Ok, Result

from telegrinder.bot.dispatch.context import Context
from telegrinder.modules import logger
from telegrinder.node.base import (
    ComposeError,
    IsNode,
    Name,
    NodeImpersonation,
    NodeScope,
    NodeType,
    unwrap_node,
)
from telegrinder.tools.aio import maybe_awaitable
from telegrinder.tools.magic import bundle, join_dicts

type AsyncGenerator = typing.AsyncGenerator[typing.Any, None]

CONTEXT_STORE_NODES_KEY = "_node_ctx"
GLOBAL_VALUE_KEY = "_value"


def get_scope(node: type[NodeType], /) -> NodeScope | None:
    return getattr(node, "scope", None)


async def compose_node(
    node: type[NodeType],
    linked: dict[type[typing.Any], typing.Any],
    data: dict[type[typing.Any], typing.Any] | None = None,
) -> "NodeSession":
    subnodes = node.get_subnodes()
    compose_bundle = bundle(node.compose, join_dicts(subnodes, linked), bundle_kwargs=True)
    args = compose_bundle.args
    kwargs = compose_bundle.kwargs.copy()

    # Linking data via typebundle
    if data:
        compose_type_bundle = bundle(node.compose, data, typebundle=True)
        args += compose_type_bundle.args
        kwargs |= compose_type_bundle.kwargs

    compose_result = node.compose(*args, **kwargs)
    if node.is_generator():
        generator = typing.cast("AsyncGenerator", compose_result)
        value = await generator.asend(None)
    else:
        generator = None
        value = await maybe_awaitable(compose_result)

    return NodeSession(node, value, subnodes={}, generator=generator)


async def compose_nodes(
    nodes: typing.Mapping[str, IsNode | NodeImpersonation],
    ctx: Context,
    data: dict[type[typing.Any], typing.Any] | None = None,
) -> Result["NodeCollection", ComposeError]:
    logger.debug("Composing nodes: ({})...", " ".join(f"{k}={v!r}" for k, v in nodes.items()))

    data = {Context: ctx} | (data or {})
    parent_nodes = dict[IsNode, NodeSession]()
    event_nodes: dict[IsNode, NodeSession] = ctx.get_or_set(CONTEXT_STORE_NODES_KEY, {})
    unwrapped_nodes = {(key, n := node.as_node()): unwrap_node(n) for key, node in nodes.items()}

    for (parent_node_name, parent_node_t), linked_nodes in unwrapped_nodes.items():
        local_nodes = dict[type[NodeType], NodeSession]()
        subnodes = {}
        data[Name] = parent_node_name

        for node_t in linked_nodes:
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
                local_nodes[node_t] = await compose_node(node_t, linked=subnodes, data=data)
            except ComposeError as exc:
                for t, local_node in local_nodes.items():
                    if get_scope(t) is NodeScope.PER_CALL:
                        await local_node.close()
                return Error(ComposeError(f"Cannot compose {node_t!r}, error: {str(exc)}"))

            if scope is NodeScope.PER_EVENT:
                event_nodes[node_t] = local_nodes[node_t]
            elif scope is NodeScope.GLOBAL:
                setattr(node_t, GLOBAL_VALUE_KEY, local_nodes[node_t].value)

        parent_nodes[parent_node_t] = local_nodes[parent_node_t]

    return Ok(NodeCollection({k: parent_nodes[t] for k, t in unwrapped_nodes}))


@dataclasses.dataclass(slots=True, repr=False)
class NodeSession:
    node_type: type[NodeType] | None
    value: typing.Any
    subnodes: dict[str, typing.Self]
    generator: typing.AsyncGenerator[typing.Any, typing.Any | None] | None = None

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.value!r}" + (" (ACTIVE)>" if self.generator else ">")

    async def close(
        self,
        with_value: typing.Any | None = None,
        scopes: tuple[NodeScope, ...] = (NodeScope.PER_CALL,),
    ) -> None:
        if self.node_type and getattr(self.node_type, "scope", None) not in scopes:
            return

        for subnode in self.subnodes.values():
            await subnode.close(scopes=scopes)

        if self.generator is None:
            return
        try:
            logger.debug("Closing session for node {!r}...", self.node_type)
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


__all__ = ("NodeCollection", "NodeSession", "compose_node", "compose_nodes")
