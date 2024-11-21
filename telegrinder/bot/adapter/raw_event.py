from fntypes.result import Error, Ok, Result

from telegrinder.api.api import API
from telegrinder.bot.adapter.abc import ABCAdapter
from telegrinder.bot.adapter.errors import AdapterError
from telegrinder.bot.dispatch.context import Context
from telegrinder.model import Model
from telegrinder.types.objects import Update


class RawEventAdapter(ABCAdapter[Update, Model]):
    def __init__(self, event_model: type[Model], /) -> None:
        self.event_model = event_model

    def __repr__(self) -> str:
        return "<{}: adapt Update -> {}>".format(
            self.__class__.__name__,
            self.event_model.__name__,
        )

    def adapt(self, api: API, update: Update, context: Context) -> Result[Model, AdapterError]:
        if isinstance(update.incoming_update, self.event_model):
            return Ok(update.incoming_update)
        return Error(AdapterError(f"Update is not an {self.event_model.__name__!r}."))


__all__ = ("RawEventAdapter",)
