import dataclasses

import typing_extensions as typing

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.cute_types import BaseCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.process import check_rule
from telegrinder.modules import logger
from telegrinder.tools.error_handler import ABCErrorHandler, ErrorHandler
from telegrinder.types import Update

from .abc import ABCHandler

if typing.TYPE_CHECKING:
    from telegrinder.bot.rules import ABCRule

F = typing.TypeVar("F", bound=typing.Callable[typing.Concatenate[typing.Any, ...], typing.Awaitable[typing.Any]])
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
    ctx: Context = dataclasses.field(default_factory=lambda: Context(), init=False)

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
        ctx = ctx or Context()
        preset_ctx = self.ctx.copy()
        self.ctx |= ctx
        for rule in self.rules:
            if not await check_rule(api, rule, event, self.ctx):
                logger.debug("Rule {!r} failed!", rule)
                self.ctx = preset_ctx
                return False
        return True

    async def run(self, event: EventT) -> typing.Any:
        if self.dataclass is not None:
            event = self.dataclass(**event.to_dict())
        return (await self.error_handler.run(self.func, event, event.api, self.ctx)).unwrap()


__all__ = ("FuncHandler",)
