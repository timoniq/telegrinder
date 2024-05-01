import typing

from telegrinder.bot.cute_types import UpdateCute
from telegrinder.node import Node


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

    def values(self) -> dict[str, typing.Any]:
        return {name: session.value for name, session in self.sessions.items()}
    
    async def close_all(self, with_value: typing.Any | None = None) -> None:
        for session in self.sessions.values():
            await session.close(with_value)


async def compose_node(
    node: type[Node],
    update: UpdateCute,
    ready_context: dict[str, NodeSession] | None = None,
) -> NodeSession:
    _node = node.as_node()
    context = NodeCollection(ready_context.copy() if ready_context else {})

    for name, subnode in _node.get_sub_nodes().items():
        if subnode is UpdateCute:
            context.sessions[name] = NodeSession(update, {})
        else:
            context.sessions[name] = await compose_node(subnode, update)

    generator: typing.AsyncGenerator | None

    if _node.is_generator():
        generator = typing.cast(typing.AsyncGenerator, _node.compose(**context.values()))
        value = await generator.asend(None)
    else:
        generator = None
        value = await _node.compose(**context.values())  # type: ignore
    
    return NodeSession(value, context.sessions, generator)


__all__ = ("NodeCollection", "NodeSession", "compose_node")
