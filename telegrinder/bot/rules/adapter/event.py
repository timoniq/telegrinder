import typing

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.rules.adapter.abc import ABCAdapter
from telegrinder.bot.rules.adapter.errors import AdapterError
from telegrinder.result import Error, Ok, Result
from telegrinder.types.objects import Model, Update

Event = typing.TypeVar("Event", bound=Model)


def get_updates() -> dict[str, Model]:
    dct = {}
    for k, hint in typing.get_type_hints(Update).items():
        if k in ("_dict_cached", "update_id"):
            continue
        dct[k] = hint.__args__[0]
    return dct


UPDATES = get_updates()


class EventAdapter(ABCAdapter[Update, Event]):
    def __init__(self, event_name: str, model: typing.Type[Event]) -> None:
        self.event_name = event_name
        self.model = model

    async def adapt(
        self, api: ABCAPI, update: Update | Event
    ) -> Result[Event, AdapterError]:
        if isinstance(update, UPDATES[self.event_name]):
            return Ok(update)

        update_dct = update.to_dict()
        if self.event_name not in update_dct.keys():
            return Error(
                AdapterError(f"Update is not of event type {self.event_name!r}")
            )
        return Ok(self.model(**update_dct[self.event_name].to_dict(), api=api))
