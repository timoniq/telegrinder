from telegrinder.bot.cute_types import CallbackQueryCute

from .abc import BaseReturnManager, register_manager


class CallbackQueryReturnManager(BaseReturnManager[CallbackQueryCute]):
    @register_manager(str)
    @staticmethod
    async def str_manager(value: str, event: CallbackQueryCute, ctx: dict) -> None:
        await event.answer(value)
    
    @register_manager(dict)
    @staticmethod
    async def dict_manager(value: dict, event: CallbackQueryCute, ctx: dict) -> None:
        await event.answer(**value)
