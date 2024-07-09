import dataclasses

import typing_extensions as typing

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.cute_types import BaseCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.process import check_rule
from telegrinder.modules import logger
from telegrinder.tools.error_handler import ABCErrorHandler, ErrorHandler
from telegrinder.types import Update
from telegrinder.types.enums import UpdateType

from .abc import ABCHandler

if typing.TYPE_CHECKING:
    from telegrinder.bot.rules import ABCRule

F = typing.TypeVar(
    "F",
    bound=typing.Callable[typing.Concatenate[typing.Any, ...], typing.Awaitable[typing.Any]],
)
EventT = typing.TypeVar("EventT", bound=BaseCute)
ErrorHandlerT = typing.TypeVar("ErrorHandlerT", bound=ABCErrorHandler, default=ErrorHandler)


@dataclasses.dataclass(repr=False)
class FuncHandler(ABCHandler[EventT], typing.Generic[EventT, F, ErrorHandlerT]):
    func: F
    rules: list["ABCRule[EventT]"]
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

    async def check(self, api: ABCAPI, event: Update, ctx: Context | None = None) -> bool:
        if self.update_type is not None and self.update_type != event.update_type:
            return False
        ctx = ctx or Context()
        temp_ctx = ctx.copy()
        temp_ctx |= self.preset_context

        for rule in self.rules:
            if not await check_rule(api, rule, event, temp_ctx):
                logger.debug("Rule {!r} failed!", rule)
                return False

        ctx |= temp_ctx
        return True

    async def run(self, event: EventT, ctx: Context) -> typing.Any:
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
        return (await self.error_handler.run(self.func, event, api, ctx)).unwrap()


__all__ = ("FuncHandler",)
