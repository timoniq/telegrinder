import typing
from abc import ABC

from telegrinder.bot.dispatch.context import Context
from telegrinder.model import Model

Event = typing.TypeVar("Event", bound=Model)


class ABCMiddleware(ABC, typing.Generic[Event]):
    async def pre(self, event: Event, ctx: Context) -> bool: ...

    async def post(self, event: Event, responses: list[typing.Any], ctx: Context) -> None: ...


__all__ = ("ABCMiddleware",)
