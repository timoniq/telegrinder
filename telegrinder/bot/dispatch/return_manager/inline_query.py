import typing

from telegrinder.bot.cute_types.inline_query import InlineQueryCute
from telegrinder.bot.dispatch.return_manager.abc import BaseReturnManager, register_manager


class InlineQueryReturnManager(BaseReturnManager):
    @register_manager(dict)
    @staticmethod
    async def dict_manager(response: dict[str, typing.Any], event: InlineQueryCute) -> None:
        await event.answer(**response)


__all__ = ("InlineQueryReturnManager",)
