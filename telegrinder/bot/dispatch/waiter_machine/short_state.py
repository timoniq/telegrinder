import asyncio
import dataclasses
import datetime
import typing
from contextlib import suppress

from telegrinder.bot.cute_types import BaseCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.rules.abc import ABCRule

if typing.TYPE_CHECKING:
    from .actions import WaiterActions


class ShortStateContext[Event: BaseCute](typing.NamedTuple):
    event: Event
    context: Context


@dataclasses.dataclass(slots=True)
class ShortState[Event: BaseCute]:
    event: asyncio.Event
    actions: "WaiterActions[Event]"

    release: ABCRule | None = dataclasses.field(
        default=None,
        kw_only=True,
    )
    filter: ABCRule | None = dataclasses.field(
        default=None,
        kw_only=True,
    )

    lifetime: dataclasses.InitVar[datetime.timedelta | None] = dataclasses.field(
        default=None,
        kw_only=True,
    )

    expiration_date: datetime.datetime | None = dataclasses.field(init=False, kw_only=True)
    creation_date: datetime.datetime = dataclasses.field(init=False)
    context: ShortStateContext[Event] | None = dataclasses.field(default=None, init=False, kw_only=True)

    def __post_init__(self, expiration: datetime.timedelta | None = None) -> None:
        self.creation_date = datetime.datetime.now()
        self.expiration_date = (self.creation_date + expiration) if expiration is not None else None

    async def cancel(self) -> None:
        """Cancel schedule waiters."""

        waiters = typing.cast(
            typing.Iterable[asyncio.Future[typing.Any]],
            self.event._waiters,  # type: ignore
        )
        for future in waiters:
            future.cancel()
            with suppress(asyncio.CancelledError):
                await future


__all__ = ("ShortState", "ShortStateContext")
