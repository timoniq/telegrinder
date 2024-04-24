import typing
from abc import ABC, abstractmethod

from fntypes.result import Result

from telegrinder.api import ABCAPI
from telegrinder.bot.cute_types import BaseCute
from telegrinder.bot.dispatch.context import Context

EventT = typing.TypeVar("EventT", bound=BaseCute)
Handler = typing.Callable[typing.Concatenate[EventT, ...], typing.Awaitable[typing.Any]]


class ABCErrorHandler(ABC, typing.Generic[EventT]):
    @abstractmethod
    def __call__(
        self,
        *args: typing.Any,
        **kwargs: typing.Any,
    ) -> typing.Callable[[typing.Callable[..., typing.Any]], typing.Callable[..., typing.Any]]:
        """Decorator for registering callback as an error handler."""

    @abstractmethod
    async def run(
        self,
        handler: Handler[EventT],
        event: EventT,
        api: ABCAPI,
        ctx: Context,
    ) -> Result[typing.Any, typing.Any]:
        """Run error handler."""


__all__ = ("ABCErrorHandler",)
