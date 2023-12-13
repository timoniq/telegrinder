import datetime
import typing

from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.bot.dispatch.handler.func import FuncHandler
from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware
from telegrinder.bot.dispatch.view.abc import ABCStateView

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

    async def pre(self, event: EventType, ctx: dict) -> bool:
        if not self.view or not hasattr(self.view, "get_state_key"):
            raise RuntimeError(
                "WaiterMiddleware cannot be used inside a view which doesn't "
                "provide get_state_key (ABCStateView Protocol)."
            )

        view_name = self.view.__class__.__name__
        if view_name not in self.machine.storage:
            return True

        key = self.view.get_state_key(event)
        short_state: typing.Optional["ShortState"] = self.machine.storage[
            view_name
        ].get(key)  # type: ignore
        if not short_state:
            return True

        if (
            short_state.expiration is not None
            and datetime.datetime.now() >= short_state.expiration
        ):
            await self.machine.drop(self.view, short_state.key)  # type: ignore
            return True

        handler: FuncHandler = FuncHandler(
            self.pass_runtime, list(short_state.rules), dataclass=None
        )
        handler.ctx["short_state"] = short_state
        result = await handler.check(event.ctx_api, event, ctx)  # type: ignore
        if result is True:
            await handler.run(event)

        elif short_state.default_behaviour is not None:
            await self.machine.call_behaviour(
                self.view,
                short_state.default_behaviour,
                event,
                **handler.ctx,
            )

        return False

    async def pass_runtime(self, event, short_state: "ShortState", ctx: dict) -> None:
        setattr(short_state.event, "context", (event, ctx))
        short_state.event.set()
