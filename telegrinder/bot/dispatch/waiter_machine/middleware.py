import datetime
import typing

from telegrinder.api.api import API
from telegrinder.bot.cute_types.update import UpdateCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.handler.func import FuncHandler
from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware
from telegrinder.bot.dispatch.process import check_rule
from telegrinder.bot.dispatch.waiter_machine.short_state import ShortStateContext
from telegrinder.modules import logger
from telegrinder.types.objects import Update

from .hasher import Hasher

if typing.TYPE_CHECKING:
    from .machine import WaiterMachine
    from .short_state import ShortState

type State = ShortState[typing.Any]


class WaiterMiddleware(ABCMiddleware):
    def __init__(
        self,
        machine: "WaiterMachine",
        hasher: Hasher[typing.Any, typing.Any],
    ) -> None:
        self.machine = machine
        self.hasher = hasher

    async def pre(self, update: UpdateCute, raw_update: Update, api: API, ctx: Context) -> bool:
        if self.hasher not in self.machine.storage:
            return True

        event = update.incoming_update
        key = self.hasher.get_hash_from_data_from_event(event)
        if not key:
            logger.info(f"Unable to get hash from event with hasher {self.hasher!r}")
            return True

        short_state: "ShortState | None" = self.machine.storage[self.hasher].get(key.unwrap())
        if not short_state:
            return True

        preset_context = Context(short_state=short_state)
        if short_state.context is not None:
            preset_context.update(short_state.context.context)

        # Run filter rule
        if short_state.filter and not await check_rule(
            api,
            short_state.filter,
            raw_update,
            preset_context,
        ):
            logger.debug("Filter rule {!r} failed!", short_state.filter)
            return True

        if short_state.expiration_date is not None and datetime.datetime.now() >= short_state.expiration_date:
            await self.machine.drop(
                self.hasher,
                self.hasher.get_data_from_event(event).unwrap(),
                **preset_context.copy(),
            )
            return True

        result = await FuncHandler(
            self.pass_runtime,
            [short_state.release] if short_state.release else [],
            preset_context=preset_context,
        ).run(api, raw_update, ctx)

        if not result and (on_miss := short_state.actions.get("on_miss")):
            await on_miss.run(api, raw_update, ctx)

        return False

    async def pass_runtime(
        self,
        event: UpdateCute,
        ctx: Context,
        short_state: State,
    ) -> None:
        ctx.initiator = self.hasher
        short_state.context = ShortStateContext(event.incoming_update, ctx)  # type: ignore
        short_state.event.set()


__all__ = ("WaiterMiddleware",)
