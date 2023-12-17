import typing
from abc import ABC, abstractmethod

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.cute_types import BaseCute
from telegrinder.types import Update

EventType = typing.TypeVar("EventType", bound=BaseCute)


class ABCView(ABC):
    @abstractmethod
    async def check(self, event: Update) -> bool:
        pass

    @abstractmethod
    async def process(self, event: Update, api: ABCAPI):
        pass

    @abstractmethod
    def load(self, external: typing.Self) -> None:
        pass


class ABCStateView(ABCView, typing.Generic[EventType]):
    @abstractmethod
    def get_state_key(self, event: EventType) -> int | None:
        pass

    def __repr__(self) -> str:
        return "<{!r}: {}>".format(
            self.__class__.__name__,
            ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        )
