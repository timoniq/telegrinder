import typing
from abc import ABC

from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.bot.dispatch.context import Context

Event = typing.TypeVar("Event", bound=BaseCute)


class ABCMiddleware(ABC, typing.Generic[Event]):
    async def pre(self, event: Event, ctx: Context) -> bool: ...

    async def post(self, event: Event, responses: list[typing.Any], ctx: Context) -> None: ...


__all__ = ("ABCMiddleware",)
