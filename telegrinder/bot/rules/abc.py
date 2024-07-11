import inspect
from abc import ABC, abstractmethod

import typing_extensions as typing

from telegrinder.bot.cute_types import MessageCute, UpdateCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.process import check_rule
from telegrinder.bot.rules.adapter import ABCAdapter, RawUpdateAdapter
from telegrinder.bot.rules.adapter.node import Event
from telegrinder.node.base import Node, is_node
from telegrinder.node.composer import NodeCollection
from telegrinder.tools.i18n.base import ABCTranslator
from telegrinder.tools.magic import cache_translation, get_annotations, get_cached_translation
from telegrinder.types.objects import Update as UpdateObject

AdaptTo = typing.TypeVar("AdaptTo", default=typing.Any)

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
    adapter: ABCAdapter[UpdateObject, AdaptTo] = RawUpdateAdapter()  # type: ignore
    requires: list["ABCRule"] = []

    @abstractmethod
    async def check(self, event: AdaptTo, *, ctx: Context) -> bool:
        pass

    def get_required_nodes(self) -> dict[str, type[Node]]:
        return {k: v for k, v in get_annotations(self.check).items() if is_node(v)}

    async def bounding_check(
        self,
        adapted_value: AdaptTo,
        ctx: Context,
        node_col: NodeCollection | None = None,
    ) -> bool:
        kw = {}
        node_col_values = node_col.values() if node_col is not None else {}

        for i, (k, v) in enumerate(get_annotations(self.check).items()):
            if (isinstance(adapted_value, Event) and not i) or (
                isinstance(v, type) and isinstance(adapted_value, v)
            ):
                kw[k] = adapted_value if not isinstance(adapted_value, Event) else adapted_value.obj
            elif is_node(v):
                assert k in node_col_values, "Node is undefined, error while bounding."
                kw[k] = node_col_values[k]
            elif k in ctx:
                kw[k] = ctx[k]
            elif v is Context:
                kw[k] = ctx
            else:
                raise LookupError(
                    f"Cannot bound {k!r} to '{self.__class__.__name__}.check()', because it cannot be resolved."
                )

        return await self.check(**kw)

    def __init_subclass__(cls, requires: list["ABCRule"] | None = None) -> None:
        """Merges requirements from inherited classes and rule-specific requirements."""

        requirements = []
        for base in inspect.getmro(cls):
            if issubclass(base, ABCRule) and base != cls:
                requirements.extend(base.requires or ())  # type: ignore

        requirements.extend(requires or ())
        cls.requires = list(dict.fromkeys(requirements))

    def __and__(self, other: "ABCRule") -> "AndRule":
        """And Rule.

        ```python
        rule = HasText() & HasCaption()
        rule #> AndRule(HasText(), HasCaption()) -> True if all rules in an AndRule are True, otherwise False.
        ```
        """

        return AndRule(self, other)

    def __or__(self, other: "ABCRule") -> "OrRule":
        """Or Rule.

        ```python
        rule = HasText() | HasCaption()
        rule #> OrRule(HasText(), HasCaption()) -> True if any rule in an OrRule are True, otherwise False.
        ```
        """

        return OrRule(self, other)

    def __invert__(self) -> "NotRule":
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


class AndRule(ABCRule):
    def __init__(self, *rules: ABCRule[AdaptTo]) -> None:
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


__all__ = (
    "ABCRule",
    "AndRule",
    "NotRule",
    "OrRule",
    "with_caching_translations",
)
