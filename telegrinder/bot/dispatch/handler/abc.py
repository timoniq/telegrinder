import typing
from abc import ABC, abstractmethod

from telegrinder.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.model import Model
from telegrinder.types.objects import Update


class ABCHandler[Event: Model](ABC):
    is_blocking: bool

    @abstractmethod
    async def check(self, api: API, event: Update, ctx: Context | None = None) -> bool:
        pass

    @abstractmethod
    async def run(self, api: API, event: Event, ctx: Context) -> typing.Any:
        pass


__all__ = ("ABCHandler",)
