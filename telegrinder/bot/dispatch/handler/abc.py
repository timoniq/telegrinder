import typing
from abc import ABC, abstractmethod

from fntypes.result import Result

from telegrinder.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.types.objects import Update


class ABCHandler(ABC):
    final: bool

    @abstractmethod
    async def run(
        self,
        api: API,
        event: Update,
        context: Context,
        check: bool = True,
    ) -> Result[typing.Any, typing.Any]:
        pass


__all__ = ("ABCHandler",)
