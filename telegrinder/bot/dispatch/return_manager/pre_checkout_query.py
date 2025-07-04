import typing

from telegrinder.bot.cute_types.pre_checkout_query import PreCheckoutQueryCute
from telegrinder.bot.dispatch.return_manager.abc import BaseReturnManager, register_manager


class PreCheckoutQueryManager(BaseReturnManager):
    @register_manager(bool)
    @staticmethod
    async def bool_manager(value: bool, event: PreCheckoutQueryCute) -> None:
        await event.answer(value)

    @register_manager(dict)
    @staticmethod
    async def dict_manager(value: dict[str, typing.Any], event: PreCheckoutQueryCute) -> None:
        await event.answer(**value)


__all__ = ("PreCheckoutQueryManager",)
