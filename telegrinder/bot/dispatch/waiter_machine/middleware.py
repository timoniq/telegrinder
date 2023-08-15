import typing
import types
import datetime

from telegrinder.bot.dispatch.handler.func import FuncHandler
from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware
from telegrinder.bot.dispatch.view.abc import ABCStateView

if typing.TYPE_CHECKING:
    from .machine import WaiterMachine, Behaviour
    from .short_state import ShortState


EventType = typing.TypeVar("EventType")


class WaiterMiddleware(ABCMiddleware[EventType]):
    def __init__(
        self,
        machine: "WaiterMachine",
        view: ABCStateView[EventType],
    ) -> None:
        self.machine = machine
        self.view = view

    async def pre(self, event: EventType, ctx: dict) -> None:
        if not self.view or not hasattr(self.view, "get_state_key"):
            msg = "WaiterMiddleware cannot be used inside a view which doesn't provide get_state_key (ABCDispenseView Protocol)"
            raise RuntimeError(msg)

        view_name = self.view.__class__.__name__
        if view_name not in self.machine.storage:
            return

        key = self.view.get_state_key(event)
        short_state: typing.Optional["ShortState"] = self.machine.storage[
            view_name
        ].get(key)
        if not short_state:
            return

        if (
            short_state.expiration is not None
            and datetime.datetime.now() >= short_state.expiration
        ):
            await self.machine.drop(self.view, short_state.key)  # type: ignore
            return

        handler: FuncHandler = FuncHandler(
            self.pass_runtime, short_state.rules, dataclass=None
        )
        handler.ctx["short_state"] = short_state

        result = await handler.check(event.ctx_api, event, ctx)

        if result is True:
            await handler.run(event)

        elif short_state.default_behaviour is not None:
            await self.machine.call_behaviour(
                self.view,  # type: ignore
                short_state.default_behaviour,
                event,
                **handler.ctx,
            )

        return False

    async def pass_runtime(self, event, short_state: "ShortState", ctx: dict) -> None:
        setattr(short_state.event, "context", (event, ctx))  # ruff: noqa
        short_state.event.set()
