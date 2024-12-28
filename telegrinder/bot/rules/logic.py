import typing

from .abc import ABCRule, Context, UpdateCute, check_rule


class If(ABCRule):
    def __init__(self, condition: ABCRule) -> None:
        self.conditions = [condition]

    async def check(self, update: UpdateCute, ctx: Context) -> bool:
        for condition in self.conditions[:-1]:
            if not await check_rule(update.api, condition, update, ctx):
                return True
        return await check_rule(update.api, self.conditions[-1], update, ctx)

    def then(self, condition: ABCRule) -> typing.Self:
        self.conditions.append(condition)
        return self
