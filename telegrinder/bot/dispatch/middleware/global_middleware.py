import inspect
import typing
from contextlib import contextmanager

from telegrinder.api import API
from telegrinder.bot.cute_types.update import UpdateCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware
from telegrinder.bot.rules.abc import ABCRule, check_rule
from telegrinder.node import IsNode, compose_nodes
from telegrinder.tools.adapter.abc import ABCAdapter
from telegrinder.tools.adapter.raw_update import RawUpdateAdapter
from telegrinder.types import Update


class GlobalMiddleware(ABCMiddleware[UpdateCute]):
    adapter = RawUpdateAdapter()

    def __init__(self) -> None:
        self.filters: set[ABCRule] = set()
        self.source_filters: dict[ABCAdapter | IsNode, dict[typing.Any, ABCRule]] = {}

    async def pre(self, event: UpdateCute, ctx: Context) -> bool:
        for filter in self.filters:
            if not await check_rule(event.api, filter, event, ctx):
                return False

        # Simple implication.... Grouped by source categories
        for source, identifiers in self.source_filters.items():
            if isinstance(source, ABCAdapter):
                result = source.adapt(event.api, event, ctx)
                if inspect.isawaitable(result):
                    result = await result

                result = result.unwrap_or_none()
                if result is None:
                    return True

            else:
                result = await compose_nodes({"value": source}, ctx, {Update: event, API: event.api})
                if result := result.unwrap():
                    result = result.values["value"]
                else:
                    return True

            if result in identifiers:
                return await check_rule(event.api, identifiers[result], event, ctx)

        return True

    @contextmanager
    def apply_filters(
        self,
        *filters: ABCRule,
        source_filter: tuple[ABCAdapter | IsNode, typing.Any, ABCRule] | None = None,
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
