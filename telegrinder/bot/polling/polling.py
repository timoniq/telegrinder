import asyncio
import contextlib
import datetime
import typing
from http import HTTPStatus

import msgspec
from msgspex import decoder

from telegrinder.api.api import API
from telegrinder.api.error import APIError, APIServerError, InvalidTokenError
from telegrinder.bot.cute_types.update import BaseCute, UpdateCute
from telegrinder.bot.polling.abc import ABCPolling
from telegrinder.bot.polling.error_handler import ErrorHandler, StopPolling
from telegrinder.bot.polling.utils import compute_number
from telegrinder.modules import logger
from telegrinder.tools.backoff.exponential import ExponentialBackoff
from telegrinder.tools.bound_cute import BoundCuteMixin
from telegrinder.tools.fullname import fullname
from telegrinder.tools.retry import retry
from telegrinder.types.objects import Update, UpdateType

if typing.TYPE_CHECKING:
    from telegrinder.tools.backoff.abc import ABCBackoff

DEFAULT_UPDATE_MODEL: typing.Final = UpdateCute
DEFAULT_TIMEOUT: typing.Final = 30
DEFAULT_OFFSET: typing.Final = 0
DEFAULT_RECONNECT_AFTER: typing.Final = 5.0
DEFAULT_MAX_RECONNECTS: typing.Final = 15
MAX_LIMIT: typing.Final = 100
GET_UPDATES_METHOD: typing.Final = "getUpdates"


