import inspect
import typing

from telegrinder.bot.dispatch.context import Context
from telegrinder.types import Update

from .abc import ABCAdapter, ABCRule, AdaptTo, EventCute, RawUpdateAdapter


class FuncRule(ABCRule[EventCute, AdaptTo], typing.Generic[AdaptTo, EventCute]):
    def __init__(
        self,
        func: typing.Callable[[AdaptTo, Context], typing.Awaitable[bool] | bool],
        adapter: ABCAdapter[Update, AdaptTo] | None = None,
    ):
        self.func = func
        self.adapter = adapter or RawUpdateAdapter()  # type: ignore

    async def check(self, event: AdaptTo, ctx: Context) -> bool:
        result = self.func(event, ctx)
        if inspect.isawaitable(result):
            return await result
        return result  # type: ignore


__all__ = ("FuncRule",)
