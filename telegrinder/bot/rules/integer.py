from telegrinder.bot.dispatch.context import Context
from telegrinder.node.text import TextInteger

from .abc import ABCRule
from .node import NodeRule


class IsInteger(NodeRule):
    def __init__(self) -> None:
        super().__init__(TextInteger)


class IntegerInRange(ABCRule):
    def __init__(self, rng: range):
        self.rng = rng

    async def check(self, integer: TextInteger, ctx: Context) -> bool:
        return integer in self.rng


__all__ = ("IsInteger", "IntegerInRange")
