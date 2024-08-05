import dataclasses

import typing_extensions as typing

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.cute_types import BaseCute, UpdateCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.process import check_rule
from telegrinder.model import Model
from telegrinder.modules import logger
from telegrinder.node.base import Node, is_node
from telegrinder.node.composer import compose_nodes
from telegrinder.node.event import EVENT_NODE_KEY
from telegrinder.tools.error_handler import ABCErrorHandler, ErrorHandler
from telegrinder.tools.magic import get_annotations
from telegrinder.types.enums import UpdateType
from telegrinder.types.objects import Update

from .abc import ABCHandler

if typing.TYPE_CHECKING:
    from telegrinder.bot.rules import ABCRule

F = typing.TypeVar(
    "F",
    bound=typing.Callable[typing.Concatenate[typing.Any, ...], typing.Awaitable[typing.Any]],
)
Event = typing.TypeVar("Event", bound=Model)
ErrorHandlerT = typing.TypeVar("ErrorHandlerT", bound=ABCErrorHandler, default=ErrorHandler)


@dataclasses.dataclass(repr=False)
class FuncHandler(ABCHandler[Event], typing.Generic[Event, F, ErrorHandlerT]):
    func: F
    rules: list["ABCRule"]
    is_blocking: bool = dataclasses.field(default=True, kw_only=True)
    dataclass: type[typing.Any] | None = dataclasses.field(default=dict, kw_only=True)
    error_handler: ErrorHandlerT = dataclasses.field(
        default_factory=lambda: typing.cast(ErrorHandlerT, ErrorHandler()),
        kw_only=True,
    )
    preset_context: Context = dataclasses.field(default_factory=lambda: Context(), kw_only=True)
    update_type: UpdateType | None = dataclasses.field(default=None, kw_only=True)

    def __repr__(self) -> str:
        return "<{}: {}={!r} with rules={!r}, dataclass={!r}, error_handler={!r}>".format(
            self.__class__.__name__,
            "blocking function" if self.is_blocking else "function",
            self.func.__name__,
            self.rules,
            self.dataclass,
            self.error_handler,
        )

    def get_required_nodes(self) -> dict[str, type[Node]]:
        return {k: v for k, v in get_annotations(self.func).items() if is_node(v)}

    async def check(self, api: ABCAPI, event: Update, ctx: Context | None = None) -> bool:
        if self.update_type is not None and self.update_type != event.update_type:
            return False

        ctx = Context(raw_update=event) if ctx is None else ctx
        temp_ctx = ctx.copy()
        temp_ctx |= self.preset_context

        nodes = self.get_required_nodes()
        node_col = None

        if nodes:
            node_col = await compose_nodes(nodes, UpdateCute.from_update(event, api), ctx)
            if node_col is None:
                return False
            temp_ctx |= node_col.values()

            if EVENT_NODE_KEY in ctx:
                for name, node in nodes.items():
                    if node is ctx[EVENT_NODE_KEY] and name in temp_ctx:
                        ctx[EVENT_NODE_KEY] = temp_ctx.pop(name)

        for rule in self.rules:
            if not await check_rule(api, rule, event, temp_ctx):
                logger.debug("Rule {!r} failed!", rule)
                return False

        temp_ctx["node_col"] = node_col
        ctx |= temp_ctx
        return True

    async def run(self, api: ABCAPI, event: Event, ctx: Context) -> typing.Any:
        if self.dataclass is Update and (event_node := ctx.pop(EVENT_NODE_KEY, None)) is not None:
            event = event_node

        elif self.dataclass is not None:
            if self.update_type is not None and isinstance(event, Update):
                update = event.to_dict()[self.update_type.value].unwrap()
                event = (
                    self.dataclass.from_update(update, bound_api=api)  # type: ignore
                    if issubclass(self.dataclass, BaseCute)
                    else self.dataclass(**update.to_dict())
                )
            else:
                event = self.dataclass(**event.to_dict())  # type: ignore

        result = (await self.error_handler.run(self.func, event, api, ctx)).unwrap()
        if node_col := ctx.node_col:
            await node_col.close_all()
        return result


__all__ = ("FuncHandler",)
