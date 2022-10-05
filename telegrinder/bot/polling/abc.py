import typing
from abc import ABC, abstractmethod
from telegrinder.types import Update
from telegrinder.model import Raw


class ABCPolling(ABC):
    @abstractmethod
    async def get_updates(self) -> typing.List[Raw]:
        pass

    @abstractmethod
    async def listen(self) -> typing.AsyncIterator[typing.List[Update]]:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass
