import typing
from abc import ABC, abstractmethod

from telegrinder.api.api import API
from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.bot.dispatch.handler.abc import ABCHandler
from telegrinder.types.objects import Update


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


class ABCEventRawView[Event: BaseCute](ABCView, ABC):
    handlers: list[ABCHandler[Event]]


class ABCStateView[Event: BaseCute](ABCView):
    @abstractmethod
    def get_state_key(self, event: Event) -> int | None:
        pass


__all__ = (
    "ABCEventRawView",
    "ABCStateView",
    "ABCView",
)
