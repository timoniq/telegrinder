from telegrinder.bot.cute_types.update import UpdateCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.types.enums import UpdateType

from .abc import ABCRule, T


class IsUpdate(ABCRule[T]):
    def __init__(self, update_type: UpdateType, /) -> None:
        self.update_type = update_type

    async def check(self, event: UpdateCute, ctx: Context) -> bool:
        return event.update_type.unwrap_or_none() == self.update_type


__all__ = ("IsUpdate",)
