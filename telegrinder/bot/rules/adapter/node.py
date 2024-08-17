import typing_extensions as typing
from fntypes.result import Error, Ok, Result

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.rules.adapter.abc import ABCAdapter, Event
from telegrinder.bot.rules.adapter.errors import AdapterError
from telegrinder.bot.rules.adapter.raw_update import RawUpdateAdapter
from telegrinder.msgspec_utils import repr_type
from telegrinder.node.base import ComposeError
from telegrinder.node.composer import NodeSession, compose_node
from telegrinder.types.objects import Update

if typing.TYPE_CHECKING:
    from telegrinder.node.base import Node

Ts = typing.TypeVarTuple("Ts", default=typing.Unpack[tuple[type["Node"], ...]])


class NodeAdapter(typing.Generic[*Ts], ABCAdapter[Update, Event[tuple[*Ts]]]):
    ADAPTED_VALUE_KEY: str = "_adapted_update_cute"

    def __init__(self, *nodes: *Ts) -> None:
        self.nodes = nodes
        self.raw_update_adapter = RawUpdateAdapter()

    def __repr__(self) -> str:
        return "<{}: adapt Update -> UpdateCute -> ({})>".format(
            self.__class__.__name__,
            ", ".join(repr_type(node) for node in self.nodes),
        )

    async def adapt(
        self,
        api: ABCAPI,
        update: Update,
        context: Context,
    ) -> Result[Event[tuple[*Ts]], AdapterError]:
        match await self.raw_update_adapter.adapt(api, update, context):
            case Ok(update_cute):
                update_cute = update_cute
            case Error(_) as err:
                return err

        node_sessions: list[NodeSession] = []
        for node_t in self.nodes:
            try:
                node_sessions.append(
                    await compose_node(typing.cast(type["Node"], node_t), update_cute, context),
                )
            except ComposeError:
                for session in node_sessions:
                    await session.close(with_value=None)
                return Error(AdapterError(f"Couldn't compose nodes, error on {node_t!r}."))

        return Ok(Event(tuple(node_sessions)))  # type: ignore


__all__ = ("NodeAdapter",)
