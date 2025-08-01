from __future__ import annotations

import inspect
import typing

from fntypes.library import Error, Ok, Result, unwrapping

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.handler.func import FuncHandler
from telegrinder.bot.dispatch.process import check_rule
from telegrinder.bot.rules.abc import ABCRule, Always, AndRule
from telegrinder.modules import logger
from telegrinder.node.base import get_nodes
from telegrinder.node.composer import compose_nodes
from telegrinder.tools.aio import maybe_awaitable, next_generator, stop_generator
from telegrinder.tools.magic.function import bundle
from telegrinder.types.objects import Update

type When = ABCRule
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
) -> Result[typing.Any, str]:
    data = {API: api, Update: update}
    node_col = (
        (
            await compose_nodes(
                nodes=get_nodes(function),
                ctx=context,
                data=data,
            )
        )
        .map_err(lambda error: error.message)
        .unwrap()
    )

    temp_ctx = context.copy()
    bundle_function = bundle(function, {Context: temp_ctx, **data}, start_idx=0, typebundle=True)
    bundle_function &= bundle(
        function,
        context | ({} if node_col is None else node_col.values),
        start_idx=0,
    )
    result = bundle_function()

    try:
        if inspect.isasyncgen(result) or inspect.isgenerator(result):
            value = await next_generator(result)
            handler_result = await func_handler.run(api, update, context)
            await stop_generator(result, value)
            return handler_result

        await maybe_awaitable(result)
        return await func_handler.run(api, update, context)
    finally:
        context |= temp_ctx
        # Closing per call node sessions
        await node_col.close_all()


def action(function: ActionFunction, /) -> Action:
    return Action(function)


class Action:
    _on: ABCRule

    def __init__(self, function: ActionFunction) -> None:
        self.function = function
        self._on = Always()

    def on(self, *rules: ABCRule) -> typing.Self:
        self._on &= AndRule(*rules)
        return self

    def __call__[T: Handler](self, handler: T) -> T:
        func_handler = FuncHandler(function=handler)

        async def action_wrapper(api: API, update: Update, context: Context) -> typing.Any:
            if not await check_rule(api, self._on, update, context):
                logger.debug("When action rule `{!r}` failed.", self._on)
                result = await func_handler.run(api, update, context)
            else:
                result = await run_action_function(func_handler, self.function, api, update, context)

            match result:
                case Ok(value):
                    return value
                case Error(error):
                    logger.debug(error)
                    return None

        action_wrapper.__name__ = f"<action for {handler.__name__}>"
        action_wrapper.__qualname__ = f"<action for {handler.__qualname__}>"
        return action_wrapper  # type: ignore


__all__ = ("Action", "action")
