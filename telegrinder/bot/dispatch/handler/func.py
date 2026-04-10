import dataclasses
import typing
from collections import deque

from kungfu.library.monad.result import Error, Result
from nodnod.agent.event_loop.agent import EventLoopAgent
from nodnod.error import NodeError

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.handler.abc import ABCHandler
from telegrinder.bot.dispatch.process import check_rule
from telegrinder.modules import log_scope, logger
from telegrinder.node.compose import compose
from telegrinder.tools.fullname import fullname
from telegrinder.types.objects import Update

if typing.TYPE_CHECKING:
    from nodnod.agent.base import Agent

    from telegrinder.bot.rules.abc import ABCRule

type Function[**P = ..., R = typing.Any] = typing.Callable[P, R]


@dataclasses.dataclass(repr=False, slots=True)
class FuncHandler[T: Function](ABCHandler):
    function: T
    rules: dataclasses.InitVar[typing.Iterable[ABCRule] | None] = dataclasses.field(default=None)
    agent: dataclasses.InitVar[type[Agent] | None] = dataclasses.field(default=None, kw_only=True)
    final: bool = dataclasses.field(default=True, kw_only=True)
    preset_context: Context | None = dataclasses.field(default=None, kw_only=True)

    def __post_init__(self, rules: typing.Iterable[ABCRule] | None, agent: type[Agent] | None) -> None:
        self.check_rules = deque(rules or ())
        self.agent_cls = agent or EventLoopAgent

    def __repr__(self) -> str:
        return fullname(self.function)

    @property
    def __call__(self) -> Function:
        return self.function

    async def run(
        self,
        api: API,
        update: Update,
        context: Context,
        check: bool = True,
    ) -> Result[typing.Any, str]:
        if self.preset_context:
            context |= self.preset_context

        if check and self.check_rules:
            logger.debug("Checking rules for handler `{!r}`...", self)

            with log_scope(lambda: self.function.__name__):
                for rule in self.check_rules:
                    if not await check_rule(rule, context):
                        return Error(f"Rule {rule!r} failed.")

            logger.debug("Rules passed, composing nodes and running handler `{!r}`...", self)
        else:
            logger.debug("Composing nodes and running handler `{!r}`...", self)

        async with compose(self.function, context, agent_cls=self.agent_cls) as result:
            return result.map_err(
                lambda error: "{}\n".format(
                    NodeError(f"* failed to compose handler `{self!r}`", from_error=error),
                ),
            )


__all__ = ("FuncHandler",)
