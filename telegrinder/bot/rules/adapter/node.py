import typing

from fntypes.result import Error, Ok, Result

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.cute_types.update import UpdateCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.rules.adapter.abc import ABCAdapter, Event
from telegrinder.bot.rules.adapter.errors import AdapterError
from telegrinder.node.base import ComposeError
from telegrinder.node.composer import NodeSession, compose_node
from telegrinder.types.objects import Update

Ts = typing.TypeVarTuple("Ts")


class NodeAdapter(typing.Generic[*Ts], ABCAdapter[Update, Event[tuple[*Ts]]]):
    def __init__(self, *nodes: *Ts) -> None:
        self.nodes = nodes

    def __repr__(self) -> str:
        return "<{}: adapt Update -> {}>".format(
            self.__class__.__name__,
            Update.__name__,
            ", ".join(node.__name__ for node in self.nodes),  # type: ignore
        )

    async def adapt(self, api: ABCAPI, update: Update) -> Result[Event[tuple[*Ts]], AdapterError]:
        update_cute = UpdateCute.from_update(update, api)
        node_sessions: list[NodeSession] = []
        for node_t in self.nodes:
            try:
                # FIXME: adapters should have context
                node_sessions.append(await compose_node(node_t, update_cute, Context(raw_update=update)))  # type: ignore
            except ComposeError:
                for session in node_sessions:
                    await session.close(with_value=None)
                return Error(AdapterError(f"Couldn't compose nodes, error on {node_t!r}"))
        return Ok(Event(tuple(node_sessions)))  # type: ignore


__all__ = ("NodeAdapter",)
