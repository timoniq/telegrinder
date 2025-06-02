import typing
from abc import ABC, abstractmethod

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.handler.abc import ABCHandler
from telegrinder.types.objects import Update


class ABCView(ABC):
    def __repr__(self) -> str:
        return "<{}>".format(type(self).__name__)

    @abstractmethod
    async def check(self, event: Update) -> bool:
        pass

    @abstractmethod
    async def process(
        self,
        event: Update,
        api: API,
        context: Context,
    ) -> bool:
        pass

    @abstractmethod
    def load(self, external: typing.Self, /) -> None:
        pass


class ABCEventRawView(ABCView, ABC):
    handlers: list[ABCHandler]


__all__ = ("ABCEventRawView", "ABCView")
