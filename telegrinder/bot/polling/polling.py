import asyncio
import contextlib
import datetime
import typing
from http import HTTPStatus

import msgspec
from msgspex import decoder

from telegrinder.api.api import API
from telegrinder.api.error import APIServerError, InvalidTokenError
from telegrinder.bot.cute_types.update import BaseCute, UpdateCute
from telegrinder.bot.polling.abc import ABCPolling
from telegrinder.bot.polling.error_handler import ErrorHandler, StopPolling
from telegrinder.bot.polling.utils import compute_number
from telegrinder.modules import logger
from telegrinder.tools.bound_cute import BoundCuteMixin
from telegrinder.types.objects import Update, UpdateType

DEFAULT_UPDATE_MODEL: typing.Final = UpdateCute
DEFAULT_TIMEOUT: typing.Final = 30
DEFAULT_OFFSET: typing.Final = 0
DEFAULT_RECONNECT_AFTER: typing.Final = 5.0
DEFAULT_MAX_RECONNECTS: typing.Final = 15
MAX_LIMIT: typing.Final = 100


class Polling(ABCPolling):
    update_model: type[Update]

    __slots__ = (
        "api",
        "timeout",
        "limit",
        "allowed_updates",
        "reconnect_after",
        "update_model",
        "max_reconnects",
        "offset",
        "_running",
        "_timeout_seconds",
        "_reconnects_counter",
        "_request_timeout",
        "_event_stop",
        "_error_handler",
        "_stop_task",
    )

    def __init__(
        self,
        api: API,
        *,
        update_model: type[Update] = DEFAULT_UPDATE_MODEL,
        reconnect_after: float = DEFAULT_RECONNECT_AFTER,
        max_reconnects: int = DEFAULT_MAX_RECONNECTS,
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
        self.reconnect_after = compute_number(DEFAULT_RECONNECT_AFTER, reconnect_after, 0.0)
        self.max_reconnects = compute_number(DEFAULT_MAX_RECONNECTS, max_reconnects, 0)
        self.timeout = timeout if isinstance(timeout, datetime.timedelta) else datetime.timedelta(seconds=timeout or 0)
        self.limit = None if limit is None else min(limit, MAX_LIMIT)
        self.offset = offset
        self.allowed_updates = self.get_allowed_updates(
            include_updates=set(include_updates) if include_updates is not None else None,
            exclude_updates=set(exclude_updates) if exclude_updates is not None else None,
        )
        self._running = False
        self._reconnects_counter = 0
        self._request_timeout = self.timeout + self.api.http.timeout
        self._timeout_seconds = int(self.timeout.total_seconds())
        self._event_stop = asyncio.Event()
        self._error_handler = ErrorHandler(self)
        self._stop_task: asyncio.Task[None] | None = None

    def __repr__(self) -> str:
        return (
            "<{}: api={!r}, update_model={!r}, running={}, offset={}, timeout={!r}, "
            "limit={}, allowed_updates={!r}, max_reconnects={}, reconnect_after={}>"
        ).format(
            type(self).__name__,
            self.api,
            self.update_model,
            self._running,
            self.offset,
            self.timeout,
            self.limit,
            self.allowed_updates,
            self.max_reconnects,
            self.reconnect_after,
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
    def reconnects_counter(self) -> int:
        return self._reconnects_counter

    @property
    def running(self) -> bool:
        return self._running

    def _reset_reconnects_counter(self) -> None:
        self._reconnects_counter = 0

    async def get_updates(self) -> msgspec.Raw:
        raw_updates = await self.api.request_raw(
            method="getUpdates",
            data=dict(
                offset=self.offset,
                limit=self.limit,
                timeout=self._timeout_seconds,
                allowed_updates=self.allowed_updates,
            ),
            timeout=self._request_timeout,
        )

        if raw_updates:
            return raw_updates.value

        match (error := raw_updates.error).status_code:
            case HTTPStatus.CONFLICT:
                error = APIServerError("Cannot run polling, because another bot instance is already running.")
            case HTTPStatus.UNAUTHORIZED | HTTPStatus.NOT_FOUND as status:
                error = InvalidTokenError(
                    "Token seems to be invalid" if status == HTTPStatus.NOT_FOUND else "Invalid token (unauthorized)",
                )
            case HTTPStatus.BAD_GATEWAY | HTTPStatus.GATEWAY_TIMEOUT as status:
                error = APIServerError(
                    message="Telegram API server responded a {}".format(status.name.replace("_", " ")),
                    retry_after=int(self.reconnect_after),
                )

        raise error from None

    def listen(self) -> typing.AsyncGenerator[list[Update], None]:
        async def inner() -> typing.AsyncGenerator[list[Update], None]:
            logger.debug("Listening polling")

            with decoder(
                list[self.update_model],
                context=dict(ctx_api=self.api),
            ) as updates_decoder:
                while self._running:
                    try:
                        if (raw := await self.get_updates()) and (updates := updates_decoder.decode(raw)):
                            yield updates
                            self.offset = updates[-1].update_id + 1
                    except BaseException as error:
                        if not await self._error_handler.handle(error):
                            logger.exception("Traceback message below:")

                        if isinstance(error, self.api.http.CONNECTION_TIMEOUT_ERRORS):
                            self._reconnects_counter += 1
                    else:
                        if self._reconnects_counter != 0:
                            self._reset_reconnects_counter()

        self._running = True
        self._event_stop.clear()
        generator = inner()

        async def wait_for_stop() -> None:
            await self._event_stop.wait()
            # The generator may be suspended at an inner await (the long-poll request) and so be
            # "already running", which makes athrow() raise RuntimeError. Either way the loop
            # terminates: stop() also clears _running, rechecked once the in-flight request
            # returns. Suppress so the task does not leak an unretrieved exception.
            with contextlib.suppress(StopPolling, StopAsyncIteration, RuntimeError):
                await generator.athrow(StopPolling)

        # Keep a strong reference so the task is not garbage-collected mid-flight.
        self._stop_task = asyncio.create_task(wait_for_stop())
        return generator

    def stop(self) -> None:
        self._running = False
        self._reset_reconnects_counter()

        if not self._event_stop.is_set():
            asyncio.get_running_loop().call_soon_threadsafe(self._event_stop.set)


__all__ = ("Polling",)
