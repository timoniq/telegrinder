import typing

from telegrinder.bot.cute_types.pre_checkout_query import PreCheckoutQueryCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.return_manager.abc import BaseReturnManager, register_manager


class PreCheckoutQueryManager(BaseReturnManager[PreCheckoutQueryCute]):
    @register_manager(bool)
    @staticmethod
    async def bool_manager(value: bool, event: PreCheckoutQueryCute, ctx: Context) -> None:
        await event.answer(value)

    @register_manager(dict[str, typing.Any])
    @staticmethod
    async def dict_manager(value: dict[str, typing.Any], event: PreCheckoutQueryCute, ctx: Context) -> None:
        await event.answer(**value)


__all__ = ("PreCheckoutQueryManager",)
