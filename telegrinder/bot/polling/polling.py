import asyncio
import traceback
import typing

import aiohttp
import msgspec.json

from telegrinder.api.abc import ABCAPI
from telegrinder.api.error import InvalidTokenError
from telegrinder.model import Raw
from telegrinder.modules import logger
from telegrinder.result import Error, Ok
from telegrinder.types import Update

from .abc import ABCPolling

ALLOWED_UPDATES = [
    "update_id",
    "message",
    "edited_message",
    "channel_post",
    "edited_channel_post",
    "inline_query",
    "chosen_inline_result",
    "callback_query",
    "shipping_query",
    "pre_checkout_query",
    "poll",
    "poll_answer",
    "my_chat_member",
    "chat_member",
    "chat_join_request",
]


class Polling(ABCPolling):
    def __init__(self, api: ABCAPI, *, offset: int = 0):
        self.api = api
        self.allowed_updates = ALLOWED_UPDATES
        self.offset = offset
        self._stop = False

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

    async def listen(self) -> typing.AsyncIterator[list[Update]]:
        logger.debug("Listening polling")
        while not self._stop:
            try:
                updates = await self.get_updates()
                if not updates:
                    continue
                updates_list: list[Update] = msgspec.json.decode(
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
                logger.info("Caught cancel, stopping")
            except BaseException as e:
                print(e.__class__.__name__)
                traceback.print_exc()
                logger.error(e)

    def stop(self) -> None:
        self._stop = True
