import typing
from abc import ABC, abstractmethod

from telegrinder.api import ABCAPI
from telegrinder.bot.cute_types import BaseCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.result import Result

EventT = typing.TypeVar("EventT", bound=BaseCute)
Handler = typing.Callable[typing.Concatenate[EventT, ...], typing.Awaitable[typing.Any]]


class ABCErrorHandler(ABC, typing.Generic[EventT]):
    @abstractmethod
    def catch(self) -> typing.Callable[[typing.Callable], typing.Callable]:
        ...

    @abstractmethod
    async def run(
        self,
        handler: Handler[EventT],
        event: EventT,
        api: ABCAPI,
        ctx: Context,
    ) -> Result[typing.Any, typing.Any]:
        ...
