import typing

from fntypes.option import Nothing, Some

from telegrinder.api.api import API
from telegrinder.bot.cute_types.update import UpdateCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware, run_middleware
from telegrinder.bot.dispatch.return_manager.abc import ABCReturnManager
from telegrinder.model import Model
from telegrinder.modules import logger
from telegrinder.node.composer import CONTEXT_STORE_NODES_KEY, NodeScope, compose_nodes
from telegrinder.tools.adapter.abc import run_adapter
from telegrinder.tools.i18n.abc import I18nEnum
from telegrinder.types.objects import Update

if typing.TYPE_CHECKING:
    from telegrinder.bot.dispatch.handler.abc import ABCHandler
    from telegrinder.bot.rules.abc import ABCRule


async def process_inner[Event: Model](
    api: API,
    event: Event,
    raw_event: Update,
    ctx: Context,
    middlewares: list[ABCMiddleware[Event]],
    handlers: list["ABCHandler[Event]"],
    return_manager: ABCReturnManager[Event] | None = None,
) -> bool:
    logger.debug("Processing {!r}...", event.__class__.__name__)
    ctx[CONTEXT_STORE_NODES_KEY] = {}  # For per-event shared nodes

    logger.debug("Run pre middlewares...")
    for m in middlewares:
        result = await run_middleware(m.pre, api, event, raw_event=raw_event, ctx=ctx, adapter=m.adapter)
        logger.debug("Middleware {!r} returned: {!r}", m, result)
        if result is False:
            return False

    found = False
    responses = []
    ctx_copy = ctx.copy()

    for handler in handlers:
        adapted_event = event

        if await handler.check(api, raw_event, ctx):
            if handler.adapter is not None:
                match await run_adapter(handler.adapter, api, raw_event, ctx):
                    case Some(value):
                        adapted_event = value
                    case Nothing():
                        continue

            found = True
            logger.debug("Handler {!r} matched, run...", handler)
            response = await handler.run(api, adapted_event, ctx)
            logger.debug("Handler {!r} returned: {!r}", handler, response)
            responses.append(response)

            if return_manager is not None:
                await return_manager.run(response, event, ctx)
            if handler.final:
                break

        ctx = ctx_copy

    logger.debug("Run post middlewares...")
    ctx.set("responses", responses)

    for m in middlewares:
        await run_middleware(
            m.post,
            api,
            event,
            raw_event=raw_event,
            ctx=ctx,
            adapter=m.adapter,
        )

    for session in ctx.get(CONTEXT_STORE_NODES_KEY, {}).values():
        await session.close(scopes=(NodeScope.PER_EVENT,))

    logger.debug(
        "{} handlers, returns {!r}",
        "No found" if not found else "Found",
        found,
    )
    return found


async def check_rule(
    api: API,
    rule: "ABCRule",
    update: Update,
    ctx: Context,
) -> bool:
    """Checks requirements, adapts update.
    Returns check result.
    """
    update_cute = None if not isinstance(update, UpdateCute) else update

    # Running adapter
    match await run_adapter(rule.adapter, api, update, ctx):
        case Some(val):
            adapted_value = val
        case Nothing():
            return False

    # Preparing update
    if isinstance(adapted_value, UpdateCute):
        update_cute = adapted_value
    elif isinstance(adapted_val := ctx.get(rule.adapter.ADAPTED_VALUE_KEY or ""), UpdateCute):
        update_cute = adapted_val
    else:
        update_cute = UpdateCute.from_update(update, bound_api=api)

    # Running subrules to fetch requirements
    ctx_copy = ctx.copy()
    for requirement in rule.requires:
        if not await check_rule(api, requirement, update_cute, ctx_copy):
            return False

    # Translating translatable rules
    if I18nEnum.I18N in ctx:
        rule = await rule.translate(ctx[I18nEnum.I18N])

    ctx |= ctx_copy

    # Composing required nodes
    nodes = rule.required_nodes
    node_col = None
    if nodes:
        result = await compose_nodes(nodes, ctx, data={Update: update, API: api})
        if not result:
            logger.debug(f"Cannot compose nodes for rule, error: {str(result.error)}")
            return False
        node_col = result.value

    # Running check
    result = await rule.bounding_check(ctx, adapted_value=adapted_value, node_col=node_col)

    # Closing node sessions if there are any
    if node_col is not None:
        await node_col.close_all()

    return result


__all__ = ("check_rule", "process_inner")
