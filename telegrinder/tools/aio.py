import asyncio
import typing
from inspect import isasyncgen, isawaitable

type Generator[Yield, Send, Return] = typing.AsyncGenerator[Yield, Send] | typing.Generator[Yield, Send, Return]


def run_task[T](
    task: typing.Awaitable[T],
    /,
    *,
    loop: asyncio.AbstractEventLoop | None = None,
) -> T:
    loop = loop or asyncio.get_event_loop()
    return loop.run_until_complete(future=task)


async def next_generator[T](generator: Generator[T, typing.Any, typing.Any], /) -> T:
    return await send_generator_value(generator, None)


async def send_generator_value[Yield, Send](
    generator: Generator[Yield, Send, typing.Any],
    value: Send | None,
    /,
) -> Yield:
    try:
        return (
            await generator.asend(value) if isasyncgen(generator) else generator.send(value)  # type: ignore
        )
    except StopIteration as exc:
        raise StopGenerator(exc.value, exc.args) from exc


async def stop_generator[Send, Return](
    generator: Generator[typing.Any, Send, Return],
    with_value: Send | None = None,
    /,
) -> Return | None:
    try:
        await send_generator_value(generator, with_value)
    except (StopGenerator, StopAsyncIteration) as exc:
        return exc.value if isinstance(exc, StopGenerator) else None


async def maybe_awaitable[T](obj: T | typing.Awaitable[T], /) -> T:
    if isawaitable(obj):
        return await obj
    return obj


# Source code: https://github.com/facebookincubator/later/blob/main/later/task.py#L75
async def cancel_future(fut: asyncio.Future[typing.Any], /) -> None:
    if fut.done():
        return

    fut.cancel()
    exc: asyncio.CancelledError | None = None

    while not fut.done():
        shielded = asyncio.shield(fut)
        try:
            await asyncio.wait([shielded])
        except asyncio.CancelledError as ex:
            exc = ex
        finally:
            # Insure we handle the exception/value that may exist on the shielded task
            # This will prevent errors logged to the asyncio logger
            if shielded.done() and not shielded.cancelled() and not shielded.exception():
                shielded.result()

    if fut.cancelled():
        if exc is None:
            return
        raise exc from None

    ex = fut.exception()
    if ex is not None:
        raise ex from None

    raise asyncio.InvalidStateError(
        f"Task did not raise CancelledError on cancel: {fut!r} had result {fut.result()!r}",
    )


class StopGenerator(Exception):
    value: typing.Any

    def __init__(self, value: typing.Any, *args: object) -> None:
        super().__init__(*args)
        self.value = value


__all__ = (
    "StopGenerator",
    "cancel_future",
    "maybe_awaitable",
    "next_generator",
    "run_task",
    "send_generator_value",
    "stop_generator",
)
