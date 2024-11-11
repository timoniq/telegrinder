from abc import ABC

import typing_extensions as typing

from telegrinder.bot.dispatch.context import Context
from telegrinder.model import Model
from telegrinder.types.objects import Update

if typing.TYPE_CHECKING:
    from telegrinder.bot.rules.adapter.abc import ABCAdapter

ToEvent = typing.TypeVar("ToEvent", bound=Model, default=typing.Any)


class MiddlewareProto[Event: Model](typing.Protocol):
    adapter: "ABCAdapter[Update, Event] | None" = None

    async def pre(self, event: Event, ctx: Context, /) -> bool: ...

    async def post(self, event: Event, ctx: Context, /) -> None: ...


class ABCMiddleware[Event: Model](ABC):
    adapter: "ABCAdapter[Update, Event] | None" = None

    async def pre(self, event: Event, ctx: Context) -> bool: ...

    async def post(self, event: Event, ctx: Context, responses: list[typing.Any]) -> None: ...


class ABCGlobalMiddleware(ABC, typing.Generic[ToEvent]):
    _global = True
    adapter: "ABCAdapter[Update, ToEvent] | None" = None

    async def pre(self, event: ToEvent, ctx: Context) -> bool: ...

    async def post(self, event: ToEvent, ctx: Context) -> None: ...


__all__ = ("ABCGlobalMiddleware", "ABCMiddleware", "MiddlewareProto")
