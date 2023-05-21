import traceback
import asyncio

import msgspec.json

from .abc import ABCPolling
from telegrinder.api.abc import ABCAPI
from telegrinder.api.error import InvalidTokenError
import typing
from telegrinder.modules import logger
from telegrinder.model import Raw
from telegrinder.types import Update
from telegrinder.result import Ok, Error

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
    def __init__(
        self,
        api: ABCAPI | None = None,
        offset: int | None = None,
    ):
        self.api = api
        self.offset = offset or 0
        self._stop = False
        self.allowed_updates = ALLOWED_UPDATES

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
                traceback.print_exc()
                logger.error(e)

    def stop(self) -> None:
        self._stop = True
