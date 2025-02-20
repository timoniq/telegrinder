import inspect
import typing

from telegrinder.bot.dispatch.context import Context
from telegrinder.tools.adapter.abc import ABCAdapter
from telegrinder.tools.adapter.raw_update import RawUpdateAdapter
from telegrinder.types.objects import Update

from .abc import ABCRule, AdaptTo


class FuncRule(ABCRule, typing.Generic[AdaptTo]):
    def __init__(
        self,
        func: typing.Callable[[AdaptTo, Context], typing.Awaitable[bool] | bool],
        adapter: ABCAdapter[Update, AdaptTo] | None = None,
    ) -> None:
        self.func = func
        self.adapter = adapter or RawUpdateAdapter()  # type: ignore

    async def check(self, event: AdaptTo, ctx: Context) -> bool:
        result = self.func(event, ctx)
        if inspect.isawaitable(result):
            result = await result
        return result


__all__ = ("FuncRule",)
