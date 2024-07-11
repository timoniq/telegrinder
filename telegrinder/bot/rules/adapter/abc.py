import abc
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


class Event(typing.Generic[To]):
    def __init__(self, obj: To) -> None:
        self.obj = obj

__all__ = ("ABCAdapter", "Event")
