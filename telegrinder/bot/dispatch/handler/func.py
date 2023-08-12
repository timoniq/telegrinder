import typing
import types
from telegrinder.bot.dispatch.process import check_rule
from telegrinder.tools.magic import magic_bundle
from telegrinder.types import Update
from telegrinder.api.abc import ABCAPI
from .abc import ABCHandler
from telegrinder.modules import logger

T = typing.TypeVar("T")


if typing.TYPE_CHECKING:
    from telegrinder.bot.rules import ABCRule


class FuncHandler(ABCHandler, typing.Generic[T]):
    def __init__(
        self,
        func: types.FunctionType | typing.Callable,
        rules: list["ABCRule"],
        is_blocking: bool = True,
        dataclass: typing.Any | None = dict,
    ):
        self.func = func
        self.is_blocking = is_blocking
        self.rules = rules
        self.dataclass = dataclass
        self.ctx = {}

    async def check(self, api: ABCAPI, event: Update, ctx: dict = None) -> bool:
        ctx = ctx or {}
        preset_ctx = self.ctx.copy()
        self.ctx |= ctx
        for rule in self.rules:
            if not await check_rule(api, rule, event, self.ctx):
                logger.debug("Rule {} failed", rule)
                self.ctx = preset_ctx
                return False
        return True

    async def run(self, event: T) -> typing.Any:
        if self.dataclass:
            event = self.dataclass(**event)
        return await self.func(event, **magic_bundle(self.func, self.ctx))
