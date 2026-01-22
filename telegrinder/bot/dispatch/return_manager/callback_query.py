import typing

from telegrinder.bot.cute_types.callback_query import CallbackQueryCute
from telegrinder.bot.dispatch.return_manager.abc import BaseReturnManager, register_manager


class CallbackQueryReturnManager(BaseReturnManager):
    @register_manager(str)
    @staticmethod
    async def str_manager(handler_response: str, event: CallbackQueryCute) -> None:
        await event.answer(handler_response)

    @register_manager(dict)
    @staticmethod
    async def dict_manager(handler_response: dict[str, typing.Any], event: CallbackQueryCute) -> None:
        await event.answer(**handler_response)


__all__ = ("CallbackQueryReturnManager",)
