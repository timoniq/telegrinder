import asyncio
import dataclasses
import types
import typing
from functools import wraps
from http import HTTPStatus

from kungfu import is_ok

from telegrinder.tools.aio import maybe_awaitable
from telegrinder.tools.backoff.exponential import ExponentialBackoff

if typing.TYPE_CHECKING:
    from kungfu import Result

    from telegrinder.api.api import API
    from telegrinder.api.error import APIError
    from telegrinder.tools.backoff.abc import ABCBackoff

    type Fail = typing.Callable[[APIError, float], typing.Any]
    type APIRequestMethod[T: API, **P, R] = typing.Callable[
        typing.Concatenate[T, P],
        typing.Coroutine[typing.Any, typing.Any, Result[R, APIError]],
    ]

DEFAULT_FAIL_HANDLERS = types.MappingProxyType[HTTPStatus, "list[Fail]"](
    mapping={
        HTTPStatus.TOO_MANY_REQUESTS: [
            lambda err, backoff: asyncio.sleep(err.retry_after.unwrap_or(backoff)),
        ],
        HTTPStatus.INTERNAL_SERVER_ERROR: [
            lambda err, backoff: asyncio.sleep(backoff) if "restart" in err.error else None,
        ],
    },
)


def retryer[T: API, **P, R](func: APIRequestMethod[T, P, R], /) -> APIRequestMethod[T, P, R]:
    @wraps(func)
    async def wrapper(
        self: T,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[typing.Any, APIError]:
        failures = 0

        while True:
            result = await func(self, *args, **kwargs)

            if is_ok(result) or not self.retryer_is_enabled or failures >= self.max_retries:
                return result

            error = result.error

            if self.retryer is not None and error in self.retryer.fail_handlers:
                backoff = self.retryer.backoff.compute(failures)

                for handler in self.retryer.fail_handlers[error.status_code]:
                    if await maybe_awaitable(handler(error, backoff)) is False:
                        continue

            else:
                return result

            failures += 1

    return wrapper


@dataclasses.dataclass(kw_only=True)
class APIRetryer:
    retries: int
    backoff: ABCBackoff = dataclasses.field(default_factory=ExponentialBackoff)
    fail_handlers: typing.Mapping[HTTPStatus, list[Fail]] = DEFAULT_FAIL_HANDLERS

    @classmethod
    def build(
        cls, *, retries: int, fail_handlers: typing.Mapping[HTTPStatus, list[Fail]], backoff: ABCBackoff | None = None
    ) -> typing.Self:
        handlers = DEFAULT_FAIL_HANDLERS | fail_handlers
        return (
            cls(retries=retries, fail_handlers=handlers)
            if backoff is None
            else cls(retries=retries, backoff=backoff, fail_handlers=handlers)
        )


__all__ = ("APIRetryer", "retryer")
