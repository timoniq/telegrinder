import typing
from abc import ABC, abstractmethod

from fntypes.result import Result

from telegrinder.api import API
from telegrinder.bot.dispatch.context import Context

type Handler = typing.Callable[..., typing.Awaitable[typing.Any]]


class ABCErrorHandler[Event](ABC):
    @abstractmethod
    def __call__(
        self,
        *args: typing.Any,
        **kwargs: typing.Any,
    ) -> typing.Callable[[typing.Callable[..., typing.Any]], typing.Callable[..., typing.Any]]:
        """Decorator for registering callback as a catcher for the error handler."""

    @abstractmethod
    async def run(
        self,
        handler: Handler,
        event: Event,
        api: API,
        ctx: Context,
    ) -> Result[typing.Any, typing.Any]:
        """Run the error handler."""


__all__ = ("ABCErrorHandler",)
