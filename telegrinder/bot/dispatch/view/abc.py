from abc import ABC, abstractmethod
from telegrinder.api.abc import ABCAPI
from telegrinder.types import Update


class ABCView(ABC):
    @abstractmethod
    async def check(self, event: Update) -> bool:
        pass

    @abstractmethod
    async def process(self, event: Update, api: ABCAPI):
        pass

    @abstractmethod
    async def load(self, external: "ABCView"):
        pass
