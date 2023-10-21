import asyncio

from telegrinder.api import API
from telegrinder.bot.dispatch import ABCDispatch, Dispatch
from telegrinder.bot.polling import ABCPolling, Polling
from telegrinder.modules import logger


class Telegrinder:
    def __init__(
        self,
        api: API,
        polling: ABCPolling | None = None,
        dispatch: ABCDispatch | None = None,
        loop: asyncio.AbstractEventLoop | None = None,
    ):
        self.api = api
        self.polling = polling or Polling(api)
        self.dispatch = dispatch or Dispatch()
        self.loop = loop

    @property
    def on(self) -> Dispatch:
        return self.dispatch  # type: ignore

    async def reset_webhook(self) -> None:
        if not (await self.api.get_webhook_info()).unwrap().url:
            return
        await self.api.delete_webhook()

    async def run_polling(self, offset: int = 0, skip_updates: bool = False) -> None:
        if skip_updates:
            logger.debug("Dropping pending updates")
            await self.reset_webhook()
            await self.api.delete_webhook(drop_pending_updates=True)
        self.polling.offset = offset

        loop = asyncio.get_running_loop()
        async for updates in self.polling.listen():  # type: ignore
            for update in updates:
                logger.debug("Received update (update_id={})", update.update_id)
                loop.create_task(self.dispatch.feed(update, self.api))

    def run_forever(self, offset: int = 0, skip_updates: bool = False) -> None:
        logger.debug("Running blocking polling (id={})", self.api.id)
        loop = self.loop or asyncio.new_event_loop()
        polling_task = loop.create_task(
            self.run_polling(offset, skip_updates=skip_updates)
        )

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            logger.info("KeyboardInterrupt")
        except SystemExit as e:
            logger.info("System exit with code {}", e.code)
        finally:
            self.polling.stop()
            polling_task.cancel()
