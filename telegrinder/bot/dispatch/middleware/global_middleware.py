from telegrinder.bot.cute_types import UpdateCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware
from telegrinder.bot.rules.abc import ABCRule, check_rule


class GlobalMiddleware(ABCMiddleware):
    def __init__(self):
        self.filters: set[ABCRule] = set()

    async def pre(self, event: UpdateCute, ctx: Context) -> bool:
        for filter in self.filters:
            if not await check_rule(event.api, filter, event, ctx):
                return False
        return True
