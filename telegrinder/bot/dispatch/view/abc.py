from abc import ABC, abstractmethod
from telegrinder.api.abc import ABCAPI
from telegrinder.types import Update
import typing


class ABCView(ABC):
    @abstractmethod
    async def check(self, event: Update) -> bool:
        pass

    @abstractmethod
    async def process(self, event: Update, api: ABCAPI):
        pass

    @abstractmethod
    def load(self, external: typing.Self):
        pass
