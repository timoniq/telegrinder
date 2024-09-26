import abc
import dataclasses
import typing

from fntypes.result import Result

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.rules.adapter.errors import AdapterError
from telegrinder.model import Model

From = typing.TypeVar("From", bound=Model)
To = typing.TypeVar("To")


class ABCAdapter(abc.ABC, typing.Generic[From, To]):
    ADAPTED_VALUE_KEY: str | None = None

    @abc.abstractmethod
    async def adapt(self, api: API, update: From, context: Context) -> Result[To, AdapterError]:
        pass


@dataclasses.dataclass(slots=True)
class Event(typing.Generic[To]):
    obj: To


__all__ = ("ABCAdapter", "Event")
