from abc import ABC, abstractmethod
from telegrinder.bot.cute_types import MessageCute
from telegrinder.types import Update
import typing
import collections
import inspect
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

    def __init_subclass__(cls, require: typing.List["ABCRule[T]"] = None):
        """Merges requirements from inherited classes and rule-specific requirements"""
        requirements = []
        for base in inspect.getmro(cls):
            if issubclass(base, ABCRule) and base != cls:
                requirements.extend(base.require or ())

        requirements.extend(require or ())
        cls.require = list(dict.fromkeys(requirements))

    def __and__(self, other: "ABCRule"):
        return AndRule(self, other)

    def __or__(self, other: "ABCRule"):
        return OrRule(self, other)

    def __repr__(self) -> str:
        return f"(rule {self.__class__.__name__})"


class AndRule(ABCRule):
    def __init__(self, *rules: ABCRule):
        self.rules = rules

    async def check(self, event: Update, ctx: dict) -> bool:
        ctx_copy = ctx.copy()
        for rule in self.rules:
            e = event
            if rule.__event__:
                event_dict = event.to_dict()
                if rule.__event__.name not in event:
                    return False
                e = rule.__event__.dataclass(
                    **event_dict[rule.__event__.name].to_dict()
                )
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


class ABCMessageRule(ABCRule, ABC, require=[]):
    __event__ = EventScheme("message", Message)

    @abstractmethod
    async def check(self, message: Message, ctx: dict) -> bool:
        ...
