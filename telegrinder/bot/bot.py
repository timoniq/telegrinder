import asyncio

import typing_extensions as typing

from telegrinder.api import API
from telegrinder.bot.dispatch import ABCDispatch, Dispatch
from telegrinder.bot.polling import ABCPolling, Polling
from telegrinder.modules import logger

DispatchT = typing.TypeVar("DispatchT", bound=ABCDispatch, default=Dispatch)
PollingT = typing.TypeVar("PollingT", bound=ABCPolling, default=Polling)


class Telegrinder(typing.Generic[DispatchT, PollingT]):
    dispatch: DispatchT
    polling: PollingT

    def __init__(
        self,
        api: API,
        polling: PollingT | None = None,
        dispatch: DispatchT | None = None,
        loop: asyncio.AbstractEventLoop | None = None,
    ):
        self.api = api
        self.dispatch = dispatch or Dispatch()  # type: ignore
        self.polling = polling or Polling(api)  # type: ignore
        self.loop = loop or asyncio.new_event_loop()
    
    @property
    def on(self) -> DispatchT:
        return self.dispatch

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

        async for updates in self.polling.listen():
            for update in updates:
                logger.debug("Received update (update_id={})", update.update_id)
                self.loop.create_task(self.dispatch.feed(update, self.api))

    def run_forever(self, offset: int = 0, skip_updates: bool = False) -> None:
        logger.debug("Running blocking polling (id={})", self.api.id)
        polling_task = self.loop.create_task(
            self.run_polling(offset, skip_updates=skip_updates)
        )

        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            logger.info("KeyboardInterrupt")
        except SystemExit as e:
            logger.info("System exit with code {}", e.code)
        finally:
            self.polling.stop()
            polling_task.cancel()
