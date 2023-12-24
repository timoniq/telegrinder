import typing

from telegrinder.bot.cute_types import UpdateCute
from telegrinder.node import Node


class NodeSession:
    def __init__(
            self, 
            value: typing.Any,
            subnodes: dict[str, "NodeSession"],
            generator: typing.AsyncGenerator[typing.Any, None] | None = None,
        ):
        self.value = value
        self.subnodes = subnodes
        self.generator = generator
    
    async def close(self) -> None:
        for subnode in self.subnodes.values():
            await subnode.close()
        
        if self.generator is None:
            return
        try:
            await self.generator.asend(None)
        except StopAsyncIteration:
            self.generator = None


class NodeCollection:
    def __init__(self, sessions: dict[str, NodeSession]) -> None:
        self.sessions = sessions

    def values(self) -> dict[str, typing.Any]:
        return {name: session.value for name, session in self.sessions.items()}
    
    async def close_all(self) -> None:
        for session in self.sessions.values():
            await session.close()



async def compose_node(_node: type[Node], update: UpdateCute, ready_context: dict[str, NodeSession] | None = None) -> NodeSession:
    node = _node.as_node()

    context = NodeCollection(ready_context.copy() if ready_context else {})

    for name, subnode in node.get_sub_nodes().items():
        if subnode is UpdateCute:
            context.sessions[name] = NodeSession(update, {})
        else:
            context.sessions[name] = await compose_node(subnode, update, context.sessions)

    generator: typing.AsyncGenerator | None

    if node.is_generator():
        generator = typing.cast(typing.AsyncGenerator, node.compose(**context.values()))
        value = await generator.asend(None)
    else:
        generator = None
        value = await node.compose(**context.values())  # type: ignore
    
    return NodeSession(value, context.sessions, generator)

