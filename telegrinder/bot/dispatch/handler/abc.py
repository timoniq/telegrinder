import typing
from abc import ABC, abstractmethod

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.dispatch.context import Context
from telegrinder.model import Model
from telegrinder.types import Update

T = typing.TypeVar("T", bound=Model)


class ABCHandler(ABC, typing.Generic[T]):
    is_blocking: bool

    @abstractmethod
    async def check(self, api: ABCAPI, event: Update, ctx: Context | None = None) -> bool:
        pass

    @abstractmethod
    async def run(self, event: T, ctx: Context) -> typing.Any:
        pass


__all__ = ("ABCHandler",)
