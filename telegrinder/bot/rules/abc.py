from abc import ABC, abstractmethod
from functools import cached_property

import typing_extensions as typing

from telegrinder.bot.cute_types import MessageCute, UpdateCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.process import check_rule
from telegrinder.node.base import NodeType, get_nodes, is_node
from telegrinder.tools.adapter import ABCAdapter
from telegrinder.tools.adapter.node import Event
from telegrinder.tools.adapter.raw_update import RawUpdateAdapter
from telegrinder.tools.awaitable import maybe_awaitable
from telegrinder.tools.i18n.abc import ABCTranslator
from telegrinder.tools.magic import (
    cache_translation,
    get_annotations,
    get_cached_translation,
    get_default_args,
)
from telegrinder.tools.repr import fullname
from telegrinder.types.objects import Update as UpdateObject

if typing.TYPE_CHECKING:
    from telegrinder.node.composer import NodeCollection

AdaptTo = typing.TypeVar("AdaptTo", default=typing.Any, contravariant=True)

type CheckResult = bool | typing.Awaitable[bool]

Message: typing.TypeAlias = MessageCute
Update: typing.TypeAlias = UpdateCute


def with_caching_translations(func: typing.Callable[..., typing.Any]):
    """Should be used as decorator for .translate method. Caches rule translations."""

    async def wrapper(self: "ABCRule", translator: ABCTranslator):
        if translation := get_cached_translation(self, translator.locale):
            return translation
        translation = await func(self, translator)
        cache_translation(self, translator.locale, translation)
        return translation

    return wrapper


class ABCRule(ABC, typing.Generic[AdaptTo]):
    adapter: ABCAdapter[UpdateObject, AdaptTo]
    requires: list["ABCRule"] = []

    if typing.TYPE_CHECKING:

        @abstractmethod
        def check(self, *args: typing.Any, **kwargs: typing.Any) -> CheckResult:
            pass
    else:
        adapter = RawUpdateAdapter()

        @abstractmethod
        def check(self, *args, **kwargs):
            pass

    def __init_subclass__(
        cls,
        *,
        requires: list["ABCRule"] | None = None,
        adapter: ABCAdapter[UpdateObject, AdaptTo] | None = None,
    ) -> None:
        """Merges requirements from inherited classes and rule-specific requirements."""
        if adapter is not None:
            cls.adapter = adapter

        requirements = list[ABCRule]()
        for base in cls.__mro__:
            if issubclass(base, ABCRule) and base != cls:
                requirements.extend(base.requires or ())

        requirements.extend(requires or ())
        cls.requires = list(dict.fromkeys(requirements))

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

    def __invert__(self, other: object, /) -> "NotRule":
        if not isinstance(other, ABCRule):
            return NotImplemented
        return NotRule(self)

    def __repr__(self) -> str:
        return "<{}, requires={!r}>".format(fullname(self), self.requires)

    @cached_property
    def required_nodes(self) -> dict[str, type[NodeType]]:
        return get_nodes(self.check)

    def as_optional(self) -> "ABCRule":
        return self | Always()

    def should_fail(self) -> "ABCRule":
        return self & Never()

    async def bounding_check(
        self,
        ctx: Context,
        *,
        adapted_value: AdaptTo,
        node_col: "NodeCollection | None" = None,
    ) -> bool:
        bound_check_rule = self.check
        kw = {}
        node_col_values = node_col.values if node_col is not None else {}
        temp_ctx = get_default_args(bound_check_rule) | ctx

        for i, (k, v) in enumerate(get_annotations(bound_check_rule).items()):
            if (isinstance(adapted_value, Event) and i == 0) or (  # First arg is Event
                isinstance(v, type) and isinstance(adapted_value, v)
            ):
                kw[k] = adapted_value if not isinstance(adapted_value, Event) else adapted_value.obj
            elif is_node(v):
                assert k in node_col_values, "Node is undefined, error while bounding."
                kw[k] = node_col_values[k]
            elif k in temp_ctx:
                kw[k] = temp_ctx[k]
            elif v is Context:
                kw[k] = ctx
            else:
                raise LookupError(
                    f"Cannot bound {k!r} of type {v!r} to '{self.__class__.__qualname__}.check()', "
                    "because it cannot be resolved."
                )

        return await maybe_awaitable(bound_check_rule(**kw))

    async def translate(self, translator: ABCTranslator) -> typing.Self:
        return self


class AndRule(ABCRule):
    def __init__(self, *rules: ABCRule) -> None:
        self.rules = rules

    async def check(self, event: Update, ctx: Context) -> bool:
        ctx_copy = ctx.copy()
        for rule in self.rules:
            if not await check_rule(event.ctx_api, rule, event, ctx_copy):
                return False
        ctx |= ctx_copy
        return True


class OrRule(ABCRule):
    def __init__(self, *rules: ABCRule) -> None:
        self.rules = rules

    async def check(self, event: Update, ctx: Context) -> bool:
        for rule in self.rules:
            ctx_copy = ctx.copy()
            if await check_rule(event.ctx_api, rule, event, ctx_copy):
                ctx |= ctx_copy
                return True
        return False


class NotRule(ABCRule):
    def __init__(self, rule: ABCRule) -> None:
        self.rule = rule

    async def check(self, event: Update, ctx: Context) -> bool:
        ctx_copy = ctx.copy()
        return not await check_rule(event.ctx_api, self.rule, event, ctx_copy)


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
    "with_caching_translations",
)
