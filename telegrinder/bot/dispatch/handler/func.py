import typing
import types
from telegrinder.bot.rules import ABCRule
from telegrinder.tools import magic_bundle
from telegrinder.types import Update
from telegrinder.api.abc import ABCAPI
from .abc import ABCHandler
from telegrinder.modules import logger

T = typing.TypeVar("T")


class FuncHandler(ABCHandler, typing.Generic[T]):
    def __init__(
        self,
        func: typing.Union[types.FunctionType, typing.Callable],
        rules: typing.List[ABCRule],
        is_blocking: bool = True,
        dataclass: typing.Optional[typing.Any] = dict,
    ):
        self.func = func
        self.is_blocking = is_blocking
        self.rules = rules
        self.dataclass = dataclass
        self.ctx = {}

    async def check(self, api: ABCAPI, event: Update) -> bool:
        self.ctx = {}
        for rule in self.rules:
            e = event
            if rule.__event__ is None:
                pass
            else:
                event_dict = event.to_dict()
                if event_dict.get(rule.__event__.name) is None:
                    return False
                e = rule.__event__.dataclass(
                    **event_dict[rule.__event__.name].to_dict(),
                    api=api,
                )
            if not await rule.run_check(e, self.ctx):
                logger.debug("Rule {} failed", rule)
                return False
        return True

    async def run(self, event: T) -> typing.Any:
        if self.dataclass:
            event = self.dataclass(**event)
        return await self.func(event, **magic_bundle(self.func, self.ctx))
