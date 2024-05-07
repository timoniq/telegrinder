import typing

from fntypes.result import Error, Ok, Result

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.cute_types import BaseCute
from telegrinder.bot.rules.adapter.abc import ABCAdapter
from telegrinder.bot.rules.adapter.errors import AdapterError
from telegrinder.msgspec_utils import Nothing
from telegrinder.types.objects import Model, Update

CuteT = typing.TypeVar("CuteT", bound=BaseCute)


class EventAdapter(ABCAdapter[Update, CuteT]):
    def __init__(self, event: str | type[Model], cute_model: type[CuteT]) -> None:
        self.event = event
        self.cute_model = cute_model

    def __repr__(self) -> str:
        if isinstance(self.event, str):
            raw_update_type = Update.__annotations__.get(self.event, "Unknown")
            raw_update_type = (
                typing.get_args(raw_update_type)[0].__forward_arg__
                if typing.get_args(raw_update_type)
                else raw_update_type
            )
        else:
            raw_update_type = self.event.__name__
        return "<{}: adapt {} -> {}>".format(
            self.__class__.__name__,
            raw_update_type,
            self.cute_model.__name__,
        )

    async def adapt(self, api: ABCAPI, update: Update) -> Result[CuteT, AdapterError]:
        update_dct = update.to_dict()
        if isinstance(self.event, str):
            if self.event not in update_dct:
                return Error(
                    AdapterError(f"Update is not of event type {self.event!r}."),
                )
            if update_dct[self.event] is Nothing:
                return Error(
                    AdapterError(f"Update is not an {self.event!r}."),
                )
            return Ok(
                self.cute_model.from_update(
                    update_dct[self.event].unwrap(), bound_api=api
                ),
            )
        event = update_dct[update.update_type.unwrap()].unwrap()
        if not update.update_type or not issubclass(event.__class__, self.event):
            return Error(AdapterError(f"Update is not an {self.event.__name__!r}."))
        return Ok(self.cute_model.from_update(event, bound_api=api))


__all__ = ("EventAdapter",)
