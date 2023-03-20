from abc import ABC, abstractmethod
from telegrinder.bot.cute_types import MessageCute
from telegrinder.types import Update
from telegrinder.tools import dependencies_bundle
import typing
import collections
import inspect

T = typing.TypeVar("T")

Message = MessageCute
EventScheme = collections.namedtuple("EventScheme", ["name", "dataclass"])


class ABCRule(ABC, typing.Generic[T]):
    __event__: typing.Optional[EventScheme] = None
    require: typing.List["ABCRule[T]"] = []

    async def run_check(self, event: T, ctx: dict, **rule_dependencies) -> bool:
        ctx_copy = ctx.copy()
        for required in self.require:
            if not await required.run_check(
                event, ctx_copy, **dependencies_bundle(
                    required.__class__.__name__,
                    required.check, rule_dependencies
                )
            ):
                return False
        ctx.update(ctx_copy)
        return await self.check(
            event, ctx, **dependencies_bundle(
                self.__class__.__name__,
                self.check, rule_dependencies
            )
        )

    @abstractmethod
    async def check(self, event: T, ctx: dict) -> bool:
        ...

    def __init_subclass__(cls, require: typing.Optional[typing.List["ABCRule[T]"]] = None):
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

    async def check(self, event: Update, ctx: dict, **rule_dependencies) -> bool:
        ctx_copy = ctx.copy()
        for rule in self.rules:
            e = event
            if rule.__event__:
                event_dict = event.to_dict()
                if rule.__event__.name not in event.to_dict().keys():
                    return False
                e = event_dict[rule.__event__.name]
            if not await rule.run_check(e, ctx_copy, **rule_dependencies):
                return False
        
        ctx.clear()
        ctx.update(ctx_copy)
        return True


class OrRule(ABCRule):
    def __init__(self, *rules: ABCRule):
        self.rules = rules

    async def check(self, event: Update, ctx: dict, **rule_dependencies) -> bool:
        ctx_copy = ctx.copy()
        found = False

        for rule in self.rules:
            e = event
            if rule.__event__:
                event_dict = event.to_dict()
                if rule.__event__.name not in event.to_dict().keys():
                    continue
                e = event_dict[rule.__event__.name]
            if await rule.run_check(e, ctx_copy, **rule_dependencies):
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