class Polling(ABCPolling):
    update_model: type[Update]
    _stop_task: asyncio.Task[None] | None

    __slots__ = (
        "api",
        "backoff",
        "timeout",
        "limit",
        "allowed_updates",
        "reconnect_after",
        "update_model",
        "max_reconnects",
        "offset",
        "get_updates",
        "_running",
        "_timeout_seconds",
        "_request_timeout",
        "_event_stop",
        "_error_handler",
        "_stop_task",
    )

    @typing.overload
    def __init__(self, api: API) -> None: ...

    @typing.overload
    def __init__(
        self,
        api: API,
        *,
        update_model: type[Update] = DEFAULT_UPDATE_MODEL,
        timeout: int | float | datetime.timedelta | None = DEFAULT_TIMEOUT,
        offset: int = DEFAULT_OFFSET,
        limit: int | None = None,
        include_updates: typing.Iterable[UpdateType] | None = None,
        exclude_updates: typing.Iterable[UpdateType] | None = None,
    ) -> None: ...

    @typing.overload
    def __init__(
        self,
        api: API,
        *,
        backoff: ABCBackoff,
        max_reconnects: int = ...,
        update_model: type[Update] = ...,
        timeout: int | float | datetime.timedelta | None = ...,
        offset: int = ...,
        limit: int | None = ...,
        include_updates: typing.Iterable[UpdateType] | None = ...,
        exclude_updates: typing.Iterable[UpdateType] | None = ...,
    ) -> None: ...

    @typing.overload
    def __init__(
        self,
        api: API,
        *,
        max_reconnects: int = ...,
        reconnect_after: float = ...,
        update_model: type[Update] = ...,
        timeout: int | float | datetime.timedelta | None = ...,
        offset: int = ...,
        limit: int | None = ...,
        include_updates: typing.Iterable[UpdateType] | None = ...,
        exclude_updates: typing.Iterable[UpdateType] | None = ...,
    ) -> None: ...

    def __init__(
        self,
        api: API,
        *,
        update_model: type[Update] = DEFAULT_UPDATE_MODEL,
        backoff: ABCBackoff | None = None,
        max_reconnects: int = DEFAULT_MAX_RECONNECTS,
        reconnect_after: float = DEFAULT_RECONNECT_AFTER,
        timeout: int | float | datetime.timedelta | None = DEFAULT_TIMEOUT,
        offset: int = DEFAULT_OFFSET,
        limit: int | None = None,
        include_updates: typing.Iterable[UpdateType] | None = None,
        exclude_updates: typing.Iterable[UpdateType] | None = None,
    ) -> None:
        self.api = api
        self.update_model = (
            typing.cast("type[Update]", BoundCuteMixin[update_model])
            if issubclass(update_model, BaseCute)
            else update_model
        )
        self.reconnect_after = float(compute_number(DEFAULT_RECONNECT_AFTER, reconnect_after, 0.0))
        self.max_reconnects = int(compute_number(DEFAULT_MAX_RECONNECTS, max_reconnects, 0))
        self.timeout = timeout if isinstance(timeout, datetime.timedelta) else datetime.timedelta(seconds=timeout or 0)
        self.limit = None if limit is None else min(limit, MAX_LIMIT)
        self.offset = offset
        self.allowed_updates = self.get_allowed_updates(
            include_updates=set(include_updates) if include_updates is not None else None,
            exclude_updates=set(exclude_updates) if exclude_updates is not None else None,
        )
        self.backoff = ExponentialBackoff(cap=self.reconnect_after, base=0.008) if backoff is None else backoff
        self.get_updates = retry(
            APIServerError,
            *api.http.CLIENT_CONNECTION_ERRORS,
            *api.http.CONNECTION_TIMEOUT_ERRORS,
            retries=max_reconnects,
            backoff=self.backoff,
            check=None,
            sleep=self._wait_for_reconnect,
        )(self._get_updates)
        self._running = False
        self._stop_task = None
        self._request_timeout = self.timeout + self.api.http.timeout
        self._timeout_seconds = int(self.timeout.total_seconds())
        self._event_stop = asyncio.Event()
        self._error_handler = ErrorHandler(self)

    def __repr__(self) -> str:
        return (
            "<{}: api={!r}, update_model={!r}, running={}, offset={}, timeout={!r}, "
            "limit={}, allowed_updates={!r}, max_reconnects={}, backoff={!r}>"
        ).format(
            fullname(self),
            self.api,
            self.update_model,
            self._running,
            self.offset,
            self.timeout,
            self.limit,
            self.allowed_updates,
            self.max_reconnects,
            self.backoff,
        )

    @staticmethod
    def get_allowed_updates(
        *,
        include_updates: set[UpdateType] | None = None,
        exclude_updates: set[UpdateType] | None = None,
    ) -> list[UpdateType] | None:
        if include_updates is None and exclude_updates is None:
            return None

        allowed_updates = list(UpdateType)

        if include_updates and exclude_updates:
            return [x for x in allowed_updates if x in include_updates and x not in exclude_updates]

        if exclude_updates:
            return [x for x in allowed_updates if x not in exclude_updates]

        if include_updates:
            return [x for x in allowed_updates if x in include_updates]

        return allowed_updates

    @property
    def running(self) -> bool:
        return self._running

    def _convert_polling_err_status_to_py_err(self, error: APIError, /) -> BaseException:
        if error.method != GET_UPDATES_METHOD:
            return error

        match error.status_code:
            case HTTPStatus.CONFLICT:
                return APIServerError("Cannot run polling, because another bot instance is already running")
            case HTTPStatus.UNAUTHORIZED | HTTPStatus.NOT_FOUND | HTTPStatus.MISDIRECTED_REQUEST as status:
                return InvalidTokenError(
                    "Invalid token (unauthorized)"
                    if status == HTTPStatus.UNAUTHORIZED
                    else "Token seems to be invalid",
                )
            case HTTPStatus.BAD_GATEWAY | HTTPStatus.GATEWAY_TIMEOUT as status:
                return APIServerError(
                    message="Telegram API server responded: {} — {}".format(status.phrase, error.error),
                    retry_after=self.reconnect_after,
                )
            case _:
                return error

    async def _get_updates(self) -> msgspec.Raw:
        return (
            (
                await self.api.request_raw(
                    method=GET_UPDATES_METHOD,
                    data=dict(
                        offset=self.offset,
                        limit=self.limit,
                        timeout=self._timeout_seconds,
                        allowed_updates=self.allowed_updates,
                    ),
                    timeout=self._request_timeout,
                )
            )
            .map_err(self._convert_polling_err_status_to_py_err)
            .unwrap()
        )

    @staticmethod
    async def _wait_for_reconnect(backoff: float) -> None:
        logger.error("Waiting {} s for reconnect...", backoff)
        await asyncio.sleep(backoff)

    def listen(self) -> typing.AsyncGenerator[list[Update], None]:
        async def listener() -> typing.AsyncGenerator[list[Update], None]:
            logger.debug("Listening polling")

            with decoder(
                list[self.update_model],
                context=dict(ctx_api=self.api),
            ) as updates_decoder:
                self._running = True

                while self._running:
                    try:
                        if (raw := await self.get_updates()) and (updates := updates_decoder.decode(raw)):
                            yield updates
                            self.offset = updates[-1].update_id + 1
                    except BaseException as error:
                        if isinstance(error, SystemExit | KeyboardInterrupt):
                            raise

                        if not await self._error_handler.handle(error):
                            logger.exception("Traceback message below:")

        generator = listener()

        async def wait_for_stop() -> None:
            try:
                await self._event_stop.wait()
            finally:
                with contextlib.suppress(StopPolling, StopAsyncIteration, RuntimeError, asyncio.CancelledError):
                    await generator.athrow(StopPolling)

        self._event_stop.clear()
        self._stop_task = asyncio.create_task(wait_for_stop())
        return generator

    def stop(self) -> None:
        self._running = False

        if not self._event_stop.is_set() and self._stop_task is not None and not self._stop_task.done():
            asyncio.get_running_loop().call_soon_threadsafe(self._event_stop.set)


__all__ = ("Polling",)
