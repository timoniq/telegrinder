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


__all__ = ("ABCAdapter",)
