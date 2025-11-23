from __future__ import annotations

import asyncio
import sys
import typing

from telegrinder.api.error import APIServerError, InvalidTokenError
from telegrinder.modules import logger
from telegrinder.tools.aio import maybe_awaitable

if typing.TYPE_CHECKING:
    from telegrinder.bot.polling.polling import Polling


class ErrorHandler:
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
            await self._handle_system_exit(sys_exit_err)

    async def _handle_system_exit(self, error: SystemExit) -> typing.NoReturn:
        await logger.aerror("Forced exit from the program with code {}.", error.code)
        raise error from None

    async def _handle_invalid_token_error(
        self,
        error: InvalidTokenError,
    ) -> typing.NoReturn:
        await logger.aerror("{}", error)
        self._polling.stop()
        sys.exit(3)

    async def _handle_cancelled_error(self, _: asyncio.CancelledError) -> None:
        await logger.ainfo("Caught cancel, stopping polling...")
        self._polling.stop()

    async def _handle_connection_timeout_error(self, _: BaseException) -> None:
        if self._polling.reconnects_counter > self._polling.max_reconnects:
            await logger.aerror(
                "Failed to reconnect to Telegram API server after {} attempts, stopping polling...",
                self._polling.max_reconnects,
            )
            self._polling.stop()
            sys.exit(6)

        await logger.awarning(
            "Server disconnected, waiting {} seconds to reconnect...",
            self._polling.reconnect_after,
        )
        await asyncio.sleep(self._polling.reconnect_after)

    async def _handle_client_connection_error(self, _: BaseException) -> None:
        await logger.aerror(
            "Client connection failed, attempt to reconnect after {} seconds...",
            self._polling.reconnect_after,
        )
        await asyncio.sleep(self._polling.reconnect_after)

    async def _handle_api_server_error(
        self,
        error: APIServerError,
    ) -> None:
        if error.retry_after is None:
            await logger.aerror("{}", error)
            sys.exit(9)

        await logger.aerror("{}, waiting {} seconds to the next request...", error, error.retry_after)
        await asyncio.sleep(error.retry_after)


__all__ = ("ErrorHandler",)
