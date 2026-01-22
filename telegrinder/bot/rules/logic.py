import typing

from telegrinder.bot.rules.abc import ABCRule, Context, check_rule


class If(ABCRule):
    def __init__(self, condition: ABCRule) -> None:
        self.conditions = [condition]

    async def check(self, context: Context) -> bool:
        for condition in self.conditions[:-1]:
            if not await check_rule(condition, context):
                return True

        return await check_rule(self.conditions[-1], context)

    def then(self, condition: ABCRule, /) -> typing.Self:
        self.conditions.append(condition)
        return self


__all__ = ("If",)
