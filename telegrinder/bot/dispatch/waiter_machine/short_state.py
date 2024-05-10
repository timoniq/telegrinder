import asyncio
import dataclasses
import datetime
import typing

from telegrinder.api import ABCAPI
from telegrinder.bot.cute_types import BaseCute
from telegrinder.bot.dispatch.handler.abc import ABCHandler
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.model import Model

if typing.TYPE_CHECKING:
    from .machine import Identificator

T = typing.TypeVar("T", bound=Model)
EventModel = typing.TypeVar("EventModel", bound=BaseCute)

Behaviour: typing.TypeAlias = ABCHandler[T] | None


@dataclasses.dataclass
class ShortState(typing.Generic[EventModel]):
    key: "Identificator"
    ctx_api: ABCAPI
    event: asyncio.Event
    rules: tuple[ABCRule[EventModel], ...]
    _: dataclasses.KW_ONLY
    expiration: dataclasses.InitVar[datetime.timedelta | None] = dataclasses.field(
        default=None,
    )
    default_behaviour: Behaviour[EventModel] | None = dataclasses.field(default=None)
    on_drop_behaviour: Behaviour[EventModel] | None = dataclasses.field(default=None)
    expiration_date: datetime.datetime | None = dataclasses.field(init=False)

    def __post_init__(self, expiration: datetime.timedelta | None = None) -> None:
        self.expiration_date = (datetime.datetime.now() - expiration) if expiration is not None else None


__all__ = ("ShortState",)
