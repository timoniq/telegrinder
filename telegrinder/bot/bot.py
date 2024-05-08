import typing_extensions as typing

from telegrinder.api import API
from telegrinder.bot.dispatch import ABCDispatch, Dispatch
from telegrinder.bot.polling import ABCPolling, Polling
from telegrinder.modules import logger
from telegrinder.tools.loop_wrapper import ABCLoopWrapper, LoopWrapper

DispatchT = typing.TypeVar("DispatchT", bound=ABCDispatch, default=Dispatch)
PollingT = typing.TypeVar("PollingT", bound=ABCPolling, default=Polling)
LoopWrapperT = typing.TypeVar("LoopWrapperT", bound=ABCLoopWrapper, default=LoopWrapper)


class Telegrinder(typing.Generic[DispatchT, PollingT, LoopWrapperT]):
    def __init__(
        self,
        api: API,
        *,
        polling: PollingT | None = None,
        dispatch: DispatchT | None = None,
        loop_wrapper: LoopWrapperT | None = None,
    ) -> None:
        self.api = api
        self.dispatch = typing.cast(DispatchT, dispatch or Dispatch())
        self.polling = typing.cast(PollingT, polling or Polling(api))
        self.loop_wrapper = typing.cast(LoopWrapperT, loop_wrapper or LoopWrapper())

    def __repr__(self) -> str:
        return "<{}: api={!r}, dispatch={!r}, polling={!r}, loop_wrapper={!r}>".format(
            self.__class__.__name__,
            self.api,
            self.dispatch,
            self.polling,
            self.loop_wrapper,
        )

    @property
    def on(self) -> DispatchT:
        return self.dispatch

    async def reset_webhook(self) -> None:
        if not (await self.api.get_webhook_info()).unwrap().url:
            return
        await self.api.delete_webhook()

    async def run_polling(self, *, offset: int = 0, skip_updates: bool = False) -> None:
        if skip_updates:
            logger.debug("Dropping pending updates")
            await self.reset_webhook()
            await self.api.delete_webhook(drop_pending_updates=True)
        self.polling.offset = offset

        async for updates in self.polling.listen():
            for update in updates:
                logger.debug("Received update (update_id={})", update.update_id)
                self.loop_wrapper.add_task(self.dispatch.feed(update, self.api))

    def run_forever(self, *, offset: int = 0, skip_updates: bool = False) -> None:
        logger.debug("Running blocking polling (id={})", self.api.id)
        self.loop_wrapper.add_task(self.run_polling(offset=offset, skip_updates=skip_updates))
        self.loop_wrapper.run_event_loop()


__all__ = ("Telegrinder",)
