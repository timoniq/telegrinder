import typing
from abc import ABC, abstractmethod

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.bot.dispatch.handler.func import FuncHandler
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.tools.global_context import ABCGlobalContext
from telegrinder.types import Update

if typing.TYPE_CHECKING:
    from .view.abc import ABCView

T = typing.TypeVar("T", bound=BaseCute)
R = typing.TypeVar("R")
P = typing.ParamSpec("P")


class ABCDispatch(ABC):
    global_context: ABCGlobalContext

    @abstractmethod
    async def feed(self, event: Update, api: ABCAPI) -> bool:
        pass

    @abstractmethod
    def load(self, external: "ABCDispatch"):
        pass

    @abstractmethod
    def mount(self, view: "ABCView", name: str):
        pass

    @classmethod
    def to_handler(
        cls,
        *rules: ABCRule[T],
        is_blocking: bool = True,
    ):
        def wrapper(
            func: typing.Callable[typing.Concatenate[T, P], typing.Awaitable[R]]
        ) -> FuncHandler[T, typing.Callable[typing.Concatenate[T, P], typing.Awaitable[R]]]:
            return FuncHandler(func, list(rules), is_blocking, dataclass=None)

        return wrapper
