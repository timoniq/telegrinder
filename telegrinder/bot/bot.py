import asyncio

from telegrinder.api import ABCAPI
from telegrinder.bot.polling import ABCPolling, Polling
from telegrinder.bot.dispatch import ABCDispatch, Dispatch
import typing


class Telegrinder:
    def __init__(
        self,
        api: ABCAPI,
        polling: typing.Optional[ABCPolling] = None,
        dispatch: typing.Optional[ABCDispatch] = None,
    ):
        self.api = api
        self.polling = polling or Polling(api)
        self.dispatch = dispatch or Dispatch()

    @property
    def on(self) -> Dispatch:
        return self.dispatch  # type: ignore

    async def run_polling(self, offset: int = 0) -> None:
        self.polling.offset = offset
        async for update in self.polling.listen():
            self.dispatch.loop.create_task(self.dispatch.feed(update, self.api))

    def run_forever(self, offset: int = 0) -> None:
        loop = asyncio.get_event_loop()
        loop.create_task(self.run_polling(offset))
        loop.run_forever()
