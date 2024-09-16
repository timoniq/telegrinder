from telegrinder.bot.cute_types.update import UpdateCute
from telegrinder.types.enums import UpdateType

from .abc import ABCRule


class IsUpdateType(ABCRule):
    def __init__(self, update_type: UpdateType, /) -> None:
        self.update_type = update_type

    def check(self, event: UpdateCute) -> bool:
        return event.update_type == self.update_type


__all__ = ("IsUpdateType",)
