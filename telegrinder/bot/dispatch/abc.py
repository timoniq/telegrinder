import typing
from abc import ABC, abstractmethod

from fntypes import Option

from telegrinder.api.api import API
from telegrinder.tools.global_context.abc import ABCGlobalContext
from telegrinder.types.objects import Update

T = typing.TypeVar("T")


class ABCDispatch(ABC):
    @property
    @abstractmethod
    def global_context(self) -> ABCGlobalContext:
        pass

    @abstractmethod
    async def feed(self, event: Update, api: API) -> bool:
        pass

    @abstractmethod
    def load(self, external: typing.Self) -> None:
        pass

    def load_many(self, *externals: typing.Self) -> None:
        for external in externals:
            self.load(external)

    @abstractmethod
    def get_view(self, of_type: type[T]) -> Option[T]: ...


__all__ = ("ABCDispatch",)
