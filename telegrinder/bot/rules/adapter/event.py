import typing

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.cute_types import BaseCute
from telegrinder.bot.rules.adapter.abc import ABCAdapter
from telegrinder.bot.rules.adapter.errors import AdapterError
from telegrinder.result import Error, Ok, Result
from telegrinder.types.objects import Model, Update

EventT = typing.TypeVar("EventT", bound=Model)
CuteT = typing.TypeVar("CuteT", bound=BaseCute)


def get_updates() -> dict[str, type[Model]]:
    dct = {}
    for k, hint in typing.get_type_hints(Update).items():
        if k in ("_dict_cached", "update_id"):
            continue
        dct[k] = (typing.get_args(hint) or (hint,))[0]
    return dct


UPDATES = get_updates()


class EventAdapter(ABCAdapter[Update, CuteT]):
    def __init__(self, event_name: str, model: typing.Type[CuteT]) -> None:
        self.event_name = event_name
        self.model = model

    async def adapt(self, api: ABCAPI, update: Update) -> Result[CuteT, AdapterError]:
        if isinstance(update, UPDATES[self.event_name]):
            return Ok(self.model.from_update(update, bound_api=api))

        update_dct = update.to_dict()
        if self.event_name not in update_dct:
            return Error(
                AdapterError(f"Update is not of event type {self.event_name!r}")
            )
        return Ok(self.model.from_update(update_dct[self.event_name], bound_api=api))
