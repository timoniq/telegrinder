import typing
from abc import ABC

T = typing.TypeVar("T")


class ABCMiddleware(ABC, typing.Generic[T]):
    async def pre(self, event: T, ctx: dict) -> bool:
        ...

    async def post(self, event: T, responses: list[typing.Any], ctx: dict):
        ...
