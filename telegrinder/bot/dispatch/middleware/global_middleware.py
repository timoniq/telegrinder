import typing
from contextlib import contextmanager

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware
from telegrinder.bot.rules.abc import ABCRule, check_rule
from telegrinder.node.base import IsNode
from telegrinder.node.composer import compose_nodes
from telegrinder.types import Update
from telegrinder.types.objects import Update


class GlobalMiddleware(ABCMiddleware):
    def __init__(self) -> None:
        self.filters: set[ABCRule] = set()
        self.source_filters: dict[IsNode, dict[typing.Any, ABCRule]] = {}

    async def pre(self, event: Update, api: API, ctx: Context) -> bool:
        for filter in self.filters:
            if not await check_rule(api, filter, event, ctx):
                return False

        # Simple implication. Grouped by source categories
        for source, identifiers in self.source_filters.items():
            result = await compose_nodes({"value": source}, ctx, {Update: event, API: api})
            if result := result.unwrap():
                result = result.values["value"]
            else:
                return True

            if result in identifiers:
                return await check_rule(api, identifiers[result], event, ctx)

        return True

    @contextmanager
    def apply_filters(
        self,
        *filters: ABCRule,
        source_filter: tuple[IsNode, typing.Any, ABCRule] | None = None,
    ) -> typing.Generator[None, typing.Any, None]:
        if source_filter is not None:
            self.source_filters.setdefault(source_filter[0], {})
            self.source_filters[source_filter[0]].update({source_filter[1]: source_filter[2]})

        self.filters |= set(filters)
        yield
        self.filters.difference_update(filters)

        if source_filter is not None and (identifiers := self.source_filters.get(source_filter[0])):
            identifiers.pop(source_filter[1], None)


__all__ = ("GlobalMiddleware",)
