import traceback

from .abc import ABCPolling
from telegrinder.api.abc import ABCAPI
import typing
from telegrinder.modules import logger

ALLOWED_UPDATES = ["update_id", "message", "edited_message",
                   "channel_post", "edited_channel_post", "inline_query",
                   "chosen_inline_result", "callback_query", "shipping_query",
                   "pre_checkout_query", "poll", "poll_answer",
                   "my_chat_member", "chat_member"]


class Polling(ABCPolling):
    def __init__(
        self,
        api: typing.Optional[ABCAPI] = None,
        offset: typing.Optional[int] = None,
    ):
        self.api = api
        self.offset = offset or 0
        self.stop = False
        self.allowed_updates = ALLOWED_UPDATES

    async def get_updates(self) -> typing.Optional[typing.List[dict]]:
        raw_updates = await self.api.request(
            "getUpdates", {"offset": self.offset, "allowed_updates": self.allowed_updates}
        )
        return raw_updates.unwrap()

    async def listen(self) -> typing.AsyncIterator[dict]:
        while not self.stop:
            try:
                updates = await self.get_updates()
                for update in updates:
                    self.offset = updates[0]["update_id"] + 1
                    logger.info(f"Received update: {update}")
                    yield update
            except BaseException as e:
                traceback.print_exc()
                logger.error(e)
