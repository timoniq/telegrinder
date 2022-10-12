import asyncio

from telegrinder.api import API
from telegrinder.bot.polling import ABCPolling, Polling
from telegrinder.bot.dispatch import ABCDispatch, Dispatch
from telegrinder.modules import logger
import typing


class Telegrinder:
    def __init__(
        self,
        api: API,
        polling: typing.Optional[ABCPolling] = None,
        dispatch: typing.Optional[ABCDispatch] = None,
    ):
        self.api = api
        self.polling = polling or Polling(api)
        self.dispatch = dispatch or Dispatch()

    @property
    def on(self) -> Dispatch:
        return self.dispatch  # type: ignore

    async def reset_webhook(self) -> None:
        if not (await self.api.get_webhook_info()).unwrap().url:
            return

        await self.api.delete_webhook()

    async def run_polling(self, offset: int = 0, skip_updates: bool = False) -> None:
        if skip_updates:
            logger.debug("dropping pending updates")
            await self.reset_webhook()
            await self.api.delete_webhook(drop_pending_updates=True)
        self.polling.offset = offset
        async for updates in self.polling.listen():
            for update in updates:
                logger.debug("received update (update_id=%d)", update.update_id)
                self.dispatch.loop.create_task(self.dispatch.feed(update, self.api))

    def run_forever(self, offset: int = 0, skip_updates: bool = False) -> None:
        logger.debug("running blocking polling (id=%d)", self.api.id)
        loop = asyncio.get_event_loop()
        loop.create_task(self.run_polling(offset, skip_updates=skip_updates))
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            logger.info("KeyboardInterrupt")
