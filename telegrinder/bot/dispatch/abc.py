import typing
from abc import ABC, abstractmethod

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.bot.dispatch.handler.func import ErrorHandlerT, FuncHandler
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.tools.global_context import ABCGlobalContext
from telegrinder.types import Update

T = typing.TypeVar("T", bound=BaseCute)
R = typing.TypeVar("R")
P = typing.ParamSpec("P")


class ABCDispatch(ABC):
    global_context: ABCGlobalContext

    @abstractmethod
    async def feed(self, event: Update, api: ABCAPI) -> bool:
        pass

    @abstractmethod
    def load(self, external: typing.Self):
        pass

    @classmethod
    def to_handler(
        cls,
        *rules: ABCRule[T],
        is_blocking: bool = True,
        error_handler: ErrorHandlerT | None = None,
    ):
        def wrapper(
            func: typing.Callable[typing.Concatenate[T, P], typing.Awaitable[R]]
        ) -> FuncHandler[
            T,
            typing.Callable[typing.Concatenate[T, P], typing.Awaitable[R]],
            ErrorHandlerT,
        ]:
            return FuncHandler(
                func,
                list(rules),
                is_blocking=is_blocking,
                dataclass=None,
                error_handler=error_handler,
            )

        return wrapper
