from abc import ABC, abstractmethod
from telegrinder.api.abc import ABCAPI
from telegrinder.types import Update
from .view.abc import ABCView
import typing


class ABCDispatch(ABC):
    @abstractmethod
    def feed(self, event: Update, api: ABCAPI) -> bool:
        pass

    @abstractmethod
    def load(self, external: "ABCDispatch"):
        pass

    @abstractmethod
    def mount(self, view_t: typing.Type["ABCView"], name: str):
        pass
