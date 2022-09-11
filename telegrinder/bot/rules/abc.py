from abc import ABC, abstractmethod
from telegrinder.bot.cute_types import MessageCute
import typing
import collections
import vbml

T = typing.TypeVar("T")
patcher = vbml.Patcher()

Message = MessageCute
EventScheme = collections.namedtuple("EventScheme", ["name", "dataclass"])


class ABCRule(ABC, typing.Generic[T]):
    __event__: typing.Optional[EventScheme] = None
    require: typing.List["ABCRule[T]"] = []

    async def run_check(self, event: T, ctx: dict) -> bool:
        ctx_copy = ctx.copy()
        for required in self.require:
            if not await required.run_check(event, ctx_copy):
                return False
        ctx.update(ctx_copy)
        return await self.check(event, ctx)

    @abstractmethod
    async def check(self, event: T, ctx: dict) -> bool:
        pass

    def __and__(self, other: "ABCRule"):
        return AndRule(self, other)

    def __or__(self, other: "ABCRule"):
        return OrRule(self, other)


class AndRule(ABCRule):
    def __init__(self, *rules: ABCRule):
        self.rules = rules

    async def check(self, event: dict, ctx: dict) -> bool:
        ctx_copy = ctx.copy()
        for rule in self.rules:
            e = event
            if rule.__event__:
                if rule.__event__.name not in event:
                    return False
                e = rule.__event__.dataclass(**event[rule.__event__.name])
            if not await rule.run_check(e, ctx_copy):
                return False
        ctx.clear()
        ctx.update(ctx_copy)
        return True


class OrRule(ABCRule):
    def __init__(self, *rules: ABCRule):
        self.rules = rules

    async def check(self, event: T, ctx: dict) -> bool:
        ctx_copy = ctx.copy()
        found = False

        for rule in self.rules:
            e = event
            if rule.__event__:
                if rule.__event__.name not in event:
                    continue
                e = rule.__event__.dataclass(**event[rule.__event__.name])
            if await rule.run_check(e, ctx_copy):
                found = True
                break

        ctx.clear()
        ctx.update(ctx_copy)
        return found


class ABCMessageRule(ABCRule, ABC):
    __event__ = EventScheme("message", Message)
    require: typing.List["ABCMessageRule[T]"] = []

    @abstractmethod
    async def check(self, message: Message, ctx: dict) -> bool:
        ...
