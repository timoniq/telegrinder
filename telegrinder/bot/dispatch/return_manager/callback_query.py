from telegrinder.bot.cute_types import CallbackQueryCute
from telegrinder.bot.dispatch.context import Context

from .abc import BaseReturnManager, register_manager


class CallbackQueryReturnManager(BaseReturnManager[CallbackQueryCute]):
    @register_manager(str)
    @staticmethod
    async def str_manager(value: str, event: CallbackQueryCute, ctx: Context) -> None:
        await event.answer(value)
    
    @register_manager(dict)
    @staticmethod
    async def dict_manager(value: dict, event: CallbackQueryCute, ctx: Context) -> None:
        await event.answer(**value)


__all__ = ("CallbackQueryReturnManager",)
