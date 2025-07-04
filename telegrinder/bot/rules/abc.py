from abc import ABC, abstractmethod
from collections import deque
from functools import cached_property

import typing_extensions as typing

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.process import check_rule
from telegrinder.node.base import IsNode, get_nodes
from telegrinder.tools.fullname import fullname
from telegrinder.types.objects import Update

type CheckResult = bool | typing.Awaitable[bool]


class ABCRule(ABC):
    requires: deque["ABCRule"] = deque()

    if typing.TYPE_CHECKING:

        @abstractmethod
        def check(self, *args: typing.Any, **kwargs: typing.Any) -> CheckResult:
            pass
    else:

        @abstractmethod
        def check(self, *args, **kwargs):
            pass

    def __init_subclass__(
        cls,
        *,
        requires: typing.Iterable["ABCRule"] | None = None,
    ) -> None:
        """Merges requirements from inherited classes and rule-specific requirements."""
        requirements = list[ABCRule]()
        for base in cls.__mro__:
            if issubclass(base, ABCRule) and base != cls:
                requirements.extend(base.requires or ())

        requirements.extend(requires or ())
        cls.requires = deque(dict.fromkeys(requirements))

    def __and__(self, other: object, /) -> "AndRule":
        if not isinstance(other, ABCRule):
            return NotImplemented
        return AndRule(self, other)

    def __iadd__(self, other: object, /) -> "AndRule":
        return self.__and__(other)

    def __or__(self, other: object, /) -> "OrRule":
        if not isinstance(other, ABCRule):
            return NotImplemented
        return OrRule(self, other)

    def __ior__(self, other: object, /) -> "OrRule":
        return self.__or__(other)

    def __invert__(self) -> "NotRule":
        return NotRule(self)

    def __repr__(self) -> str:
        return "<{}, requires={!r}>".format(fullname(self), self.requires)

    @cached_property
    def required_nodes(self) -> dict[str, IsNode]:
        return get_nodes(self.check)

    def as_optional(self) -> "ABCRule":
        return self | Always()

    def should_fail(self) -> "ABCRule":
        return self & Never()


class AndRule(ABCRule):
    def __init__(self, *rules: ABCRule) -> None:
        self.rules = rules

    async def check(self, event: Update, api: API, ctx: Context) -> bool:
        ctx_copy = ctx.copy()

        for rule in self.rules:
            if not await check_rule(api, rule, event, ctx_copy):
                return False

        ctx |= ctx_copy
        return True


class OrRule(ABCRule):
    def __init__(self, *rules: ABCRule) -> None:
        self.rules = rules

    async def check(self, event: Update, api: API, ctx: Context) -> bool:
        for rule in self.rules:
            ctx_copy = ctx.copy()

            if await check_rule(api, rule, event, ctx_copy):
                ctx |= ctx_copy
                return True

        return False


class NotRule(ABCRule):
    def __init__(self, rule: ABCRule) -> None:
        self.rule = rule

    async def check(self, event: Update, api: API, ctx: Context) -> bool:
        ctx_copy = ctx.copy()
        return not await check_rule(api, self.rule, event, ctx_copy)


class Never(ABCRule):
    """Neutral element for `|` (OrRule)."""

    def check(self) -> typing.Literal[False]:
        return False


class Always(ABCRule):
    """Neutral element for `&` (AndRule)."""

    def check(self) -> typing.Literal[True]:
        return True


__all__ = (
    "ABCRule",
    "Always",
    "AndRule",
    "CheckResult",
    "Never",
    "NotRule",
    "OrRule",
    "check_rule",
)
