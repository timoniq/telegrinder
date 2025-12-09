from __future__ import annotations

import typing

from telegrinder.api.api import API
from telegrinder.bot.dispatch import dispatch as dp
from telegrinder.bot.dispatch.abc import ABCDispatch
from telegrinder.bot.polling import polling as pg
from telegrinder.bot.polling.abc import ABCPolling
from telegrinder.modules import logger
from telegrinder.tools.global_context.builtin_context import TelegrinderContext
from telegrinder.tools.loop_wrapper import LoopWrapper

TELEGRINDER_CONTEXT: typing.Final[TelegrinderContext] = TelegrinderContext()


class Telegrinder[Dispatch: ABCDispatch = dp.Dispatch, Polling: ABCPolling = pg.Polling]:
    def __init__(
        self,
        api: API,
        *,
        dispatch: Dispatch | None = None,
        polling: Polling | None = None,
        loop_wrapper: LoopWrapper | None = None,
    ) -> None:
        self.api = api
        self.dispatch = typing.cast("Dispatch", dispatch or dp.Dispatch())
        self.polling = typing.cast("Polling", polling or pg.Polling(api))
        self.loop_wrapper = loop_wrapper or TELEGRINDER_CONTEXT.loop_wrapper

    def __repr__(self) -> str:
        return "<{}: api={!r}, dispatch={!r}, polling={!r}, loop_wrapper={!r}>".format(
            type(self).__name__,
            self.api,
            self.dispatch,
            self.polling,
            self.loop_wrapper,
        )

    @property
    def on(self) -> Dispatch:
        return self.dispatch

    async def drop_pending_updates(self) -> None:
        await logger.adebug("Dropping pending updates")
        await self.api.delete_webhook(drop_pending_updates=True)

    async def run_polling(
        self,
        *,
        offset: int = 0,
        skip_updates: bool = False,
    ) -> None:
        self.polling.offset = offset

        async def listen_polling() -> None:
            if skip_updates:
                await self.drop_pending_updates()

            async for updates in self.polling.listen():
                for update in updates:
                    self.loop_wrapper.add_task(self.dispatch.feed(self.api, update))

        self.loop_wrapper.add_task(listen_polling())

    def run_forever(self, *, offset: int = 0, skip_updates: bool = False) -> typing.NoReturn:
        logger.info("Running blocking polling (id={})", self.api.id)
        self.loop_wrapper.add_task(self.run_polling(offset=offset, skip_updates=skip_updates))
        self.loop_wrapper.run()


__all__ = ("Telegrinder",)
