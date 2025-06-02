import typing
from abc import ABC, abstractmethod

from telegrinder.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.types.objects import Update

type Handler = typing.Callable[..., typing.Awaitable[typing.Any]]


class ABCErrorHandler(ABC):
    @abstractmethod
    def __call__(
        self,
        *args: typing.Any,
        **kwargs: typing.Any,
    ) -> typing.Callable[[typing.Callable[..., typing.Any]], typing.Callable[..., typing.Any]]:
        """Decorator for registering a function catcher."""

    @abstractmethod
    async def run(
        self,
        exception: BaseException,
        event: Update,
        api: API,
        ctx: Context,
    ) -> typing.Any:
        """Run the error handler."""


__all__ = ("ABCErrorHandler",)
