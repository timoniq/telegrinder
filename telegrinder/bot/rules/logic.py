import typing

from telegrinder.api.api import API
from telegrinder.bot.rules.abc import ABCRule, Context, check_rule
from telegrinder.types.objects import Update


class If(ABCRule):
    def __init__(self, condition: ABCRule) -> None:
        self.conditions = [condition]

    async def check(self, update: Update, api: API, ctx: Context) -> bool:
        for condition in self.conditions[:-1]:
            if not await check_rule(api, condition, update, ctx):
                return True

        return await check_rule(api, self.conditions[-1], update, ctx)

    def then(self, condition: ABCRule, /) -> typing.Self:
        self.conditions.append(condition)
        return self


__all__ = ("If",)
