import typing
from abc import ABC, abstractmethod


class ABCPolling(ABC):
    @abstractmethod
    async def get_updates(self) -> typing.Any:
        pass

    @abstractmethod
    async def listen(self) -> typing.AsyncIterator[dict]:
        pass
