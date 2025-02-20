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
from telegrinder.types.objects import Update, UpdateType


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
                if err.code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.NOT_FOUND):
                    raise InvalidTokenError("Token seems to be invalid")
                if err.code in (HTTPStatus.BAD_GATEWAY, HTTPStatus.GATEWAY_TIMEOUT):
                    raise APIServerError("Unavilability of the API Telegram server")
                raise err from None

    async def listen(self) -> typing.AsyncGenerator[list[Update], None]:
        logger.debug("Listening polling")
        reconn_counter = 0
        self._stop = False

        with decoder(list[Update]) as dec:  # For improve performance
            while not self._stop:
                try:
                    updates = await self.get_updates()
                    reconn_counter = 0
                    updates_list = dec.decode(updates)
                    if updates_list:
                        yield updates_list
                        self.offset = updates_list[-1].update_id + 1
                except InvalidTokenError as e:
                    logger.error(e)
                    self.stop()
                    sys.exit(3)
                except APIServerError as e:
                    logger.error(f"{e}, waiting {self.reconnection_timeout} seconds to the next request...")
                    await asyncio.sleep(self.reconnection_timeout)
                except asyncio.CancelledError:
                    logger.info("Caught cancel, polling stopping...")
                    self.stop()
                except self.api.http.CONNECTION_TIMEOUT_ERRORS:
                    if reconn_counter > self.max_reconnetions:
                        logger.error(
                            "Failed to reconnect to the server after {} attempts, polling stopping.",
                            self.max_reconnetions,
                        )
                        self.stop()
                        sys.exit(6)
                    else:
                        logger.warning(
                            "Server disconnected, waiting {} seconds to reconnect...",
                            self.reconnection_timeout,
                        )
                        reconn_counter += 1
                        await asyncio.sleep(self.reconnection_timeout)
                except self.api.http.CLIENT_CONNECTION_ERRORS:
                    logger.error("Client connection failed, attempted to reconnect...")
                    await asyncio.sleep(self.reconnection_timeout)
                except BaseException as e:
                    logger.exception("Traceback message below:")

    def stop(self) -> None:
        self._stop = True


__all__ = ("Polling",)
