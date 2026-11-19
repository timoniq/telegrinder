import asyncio
import inspect
import time
import typing
from functools import wraps

from telegrinder.tools.aio import maybe_awaitable

if typing.TYPE_CHECKING:
    from telegrinder.tools.backoff.abc import ABCBackoff


def _run_retryer(
    *,
    exceptions: tuple[type[BaseException], ...],
    func: typing.Callable[..., typing.Any],
    args: tuple[typing.Any, ...],
    kwargs: dict[str, typing.Any],
    backoff: ABCBackoff,
    retries: int,
    fail: typing.Callable[[BaseException], typing.Any] | None,
    sleep: typing.Callable[[float], typing.Any] | None,
    check: typing.Callable[[BaseException], bool] | None,
) -> typing.Any:
    failures = 0

    while True:
        try:
            return func(*args, **kwargs)
        except exceptions as exception:
            if check is not None and not check(exception):
                raise

            failures += 1

            if fail is not None:
                fail(exception)

            if retries >= 0 and failures > retries:
                raise

            delay = backoff.compute(failures)

            if delay > 0:
                time.sleep(delay) if sleep is None else sleep(delay)


async def _run_async_retryer(
    *,
    exceptions: tuple[type[BaseException], ...],
    func: typing.Callable[..., typing.Any],
    args: tuple[typing.Any, ...],
    kwargs: dict[str, typing.Any],
    backoff: ABCBackoff,
    retries: int,
    fail: typing.Callable[[BaseException], typing.Any] | None,
    sleep: typing.Callable[[float], typing.Coroutine[typing.Any, typing.Any, typing.Any]] | None,
    check: typing.Callable[[BaseException], bool] | None,
) -> typing.Any:
    failures = 0

    while True:
        try:
            return await func(*args, **kwargs)
        except exceptions as exception:
            if check is not None and not check(exception):
                raise

            failures += 1

            if fail is not None:
                await maybe_awaitable(fail(exception))

            if retries >= 0 and failures > retries:
                raise

            delay = backoff.compute(failures)

            if delay > 0:
                await (asyncio.sleep(delay) if sleep is None else sleep(delay))


def retry[**P, R](
    *exceptions: type[BaseException],
    retries: int,
    backoff: ABCBackoff,
    fail: typing.Callable[[BaseException], typing.Any] | None = None,
    check: typing.Callable[[BaseException], bool] | None = lambda e: isinstance(e, RetryableError),
    sleep: typing.Callable[[float], typing.Any] | None = None,
) -> typing.Callable[[typing.Callable[P, R]], typing.Callable[P, R]]:
    def decorator(f: typing.Callable[P, R], /) -> typing.Callable[P, R]:
        retryer = _run_async_retryer if inspect.iscoroutinefunction(f) else _run_retryer

        @wraps(f)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            result = retryer(
                exceptions=exceptions,
                func=f,
                args=args,
                kwargs=kwargs,
                backoff=backoff,
                retries=retries,
                fail=fail,
                check=check,
                sleep=sleep,
            )
            return typing.cast("R", result)

        return wrapper

    return decorator


class RetryableError(BaseException):
    pass


__all__ = ("RetryableError", "retry")
