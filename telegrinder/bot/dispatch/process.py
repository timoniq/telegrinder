from __future__ import annotations

import typing

from fntypes.result import Error, Ok

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware, run_middleware
from telegrinder.modules import logger
from telegrinder.node.composer import CONTEXT_STORE_NODES_KEY, compose_nodes
from telegrinder.tools.aio import maybe_awaitable
from telegrinder.tools.fullname import fullname
from telegrinder.tools.magic.function import bundle
from telegrinder.types.objects import Update

if typing.TYPE_CHECKING:
    from telegrinder.bot.dispatch.view.base import BaseView
    from telegrinder.bot.rules.abc import ABCRule


async def process_inner(
    api: API,
    event: Update,
    ctx: Context,
    view: BaseView,
) -> bool:
    ctx[CONTEXT_STORE_NODES_KEY] = {}  # For per-event shared nodes

    for m in view.middlewares:
        if m.pre is ABCMiddleware.pre:
            continue

        if await run_middleware(m.pre, api, event, ctx, required_nodes=m.pre_required_nodes) is False:
            logger.info(
                "Update(id={}, type={!r}) processed with view `{}`. Pre-middleware `{}` raised failure.",
                event.update_id,
                event.update_type,
                type(view).__name__,
                fullname(m),
            )
            return False

    found_handlers = []
    responses = list[typing.Any]()
    ctx_copy = ctx.copy()

    for handler in view.handlers:
        match await handler.run(api, event, ctx):
            case Ok(response):
                found_handlers.append(handler)
                responses.append(response)

                if view.return_manager is not None:
                    await view.return_manager.run(response, api, event, ctx)

                if handler.final is True:
                    break
            case Error(error):
                logger.debug(error)

    ctx = ctx_copy
    ctx.responses = responses

    for m in view.middlewares:
        if m.post is not ABCMiddleware.post:
            await run_middleware(
                m.post,
                api,
                event,
                ctx,
                required_nodes=m.post_pre_required_nodes,
            )

    logger.info(
        "Update(id={}, type={!r}) processed with view `{}`. {}",
        event.update_id,
        event.update_type,
        type(view).__name__,
        "No found corresponded handlers."
        if not found_handlers
        else f"Handler{'s' if len(found_handlers) > 1 else ''}: {', '.join(f'`{x}`' for x in found_handlers)}",
    )
    return bool(found_handlers)


async def check_rule(
    api: API,
    rule: ABCRule,
    update: Update,
    ctx: Context,
) -> bool:
    """Checks requirements, adapts update.
    Returns check result.
    """
    # Running subrules to fetch requirements
    ctx_copy = ctx.copy()
    for requirement in rule.requires:
        if not await check_rule(api, requirement, update, ctx_copy):
            return False

    ctx |= ctx_copy
    node_col = None
    data = {Update: update, API: api, Context: ctx}

    # Composing required nodes
    if rule.required_nodes:
        match await compose_nodes(rule.required_nodes, ctx, data=data):
            case Ok(value):
                node_col = value
            case Error(compose_error):
                logger.debug(
                    "Cannot compose nodes for rule `{!r}`, error: {!r}",
                    rule,
                    compose_error.message,
                )
                return False

    # Running check
    try:
        data_bundle = bundle(rule.check, data, typebundle=True)
        return await maybe_awaitable(
            bundle(rule.check, ctx | ({} if node_col is None else node_col.values))(
                *data_bundle.args,
                **data_bundle.kwargs,
            ),
        )
    finally:
        # Closing node sessions if there are any
        if node_col is not None:
            await node_col.close_all()


__all__ = ("check_rule", "process_inner")
