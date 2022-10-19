import typing

from .waiter import Waiter
from .middleware.abc import ABCMiddleware
from .handler.abc import ABCHandler
from telegrinder.types import Update
from telegrinder.modules import logger

T = typing.TypeVar("T")
E = typing.TypeVar("E")


async def process_waiters(
    waiters: typing.Dict[T, Waiter],
    key: T,
    event: typing.Optional[E],
    raw_event: dict,
    str_handler: typing.Callable,
) -> bool:
    if key not in waiters:
        return False

    logger.debug(
        "update {} found in waiter (key={})", event.__class__.__name__, str(key)
    )

    waiter = waiters[key]
    ctx = {}

    for rule in waiter.rules:
        chk_event = event
        if rule.__event__ is None:
            chk_event = raw_event
        if not await rule.run_check(chk_event, ctx):
            if not waiter.default:
                return True
            elif isinstance(waiter.default, str):
                await str_handler(waiter.default)
            else:
                await waiter.default(event)
            return True

    logger.debug("waiter set as ready")

    waiters.pop(key)
    setattr(waiter.event, "e", (event, ctx))
    waiter.event.set()
    return True


async def process_inner(
    event: T,
    raw_event: Update,
    middlewares: typing.List[ABCMiddleware[T]],
    handlers: typing.List[ABCHandler[T]],
) -> bool:
    logger.debug("processing {}", event.__class__.__name__)
    ctx = {}

    for middleware in middlewares:
        if await middleware.pre(event, ctx) is False:
            return False

    found = False
    responses = []
    for handler in handlers:
        result = await handler.check(event.api, raw_event)
        if result:
            handler.ctx.update(ctx)
            found = True
            response = await handler.run(event)
            responses.append(response)
            if handler.is_blocking:
                break

    for middleware in middlewares:
        await middleware.post(event, responses, ctx)

    return found
