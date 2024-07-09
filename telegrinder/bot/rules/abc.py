import inspect
from abc import ABC, abstractmethod

import typing_extensions as typing

from telegrinder.bot.cute_types import BaseCute, MessageCute, UpdateCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.process import check_rule
from telegrinder.bot.rules.adapter import ABCAdapter, RawUpdateAdapter
from telegrinder.bot.rules.adapter.node import NodeAdapter
from telegrinder.tools.i18n.base import ABCTranslator
from telegrinder.tools.magic import cache_translation, get_cached_translation
from telegrinder.types.objects import Update as UpdateObject

AdaptTo = typing.TypeVar("AdaptTo", default=UpdateCute)
EventCute = typing.TypeVar("EventCute", bound=BaseCute, default=UpdateCute)

Message: typing.TypeAlias = MessageCute
Update: typing.TypeAlias = UpdateCute


def with_caching_translations(func: typing.Callable[..., typing.Any]):
    """Should be used as decorator for .translate method. Caches rule translations."""

    async def wrapper(self: "ABCRule[typing.Any]", translator: ABCTranslator):
        if translation := get_cached_translation(self, translator.locale):
            return translation
        translation = await func(self, translator)
        cache_translation(self, translator.locale, translation)
        return translation

    return wrapper


class ABCRule(ABC, typing.Generic[EventCute, AdaptTo]):
    adapter: ABCAdapter[UpdateObject, AdaptTo] = RawUpdateAdapter()  # type: ignore
    requires: list["ABCRule[EventCute]"] = []

    @abstractmethod
    async def check(self, event: AdaptTo, *, ctx: Context) -> bool:
        pass

    def __init_subclass__(cls, requires: list["ABCRule[EventCute, AdaptTo]"] | None = None) -> None:
        """Merges requirements from inherited classes and rule-specific requirements."""

        requirements = []
        for base in inspect.getmro(cls):
            if issubclass(base, ABCRule) and base != cls:
                requirements.extend(base.requires or ())  # type: ignore

        requirements.extend(requires or ())
        cls.requires = list(dict.fromkeys(requirements))

    def __and__(self, other: "ABCRule[EventCute, AdaptTo]") -> "AndRule[EventCute, AdaptTo]":
        """And Rule.

        ```python
        rule = HasText() & HasCaption()
        rule #> AndRule(HasText(), HasCaption()) -> True if all rules in an AndRule are True, otherwise False.
        ```
        """

        return AndRule(self, other)

    def __or__(self, other: "ABCRule[EventCute, AdaptTo]") -> "OrRule[EventCute, AdaptTo]":
        """Or Rule.

        ```python
        rule = HasText() | HasCaption()
        rule #> OrRule(HasText(), HasCaption()) -> True if any rule in an OrRule are True, otherwise False.
        ```
        """

        return OrRule(self, other)

    def __invert__(self) -> "NotRule[EventCute, AdaptTo]":
        """Not Rule.

        ```python
        rule = ~HasText()
        rule # NotRule(HasText()) -> True if rule returned False, otherwise False.
        ```
        """

        return NotRule(self)

    def __repr__(self) -> str:
        return "<{}: adapter={!r}>".format(
            self.__class__.__name__,
            self.adapter,
        )

    async def translate(self, translator: ABCTranslator) -> typing.Self:
        return self


class AndRule(ABCRule[EventCute, AdaptTo]):
    def __init__(self, *rules: ABCRule[EventCute, AdaptTo]) -> None:
        self.rules = rules

    async def check(self, event: Update, ctx: Context) -> bool:
        ctx_copy = ctx.copy()
        for rule in self.rules:
            if not await check_rule(event.ctx_api, rule, event, ctx_copy):
                return False
        ctx |= ctx_copy
        return True


class OrRule(ABCRule[EventCute, AdaptTo]):
    def __init__(self, *rules: ABCRule[EventCute, AdaptTo]) -> None:
        self.rules = rules

    async def check(self, event: Update, ctx: Context) -> bool:
        for rule in self.rules:
            ctx_copy = ctx.copy()
            if await check_rule(event.ctx_api, rule, event, ctx_copy):
                ctx |= ctx_copy
                return True
        return False


class NotRule(ABCRule[EventCute, AdaptTo]):
    def __init__(self, rule: ABCRule[EventCute, AdaptTo]) -> None:
        self.rule = rule

    async def check(self, event: Update, ctx: Context) -> bool:
        ctx_copy = ctx.copy()
        return not await check_rule(event.ctx_api, self.rule, event, ctx_copy)


Ts = typing.TypeVarTuple("Ts")


class NodeRule(ABCRule[Update, tuple[*Ts]], ABC, typing.Generic[*Ts]):
    @property
    def adapter(self) -> NodeAdapter[*Ts]:
        nodes = {
            name: parameter.annotation
            for name, parameter in inspect.signature(self.check).parameters.items()
            if parameter.annotation is not inspect._empty
        }
        return NodeAdapter(*list(nodes.values()))  # type: ignore

    @abstractmethod
    async def check(self, *nodes: *Ts, ctx: Context) -> bool: ...


__all__ = (
    "ABCRule",
    "AndRule",
    "NotRule",
    "OrRule",
    "with_caching_translations",
)
