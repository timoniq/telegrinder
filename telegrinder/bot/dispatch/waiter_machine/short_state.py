import asyncio
import dataclasses
import datetime
import typing

from telegrinder.bot.cute_types import BaseCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.handler.abc import ABCHandler
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.model import Model

if typing.TYPE_CHECKING:
    from .actions import WaiterActions


T = typing.TypeVar("T", bound=Model)
EventModel = typing.TypeVar("EventModel", bound=BaseCute)

Behaviour: typing.TypeAlias = ABCHandler[T] | None


class ShortStateContext(typing.Generic[EventModel], typing.NamedTuple):
    event: EventModel
    context: Context


@dataclasses.dataclass(slots=True)
class ShortState(typing.Generic[EventModel]):
    event: asyncio.Event
    actions: "WaiterActions[EventModel]"

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
    context: ShortStateContext[EventModel] | None = dataclasses.field(default=None, init=False, kw_only=True)

    def __post_init__(self, expiration: datetime.timedelta | None = None) -> None:
        self.creation_date = datetime.datetime.now()
        self.expiration_date = (self.creation_date + expiration) if expiration is not None else None

    def cancel(self) -> None:
        """Cancel schedule waiters."""

        waiters = typing.cast(
            typing.Iterable[asyncio.Future[typing.Any]],
            self.event._waiters,  # type: ignore
        )
        for future in waiters:
            future.cancel()


__all__ = ("ShortState", "ShortStateContext")
