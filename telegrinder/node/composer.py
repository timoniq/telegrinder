import typing

from telegrinder.bot.cute_types import UpdateCute
from telegrinder.node import ComposeError, Node
from telegrinder.tools.magic import get_annotations, magic_bundle


async def compose_node(
    _node: type[Node], update: UpdateCute, ready_context: dict[str, "NodeSession"] | None = None
) -> "NodeSession":
    node = _node.as_node()

    context = NodeCollection(ready_context.copy() if ready_context else {})

    for name, subnode in node.get_sub_nodes().items():
        if subnode is UpdateCute:
            context.sessions[name] = NodeSession(update, {})
        else:
            context.sessions[name] = await compose_node(subnode, update)

    generator: typing.AsyncGenerator | None

    if node.is_generator():
        generator = typing.cast(typing.AsyncGenerator, node.compose(**context.values()))
        value = await generator.asend(None)
    else:
        generator = None
        value = await node.compose(**context.values())  # type: ignore

    return NodeSession(value, context.sessions, generator)


async def compose_nodes(
    node_types: dict[str, type[Node]], update: UpdateCute
) -> typing.Optional["NodeCollection"]:
    nodes: dict[str, NodeSession] = {}
    for name, node_t in node_types.items():
        try:
            nodes[name] = await compose_node(node_t, update)
        except ComposeError:
            await NodeCollection(nodes).close_all()
            return None
    return NodeCollection(nodes)


class NodeSession:
    def __init__(
        self,
        value: typing.Any,
        subnodes: dict[str, typing.Self],
        generator: typing.AsyncGenerator[typing.Any, None] | None = None,
    ):
        self.value = value
        self.subnodes = subnodes
        self.generator = generator

    async def close(self, with_value: typing.Any | None = None) -> None:
        for subnode in self.subnodes.values():
            await subnode.close()

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

    async def close_all(self, with_value: typing.Any | None = None) -> None:
        for session in self.sessions.values():
            await session.close(with_value)


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

    async def compose_nodes(self, update: UpdateCute) -> NodeCollection | None:
        return await compose_nodes(self.nodes, update)

    async def __call__(self, **kwargs: typing.Any) -> typing.Any:
        return await self.func(**magic_bundle(self.func, kwargs, start_idx=0, bundle_ctx=False))  # type: ignore


__all__ = ("NodeCollection", "NodeSession", "Composition", "compose_node", "compose_nodes")
