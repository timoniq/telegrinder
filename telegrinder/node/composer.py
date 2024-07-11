import typing

from telegrinder.bot.cute_types import UpdateCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.node.base import ComposeError, Node
from telegrinder.node.scope import NodeScope
from telegrinder.tools.magic import get_annotations, magic_bundle

CONTEXT_STORE_NODES_KEY = "node_ctx"


async def compose_node(
    _node: type[Node],
    update: UpdateCute,
    ctx: Context,
) -> "NodeSession":
    node = _node.as_node()
    context = NodeCollection({})
    node_ctx: dict[type[Node], "NodeSession"] = ctx.get_or_set(CONTEXT_STORE_NODES_KEY, {})

    for name, subnode in node.get_sub_nodes().items():
        if subnode in node_ctx:
            context.sessions[name] = node_ctx[subnode]
        elif subnode is UpdateCute:
            context.sessions[name] = NodeSession(None, update, {})
        elif subnode is Context:
            context.sessions[name] = NodeSession(None, ctx, {})
        else:
            context.sessions[name] = await compose_node(subnode, update, ctx)

            if getattr(_node, "scope", None) is NodeScope.PER_EVENT:
                node_ctx[_node] = context.sessions[name]

    generator: typing.AsyncGenerator | None

    if node.is_generator():
        generator = typing.cast(typing.AsyncGenerator, node.compose(**context.values()))
        value = await generator.asend(None)
    else:
        generator = None
        value = await node.compose(**context.values())  # type: ignore

    return NodeSession(_node, value, context.sessions, generator)


async def compose_nodes(
    node_types: dict[str, type[Node]],
    update: UpdateCute,
    ctx: Context,
) -> typing.Optional["NodeCollection"]:
    nodes: dict[str, NodeSession] = {}
    node_ctx: dict[type[Node], "NodeSession"] = ctx.get_or_set(CONTEXT_STORE_NODES_KEY, {})

    for name, node_t in node_types.items():
        scope = getattr(node_t, "scope", None)
        try:
            if scope is NodeScope.PER_EVENT and node_t in node_ctx:
                nodes[name] = node_ctx[node_t]
                continue

            nodes[name] = await compose_node(
                node_t,
                update,
                ctx,
            )
            if scope is NodeScope.PER_EVENT:
                node_ctx[node_t] = nodes[name]
        except ComposeError:
            await NodeCollection(nodes).close_all()
            return None
    return NodeCollection(nodes)


class NodeSession:
    def __init__(
        self,
        node_type: type[Node] | None,
        value: typing.Any,
        subnodes: dict[str, typing.Self],
        generator: typing.AsyncGenerator[typing.Any, None] | None = None,
    ):
        self.node_type = node_type
        self.value = value
        self.subnodes = subnodes
        self.generator = generator

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
            await self.generator.asend(with_value)
        except StopAsyncIteration:
            self.generator = None

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.value}" + ("ACTIVE>" if self.generator else ">")


class NodeCollection:
    def __init__(self, sessions: dict[str, NodeSession]) -> None:
        self.sessions = sessions

    def __repr__(self) -> str:
        return "<{}: sessions={}>".format(self.__class__.__name__, self.sessions)

    def values(self) -> dict[str, typing.Any]:
        return {name: session.value for name, session in self.sessions.items()}

    async def close_all(
        self,
        with_value: typing.Any | None = None,
        scopes: tuple[NodeScope, ...] = (NodeScope.PER_CALL,),
    ) -> None:
        for session in self.sessions.values():
            await session.close(with_value, scopes=scopes)


class Composition:
    nodes: dict[str, type[Node]]

    def __init__(self, func: typing.Callable[..., typing.Any], is_blocking: bool) -> None:
        self.func = func
        self.nodes = get_annotations(func)
        self.is_blocking = is_blocking

    def __repr__(self) -> str:
        return "<{}: for function={!r} with nodes={}>".format(
            ("blocking " if self.is_blocking else "") + self.__class__.__name__,
            self.func.__name__,
            self.nodes,
        )

    async def compose_nodes(self, update: UpdateCute, context: Context) -> NodeCollection | None:
        return await compose_nodes(self.nodes, update, context)

    async def __call__(self, **kwargs: typing.Any) -> typing.Any:
        return await self.func(**magic_bundle(self.func, kwargs, start_idx=0, bundle_ctx=False))  # type: ignore


__all__ = ("NodeCollection", "NodeSession", "Composition", "compose_node", "compose_nodes")
