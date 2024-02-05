import typing

from fntypes.result import Error, Ok, Result

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.cute_types import BaseCute
from telegrinder.bot.rules.adapter.abc import ABCAdapter
from telegrinder.bot.rules.adapter.errors import AdapterError
from telegrinder.msgspec_utils import Nothing
from telegrinder.types.objects import Model, Update

EventT = typing.TypeVar("EventT", bound=Model)
CuteT = typing.TypeVar("CuteT", bound=BaseCute)


class EventAdapter(ABCAdapter[Update, CuteT]):
    def __init__(self, event_name: str, model: type[CuteT]):
        self.event_name = event_name
        self.model = model
    
    def __repr__(self) -> str:
        return "<{}: adapt Update.{} -> {}>".format(
            self.__class__.__name__,
            self.event_name,
            self.model.__name__,
        )

    async def adapt(self, api: ABCAPI, update: Update) -> Result[CuteT, AdapterError]:
        update_dct = update.to_dict()
        if self.event_name not in update_dct:
            return Error(
                AdapterError(f"Update is not of event type {self.event_name!r}.")
            )
        if update_dct[self.event_name] is Nothing:
            return Error(
                AdapterError(f"Update is not an {self.event_name!r}.")
            )
        return Ok(
            self.model.from_update(update_dct[self.event_name].unwrap(), bound_api=api)
        )


__all__ = ("EventAdapter",)
