import typing
from abc import ABC, abstractmethod

from telegrinder.api.api import API
from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.bot.dispatch.handler.abc import ABCHandler
from telegrinder.types.objects import Update

Event = typing.TypeVar("Event", bound=BaseCute)


class ABCView(ABC):
    def __repr__(self) -> str:
        return "<{}>".format(self.__class__.__name__)

    @abstractmethod
    async def check(self, event: Update) -> bool:
        pass

    @abstractmethod
    async def process(self, event: Update, api: API) -> bool:
        pass

    @abstractmethod
    def load(self, external: typing.Self) -> None:
        pass


class ABCEventRawView(ABCView, ABC, typing.Generic[Event]):
    handlers: list[ABCHandler[Event]]


class ABCStateView(ABCView, typing.Generic[Event]):
    @abstractmethod
    def get_state_key(self, event: Event) -> int | None:
        pass


__all__ = (
    "ABCStateView",
    "ABCEventRawView",
    "ABCView",
)
