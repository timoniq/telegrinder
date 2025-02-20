import typing

from telegrinder.bot.cute_types.inline_query import InlineQueryCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.return_manager.abc import BaseReturnManager, register_manager


class InlineQueryReturnManager(BaseReturnManager[InlineQueryCute]):
    @register_manager(dict[str, typing.Any])
    @staticmethod
    async def dict_manager(value: dict[str, typing.Any], event: InlineQueryCute, ctx: Context) -> None:
        await event.answer(**value)


__all__ = ("InlineQueryReturnManager",)
