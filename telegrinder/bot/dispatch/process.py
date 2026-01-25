import typing

from kungfu.library.monad.result import Error, Ok, Result
from nodnod.error import NodeError

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.middleware.abc import run_post_middleware, run_pre_middleware
from telegrinder.modules import logger
from telegrinder.node.compose import compose
from telegrinder.tools.fullname import fullname
from telegrinder.types.objects import Update

if typing.TYPE_CHECKING:
    from telegrinder.bot.dispatch.handler.abc import ABCHandler
    from telegrinder.bot.dispatch.view.base import View
    from telegrinder.bot.rules.abc import ABCRule


async def process_inner(
    api: API,
    update: Update,
    context: Context,
    view: View,
) -> Result[str, str]:
    for middleware in view.middlewares:
        if await run_pre_middleware(middleware, context) is False:
            await logger.ainfo(
                "Update(id={}, type={!r}) processed with view `{}`. Pre-middleware `{}` raised failure.",
                update.update_id,
                update.update_type,
                view,
                fullname(middleware),
            )
            return Error(f"Pre-middleware `{fullname(middleware)}` raised failure.")

    found_handlers: list[ABCHandler] = []
    responses: list[typing.Any] = []

    for handler in view.handlers:
        match await handler.run(api, update, context):
            case Ok(response):
                found_handlers.append(handler)
                responses.append(response)

                if view.return_manager is not None:
                    await view.return_manager.run(response, api, update, context)

                if handler.final is True:
                    break
            case Error(error):
                await logger.adebug("Running handler `{!r}` failed with error: {}", handler, error)

    context.responses = responses

    for middleware in view.middlewares:
        await run_post_middleware(middleware, context)

    if not found_handlers:
        return Error("No found corresponded handlers.")

    return Ok(
        f"Handler{'s' if len(found_handlers) > 1 else ''}: " + "".join(repr(handler) for handler in found_handlers)
    )


async def check_rule(rule: ABCRule, context: Context) -> bool:
    for requirement in rule.requires:
        if not await check_rule(requirement, context):
            return False

    await logger.adebug("  → Checking rule `{!r}`...", rule)

    async with compose(rule.composable, context) as result:
        match result:
            case Ok(result):
                await logger.adebug("    * Rule `{!r}` is {}", rule, "ok" if result else "failed")
                return result
            case Error(error):
                await logger.adebug(
                    "    * Rule `{}` failed with error:{}\n",
                    fullname(rule),
                    NodeError(f"* failed to compose check of `{fullname(rule)}` rule", from_error=error),
                )

    return False


__all__ = ("check_rule", "process_inner")
