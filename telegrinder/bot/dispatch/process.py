import typing

from fntypes.result import Error, Ok

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.cute_types import BaseCute
from telegrinder.bot.cute_types.update import UpdateCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.modules import logger
from telegrinder.node import compose_nodes
from telegrinder.tools.i18n.base import I18nEnum
from telegrinder.types import Update

from .middleware.abc import ABCMiddleware
from .return_manager.abc import ABCReturnManager

if typing.TYPE_CHECKING:
    from telegrinder.bot.dispatch.handler.abc import ABCHandler
    from telegrinder.bot.rules.abc import ABCRule

Event = typing.TypeVar("Event", bound=BaseCute)
_: typing.TypeAlias = typing.Any


async def process_inner(
    event: Event,
    raw_event: Update,
    middlewares: list[ABCMiddleware[Event]],
    handlers: list["ABCHandler[Event]"],
    return_manager: ABCReturnManager[Event] | None = None,
) -> bool:
    logger.debug("Processing {!r}...", event.__class__.__name__)
    ctx = Context(raw_update=raw_event)

    for middleware in middlewares:
        if await middleware.pre(event, ctx) is False:
            return False

    found = False
    responses = []
    ctx_copy = ctx.copy()

    for handler in handlers:
        if await handler.check(event.api, raw_event, ctx):
            found = True
            response = await handler.run(event, ctx)
            logger.debug("Handler {!r} returned: {!r}", handler, response)
            responses.append(response)
            if return_manager is not None:
                await return_manager.run(response, event, ctx)
            if handler.is_blocking:
                break
            ctx = ctx_copy

    for middleware in middlewares:
        await middleware.post(event, responses, ctx)

    return found


async def check_rule(
    api: ABCAPI,
    rule: "ABCRule",
    update: Update,
    ctx: Context,
) -> bool:
    """Checks requirements, adapts update.
    Returns check result."""

    # Running adapter to resolve event model
    match await rule.adapter.adapt(api, update):
        case Ok(value):
            adapted_value = value
        case Error(err):
            logger.debug("Adapter failed with error message: {!r}", str(err))
            return False

    # Running subrules to fetch requirements
    ctx_copy = ctx.copy()
    for requirement in rule.requires:
        if not await check_rule(api, requirement, update, ctx_copy):
            return False

    # Translating translatable rules
    if I18nEnum.I18N in ctx:
        rule = await rule.translate(ctx.get(I18nEnum.I18N))

    ctx |= ctx_copy

    # Composing required nodes
    nodes = rule.get_required_nodes()
    node_col = None
    if nodes:
        node_col = await compose_nodes(nodes, UpdateCute.from_update(update, api))
        if node_col is None:
            return False

    # Running check
    result = await rule.bounding_check(adapted_value, node_col=node_col, ctx=ctx)

    # Closing node sessions if there are any
    if node_col is not None:
        await node_col.close_all()

    return result


__all__ = ("check_rule", "process_inner")
