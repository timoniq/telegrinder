from abc import ABC, abstractmethod
from telegrinder.api.abc import ABCAPI


class ABCView(ABC):
    @abstractmethod
    async def check(self, event: dict) -> bool:
        pass

    @abstractmethod
    async def process(self, event: dict, api: ABCAPI):
        pass
