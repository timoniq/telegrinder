import asyncio
import typing

import aiohttp

from telegrinder.api.abc import ABCAPI
from telegrinder.api.error import InvalidTokenError
from telegrinder.bot.polling.abc import ABCPolling
from telegrinder.model import Raw, decoder
from telegrinder.modules import logger
from telegrinder.result import Error, Ok
from telegrinder.types import Update, UpdateType


class Polling(ABCPolling):
    def __init__(
        self,
        api: ABCAPI,
        *,
        offset: int = 0,
        reconnection_timeout: float = 5,
        max_reconnetions: int = 10,
        include_updates: set[str | UpdateType] | None = None,
        exclude_updates: set[str | UpdateType] | None = None,
    ):
        self.api = api
        self.allowed_updates = self.get_allowed_updates(
            include_updates=include_updates,
            exclude_updates=exclude_updates,
        )
        self.reconnection_timeout = 5 if reconnection_timeout < 0 else reconnection_timeout
        self.max_reconnetions = 10 if max_reconnetions < 0 else max_reconnetions
        self.offset = offset
        self._stop = False

    def get_allowed_updates(
        self,
        *,
        include_updates: set[str | UpdateType] | None = None,
        exclude_updates: set[str | UpdateType] | None = None,
    ) -> list[str]:
        allowed_updates: list[str] = list(x.value for x in UpdateType)
        if not include_updates and not exclude_updates:
            return allowed_updates

        if include_updates and exclude_updates:
            allowed_updates = [
                x
                for x in allowed_updates
                if x in include_updates and x not in exclude_updates
            ]
        elif exclude_updates:
            allowed_updates = [x for x in allowed_updates if x not in exclude_updates]
        elif include_updates:
            allowed_updates = [x for x in allowed_updates if x in include_updates]

        return [x.value if isinstance(x, UpdateType) else x for x in allowed_updates]

    async def get_updates(self) -> Raw | None:
        raw_updates = await self.api.request_raw(
            "getUpdates",
            {"offset": self.offset, "allowed_updates": self.allowed_updates},
        )
        match raw_updates:
            case Ok(value):
                return value
            case Error(err) if err.code in (401, 404):
                raise InvalidTokenError("Token seems to be invalid")

    async def listen(self) -> typing.AsyncGenerator[list[Update], None]:
        logger.debug("Listening polling")
        reconn_counter = 0
        while not self._stop:
            try:
                updates = await self.get_updates()
                if reconn_counter > 0:
                    reconn_counter = 0
                if not updates:
                    continue
                updates_list: list[Update] = decoder.decode(
                    updates, type=list[Update]
                )
                if updates_list:
                    yield updates_list
                    self.offset = updates_list[-1].update_id + 1
            except InvalidTokenError as e:
                logger.error(e)
                exit(6)
            except asyncio.CancelledError:
                self.stop()
                logger.info("Caught cancel, polling stopping...")
            except (aiohttp.client.ServerConnectionError, TimeoutError):
                if reconn_counter > self.max_reconnetions:
                    logger.error(
                        "Failed to reconnect to the server after {} attempts, polling stopping.",
                        self.max_reconnetions,
                    )
                    self.stop()
                else:
                    logger.warning("Server disconnected, waiting 5 seconds to reconnetion...")
                    reconn_counter += 1
                    await asyncio.sleep(self.reconnection_timeout)
            except aiohttp.ClientConnectorError:
                logger.error(
                    "Client connection failed, polling stopping! "
                    "Please, check your internet connection."
                )
                self.stop()
            except BaseException as e:
                logger.exception(e)

    def stop(self) -> None:
        self._stop = True
