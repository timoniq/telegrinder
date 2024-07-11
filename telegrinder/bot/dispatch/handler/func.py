import dataclasses

import typing_extensions as typing

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.cute_types import BaseCute, UpdateCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.process import check_rule
from telegrinder.modules import logger
from telegrinder.node import Node, compose_nodes, is_node
from telegrinder.tools.error_handler import ABCErrorHandler, ErrorHandler
from telegrinder.tools.magic import get_annotations
from telegrinder.types import Update
from telegrinder.types.enums import UpdateType

from .abc import ABCHandler

if typing.TYPE_CHECKING:
    from telegrinder.bot.rules import ABCRule

F = typing.TypeVar(
    "F",
    bound=typing.Callable[typing.Concatenate[typing.Any, ...], typing.Awaitable[typing.Any]],
)
AdaptTo = typing.TypeVar("AdaptTo", default=UpdateCute)
EventType = typing.TypeVar("EventType", bound=BaseCute)
ErrorHandlerT = typing.TypeVar("ErrorHandlerT", bound=ABCErrorHandler, default=ErrorHandler)


@dataclasses.dataclass(repr=False)
class FuncHandler(ABCHandler[EventType], typing.Generic[EventType, F, ErrorHandlerT]):
    func: F
    rules: list["ABCRule[EventType]"]
    _: dataclasses.KW_ONLY
    is_blocking: bool = dataclasses.field(default=True)
    dataclass: type[typing.Any] | None = dataclasses.field(default=dict)
    error_handler: ErrorHandlerT = dataclasses.field(
        default_factory=lambda: typing.cast(ErrorHandlerT, ErrorHandler()),
    )
    preset_context: Context = dataclasses.field(default_factory=lambda: Context())
    update_type: UpdateType | None = dataclasses.field(default=None)

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

        ctx = ctx or Context()
        temp_ctx = ctx.copy()
        temp_ctx |= self.preset_context

        nodes = self.get_required_nodes()
        node_col = None

        if nodes:
            node_col = await compose_nodes(nodes, UpdateCute.from_update(event, api))
            if node_col is None:
                return False
            temp_ctx |= node_col.values()

        for rule in self.rules:
            if not await check_rule(api, rule, event, temp_ctx):
                logger.debug("Rule {!r} failed!", rule)
                return False

        temp_ctx["node_col"] = node_col
        ctx |= temp_ctx
        return True

    async def run(self, event: EventType, ctx: Context) -> typing.Any:
        api = event.api

        if self.dataclass is not None:
            if self.update_type is not None:
                update = event.to_dict()[self.update_type.value].unwrap()
                event = (
                    self.dataclass.from_update(update, bound_api=api)  # type: ignore
                    if issubclass(self.dataclass, BaseCute)
                    else self.dataclass(**update.to_dict())
                )
            else:
                event = self.dataclass(**event.to_dict())

        result = (await self.error_handler.run(self.func, event, api, ctx)).unwrap()
        if node_col := ctx["node_col"]:
            await node_col.close_all()
        return result


__all__ = ("FuncHandler",)
