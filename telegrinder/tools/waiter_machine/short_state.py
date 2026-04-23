import asyncio
import dataclasses
import datetime
import typing

from telegrinder.modules import flush_log_buffer
from telegrinder.tools.aio import cancel_future

if typing.TYPE_CHECKING:
    from telegrinder.bot.cute_types.base import BaseCute
    from telegrinder.bot.dispatch.context import Context
    from telegrinder.bot.dispatch.view.base import View
    from telegrinder.bot.rules.abc import ABCRule
    from telegrinder.tools.waiter_machine.actions import WaiterActions
    from telegrinder.tools.waiter_machine.machine import HasherWithData, HasherWithViewAndData


class ShortStateContext[Event: BaseCute[typing.Any] = typing.Any](typing.NamedTuple):
    event: Event
    context: Context


@dataclasses.dataclass
class ShortState[Event: BaseCute[typing.Any] = typing.Any]:
    actions: WaiterActions[Event]
    release_rule: ABCRule | None = dataclasses.field(
        default=None,
        kw_only=True,
    )
    filter: ABCRule | None = dataclasses.field(
        default=None,
        kw_only=True,
    )
    expiration: dataclasses.InitVar[datetime.timedelta] = dataclasses.field(
        kw_only=True,
    )
    expiration_date: datetime.datetime = dataclasses.field(init=False)
    creation_date: datetime.datetime = dataclasses.field(init=False)
    event: asyncio.Event = dataclasses.field(default_factory=asyncio.Event, init=False)
    context: ShortStateContext[Event] | None = dataclasses.field(default=None, init=False)
    drop_timer: asyncio.TimerHandle | None = dataclasses.field(default=None, init=False)

    def __post_init__(self, expiration: datetime.timedelta) -> None:
        self.lifetime = expiration
        self.creation_date = datetime.datetime.now()
        self.expiration_date = self.creation_date + expiration

    def _cancel_drop_timer(self) -> None:
        if self.drop_timer is not None and not self.drop_timer.cancelled():
            self.drop_timer.cancel()
            self.drop_timer = None

    def release(
        self,
        *,
        event: Event | None = None,
        context: Context | None = None,
    ) -> None:
        if event is not None and context is not None:
            self.context = ShortStateContext(event, context)

        if self.drop_timer is not None and not self.drop_timer.cancelled():
            self.drop_timer.cancel()
            self.drop_timer = None

        if not self.event.is_set():
            self.event.set()

    async def acquire[ViewType: View, HasherData](
        self,
        dropper: typing.Callable[..., typing.Coroutine[typing.Any, typing.Any, typing.Any]],
        /,
        *hashers: HasherWithData[Event, HasherData] | HasherWithViewAndData[Event, ViewType, HasherData],
        **context: typing.Any,
    ) -> None:
        self.event.clear()

        loop = asyncio.get_running_loop()
        self.drop_timer = loop.call_later(
            delay=self.lifetime.total_seconds(),
            callback=lambda: loop.create_task(dropper(self, *hashers, expired=True, **context)),
        )

        flush_log_buffer()

        try:
            await self.event.wait()
        finally:
            self.release()

    async def cancel(self) -> None:
        self._cancel_drop_timer()

        for future in self.event._waiters:  # type: ignore
            await cancel_future(future)


__all__ = ("ShortState", "ShortStateContext")
