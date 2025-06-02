from telegrinder.bot.rules.abc import ABCRule
from telegrinder.bot.rules.node import NodeRule
from telegrinder.node.base import as_node
from telegrinder.node.text import TextInteger


class IsInteger(NodeRule):
    def __init__(self) -> None:
        super().__init__(as_node(TextInteger))


class IntegerInRange(ABCRule):
    def __init__(self, rng: range) -> None:
        self.rng = rng

    def check(self, integer: TextInteger) -> bool:
        return integer in self.rng


__all__ = ("IntegerInRange", "IsInteger")
