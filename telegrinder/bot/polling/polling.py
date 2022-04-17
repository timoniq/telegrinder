from .abc import ABCPolling
from telegrinder.api.abc import ABCAPI
import typing
from telegrinder.modules import logger


class Polling(ABCPolling):
    def __init__(
        self,
        api: typing.Optional[ABCAPI] = None,
        offset: typing.Optional[int] = None,
    ):
        self.api = api
        self.offset = offset or 0
        self.stop = False

    async def get_updates(self) -> typing.Optional[typing.List[dict]]:
        raw_updates = await self.api.request("getUpdates", {"offset": self.offset})
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
                logger.error(e)
