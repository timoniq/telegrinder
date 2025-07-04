import typing

from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.tools.aio import maybe_awaitable
from telegrinder.types.objects import Update


class FuncRule(ABCRule):
    def __init__(
        self,
        func: typing.Callable[[Update, Context], typing.Awaitable[bool] | bool],
        /,
    ) -> None:
        self.func = func

    async def check(self, update: Update, ctx: Context) -> bool:
        return await maybe_awaitable(self.func(update, ctx))


__all__ = ("FuncRule",)
