import typing
from abc import ABC, abstractmethod
from collections import deque
from functools import cached_property

from nodnod.agent.event_loop.agent import EventLoopAgent
from nodnod.interface.node_from_function import create_node_from_function

from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.process import check_rule
from telegrinder.modules import log_scope
from telegrinder.node.compose import create_composable
from telegrinder.node.scope import NodeScope
from telegrinder.node.utils import get_globals_from_function, get_locals_from_function
from telegrinder.tools.fullname import fullname

if typing.TYPE_CHECKING:
    from nodnod.agent.base import Agent

    from telegrinder.node.compose import Composable

type CheckResult = bool | typing.Awaitable[bool]
type Node = typing.Any


def get_rules_names(rules: typing.Iterable[ABCRule], /) -> typing.Iterable[str]:
    return (type(rule).__name__ for rule in rules)


class ABCRule(ABC):
    required_nodes: typing.Mapping[str, Node] | None = None
    agent_cls: type[Agent] = EventLoopAgent
    requires: deque[ABCRule] | None = None
    rule_scope: NodeScope = NodeScope.PER_CALL

    @abstractmethod
    def check(self, *args: typing.Any, **kwargs: typing.Any) -> CheckResult:
        pass

    def __init_subclass__(
        cls,
        *,
        requires: typing.Iterable[ABCRule] | None = None,
        scope: NodeScope = NodeScope.PER_CALL,
    ) -> None:
        requirements: list[ABCRule] = []

        for base in cls.__mro__:
            if issubclass(base, ABCRule) and base != cls:
                requirements.extend(base.requires or ())

        requirements.extend(requires or ())
        cls.requires = deque(dict.fromkeys(requirements))
        cls.rule_scope = scope

    def __and__(self, other: object, /) -> AndRule:
        if not isinstance(other, ABCRule):
            return NotImplemented
        return AndRule(self, other)

    def __iadd__(self, other: object, /) -> AndRule:
        return self.__and__(other)

    def __or__(self, other: object, /) -> OrRule:
        if not isinstance(other, ABCRule):
            return NotImplemented
        return OrRule(self, other)

    def __ior__(self, other: object, /) -> OrRule:
        return self.__or__(other)

    def __invert__(self) -> NotRule:
        return NotRule(self)

    def __repr__(self) -> str:
        return "<{}{}>".format(
            fullname(self),
            "" if not self.requires else ", requires={!r}".format(self.requires),
        )

    def as_optional(self) -> ABCRule:
        return self | Always()

    def should_fail(self) -> ABCRule:
        return self & Never()

    @cached_property
    def composable(self) -> Composable:
        node = create_node_from_function(
            self.check,
            dependencies=self.required_nodes,
            forward_refs=get_globals_from_function(self.check),
            namespace=get_locals_from_function(self.check),
        )
        return create_composable(node, agent_cls=self.agent_cls, scope=self.rule_scope)


class AndRule(ABCRule):
    def __init__(self, *rules: ABCRule) -> None:
        self.rules = rules

    async def check(self, context: Context) -> bool:
        with log_scope(lambda: "Rule{{{}}}".format(" & ".join(get_rules_names(self.rules)))):
            for rule in self.rules:
                if not await check_rule(rule, context):
                    return False

        return True


class OrRule(ABCRule):
    def __init__(self, *rules: ABCRule) -> None:
        self.rules = rules

    async def check(self, context: Context) -> bool:
        with log_scope(lambda: "Rule{{{}}}".format(" | ".join(get_rules_names(self.rules)))):
            for rule in self.rules:
                if await check_rule(rule, context):
                    return True

        return False


class NotRule(ABCRule):
    def __init__(self, rule: ABCRule) -> None:
        self.rule = rule

    async def check(self, context: Context) -> bool:
        with log_scope(lambda: f"~{type(self).__name__}"):
            return not await check_rule(self.rule, context)


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
