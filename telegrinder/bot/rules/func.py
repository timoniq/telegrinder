import typing

from telegrinder.bot.dispatch.context import Context
from telegrinder.tools.adapter.abc import ABCAdapter
from telegrinder.tools.adapter.raw_update import RawUpdateAdapter
from telegrinder.tools.awaitable import maybe_awaitable
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
        return await maybe_awaitable(self.func(event, ctx))


__all__ = ("FuncRule",)
