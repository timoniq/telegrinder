import typing

from telegrinder.types import Update

from .abc import ABCAdapter, ABCRule, RawUpdateAdapter, T


class FuncRule(ABCRule, typing.Generic[T]):
    def __init__(
        self,
        func: typing.Callable[[T, dict], bool],
        adapter: ABCAdapter[Update, T] | None = None,
    ):
        self.func = func
        self.adapter = adapter or RawUpdateAdapter()  # type: ignore

    async def check(self, event: T, ctx: dict) -> bool:
        return self.func(event, ctx)
