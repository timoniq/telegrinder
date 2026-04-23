from __future__ import annotations

import dataclasses
import typing
from collections import deque

from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware
from telegrinder.bot.dispatch.middleware.filter import FilterMiddleware
from telegrinder.bot.dispatch.middleware.media_group import MediaGroupMiddleware
from telegrinder.tools.singleton import Singleton

if typing.TYPE_CHECKING:
    from telegrinder.bot.dispatch.middleware.waiter import WaiterMiddleware


@dataclasses.dataclass
class BaseMiddlewareBox:
    user_middlewares: deque[ABCMiddleware] = dataclasses.field(
        default_factory=deque,
        repr=False,
        init=False,
    )

    def __call__[Middleware: ABCMiddleware](self, middleware: type[Middleware], /) -> type[Middleware]:
        self.put(middleware())
        return middleware

    def __iter__(self) -> typing.Iterator[ABCMiddleware]:
        yield from self.user_middlewares

    def __len__(self) -> int:
        return sum(1 for _ in self)

    def put(self, middleware: ABCMiddleware, /) -> None:
        self.user_middlewares.append(middleware)


@dataclasses.dataclass(kw_only=True)
class ViewMiddlewareBox(BaseMiddlewareBox):
    waiter: WaiterMiddleware

    def __iter__(self) -> typing.Iterator[ABCMiddleware]:
        if self.waiter:
            yield self.waiter

        yield from self.user_middlewares

    def extend(self, other: typing.Self, /) -> None:
        self.waiter.hashers.update(other.waiter.hashers)
        self.user_middlewares.extend(other.user_middlewares)


@dataclasses.dataclass(kw_only=True)
class MiddlewareBox(BaseMiddlewareBox, Singleton):
    waiter: WaiterMiddleware
    filter: FilterMiddleware = dataclasses.field(default_factory=FilterMiddleware)
    media_group: MediaGroupMiddleware = dataclasses.field(default_factory=MediaGroupMiddleware)

    def __iter__(self) -> typing.Iterator[ABCMiddleware]:
        if self.filter:
            yield self.filter

        if self.media_group:
            yield self.media_group

        if self.waiter:
            yield self.waiter

        yield from self.user_middlewares


__all__ = ("MiddlewareBox", "ViewMiddlewareBox")
