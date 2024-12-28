from fntypes.option import Nothing, Some
from fntypes.result import Error, Ok, Result

from telegrinder.api.api import API
from telegrinder.bot.adapter.abc import ABCAdapter
from telegrinder.bot.adapter.errors import AdapterError
from telegrinder.bot.cute_types import BaseCute, UpdateCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.types.enums import UpdateType
from telegrinder.types.objects import Update


class DataclassAdapter[Dataclass](ABCAdapter[Update, Dataclass]):
    ADAPTED_VALUE_KEY: str

    def __init__(
        self,
        dataclass: type[Dataclass],
        update_type: UpdateType | None = None,
    ) -> None:
        self.ADAPTED_VALUE_KEY = f"_adapted_dataclass_{dataclass.__name__}"
        self.dataclass = dataclass
        self.update_type = update_type

    def __repr__(self) -> str:
        return f"<Update -> {self.dataclass.__name__}>"

    def adapt(self, api: API, update: Update, context: Context) -> Result[Dataclass, AdapterError]:
        if self.ADAPTED_VALUE_KEY in context:
            return Ok(context[self.ADAPTED_VALUE_KEY])

        update_type = (self.update_type or update.update_type).value
        try:
            if self.dataclass is Update:
                return Ok(update)  # type: ignore
            elif issubclass(self.dataclass, UpdateCute):
                dataclass = self.dataclass.from_update(update, bound_api=api)
            else:
                match getattr(update, update_type):
                    case Some(val):
                        dataclass = (
                            self.dataclass.from_update(val, bound_api=api)
                            if issubclass(self.dataclass, BaseCute)
                            else self.dataclass(**val.to_dict())
                        )
                    case Nothing():
                        return Error(AdapterError(f"Update has no event {update_type!r}."))
        except Exception as e:
            return Error(AdapterError(f"Cannot adapt Update to {self.dataclass!r}, error: {e!r}"))

        context[self.ADAPTED_VALUE_KEY] = dataclass
        return Ok(dataclass)  # type: ignore


__all__ = ("DataclassAdapter",)
