import inspect
import typing

from telegrinder.bot.dispatch.context import Context
from telegrinder.types import Update

from .abc import ABCAdapter, ABCRule, RawUpdateAdapter, T


class FuncRule(ABCRule, typing.Generic[T]):
    def __init__(
        self,
        func: typing.Callable[[T, Context], typing.Awaitable[bool] | bool],
        adapter: ABCAdapter[Update, T] | None = None,
    ):
        self.func = func
        self.adapter = adapter or RawUpdateAdapter()

    async def check(self, event: T, ctx: Context) -> bool:
        result = self.func(event, ctx)
        if inspect.isawaitable(result):
            return await result
        return result  # type: ignore
