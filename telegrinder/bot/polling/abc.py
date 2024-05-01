import typing
from abc import ABC, abstractmethod

import msgspec

from telegrinder.types import Update


class ABCPolling(ABC):
    offset: int

    @abstractmethod
    async def get_updates(self) -> list[msgspec.Raw]:
        pass

    @abstractmethod
    async def listen(self) -> typing.AsyncGenerator[list[Update], None]:
        yield []

    @abstractmethod
    def stop(self) -> None:
        pass


__all__ = ("ABCPolling",)
