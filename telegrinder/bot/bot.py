import typing_extensions as typing

from telegrinder.api.api import API, HTTPClient
from telegrinder.bot.dispatch import dispatch as dp
from telegrinder.bot.dispatch.abc import ABCDispatch
from telegrinder.bot.polling import polling as pg
from telegrinder.bot.polling.abc import ABCPolling
from telegrinder.modules import logger
from telegrinder.tools.global_context.builtin_context import TelegrinderContext
from telegrinder.tools.loop_wrapper import LoopWrapper

Dispatch = typing.TypeVar("Dispatch", bound=ABCDispatch, default=dp.Dispatch[HTTPClient])
Polling = typing.TypeVar("Polling", bound=ABCPolling, default=pg.Polling[HTTPClient])

CONTEXT: typing.Final[TelegrinderContext] = TelegrinderContext()


class Telegrinder(typing.Generic[HTTPClient, Dispatch, Polling]):
    def __init__(
        self,
        api: API[HTTPClient],
        *,
        dispatch: Dispatch | None = None,
        polling: Polling | None = None,
        loop_wrapper: LoopWrapper | None = None,
    ) -> None:
        self.api = api
        self.dispatch = typing.cast("Dispatch", dispatch or dp.Dispatch())
        self.polling = typing.cast("Polling", polling or pg.Polling(api))
        self.loop_wrapper = loop_wrapper or CONTEXT.loop_wrapper

    def __repr__(self) -> str:
        return "<{}: api={!r}, dispatch={!r}, polling={!r}, loop_wrapper={!r}>".format(
            self.__class__.__name__,
            self.api,
            self.dispatch,
            self.polling,
            self.loop_wrapper,
        )

    @property
    def on(self) -> Dispatch:
        return self.dispatch

    async def reset_webhook(self) -> None:
        if not (await self.api.get_webhook_info()).unwrap().url:
            return
        await self.api.delete_webhook()

    async def run_polling(
        self,
        *,
        offset: int = 0,
        skip_updates: bool = False,
    ) -> typing.NoReturn:
        async def polling() -> typing.NoReturn:
            if skip_updates:
                logger.debug("Dropping pending updates")
                await self.reset_webhook()
                await self.api.delete_webhook(drop_pending_updates=True)
            self.polling.offset = offset

            async for updates in self.polling.listen():
                for update in updates:
                    logger.debug(
                        "Received update (update_id={}, update_type={!r})",
                        update.update_id,
                        update.update_type.name,
                    )
                    self.loop_wrapper.add_task(self.dispatch.feed(update, self.api))

        if self.loop_wrapper.is_running:
            await polling()
        else:
            self.loop_wrapper.add_task(polling())
            self.loop_wrapper.run()

    def run_forever(self, *, offset: int = 0, skip_updates: bool = False) -> typing.NoReturn:
        logger.info("Running blocking polling (id={})", self.api.id)
        self.loop_wrapper.add_task(self.run_polling(offset=offset, skip_updates=skip_updates))
        self.loop_wrapper.run()


__all__ = ("Telegrinder",)
