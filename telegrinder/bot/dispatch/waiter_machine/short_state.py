
import asyncio
import dataclasses
import datetime
import typing
from functools import partial

from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.tools.aio import cancel_future
from telegrinder.tools.global_context.builtin_context import TelegrinderContext

if typing.TYPE_CHECKING:
    from telegrinder.bot.cute_types.base import BaseCute
    from telegrinder.bot.dispatch.view.base import View
    from telegrinder.bot.dispatch.waiter_machine.actions import WaiterActions
    from telegrinder.bot.dispatch.waiter_machine.hasher import Hasher
    from telegrinder.bot.dispatch.waiter_machine.machine import HasherWithData

TELEGRINDER_CONTEXT: typing.Final = TelegrinderContext()


def _wrap_async_fn[**P](
    fn: typing.Callable[P, typing.Any],
    /,
) -> typing.Callable[P, None]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> None:
        TELEGRINDER_CONTEXT.loop_wrapper.add_task(fn(*args, **kwargs))

    return wrapper


class ShortStateContext[Event: BaseCute[typing.Any] = typing.Any](typing.NamedTuple):
    event: Event
    context: Context


@dataclasses.dataclass
class ShortState[Event: BaseCute[typing.Any] = typing.Any]:
    event: asyncio.Event
    actions: WaiterActions[Event]

    release: ABCRule | None = dataclasses.field(
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

    expiration_date: datetime.datetime | None = dataclasses.field(init=False, kw_only=True)
    creation_date: datetime.datetime = dataclasses.field(init=False)
    context: ShortStateContext[Event] | None = dataclasses.field(default=None, init=False, kw_only=True)
    drop_timer: asyncio.TimerHandle | None = dataclasses.field(default=None, init=False)

    def __post_init__(self, expiration: datetime.timedelta) -> None:
        self.lifetime = expiration
        self.creation_date = datetime.datetime.now()
        self.expiration_date = (self.creation_date + expiration) if expiration is not None else None

    def schedule_drop[HasherData](
        self,
        dropper: typing.Callable[..., typing.Any],
        /,
        hasher: Hasher[Event, HasherData],
        data: HasherData,
        **context: typing.Any,
    ) -> None:
        self.drop_timer = asyncio.get_running_loop().call_later(
            delay=self.lifetime.total_seconds(),
            callback=partial(_wrap_async_fn(dropper), self, hasher, data, expired=True, **context),
        )

    def schedule_drop_many[ViewType: View, HasherData](
        self,
        dropper: typing.Callable[..., typing.Any],
        /,
        *hashers: HasherWithData[Event, ViewType, HasherData],
        **context: typing.Any,
    ) -> None:
        self.drop_timer = asyncio.get_running_loop().call_later(
            delay=self.lifetime.total_seconds(),
            callback=partial(_wrap_async_fn(dropper), self, *hashers, expired=True, **context),
        )

    def cancel_drop(self) -> None:
        if self.drop_timer is not None:
            self.drop_timer.cancel()
            self.drop_timer = None

    async def cancel(self) -> None:
        waiters = typing.cast(
            "typing.Iterable[asyncio.Future[typing.Any]]",
            self.event._waiters,  # type: ignore
        )

        for future in waiters:
            if not future.cancelled():
                await cancel_future(future)


__all__ = ("ShortState", "ShortStateContext")
