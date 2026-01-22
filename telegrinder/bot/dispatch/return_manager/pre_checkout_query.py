import typing

from telegrinder.bot.cute_types.pre_checkout_query import PreCheckoutQueryCute
from telegrinder.bot.dispatch.return_manager.abc import BaseReturnManager, register_manager


class PreCheckoutQueryReturnManager(BaseReturnManager):
    @register_manager(bool)
    @staticmethod
    async def bool_manager(handler_response: bool, event: PreCheckoutQueryCute) -> None:
        await event.answer(handler_response)

    @register_manager(dict)
    @staticmethod
    async def dict_manager(handler_response: dict[str, typing.Any], event: PreCheckoutQueryCute) -> None:
        await event.answer(**handler_response)


__all__ = ("PreCheckoutQueryReturnManager",)
