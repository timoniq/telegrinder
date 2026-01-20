import dataclasses
import typing
from collections import deque

from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware
from telegrinder.bot.dispatch.middleware.filter import FilterMiddleware
from telegrinder.bot.dispatch.middleware.media_group import MediaGroupMiddleware


@dataclasses.dataclass(frozen=True)
class MiddlewareBox:
    filter: FilterMiddleware = dataclasses.field(default_factory=FilterMiddleware)
    media_group: MediaGroupMiddleware = dataclasses.field(default_factory=MediaGroupMiddleware)
    _custom_middlewares: deque[ABCMiddleware] = dataclasses.field(
        default_factory=deque,
        repr=False,
    )

    def __call__[Middleware: ABCMiddleware](self, middleware: type[Middleware], /) -> type[Middleware]:
        self.put(middleware())
        return middleware

    def __iter__(self) -> typing.Iterator[ABCMiddleware]:
        for middleware in (self.filter, self.media_group, *self._custom_middlewares):
            yield middleware

    def put(self, middleware: ABCMiddleware, /) -> None:
        self._custom_middlewares.append(middleware)


__all__ = ("MiddlewareBox",)
