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

if typing.TYPE_CHECKING:
    from telegrinder.node.composer import Composer

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

    @property
    def composer(self) -> Composer:
        return TELEGRINDER_CONTEXT.composer.unwrap()

    async def reset_webhook(self) -> None:
        if not (await self.api.get_webhook_info()).unwrap().url:
            return
        await self.api.delete_webhook()

    async def run_polling(
        self,
        *,
        offset: int = 0,
        skip_updates: bool = False,
    ) -> typing.NoReturn:  # type: ignore[ReturnType]
        async def polling() -> None:
            if skip_updates:
                logger.debug("Dropping pending updates")
                await self.reset_webhook()
                await self.api.delete_webhook(drop_pending_updates=True)

            async for updates in self.polling.listen():
                for update in updates:
                    await self.loop_wrapper.create_task(self.dispatch.feed(update, self.api))

        self.polling.offset = offset

        if self.loop_wrapper.running:
            await polling()
        else:
            self.loop_wrapper.add_task(polling())
            self.loop_wrapper.run()

    def run_forever(self, *, offset: int = 0, skip_updates: bool = False) -> typing.NoReturn:
        logger.info("Running blocking polling (id={})", self.api.id)
        self.loop_wrapper.add_task(self.run_polling(offset=offset, skip_updates=skip_updates))
        self.loop_wrapper.run()


__all__ = ("Telegrinder",)
