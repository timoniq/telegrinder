from abc import ABC, abstractmethod
from telegrinder.types import Update
from telegrinder.api.abc import ABCAPI
import typing

T = typing.TypeVar("T")


class ABCHandler(ABC, typing.Generic[T]):
    is_blocking: bool
    ctx: dict

    @abstractmethod
    async def run(self, event: T) -> typing.Any:
        pass

    @abstractmethod
    async def check(self, api: ABCAPI, event: Update, ctx: dict | None = None) -> bool:
        pass
