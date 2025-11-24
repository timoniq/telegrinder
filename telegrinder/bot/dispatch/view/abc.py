import typing
from abc import ABC, abstractmethod

from kungfu import Result

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.types.objects import Update


class ABCView(ABC):
    @abstractmethod
    async def process(
        self,
        api: API,
        update: Update,
        context: Context,
    ) -> Result[typing.Any, typing.Any]:
        pass


__all__ = ("ABCView",)
