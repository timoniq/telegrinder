import typing
from telegrinder.bot.rules import ABCRule, AnyDataclass
from .abc import ABCHandler

T = typing.TypeVar("T")


class FuncHandler(ABCHandler, typing.Generic[T]):
    def __init__(
        self,
        func: typing.Callable,
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
            if rule.__dataclass__ in (AnyDataclass, dict):
                pass
            else:
                e = rule.__dataclass__(**event)
            if not await rule.check(e, self.ctx):
                return False
        return True

    async def run(self, event: T) -> typing.Any:
        if self.dataclass:
            event = self.dataclass(**event)
        return await self.func(event, **self.ctx)
