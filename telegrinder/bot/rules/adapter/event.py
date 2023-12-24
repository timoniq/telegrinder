import typing

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.cute_types import BaseCute
from telegrinder.bot.rules.adapter.abc import ABCAdapter
from telegrinder.bot.rules.adapter.errors import AdapterError
from telegrinder.result import Error, Ok, Result
from telegrinder.types.objects import Model, Update

EventT = typing.TypeVar("EventT", bound=Model)
CuteT = typing.TypeVar("CuteT", bound=BaseCute)


class EventAdapter(ABCAdapter[Update, CuteT]):
    def __init__(self, event_name: str, model: type[CuteT]):
        self.event_name = event_name
        self.model = model

    async def adapt(self, api: ABCAPI, update: Update) -> Result[CuteT, AdapterError]:
        update_dct = update.to_dict()
        if self.event_name not in update_dct:
            return Error(
                AdapterError(f"Update is not of event type {self.event_name!r}")
            )
        return Ok(
            self.model.from_update(update_dct[self.event_name].unwrap(), bound_api=api)
        )
