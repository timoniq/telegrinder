from msgspex import Model

from telegrinder.bot.rules.abc import ABCRule
from telegrinder.types.enums import UpdateType
from telegrinder.types.objects import Update


class IsUpdateType(ABCRule):
    def __init__(self, update_type: UpdateType, /) -> None:
        self.update_type = update_type

    def check(self, update: Update) -> bool:
        return update.update_type == self.update_type


class IsUpdateModelType(ABCRule):
    def __init__(self, model_type: type[Model], /) -> None:
        self.model_type = model_type

    def check(self, update: Update) -> bool:
        return issubclass(type(update.incoming_update), self.model_type)


__all__ = ("IsUpdateModelType", "IsUpdateType")
