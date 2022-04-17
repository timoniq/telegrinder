import asyncio

from telegrinder.api import ABCAPI
from telegrinder.bot.polling import ABCPolling, Polling
from telegrinder.bot.dispatch import ABCDispatch, Dispatch
from telegrinder.bot.rules import ABCRule, IsMessage
import typing


class Telegrinder:
    def __init__(
        self,
        api: ABCAPI,
        polling: typing.Optional[ABCPolling] = None,
        dispatch: typing.Optional[ABCDispatch] = None
    ):
        self.api = api
        self.polling = polling or Polling(api)
        self.dispatch = dispatch or Dispatch()

    def on_message(self, *rules: ABCRule, is_blocking: bool = True):
        return self.dispatch.handle(IsMessage(), *rules, is_blocking=is_blocking)

    async def run_polling(self, offset: int = 0) -> None:
        self.polling.offset = offset
        async for update in self.polling.listen():
            await self.dispatch.feed(update)

    def run_forever(self, offset: int = 0) -> None:
        loop = asyncio.get_event_loop()
        loop.create_task(self.run_polling(offset))
        loop.run_forever()
