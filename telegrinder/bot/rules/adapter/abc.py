import abc
import dataclasses
import typing

from fntypes.result import Result

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.rules.adapter.errors import AdapterError
from telegrinder.model import Model

From = typing.TypeVar("From", bound=Model)
To = typing.TypeVar("To")


class ABCAdapter(abc.ABC, typing.Generic[From, To]):
    @abc.abstractmethod
    async def adapt(self, api: ABCAPI, update: From) -> Result[To, AdapterError]:
        pass


@dataclasses.dataclass
class Event(typing.Generic[To]):
    obj: To


__all__ = ("ABCAdapter", "Event")
