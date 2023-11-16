import typing
from abc import ABC, abstractmethod

from telegrinder.api import ABCAPI
from telegrinder.bot.cute_types import BaseCute
from telegrinder.result import Result

P = typing.ParamSpec("P")
EventT = typing.TypeVar("EventT", bound=BaseCute)
Handler = typing.Callable[
    typing.Concatenate[EventT, ...], typing.Awaitable[typing.Any]
]


class ABCErrorHandler(ABC, typing.Generic[EventT]):
    @abstractmethod
    def catch(
        self,
        *exceptions: type[BaseException] | BaseException,
        **kwargs,
    ) -> typing.Callable[..., typing.Awaitable[typing.Any]]:
        ...

    async def run(
        self,
        handler: Handler[EventT],
        event: EventT,
        api: ABCAPI,
        ctx: dict,
    ) -> Result[typing.Any, typing.Any]:
        ...
