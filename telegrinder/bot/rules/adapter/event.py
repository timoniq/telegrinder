import typing

from fntypes.result import Error, Ok, Result

from telegrinder.api import API
from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.rules.adapter.abc import ABCAdapter
from telegrinder.bot.rules.adapter.errors import AdapterError
from telegrinder.msgspec_utils import Nothing
from telegrinder.types.enums import UpdateType
from telegrinder.types.objects import Model, Update

ToCute = typing.TypeVar("ToCute", bound=BaseCute)


class EventAdapter(ABCAdapter[Update, ToCute]):
    ADAPTED_VALUE_KEY: str = "_adapted_cute_event"

    def __init__(self, event: UpdateType | type[Model], cute_model: type[ToCute]) -> None:
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

        return "<{}: adapt Update -> {} -> {}>".format(
            self.__class__.__name__,
            raw_update_type,
            self.cute_model.__name__,
        )

    async def adapt(self, api: API, update: Update, context: Context) -> Result[ToCute, AdapterError]:
        if self.ADAPTED_VALUE_KEY in context:
            return Ok(context[self.ADAPTED_VALUE_KEY])

        if isinstance(self.event, UpdateType):
            if update.update_type != self.event:
                return Error(
                    AdapterError(f"Update is not of event type {self.event!r}."),
                )

            if isinstance(event := getattr(update, self.event.value, Nothing), type(Nothing)):
                return Error(
                    AdapterError(f"Update is not an {self.event!r}."),
                )

            if type(event) is self.cute_model:
                adapted = Ok(event)  # type: ignore
            else:
                adapted = self.cute_model.from_update(event, bound_api=api)
        else:
            event = getattr(update, update.update_type.value).unwrap()
            if not update.update_type or not issubclass(type(event), self.event):
                return Error(AdapterError(f"Update is not an {self.event.__name__!r}."))

            if type(event) is self.cute_model:
                adapted = event
            else:
                adapted = self.cute_model.from_update(event, bound_api=api)

        context[self.ADAPTED_VALUE_KEY] = adapted
        return Ok(adapted)  # type: ignore


__all__ = ("EventAdapter",)
