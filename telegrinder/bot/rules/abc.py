from abc import ABC, abstractmethod
from telegrinder.bot.cute_types import MessageCute
from telegrinder.bot.rules.adapter import ABCAdapter, RawUpdateAdapter, EventAdapter
from telegrinder.bot.dispatch.process import check_rule
from telegrinder.bot.cute_types.update import UpdateCute
from telegrinder.tools.magic import get_cached_translation, cache_translation
import typing
import inspect
import vbml

from telegrinder.tools.i18n.base import ABCTranslator

T = typing.TypeVar("T")
patcher = vbml.Patcher()

Message = MessageCute
Update = UpdateCute


def with_caching_translations(func):
    """Should be used as decorator for .translate method. Caches rule translations."""

    async def wrapper(self: "ABCRule", translator: ABCTranslator):
        if translation := get_cached_translation(self, translator.locale):
            return translation
        translation = await func(self, translator)
        cache_translation(self, translator.locale, translation)
        return translation

    return wrapper


class ABCRule(ABC, typing.Generic[T]):
    adapter: ABCAdapter[Update, T] = RawUpdateAdapter()
    require: list["ABCRule[T]"] = []

    @abstractmethod
    async def check(self, event: T, ctx: dict) -> bool:
        pass

    def __init_subclass__(cls, require: list["ABCRule[T]"] | None = None):
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

    def __neg__(self) -> "ABCRule[T]":
        return NotRule(self)

    def __repr__(self) -> str:
        return f"(rule {self.__class__.__name__})"

    async def translate(self, translator: ABCTranslator) -> typing.Self:
        return self


class AndRule(ABCRule):
    def __init__(self, *rules: ABCRule):
        self.rules = rules

    async def check(self, event: Update, ctx: dict) -> bool:
        ctx_copy = ctx.copy()
        for rule in self.rules:
            if not await check_rule(event.ctx_api, rule, event, ctx_copy):
                return False
        ctx |= ctx_copy
        return True


class OrRule(ABCRule):
    def __init__(self, *rules: ABCRule):
        self.rules = rules

    async def check(self, event: Update, ctx: dict) -> bool:
        for rule in self.rules:
            ctx_copy = ctx.copy()
            if await check_rule(event.ctx_api, rule, event, ctx_copy):
                ctx |= ctx_copy
                return True
        return False


class NotRule(ABCRule):
    def __init__(self, rule: ABCRule):
        self.rule = rule

    async def check(self, event: Update, ctx: dict) -> bool:
        ctx_copy = ctx.copy()
        return not await check_rule(event.ctx_api, self.rule, event, ctx_copy)


class MessageRule(ABCRule[Message], ABC, require=[]):
    adapter = EventAdapter("message", Message)

    @abstractmethod
    async def check(self, message: Message, ctx: dict) -> bool:
        ...
