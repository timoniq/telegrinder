import dataclasses
import inspect
import typing

from fntypes.error import UnwrapError
from fntypes.result import Error, Ok, Result

from telegrinder.bot.dispatch.context import Context
from telegrinder.modules import logger
from telegrinder.node.base import (
    ComposeError,
    Name,
    Node,
    NodeScope,
    get_node_calc_lst,
)
from telegrinder.tools.magic import magic_bundle, join_dicts

CONTEXT_STORE_NODES_KEY = "_node_ctx"
GLOBAL_VALUE_KEY = "_value"


async def compose_node(
    _node: type[Node],
    linked: dict[type[typing.Any], typing.Any],
    data: dict[type[typing.Any], typing.Any] | None = None,
) -> "NodeSession":
    node = _node.as_node()

    subnodes = node.get_subnodes()
    kwargs = magic_bundle(node.compose, join_dicts(subnodes, linked))

    if data is not None:
        # Linking data via typebundle
        kwargs.update(
            magic_bundle(node.compose, data, typebundle=True)
        )

    if node.is_generator():
        generator = typing.cast(typing.AsyncGenerator[typing.Any, None], node.compose(**kwargs))
        value = await generator.asend(None)
    else:
        generator = None
        value = typing.cast(typing.Awaitable[typing.Any] | typing.Any, node.compose(**kwargs))
        if inspect.isawaitable(value):
            value = await value

    return NodeSession(_node, value, {}, generator)


async def compose_nodes(
    nodes: dict[str, type[Node]],
    ctx: Context,
    data: dict[type[typing.Any], typing.Any] | None = None,
) -> Result["NodeCollection", ComposeError]:
    logger.debug("Composing nodes: ({})...", " ".join(f"{k}={v.__qualname__}" for k, v in nodes.items()))

    local_nodes: dict[type[Node], NodeSession]
    data = {Context: ctx} | (data or {})
    parent_nodes: dict[type[Node], NodeSession] = {}
    event_nodes: dict[type[Node], NodeSession] = ctx.get_or_set(CONTEXT_STORE_NODES_KEY, {})
    # TODO: optimize flattened list calculation via caching key = tuple of node types
    calculation_nodes: dict[tuple[str, type[Node]], tuple[type[Node], ...]] = {
        (node_name, node_t): tuple(get_node_calc_lst(node_t)) for node_name, node_t in nodes.items()
    }

    for (parent_node_name, parent_node_t), linked_nodes in calculation_nodes.items():
        local_nodes = {}
        subnodes = {}
        data[Name] = parent_node_name

        for node_t in linked_nodes:
            scope = getattr(node_t, "scope", None)

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
            except (ComposeError, UnwrapError) as exc:
                for t, local_node in local_nodes.items():
                    if t.scope is NodeScope.PER_CALL:
                        await local_node.close()
                return Error(ComposeError(f"Cannot compose {node_t}. Error: {exc}"))

            if scope is NodeScope.PER_EVENT:
                event_nodes[node_t] = local_nodes[node_t]
            elif scope is NodeScope.GLOBAL:
                setattr(node_t, GLOBAL_VALUE_KEY, local_nodes[node_t].value)

        parent_nodes[parent_node_t] = local_nodes[parent_node_t]

    node_sessions = {k: parent_nodes[t] for k, t in nodes.items()}
    return Ok(NodeCollection(node_sessions))


@dataclasses.dataclass(slots=True, repr=False)
class NodeSession:
    node_type: type[Node] | None
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
