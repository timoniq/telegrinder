import typing

from fntypes.result import Error, Ok, Result

from telegrinder.api.api import API
from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.rules.adapter.abc import ABCAdapter
from telegrinder.bot.rules.adapter.errors import AdapterError
from telegrinder.bot.rules.adapter.raw_update import RawUpdateAdapter
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

        match await RawUpdateAdapter().adapt(api, update, context):
            case Ok(update_cute):
                incoming_update = None
                if isinstance(self.event, UpdateType) and self.event == update_cute.update_type:
                    incoming_update = update_cute.incoming_update
                if not isinstance(self.event, UpdateType) and (event := update_cute.get_event(self.event)):
                    incoming_update = update_cute.get_event(self.event).unwrap_or_none()

                if incoming_update is not None:
                    adapted = (
                        typing.cast(ToCute, incoming_update)
                        if isinstance(incoming_update, BaseCute)
                        else self.cute_model.from_update(incoming_update, bound_api=api)
                    )
                    context[self.ADAPTED_VALUE_KEY] = adapted
                    return Ok(adapted)

                return Error(AdapterError(f"Update is not an {self.event!r}."))
            case Error(_) as err:
                return err


__all__ = ("EventAdapter",)
