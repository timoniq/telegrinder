import typing

from fntypes.result import Error, Ok, Result

from telegrinder.api.api import API
from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.bot.cute_types.update import UpdateCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.tools.adapter.abc import ABCAdapter
from telegrinder.tools.adapter.errors import AdapterError
from telegrinder.tools.adapter.raw_update import RawUpdateAdapter
from telegrinder.types.enums import UpdateType
from telegrinder.types.objects import Model, Update


class EventAdapter[ToEvent: BaseCute](ABCAdapter[Update, ToEvent]):
    ADAPTED_VALUE_KEY: str = "_adapted_cute_event"

    def __init__(self, event: UpdateType | type[Model], cute_model: type[ToEvent]) -> None:
        self.event = event
        self.cute_model = cute_model

    def __repr__(self) -> str:
        raw_update_type = (
            f"Update -> {self.event.__name__}" if isinstance(self.event, type) else f"Update.{self.event.value}"  # type: ignore
        )
        return "<{}: adapt {} -> {}>".format(
            self.__class__.__name__,
            raw_update_type,
            self.cute_model.__name__,
        )

    def get_event(self, update: UpdateCute) -> Model | None:
        if isinstance(self.event, UpdateType) and self.event == update.update_type:
            return update.incoming_update

        if not isinstance(self.event, UpdateType) and (event := update.get_event(self.event)):
            return event.unwrap()

        return None

    def adapt(self, api: API, update: Update, context: Context) -> Result[ToEvent, AdapterError]:
        match RawUpdateAdapter().adapt(api, update, context):
            case Ok(update_cute) if event := self.get_event(update_cute):
                if self.ADAPTED_VALUE_KEY in context:
                    return Ok(context[self.ADAPTED_VALUE_KEY])

                adapted = (
                    typing.cast("ToEvent", event)
                    if isinstance(event, BaseCute)
                    else self.cute_model.from_update(event, bound_api=api)
                )
                context[self.ADAPTED_VALUE_KEY] = adapted
                return Ok(adapted)
            case Error(_) as err:
                return err
            case _:
                return Error(AdapterError(f"Update is not an {self.event!r}."))


__all__ = ("EventAdapter",)
