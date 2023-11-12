import typing

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.cute_types import BaseCute
from telegrinder.bot.dispatch.process import check_rule
from telegrinder.modules import logger
from telegrinder.tools.magic import magic_bundle
from telegrinder.types import Update

from .abc import ABCHandler

if typing.TYPE_CHECKING:
    from telegrinder.bot.rules import ABCRule

EventT = typing.TypeVar("EventT", bound=BaseCute)
F = typing.TypeVar("F", bound=typing.Callable[
    typing.Concatenate[typing.Any, ...], typing.Awaitable
])


class FuncHandler(ABCHandler, typing.Generic[EventT, F]):
    def __init__(
        self,
        func: F,
        rules: list["ABCRule[EventT]"],
        is_blocking: bool = True,
        dataclass: type[typing.Any] | None = dict,
    ):
        self.func = func
        self.is_blocking = is_blocking
        self.rules = rules
        self.dataclass = dataclass
        self.ctx = {}

    async def check(self, api: ABCAPI, event: Update, ctx: dict | None = None) -> bool:
        ctx = ctx or {}
        preset_ctx = self.ctx.copy()
        self.ctx |= ctx
        for rule in self.rules:
            if not await check_rule(api, rule, event, self.ctx):
                logger.debug("Rule {!r} failed!", rule)
                self.ctx = preset_ctx
                return False
        return True

    async def run(self, event: EventT) -> typing.Any:
        if self.dataclass:
            event = self.dataclass(**event.to_dict())
        return await self.func(event, **magic_bundle(self.func, self.ctx))
