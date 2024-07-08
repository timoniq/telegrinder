import typing

from fntypes.result import Error, Ok, Result

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.cute_types.update import UpdateCute
from telegrinder.bot.rules.adapter.abc import ABCAdapter
from telegrinder.bot.rules.adapter.errors import AdapterError
from telegrinder.node.base import ComposeError, Node
from telegrinder.node.composer import NodeSession, compose_node
from telegrinder.types.objects import Update

NodeT = typing.TypeVar("NodeT", bound=Node)
Ts = typing.TypeVarTuple("Ts")


class NodeAdapter(typing.Generic[*Ts], ABCAdapter[Update, tuple[*Ts]]):
    def __init__(self, *nodes: *Ts) -> None:
        self.nodes = nodes

    async def adapt(self, api: ABCAPI, update: Update) -> Result[tuple[*Ts], AdapterError]:
        update_cute = UpdateCute.from_update(update, api)
        node_sessions: list[NodeSession] = []
        for node_t in self.nodes:
            try:
                node_sessions.append(await compose_node(node_t, update_cute))  # type: ignore
            except ComposeError:
                for session in node_sessions:
                    await session.close(with_value=None)
                return Error(AdapterError(f"Couldn't compose nodes, error on {node_t}"))
        return Ok(tuple(node_sessions))  # type: ignore
