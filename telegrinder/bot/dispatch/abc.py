import typing
from abc import ABC, abstractmethod

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.dispatch.handler.func import FuncHandler
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.types import Update

if typing.TYPE_CHECKING:
    from .view.abc import ABCView

P = typing.ParamSpec("P")
R = typing.TypeVar("R")


class ABCDispatch(ABC):
    global_context: dict[str, typing.Any]

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
        *rules: ABCRule,
        is_blocking: bool = True,
    ) -> typing.Callable[[typing.Callable[P, R]], FuncHandler]:  # type: ignore
        def wrapper(func: typing.Callable[P, R]):  # type: ignore
            return FuncHandler(func, list(rules), is_blocking, dataclass=None)

        return wrapper
