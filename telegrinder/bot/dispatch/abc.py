from abc import ABC, abstractmethod
from telegrinder.api.abc import ABCAPI
from telegrinder.types import Update
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.bot.dispatch.handler.func import FuncHandler
import typing


if typing.TYPE_CHECKING:
    from .view.abc import ABCView


P = typing.ParamSpec("P")
R = typing.TypeVar("R")


class ABCDispatch(ABC):
    global_context: dict[str, typing.Any]

    @abstractmethod
    def feed(self, event: Update, api: ABCAPI) -> bool:
        pass

    @abstractmethod
    def load(self, external: "ABCDispatch"):
        pass

    @abstractmethod
    def mount(self, view_t: typing.Type["ABCView"], name: str):
        pass

    @classmethod
    def to_handler(
        cls,
        *rules: tuple[ABCRule, ...],  # type: ignore
        is_blocking: bool = True,
    ) -> typing.Callable[typing.Callable[P.args, R], FuncHandler]:
        def wrapper(func: typing.Callable[P.args, R]):
            return FuncHandler(func, list(rules), is_blocking, dataclass=None)

        return wrapper
