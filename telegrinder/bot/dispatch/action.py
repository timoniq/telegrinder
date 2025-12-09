from __future__ import annotations

import typing

from kungfu.library import Error, Ok, Result, unwrapping
from nodnod.error import NodeError

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.handler.func import FuncHandler
from telegrinder.bot.dispatch.process import check_rule
from telegrinder.bot.rules.abc import ABCRule, Always, AndRule
from telegrinder.modules import logger
from telegrinder.node.compose import compose
from telegrinder.tools import fullname
from telegrinder.types.objects import Update

if typing.TYPE_CHECKING:
    from nodnod.agent.base import Agent

type Handler = typing.Callable[..., typing.Any]
type ActionFunction = typing.Callable[..., ActionFunctionResult]
type ActionFunctionResult = typing.Union[
    typing.AsyncGenerator[typing.Any, typing.Any],
    typing.Awaitable[typing.Any],
    typing.Generator[typing.Any, typing.Any, typing.Any],
    typing.Any,
]


@unwrapping
async def run_action_function[T: Handler](
    func_handler: FuncHandler[T],
    function: ActionFunction,
    api: API,
    update: Update,
    context: Context,
    agent: type[Agent] | None = None,
) -> Result[typing.Any, str]:
    async with compose(
        function,
        context,
        agent_cls=agent,
    ) as result:
        match result:
            case Ok():
                res = await func_handler.run(api, update, context)
            case Error(error):
                return Error(
                    str(NodeError(f"failed to compose action function `{fullname(function)}`", from_error=error)),
                )

        return res


def action(function: ActionFunction, agent: type[Agent] | None = None) -> Action:
    return Action(function, agent=agent)


class Action:
    _on: ABCRule

    def __init__(self, function: ActionFunction, agent: type[Agent] | None = None) -> None:
        self.function = function
        self.agent = agent
        self._on = Always()

    def on(self, *rules: ABCRule) -> typing.Self:
        self._on &= AndRule(*rules)
        return self

    def __call__[T: Handler](self, handler: T) -> T:
        func_handler = FuncHandler(function=handler, agent=self.agent)

        async def action_wrapper(api: API, update: Update, context: Context) -> typing.Any:
            if not await check_rule(self._on, context):
                await logger.adebug("Action rule `{!r}` failed.", self._on)
                result = await func_handler.run(api, update, context)
            else:
                result = await run_action_function(
                    func_handler,
                    self.function,
                    api,
                    update,
                    context,
                    agent=self.agent,
                )

            match result:
                case Ok(value):
                    return value
                case Error(error):
                    await logger.adebug(error)
                    return None

        action_wrapper.__name__ = f"<action for {handler.__name__}>"
        action_wrapper.__qualname__ = f"<action for {handler.__qualname__}>"
        return action_wrapper  # type: ignore


__all__ = ("Action", "action")
