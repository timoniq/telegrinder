from .abc import ABCDispatch
from abc import ABC, abstractmethod
from telegrinder.bot.rules import ABCRule
import typing

T = typing.TypeVar("T")


class ABCHandler(ABC, typing.Generic[T]):
    is_blocking: bool

    @abstractmethod
    async def run(self, event: T) -> typing.Any:
        pass

    @abstractmethod
    async def check(self, event: T) -> bool:
        pass


class FuncHandler(ABCHandler, typing.Generic[T]):
    def __init__(
        self,
        func: typing.Callable,
        rules: typing.List[ABCRule],
        is_blocking: bool = True,
    ):
        self.func = func
        self.is_blocking = is_blocking
        self.rules = rules
        self.ctx = {}

    async def check(self, event: T) -> bool:
        self.ctx = {}
        return all([(await rule.check(event, self.ctx)) for rule in self.rules])

    async def run(self, event: T) -> typing.Any:
        return await self.func(event, **self.ctx)


class Dispatch(ABCDispatch):
    def __init__(self):
        self.handlers: typing.List[ABCHandler] = []

    def handle(self, *rules: ABCRule, is_blocking: bool = False):
        def wrapper(func: typing.Callable):
            self.handlers.append(FuncHandler(func, list(rules), is_blocking))
            return func

        return wrapper

    async def feed(self, event: dict) -> bool:
        found = False
        for handler in self.handlers:
            result = await handler.check(event)
            if result:
                found = True
                await handler.run(event)
                if handler.is_blocking:
                    return True
        return found
