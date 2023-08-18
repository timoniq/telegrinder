import typing

from .middleware.abc import ABCMiddleware
from telegrinder.types import Update
from telegrinder.modules import logger
from telegrinder.result import Error
from telegrinder.api.abc import ABCAPI
from telegrinder.tools.i18n.base import I18nEnum

if typing.TYPE_CHECKING:
    from telegrinder.bot.rules.abc import ABCRule
    from .handler.abc import ABCHandler

T = typing.TypeVar("T")
E = typing.TypeVar("E")
_ = typing.Any


async def process_inner(
    event: T,
    raw_event: Update,
    middlewares: list[ABCMiddleware[T]],
    handlers: list["ABCHandler[T]"],
) -> bool:
    logger.debug("Processing {}", event.__class__.__name__)
    ctx = {}

    for middleware in middlewares:
        if await middleware.pre(event, ctx) is False:
            return False

    found = False
    responses = []
    for handler in handlers:
        if await handler.check(event.api, raw_event, ctx):
            found = True
            handler.ctx |= ctx
            responses.append(await handler.run(event))
            if handler.is_blocking:
                break

    for middleware in middlewares:
        await middleware.post(event, responses, ctx)

    return found


async def check_rule(
    api: ABCAPI, rule: "ABCRule", update: Update, ctx: dict[str, _]
) -> bool:
    """Checks requirements, adapts update
    Returns check result"""

    ctx_copy = ctx.copy()

    model = await rule.adapter.adapt(api, update)
    match model:
        case Error(err):
            logger.debug("Adapter failed: {}", err)
            return False

    for requirement in rule.requires:
        if not await check_rule(api, requirement, update, ctx_copy):
            return False

    ctx |= ctx_copy

    if I18nEnum.I18N in ctx:
        rule = await rule.translate(ctx[I18nEnum.I18N])

    return await rule.check(model.unwrap(), ctx)
