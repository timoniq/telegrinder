import typing

from telegrinder.api.abc import ABCAPI
from telegrinder.modules import logger
from telegrinder.result import Error
from telegrinder.tools.i18n.base import I18nEnum
from telegrinder.types import Update

from .middleware.abc import ABCMiddleware

if typing.TYPE_CHECKING:
    from telegrinder.bot.dispatch.handler.abc import ABCHandler
    from telegrinder.bot.rules.abc import ABCRule

T = typing.TypeVar("T")
E = typing.TypeVar("E")  # NOTE: bound something EventType model with 'api' field
_ = typing.Any


async def process_inner(
    event: T,
    raw_event: Update,
    middlewares: list[ABCMiddleware[T]],
    handlers: list["ABCHandler[T]"],
) -> bool:
    logger.debug("Processing {!r}...", event.__class__.__name__)
    ctx = {}

    for middleware in middlewares:
        if await middleware.pre(event, ctx) is False:
            return False

    found = False
    responses = []
    for handler in handlers:
        if await handler.check(event.api, raw_event, ctx):  # type: ignore
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

    model = await rule.adapter.adapt(api, update)  # type: ignore
    # FIXME: adapter.adapt takes UpdateCute, and here it's passing Update
    match model:
        case Error(err):
            logger.debug("Adapter failed: {!r}", err)
            return False

    for requirement in rule.requires:
        if not await check_rule(api, requirement, update, ctx_copy):
            return False

    ctx |= ctx_copy

    if I18nEnum.I18N in ctx:
        rule = await rule.translate(ctx[I18nEnum.I18N])

    return await rule.check(model.unwrap(), ctx)
