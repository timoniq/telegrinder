from abc import ABC, abstractmethod
from telegrinder.types import Update
import typing

T = typing.TypeVar("T")


class ABCHandler(ABC, typing.Generic[T]):
    is_blocking: bool
    ctx: dict

    @abstractmethod
    async def run(self, event: T) -> typing.Any:
        pass

    @abstractmethod
    async def check(self, event: Update) -> bool:
        pass
