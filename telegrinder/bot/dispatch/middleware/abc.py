from abc import ABC
import typing

T = typing.TypeVar("T")


class ABCMiddleware(ABC, typing.Generic[T]):
    async def pre(self, event: T, ctx: dict) -> bool:
        ...

    async def post(self, event: T, responses: typing.List[typing.Any], ctx: dict):
        ...
