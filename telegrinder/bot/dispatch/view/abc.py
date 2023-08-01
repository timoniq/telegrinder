import typing

from abc import ABC, abstractmethod
from telegrinder.api.abc import ABCAPI
from telegrinder.types import Update

EventType = typing.TypeVar("EventType")

if typing.TYPE_CHECKING:
    from telegrinder.bot.dispatch.handler.abc import ABCHandler


class ABCView(ABC, typing.Generic[EventType]):
    @abstractmethod
    async def check(self, event: Update) -> bool:
        pass

    @abstractmethod
    async def process(self, event: Update, api: ABCAPI):
        pass


class ABCStateView(ABCView[EventType], ABC):
    @abstractmethod
    def get_state_key(self, event: EventType) -> int | None:
        pass
