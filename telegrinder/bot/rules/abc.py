import inspect
import typing
from abc import ABC, abstractmethod

from telegrinder.bot.cute_types import BaseCute, MessageCute, UpdateCute
from telegrinder.bot.dispatch.process import check_rule
from telegrinder.bot.rules.adapter import ABCAdapter, EventAdapter, RawUpdateAdapter
from telegrinder.tools.i18n.base import ABCTranslator
from telegrinder.tools.magic import cache_translation, get_cached_translation
from telegrinder.types.objects import Update as UpdateObject

T = typing.TypeVar("T", bound=BaseCute)
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
    adapter: ABCAdapter[UpdateObject, T] = RawUpdateAdapter()  # type: ignore
    requires: list["ABCRule[T]"] = []

    @abstractmethod
    async def check(self, event: T, ctx: dict) -> bool:
        pass

    def __init_subclass__(cls, requires: list["ABCRule[T]"] | None = None):
        """Merges requirements from inherited classes and rule-specific requirements"""
        requirements = []
        for base in inspect.getmro(cls):
            if issubclass(base, ABCRule) and base != cls:
                requirements.extend(base.requires or ())

        requirements.extend(requires or ())
        cls.requires = list(dict.fromkeys(requirements))

    def __and__(self, other: "ABCRule[T]"):
        return AndRule(self, other)

    def __or__(self, other: "ABCRule[T]"):
        return OrRule(self, other)

    def __neg__(self) -> "ABCRule[T]":
        return NotRule(self)

    def __repr__(self) -> str:
        return "<{!r} rule, adapter: {!r}>".format(
            self.__class__.__name__,
            self.adapter.__class__.__name__,
        )

    async def translate(self, translator: ABCTranslator) -> typing.Self:
        return self


class AndRule(ABCRule[T]):
    def __init__(self, *rules: ABCRule[T]):
        self.rules = rules

    async def check(self, event: Update, ctx: dict) -> bool:
        ctx_copy = ctx.copy()
        for rule in self.rules:
            if not await check_rule(event.ctx_api, rule, event, ctx_copy):
                return False
        ctx |= ctx_copy
        return True


class OrRule(ABCRule[T]):
    def __init__(self, *rules: ABCRule[T]):
        self.rules = rules

    async def check(self, event: Update, ctx: dict) -> bool:
        for rule in self.rules:
            ctx_copy = ctx.copy()
            if await check_rule(event.ctx_api, rule, event, ctx_copy):
                ctx |= ctx_copy
                return True
        return False


class NotRule(ABCRule[T]):
    def __init__(self, rule: ABCRule[T]):
        self.rule = rule

    async def check(self, event: Update, ctx: dict) -> bool:
        ctx_copy = ctx.copy()
        return not await check_rule(event.ctx_api, self.rule, event, ctx_copy)


class MessageRule(ABCRule[Message], ABC, requires=[]):
    adapter = EventAdapter("message", Message)

    @abstractmethod
    async def check(self, message: Message, ctx: dict) -> bool:
        ...
