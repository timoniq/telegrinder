from __future__ import annotations

from abc import ABC

import typing_extensions as typing

from telegrinder.bot.dispatch.context import Context
from telegrinder.model import Model
from telegrinder.types.objects import Update

if typing.TYPE_CHECKING:
    from telegrinder.tools.adapter.abc import ABCAdapter

ToEvent = typing.TypeVar("ToEvent", bound=Model, default=typing.Any)


def repr_middleware(middleware: ABCMiddleware[ToEvent] | ABCGlobalMiddleware[ToEvent]) -> str:
    return "<{} with adapter={!r}>".format(
        ("Global middleware " if isinstance(middleware, ABCGlobalMiddleware) else "middleware ")
        + middleware.__class__.__name__,
        middleware.adapter,
    )


class ABCMiddleware[Event: Model](ABC):
    adapter: ABCAdapter[Update, Event] | None = None

    def __repr__(self) -> str:
        return repr_middleware(self)

    async def pre(self, event: Event, ctx: Context) -> bool: ...

    async def post(self, event: Event, ctx: Context, responses: list[typing.Any]) -> None: ...


class ABCGlobalMiddleware(ABC, typing.Generic[ToEvent]):
    _global = True
    adapter: ABCAdapter[Update, ToEvent] | None = None

    def __repr__(self) -> str:
        return repr_middleware(self)

    async def pre(self, event: ToEvent, ctx: Context) -> bool: ...

    async def post(self, event: ToEvent, ctx: Context) -> None: ...


__all__ = ("ABCGlobalMiddleware", "ABCMiddleware")
