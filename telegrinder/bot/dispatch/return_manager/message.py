import typing

from telegrinder.bot.cute_types.message import MessageCute
from telegrinder.bot.dispatch.return_manager.abc import BaseReturnManager, register_manager
from telegrinder.tools.formatting import HTML


class MessageReturnManager(BaseReturnManager):
    @register_manager(str)
    @staticmethod
    async def str_manager(response: str, event: MessageCute) -> None:
        await event.answer(response)

    @register_manager(list | tuple)
    @staticmethod
    async def seq_manager(
        response: list[typing.Any] | tuple[typing.Any, ...],
        event: MessageCute,
    ) -> None:
        for message in response:
            await event.answer(str(message))

    @register_manager(dict)
    @staticmethod
    async def dict_manager(response: dict[str, typing.Any], event: MessageCute) -> None:
        await event.answer(**response)

    @register_manager(HTML)
    @staticmethod
    async def html_manager(response: HTML, event: MessageCute) -> None:
        await event.answer(response, parse_mode=HTML.PARSE_MODE)


__all__ = ("MessageReturnManager",)
