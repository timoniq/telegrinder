import datetime
import typing

from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.bot.cute_types.update import UpdateCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.handler.func import FuncHandler
from telegrinder.bot.dispatch.middleware.abc import ABCGlobalMiddleware, ABCMiddleware
from telegrinder.bot.dispatch.process import check_rule
from telegrinder.bot.dispatch.view.base import ABCView
from telegrinder.bot.dispatch.waiter_machine.short_state import ShortStateContext
from telegrinder.model import get_event_key
from telegrinder.modules import logger
from telegrinder.tools.adapter.raw_update import RawUpdateAdapter

from .hasher import Hasher

if typing.TYPE_CHECKING:
    from .machine import WaiterMachine
    from .short_state import ShortState


class WaiterIsolationMiddleware(ABCGlobalMiddleware[UpdateCute]):
    adapter = RawUpdateAdapter()

    def __init__(self, machine: "WaiterMachine") -> None:
        assert machine.dispatch is not None, "WaiterMachine must have a Dispatch."

        self.machine = machine
        self.isolated_hashers: dict[typing.Hashable, Hasher] = {}
        self.views = machine.dispatch.get_views()

    def add_isolated_hasher(self, key: typing.Hashable, hasher: Hasher) -> None:
        self.isolated_hashers[key] = hasher

    def remove_isolated_hasher(self, key: typing.Hashable) -> None:
        self.isolated_hashers.pop(key, None)

    async def get_view(self, event: UpdateCute) -> ABCView | None:
        for view in self.views.values():
            if await view.check(event):
                return view

        return None

    async def pre(self, event: UpdateCute, ctx: Context) -> bool:
        key = get_event_key(event.incoming_update)
        if key not in self.isolated_hashers:
            return True
        return isinstance(await self.get_view(event), self.isolated_hashers[key].view_class)


class WaiterMiddleware[Event: BaseCute](ABCMiddleware[Event]):
    def __init__(
        self,
        machine: "WaiterMachine",
        hasher: Hasher,
    ) -> None:
        self.machine = machine
        self.hasher = hasher

    async def pre(self, event: Event, ctx: Context) -> bool:
        if self.hasher not in self.machine.storage:
            return True

        key = self.hasher.get_hash_from_data_from_event(event)
        if not key:
            logger.info(f"Unable to get hash from event with hasher {self.hasher!r}")
            return True

        short_state: "ShortState[Event] | None" = self.machine.storage[self.hasher].get(key.unwrap())
        if not short_state:
            return True

        preset_context = Context(short_state=short_state)
        if short_state.context is not None:
            preset_context.update(short_state.context.context)

        # Run filter rule
        if short_state.filter and not await check_rule(
            event.ctx_api,
            short_state.filter,
            ctx.raw_update,
            preset_context,
        ):
            logger.debug("Filter rule {!r} failed", short_state.filter)
            return True

        if short_state.expiration_date is not None and datetime.datetime.now() >= short_state.expiration_date:
            await self.machine.drop(
                self.hasher,
                self.hasher.get_data_from_event(event).unwrap(),
                **preset_context.copy(),
            )
            return True

        handler = FuncHandler(
            self.pass_runtime,
            [short_state.release] if short_state.release else [],
            dataclass=BaseCute,
            preset_context=preset_context,
        )
        result = await handler.check(event.ctx_api, ctx.raw_update, ctx)

        if result is True:
            await handler.run(event.api, event, ctx)

        elif on_miss := short_state.actions.get("on_miss"):  # noqa: SIM102
            if await on_miss.check(event.ctx_api, ctx.raw_update, ctx):
                await on_miss.run(event.ctx_api, event, ctx)

        return False

    async def pass_runtime(
        self,
        event: BaseCute[Event],
        short_state: "ShortState[Event]",
        ctx: Context,
    ) -> None:
        short_state.context = ShortStateContext(typing.cast(Event, event), ctx)
        short_state.event.set()


__all__ = ("WaiterMiddleware", "WaiterIsolationMiddleware")
