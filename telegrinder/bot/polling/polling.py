from __future__ import annotations

import asyncio
import sys
import typing
from http import HTTPStatus

import msgspec
from fntypes.misc import is_ok

from telegrinder.api.api import API
from telegrinder.api.error import APIServerError, InvalidTokenError
from telegrinder.bot.polling.abc import ABCPolling
from telegrinder.modules import logger
from telegrinder.msgspec_utils import decoder
from telegrinder.tools.aio import maybe_awaitable
from telegrinder.types.objects import Update, UpdateType

DEFAULT_OFFSET: typing.Final[int] = 0
DEFAULT_RECONNECT_AFTER: typing.Final[float] = 5.0
DEFAULT_MAX_RECONNECTS: typing.Final[int] = 15


def _compute_number(
    default: int | float,
    input_value: int | float,
    conditional_value: int | float,
    /,
) -> int | float:
    return max(default, input_value) * (input_value <= conditional_value) + input_value * (
        input_value >= conditional_value
    )


class PollingErrorHandler:
    _handlers: dict[type[BaseException], typing.Callable[[BaseException], typing.Any]]

    __slots__ = ("_polling", "_handlers")

    def __init__(self, polling: Polling, /) -> None:
        self._polling = polling
        self._handlers = {  # type: ignore
            InvalidTokenError: self._handle_invalid_token_error,
            asyncio.CancelledError: self._handle_cancelled_error,
            APIServerError: self._handle_api_server_error,
            **{e: self._handle_connection_timeout_error for e in polling.api.http.CONNECTION_TIMEOUT_ERRORS},
            **{e: self._handle_client_connection_error for e in polling.api.http.CLIENT_CONNECTION_ERRORS},
        }

    async def handle(self, error: BaseException) -> bool:
        error_class = type(error)

        if error_class is SystemExit:
            self._handle_system_exit(error)  # type: ignore

        if error_class not in self._handlers:
            return False

        try:
            await maybe_awaitable(self._handlers[error_class](error))
            return True
        except SystemExit as sys_exit_err:
            self._handle_system_exit(sys_exit_err)

    def _handle_system_exit(self, error: SystemExit) -> typing.NoReturn:
        logger.error(f"Forced exit from the program with code {error.code}.")
        raise error from None

    def _handle_invalid_token_error(
        self,
        error: InvalidTokenError,
    ) -> typing.NoReturn:
        logger.error(error)
        self._polling.stop()
        sys.exit(3)

    def _handle_cancelled_error(self, _: asyncio.CancelledError) -> None:
        logger.info("Caught cancel, stopping polling...")
        self._polling.stop()

    async def _handle_connection_timeout_error(self, _: BaseException) -> None:
        if self._polling.reconnects_counter > self._polling.max_reconnects:
            logger.error(
                "Failed to reconnect to Telegram API server after {} attempts, stopping polling...",
                self._polling.max_reconnects,
            )
            self._polling.stop()
            sys.exit(6)

        logger.warning(
            "Server disconnected, waiting {} seconds to reconnect...",
            self._polling.reconnect_after,
        )
        await asyncio.sleep(self._polling.reconnect_after)

    async def _handle_client_connection_error(self, _: BaseException) -> None:
        logger.error(
            "Client connection failed, attempt to reconnect after {} seconds...",
            self._polling.reconnect_after,
        )
        await asyncio.sleep(self._polling.reconnect_after)

    async def _handle_api_server_error(
        self,
        error: APIServerError,
    ) -> None:
        logger.error(f"{error}, waiting {error.retry_after} seconds to the next request...")
        await asyncio.sleep(error.retry_after)


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
        self.allowed_updates = self.get_allowed_updates(
            include_updates=include_updates,
            exclude_updates=exclude_updates,
        )
        self.reconnect_after = _compute_number(DEFAULT_RECONNECT_AFTER, reconnect_after, 0.0)
        self.max_reconnects = _compute_number(DEFAULT_MAX_RECONNECTS, max_reconnects, 0)
        self.offset = max(DEFAULT_OFFSET, offset)
        self._running = False
        self._reconnects_counter = 0
        self._error_handler = PollingErrorHandler(self)

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
                    if (raw := await self.get_updates()) and (updates := dec.decode(raw)):
                        yield updates
                        self.offset = updates[-1].update_id + 1

                    self._reconnects_counter = 0
                except BaseException as error:
                    if not await self._error_handler.handle(error):
                        logger.exception("Traceback message below:")

                    if isinstance(error, self.api.http.CONNECTION_TIMEOUT_ERRORS):
                        self._reconnects_counter += 1

    def stop(self) -> None:
        self._reconnects_counter = 0
        self._running = False


__all__ = ("Polling",)
