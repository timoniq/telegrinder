import typing

from telegrinder.types.objects import Update

from .abc import ABCRule

if typing.TYPE_CHECKING:
    from telegrinder.bot.adapter import ABCAdapter


class IdRule[Identifier](ABCRule[Identifier]):
    def __init__(
        self,
        adapter: "ABCAdapter[Update, Identifier]",
        tracked_identifiers: set[Identifier] | None = None,
    ):
        self.tracked_identifiers = tracked_identifiers or set()
        self.adapter = adapter

    async def check(self, event: Identifier) -> bool:
        return event in self.tracked_identifiers


__all__ = ("IdRule",)
