import typing

from telegrinder.bot.cute_types.message import MessageCute
from telegrinder.bot.dispatch.return_manager.abc import BaseReturnManager, register_manager
from telegrinder.tools.formatting import HTMLFormatter


class MessageReturnManager(BaseReturnManager):
    @register_manager(str)
    @staticmethod
    async def str_manager(value: str, event: MessageCute) -> None:
        await event.answer(value)

    @register_manager(list | tuple)
    @staticmethod
    async def seq_manager(
        value: list[typing.Any] | tuple[typing.Any, ...],
        event: MessageCute,
    ) -> None:
        for message in value:
            await event.answer(str(message))

    @register_manager(dict)
    @staticmethod
    async def dict_manager(value: dict[str, typing.Any], event: MessageCute) -> None:
        await event.answer(**value)

    @register_manager(HTMLFormatter)
    @staticmethod
    async def htmlformatter_manager(value: HTMLFormatter, event: MessageCute) -> None:
        await event.answer(value, parse_mode=HTMLFormatter.PARSE_MODE)


__all__ = ("MessageReturnManager",)
