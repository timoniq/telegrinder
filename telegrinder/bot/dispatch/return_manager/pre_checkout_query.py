import typing

from telegrinder.bot.cute_types.pre_checkout_query import PreCheckoutQueryCute
from telegrinder.bot.dispatch.return_manager.abc import BaseReturnManager, register_manager


class PreCheckoutQueryReturnManager(BaseReturnManager):
    @register_manager(bool)
    @staticmethod
    async def bool_manager(response: bool, event: PreCheckoutQueryCute) -> None:
        await event.answer(response)

    @register_manager(dict)
    @staticmethod
    async def dict_manager(response: dict[str, typing.Any], event: PreCheckoutQueryCute) -> None:
        await event.answer(**response)


__all__ = ("PreCheckoutQueryReturnManager",)
