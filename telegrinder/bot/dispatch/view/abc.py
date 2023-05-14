from abc import ABC, abstractmethod
from telegrinder.api.abc import ABCAPI
from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware
from telegrinder.bot.dispatch.handler.abc import ABCHandler
from telegrinder.bot.dispatch.waiter import Waiter
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.types import Update
import typing

T = typing.TypeVar("T", bound=ABCMiddleware)


class ABCView(ABC):
    auto_rules: list[ABCRule]
    handlers: list[ABCHandler]
    middlewares: list[ABCMiddleware]
    short_waiters: dict[int, Waiter]

    @abstractmethod
    async def check(self, event: Update) -> bool:
        pass

    @abstractmethod
    async def process(self, event: Update, api: ABCAPI):
        pass

    def load(self, external: typing.Self):
        self.short_waiters = external.short_waiters
        self.handlers.extend(external.handlers)
        self.middlewares.extend(external.middlewares)

    def register_middleware(self, *args, **kwargs):
        def wrapper(middleware: typing.Type[T]) -> typing.Type[T]:
            self.middlewares.append(middleware(*args, **kwargs))
            return middleware

        return wrapper
