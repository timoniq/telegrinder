from __future__ import annotations

import typing
from http import HTTPStatus

import msgspec
from fntypes.misc import is_ok

from telegrinder.api.api import API
from telegrinder.api.error import APIServerError, InvalidTokenError
from telegrinder.bot.polling.abc import ABCPolling
from telegrinder.bot.polling.error_handler import ErrorHandler
from telegrinder.bot.polling.utils import compute_number
from telegrinder.modules import logger
from telegrinder.msgspec_utils import decoder
from telegrinder.types.objects import Update, UpdateType

DEFAULT_OFFSET: typing.Final[int] = 0
DEFAULT_RECONNECT_AFTER: typing.Final[float] = 5.0
DEFAULT_MAX_RECONNECTS: typing.Final[int] = 15


class Polling(ABCPolling):
    __slots__ = (
        "api",
        "timeout",
        "limit",
        "allowed_updates",
        "reconnect_after",
        "max_reconnects",
        "offset",
        "_running",
        "_reconnects_counter",
        "_error_handler",
    )

    def __init__(
        self,
        api: API,
        *,
        timeout: int | None = None,
        limit: int | None = None,
        offset: int = DEFAULT_OFFSET,
        reconnect_after: float = DEFAULT_RECONNECT_AFTER,
        max_reconnects: int = DEFAULT_MAX_RECONNECTS,
        include_updates: set[UpdateType] | None = None,
        exclude_updates: set[UpdateType] | None = None,
    ) -> None:
        self.api = api
        self.timeout = timeout
        self.limit = limit
        self.offset = max(DEFAULT_OFFSET, offset)
        self.allowed_updates = self.get_allowed_updates(
            include_updates=include_updates,
            exclude_updates=exclude_updates,
        )
        self.reconnect_after = compute_number(DEFAULT_RECONNECT_AFTER, reconnect_after, 0.0)
        self.max_reconnects = compute_number(DEFAULT_MAX_RECONNECTS, max_reconnects, 0)
        self._running = False
        self._reconnects_counter = 0
        self._error_handler = ErrorHandler(self)

    def __repr__(self) -> str:
        return (
            "<{}: api={!r}, running={}, offset={}, timeout={}, limit={}, "
            "allowed_updates={!r}, max_reconnects={}, reconnect_after={}>"
        ).format(
            type(self).__name__,
            self.api,
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
    ) -> list[UpdateType]:
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
        try:
            raw_updates = await self.api.request_raw(
                method="getUpdates",
                data=dict(
                    offset=self.offset,
                    limit=self.limit,
                    timeout=self.timeout,
                    allowed_updates=self.allowed_updates,
                ),
                timeout=self.timeout or 0 + self.api.http.timeout,
            )
        except TimeoutError:
            return msgspec.Raw(b"")

        if is_ok(raw_updates):
            return raw_updates.value

        match (error := raw_updates.error).status_code:
            case HTTPStatus.TOO_MANY_REQUESTS:
                error = APIServerError(
                    message="Too many requests to get updates",
                    retry_after=error.retry_after.unwrap_or(int(self.reconnect_after)),
                )
            case HTTPStatus.UNAUTHORIZED | HTTPStatus.NOT_FOUND as status:
                error = InvalidTokenError(
                    "Token seems to be invalid"
                    if status == HTTPStatus.NOT_FOUND
                    else "Invalid token (unauthorized)",
                )
            case HTTPStatus.BAD_GATEWAY | HTTPStatus.GATEWAY_TIMEOUT as status:
                error = APIServerError(
                    message="Telegram API server responded a {}".format(status.name.replace("_", " ")),
                    retry_after=int(self.reconnect_after),
                )

        raise error from None

    async def listen(self) -> typing.AsyncGenerator[list[Update], None]:
        logger.debug("Listening polling")
        self._running = True

        with decoder(list[Update]) as dec:
            while self._running:
                try:
                    if self._running and (raw := await self.get_updates()) and (updates := dec.decode(raw)):
                        yield updates
                        self.offset = updates[-1].update_id + 1

                    if self._reconnects_counter != 0:
                        self._reset_reconnects_counter()
                except BaseException as error:
                    if not await self._error_handler.handle(error):
                        logger.exception("Traceback message below:")

                    if isinstance(error, self.api.http.CONNECTION_TIMEOUT_ERRORS):
                        self._reconnects_counter += 1

    def stop(self) -> None:
        self._running = False
        self._reset_reconnects_counter()


__all__ = ("Polling",)
