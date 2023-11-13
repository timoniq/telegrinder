import asyncio
import datetime
import typing

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.cute_types import BaseCute
from telegrinder.bot.dispatch.handler.abc import ABCHandler
from telegrinder.bot.rules.abc import ABCRule

if typing.TYPE_CHECKING:
    from .machine import Identificator

EventModel = typing.TypeVar("EventModel", bound=BaseCute)
Behaviour = ABCHandler | None


class ShortState(typing.Generic[EventModel]):
    def __init__(
        self,
        key: "Identificator",
        ctx_api: ABCAPI,
        event: asyncio.Event,
        rules: tuple[ABCRule[EventModel], ...],
        expiration: datetime.timedelta | None = None,
        default_behaviour: Behaviour = None,
        on_drop_behaviour: Behaviour = None,
    ) -> None:
        self.key = key
        self.ctx_api = ctx_api
        self.event = event
        self.rules = rules
        self.default_behaviour = default_behaviour
        self.expiration = (datetime.datetime.now() + expiration) if expiration else None
        self.on_drop_behaviour = on_drop_behaviour
