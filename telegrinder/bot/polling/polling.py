from __future__ import annotations

import asyncio
import sys
import typing
from http import HTTPStatus

import msgspec
from fntypes.result import Error, Ok

from telegrinder.api.api import API, HTTPClient
from telegrinder.api.error import APIServerError, InvalidTokenError
from telegrinder.bot.polling.abc import ABCPolling
from telegrinder.modules import logger
from telegrinder.msgspec_utils import decoder
from telegrinder.tools.aio import maybe_awaitable
from telegrinder.types.objects import Update, UpdateType


class PollingErrorHandler(typing.Generic[HTTPClient]):
    _handlers: dict[type[BaseException], typing.Callable[[BaseException], typing.Any]]

    __slots__ = ("_polling", "_reconn_counter", "_handlers")

    def __init__(self, polling: Polling[HTTPClient]) -> None:
        self._polling = polling
        self._reconn_counter = 0
        self._handlers = {  # type: ignore
            SystemExit: self._handle_system_exit,
            InvalidTokenError: self._handle_invalid_token_error,
            asyncio.CancelledError: self._handle_cancelled_error,
            APIServerError: self._handle_api_server_error,
            **{e: self._handle_connection_timeout_error for e in polling.api.http.CONNECTION_TIMEOUT_ERRORS},
            **{e: self._handle_client_connection_error for e in polling.api.http.CLIENT_CONNECTION_ERRORS},
        }

    async def handle(self, error: BaseException) -> bool:
        if type(error) not in self._handlers:
            return False

        try:
            await maybe_awaitable(self._handlers[type(error)](error))
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
        logger.info("Caught cancel, polling stopping...")
        self._polling.stop()

    async def _handle_connection_timeout_error(self, _: BaseException) -> None:
        if self._reconn_counter > self._polling.max_reconnetions:
            logger.error(
                "Failed to reconnect to the server after {} attempts, polling stopping.",
                self._polling.max_reconnetions,
            )
            self._polling.stop()
            sys.exit(6)

        logger.warning(
            "Server disconnected, waiting {} seconds to reconnect...",
            self._polling.reconnection_timeout,
        )
        self._reconn_counter += 1
        await asyncio.sleep(self._polling.reconnection_timeout)

    async def _handle_client_connection_error(self, _: BaseException) -> None:
        logger.error("Client connection failed, attempted to reconnect...")
        await asyncio.sleep(self._polling.reconnection_timeout)

    async def _handle_api_server_error(
        self,
        error: APIServerError,
    ) -> None:
        logger.error(f"{error}, waiting {error.retry_after} seconds to the next request...")
        await asyncio.sleep(error.retry_after)


class Polling(ABCPolling, typing.Generic[HTTPClient]):
    def __init__(
        self,
        api: API[HTTPClient],
        *,
        offset: int = 0,
        reconnection_timeout: float = 5.0,
        max_reconnetions: int = 15,
        include_updates: set[str | UpdateType] | None = None,
        exclude_updates: set[str | UpdateType] | None = None,
    ) -> None:
        self.api = api
        self.allowed_updates = self.get_allowed_updates(
            include_updates=include_updates,
            exclude_updates=exclude_updates,
        )
        self.reconnection_timeout = 5.0 if reconnection_timeout < 0 else reconnection_timeout
        self.max_reconnetions = 15 if max_reconnetions < 0 else max_reconnetions
        self.offset = offset
        self._stop = True
        self._error_handler = PollingErrorHandler(self)

    def __repr__(self) -> str:
        return (
            "<{}: with api={!r}, stopped={}, offset={}, allowed_updates={!r}, "
            "max_reconnetions={}, reconnection_timeout={}>"
        ).format(
            self.__class__.__name__,
            self.api,
            self._stop,
            self.offset,
            self.allowed_updates,
            self.max_reconnetions,
            self.reconnection_timeout,
        )

    @staticmethod
    def get_allowed_updates(
        *,
        include_updates: set[str | UpdateType] | None = None,
        exclude_updates: set[str | UpdateType] | None = None,
    ) -> list[str]:
        allowed_updates: list[str] = list(x.value for x in UpdateType)
        if not include_updates and not exclude_updates:
            return allowed_updates

        if include_updates and exclude_updates:
            allowed_updates = [x for x in allowed_updates if x in include_updates and x not in exclude_updates]
        elif exclude_updates:
            allowed_updates = [x for x in allowed_updates if x not in exclude_updates]
        elif include_updates:
            allowed_updates = [x for x in allowed_updates if x in include_updates]

        return [x.value if isinstance(x, UpdateType) else x for x in allowed_updates]

    async def get_updates(self) -> msgspec.Raw:
        raw_updates = await self.api.request_raw(
            method="getUpdates",
            data=dict(
                offset=self.offset,
                allowed_updates=self.allowed_updates,
            ),
        )

        match raw_updates:
            case Ok(value):
                return value
            case Error(err):
                if err.status_code == HTTPStatus.TOO_MANY_REQUESTS:
                    raise APIServerError(
                        "Too many requests to get updates",
                        err.retry_after.unwrap_or(int(self.reconnection_timeout)),
                    ) from None

                if err.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.NOT_FOUND):
                    raise InvalidTokenError("Token seems to be invalid") from None

                if err.status_code in (HTTPStatus.BAD_GATEWAY, HTTPStatus.GATEWAY_TIMEOUT):
                    raise APIServerError(
                        "Unavilability of the API Telegram server",
                        int(self.reconnection_timeout),
                    ) from None

                raise err from None

    async def listen(self) -> typing.AsyncGenerator[list[Update], None]:
        logger.debug("Listening polling")
        self._stop = False

        with decoder(list[Update]) as dec:
            while not self._stop:
                try:
                    updates = await self.get_updates()
                    updates_list = dec.decode(updates)
                    if updates_list:
                        yield updates_list
                        self.offset = updates_list[-1].update_id + 1
                except BaseException as error:
                    if not await self._error_handler.handle(error):
                        logger.exception("Traceback message below:")

    def stop(self) -> None:
        self._stop = True


__all__ = ("Polling",)
