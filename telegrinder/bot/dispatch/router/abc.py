import typing
from abc import ABC, abstractmethod

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.types.objects import Update


class ABCRouter(ABC):
    @abstractmethod
    async def route(self, api: API, update: Update, context: Context) -> typing.Any:
        pass


__all__ = ("ABCRouter",)
