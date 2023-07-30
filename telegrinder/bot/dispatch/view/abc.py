from abc import ABC, abstractmethod
from telegrinder.api.abc import ABCAPI
from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.types import Update
import typing

T = typing.TypeVar("T", bound=ABCMiddleware)
EventType = typing.TypeVar("EventType")

if typing.TYPE_CHECKING:
    from telegrinder.bot.dispatch.handler.abc import ABCHandler


class ABCView(ABC, typing.Generic[EventType]):
    auto_rules: list[ABCRule]
    handlers: list["ABCHandler"]
    middlewares: list[ABCMiddleware]

    @abstractmethod
    async def check(self, event: Update) -> bool:
        pass

    @abstractmethod
    async def process(self, event: Update, api: ABCAPI):
        pass

    def load(self, external: typing.Self):
        self.auto_rules.append(external.auto_rules)
        self.handlers.extend(external.handlers)
        self.middlewares.extend(external.middlewares)
        self.short_waiters.update(external.short_waiters)

    def register_middleware(self, *args, **kwargs):
        def wrapper(middleware: typing.Type[T]) -> typing.Type[T]:
            self.middlewares.append(middleware(*args, **kwargs))
            return middleware

        return wrapper


class ABCStateView(ABCView[T], ABC):
    @abstractmethod
    def get_state_key(self, event: EventType) -> int | None:
        pass
