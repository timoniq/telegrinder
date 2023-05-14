import abc
import typing
from telegrinder.result import Result
from telegrinder.bot.rules.adapter.errors import AdapterError
from telegrinder.api.abc import ABCAPI

UpdateT = typing.TypeVar("UpdateT")
T = typing.TypeVar("T")


class ABCAdapter(abc.ABC, typing.Generic[UpdateT, T]):
    @abc.abstractmethod
    async def adapt(self, api: ABCAPI, update: UpdateT) -> Result[T, AdapterError]:
        pass
