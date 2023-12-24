import typing
from abc import ABC, abstractmethod

from telegrinder.api.abc import ABCAPI
from telegrinder.tools.global_context import ABCGlobalContext
from telegrinder.types import Update


class ABCDispatch(ABC):
    global_context: ABCGlobalContext

    @abstractmethod
    async def feed(self, event: Update, api: ABCAPI) -> bool:
        pass

    @abstractmethod
    def load(self, external: typing.Self):
        pass
