import typing

from fntypes.result import Error, Ok, Result

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.bot.rules.adapter.abc import ABCAdapter
from telegrinder.bot.rules.adapter.errors import AdapterError
from telegrinder.bot.rules.adapter.raw_update import RawUpdateAdapter
from telegrinder.bot.rules.adapter.utils import Source, get_by_sources
from telegrinder.types.objects import Chat, Update

ToCute = typing.TypeVar("ToCute", bound=BaseCute)


@typing.runtime_checkable
class HasChat(Source, typing.Protocol):
    chat: Chat


class ChatAdapter(ABCAdapter[Update, Chat]):
    def __init__(self) -> None:
        self.raw_adapter = RawUpdateAdapter()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: Update -> UpdateCute -> Chat>"

    async def adapt(self, api: ABCAPI, update: Update) -> Result[Chat, AdapterError]:
        match await self.raw_adapter.adapt(api, update):
            case Ok(event):
                if source := get_by_sources(event.incoming_update, HasChat):
                    return Ok(source)
                return Error(AdapterError(f"{event.incoming_update.__class__.__name__!r} has no chat."))
            case Error(_) as error:
                return error


__all__ = ("ChatAdapter",)
