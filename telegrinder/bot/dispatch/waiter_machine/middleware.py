import datetime
import typing

from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.handler.func import FuncHandler
from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware
from telegrinder.bot.dispatch.view.abc import ABCStateView
from telegrinder.bot.dispatch.waiter_machine.short_state import ShortStateContext

if typing.TYPE_CHECKING:
    from .machine import WaiterMachine
    from .short_state import ShortState

EventType = typing.TypeVar("EventType", bound=BaseCute)


class WaiterMiddleware(ABCMiddleware[EventType]):
    def __init__(
        self,
        machine: "WaiterMachine",
        view: ABCStateView[EventType],
    ) -> None:
        self.machine = machine
        self.view = view

    async def pre(self, event: EventType, ctx: Context) -> bool:
        if not self.view or not hasattr(self.view, "get_state_key"):
            raise RuntimeError(
                "WaiterMiddleware cannot be used inside a view which doesn't "
                "provide get_state_key (ABCStateView interface)."
            )

        view_name = self.view.__class__.__name__
        if view_name not in self.machine.storage:
            return True

        key = self.view.get_state_key(event)
        if key is None:
            raise RuntimeError("Unable to get state key.")

        short_state: "ShortState[EventType] | None" = self.machine.storage[view_name].get(key)
        if not short_state:
            return True
        
        preset_context = Context(short_state=short_state)
        if (
            short_state.expiration_date is not None
            and datetime.datetime.now() >= short_state.expiration_date
        ):
            await self.machine.drop(self.view, short_state.key, ctx.raw_update, **preset_context.copy())
            return True

        # before running the handler we check if the user wants to exit waiting
        if short_state.exit_behaviour is not None:
            await self.machine.call_behaviour(
                self.view,
                event,
                ctx.raw_update,
                behaviour=short_state.exit_behaviour,
                **preset_context,
            )
            await self.machine.drop(self.view, short_state.key, ctx.raw_update, **preset_context.copy())
            return True

        handler = FuncHandler(
            self.pass_runtime,
            list(short_state.rules),
            dataclass=None,
            preset_context=preset_context,
        )
        result = await handler.check(event.ctx_api, ctx.raw_update, ctx)

        if result is True:
            await handler.run(event, ctx)

        elif short_state.default_behaviour is not None:
            await self.machine.call_behaviour(
                self.view,
                event,
                ctx.raw_update,
                behaviour=short_state.default_behaviour,
                **handler.preset_context,
            )

        return False

    async def pass_runtime(
        self,
        event: EventType,
        short_state: "ShortState[EventType]",
        ctx: Context,
    ) -> None:
        short_state.context = ShortStateContext(event, ctx)
        short_state.event.set()


__all__ = ("WaiterMiddleware",)
