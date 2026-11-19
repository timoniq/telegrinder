import asyncio
import typing

from kungfu import UnwrapError

from telegrinder.api.error import APIServerError, InvalidTokenError
from telegrinder.modules import logger
from telegrinder.tools.aio import maybe_awaitable

if typing.TYPE_CHECKING:
    from telegrinder.bot.polling.polling import Polling


class StopPolling(Exception):
    def __init__(self) -> None:
        super().__init__("Polling was stopped")


class ErrorHandler:
    type Handlers = dict[type[BaseException], typing.Callable[[BaseException], typing.Any]]

    _handlers: Handlers

    __slots__ = ("_polling", "_handlers")

    def __init__(self, polling: Polling, /) -> None:
        self._polling = polling
        self._handlers = typing.cast(
            "ErrorHandler.Handlers",
            {
                InvalidTokenError: self._handle_invalid_token_error,
                asyncio.CancelledError: self._handle_cancelled_error,
                StopPolling: lambda error: logger.debug("{!s}", error),
            },
        )

        for error in (
            APIServerError,
            *self._polling.api.http.CONNECTION_TIMEOUT_ERRORS,
            *self._polling.api.http.CLIENT_CONNECTION_ERRORS,
        ):
            self._handlers[error] = self._handle_fail_reconnections

    async def handle(self, error: BaseException) -> bool:
        if isinstance(error, UnwrapError):
            error = error.__error__.unwrap_or(error)

        error_class = type(error)

        if error_class not in self._handlers:
            return False

        await maybe_awaitable(self._handlers[error_class](error))
        return True

    def _handle_invalid_token_error(self, error: InvalidTokenError) -> typing.NoReturn:
        logger.error("{!s}", error)
        self._polling.stop()
        raise SystemExit(3) from None

    def _handle_cancelled_error(self, _: BaseException) -> None:
        logger.info("Caught cancel, stopping polling")
        self._polling.stop()

    def _handle_fail_reconnections(self, error: BaseException) -> None:
        logger.error(
            "Exit the program after failed tries to reconnect; last reconnection error type: `{}`",
            error.__class__.__name__,
        )
        raise SystemExit(9) from None


__all__ = ("ErrorHandler",)
