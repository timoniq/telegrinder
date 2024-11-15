import typing

from telegrinder.bot.cute_types import UpdateCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware
from telegrinder.bot.rules.abc import ABCRule, check_rule


class GlobalMiddleware(ABCMiddleware):
    def __init__(self):
        self._filters: list[ABCRule] = []

    @property
    def filters(self) -> typing.Generator[ABCRule, None, None]:
        yield from self._filters

    def add_filter(self, filter_rule: ABCRule) -> None:
        self._filters.append(filter_rule)

    async def pre(self, event: UpdateCute, ctx: Context) -> bool:
        for filter in self.filters:
            if not await check_rule(event.api, filter, event, ctx):
                return False
        return True
