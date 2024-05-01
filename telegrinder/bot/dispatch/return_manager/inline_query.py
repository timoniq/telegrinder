import typing

from telegrinder.bot.cute_types import InlineQueryCute
from telegrinder.bot.dispatch.context import Context

from .abc import BaseReturnManager, register_manager


class InlineQueryReturnManager(BaseReturnManager[InlineQueryCute]):         
    @register_manager(dict)
    @staticmethod
    async def dict_manager(value: dict[str, typing.Any], event: InlineQueryCute, ctx: Context) -> None:
        await event.answer(**value)


__all__ = ("InlineQueryReturnManager",)
