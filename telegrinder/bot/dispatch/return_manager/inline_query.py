import typing

from telegrinder.bot.cute_types.inline_query import InlineQueryCute
from telegrinder.bot.dispatch.return_manager.abc import BaseReturnManager, register_manager


class InlineQueryReturnManager(BaseReturnManager):
    @register_manager(dict)
    @staticmethod
    async def dict_manager(value: dict[str, typing.Any], event: InlineQueryCute) -> None:
        await event.answer(**value)


__all__ = ("InlineQueryReturnManager",)
