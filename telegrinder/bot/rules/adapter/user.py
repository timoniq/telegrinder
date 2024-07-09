import typing

from fntypes.result import Error, Ok, Result

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.bot.rules.adapter.abc import ABCAdapter
from telegrinder.bot.rules.adapter.errors import AdapterError
from telegrinder.bot.rules.adapter.raw_update import RawUpdateAdapter
from telegrinder.bot.rules.adapter.utils import Source, get_by_sources
from telegrinder.types.objects import Update, User

ToCute = typing.TypeVar("ToCute", bound=BaseCute)


@typing.runtime_checkable
class HasFrom(Source, typing.Protocol):
    from_: User


@typing.runtime_checkable
class HasUser(Source, typing.Protocol):
    user: User


class UserAdapter(ABCAdapter[Update, User]):
    def __init__(self) -> None:
        self.raw_adapter = RawUpdateAdapter()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: Update -> UpdateCute -> User>"

    async def adapt(self, api: ABCAPI, update: Update) -> Result[User, AdapterError]:
        match await self.raw_adapter.adapt(api, update):
            case Ok(event):
                if source := get_by_sources(event.incoming_update, [HasFrom, HasUser]):
                    return Ok(source)
                return Error(AdapterError(f"{event.incoming_update.__class__.__name__!r} has no user."))
            case Error(_) as error:
                return error


__all__ = ("UserAdapter",)
