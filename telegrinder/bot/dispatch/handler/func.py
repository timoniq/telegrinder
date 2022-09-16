import typing
import types
from telegrinder.bot.rules import ABCRule
from telegrinder.tools import magic_bundle
from .abc import ABCHandler

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

    async def check(self, event: dict) -> bool:
        self.ctx = {}
        for rule in self.rules:
            e = event
            if rule.__event__ is None:
                pass
            else:
                if rule.__event__.name not in event:
                    return False
                e = rule.__event__.dataclass(**event[rule.__event__.name])
            if not await rule.run_check(e, self.ctx):
                return False
        return True

    async def run(self, event: T) -> typing.Any:
        if self.dataclass:
            event = self.dataclass(**event)
        return await self.func(event, **magic_bundle(self.func, self.ctx))
