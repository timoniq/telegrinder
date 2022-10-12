import traceback

import msgspec.json

from .abc import ABCPolling
from telegrinder.api.abc import ABCAPI
import typing
from telegrinder.modules import logger
from telegrinder.model import Raw
from telegrinder.types import Update

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
]


class Polling(ABCPolling):
    def __init__(
        self,
        api: typing.Optional[ABCAPI] = None,
        offset: typing.Optional[int] = None,
    ):
        self.api = api
        self.offset = offset or 0
        self._stop = False
        self.allowed_updates = ALLOWED_UPDATES

    async def get_updates(self) -> typing.Optional[Raw]:
        raw_updates = await self.api.request_raw(
            "getUpdates",
            {"offset": self.offset, "allowed_updates": self.allowed_updates},
        )
        if not raw_updates.is_ok and raw_updates.error.code == 404:
            logger.fatal("Token seems to be invalid")
            exit(6)
        return raw_updates.unwrap()

    async def listen(self) -> typing.AsyncIterator[typing.List[Update]]:
        logger.debug("listening polling")
        while not self._stop:
            try:
                updates = await self.get_updates()
                updates_list: typing.List[Update] = msgspec.json.decode(
                    updates, type=typing.List[Update]
                )
                if updates_list:
                    yield updates_list
                    self.offset = updates_list[-1].update_id + 1
            except BaseException as e:
                traceback.print_exc()
                logger.error(e)

    def stop(self) -> None:
        self._stop = True
