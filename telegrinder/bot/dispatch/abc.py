import typing
from abc import ABC, abstractmethod

from telegrinder.api.abc import ABCAPI
from telegrinder.tools.global_context.abc import ABCGlobalContext
from telegrinder.types.objects import Update


class ABCDispatch(ABC):
    @property
    @abstractmethod
    def global_context(self) -> ABCGlobalContext:
        pass

    @abstractmethod
    async def feed(self, event: Update, api: ABCAPI) -> bool:
        pass

    @abstractmethod
    def load(self, external: typing.Self) -> None:
        pass

    def load_many(self, *externals: typing.Self) -> None:
        for external in externals:
            self.load(external)


__all__ = ("ABCDispatch",)
