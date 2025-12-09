import typing
from contextlib import contextmanager

from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware
from telegrinder.bot.rules.abc import ABCRule


# TODO: REMAKE https://github.com/timoniq/telegrinder/issues/317
class GlobalMiddleware(ABCMiddleware):
    def __init__(self) -> None:
        self.filters: set[ABCRule] = set()
        self.source_filters: dict[typing.Any, dict[typing.Any, ABCRule]] = {}

    def pre(self) -> bool:
        return True

    @contextmanager
    def apply_filters(
        self,
        *filters: ABCRule,
        source_filter: tuple[typing.Any, typing.Any, ABCRule] | None = None,
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
