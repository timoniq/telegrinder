import difflib

from telegrinder.bot.dispatch.context import Context
from telegrinder.node.text import Text

from .abc import ABCRule


class FuzzyText(ABCRule):
    def __init__(self, texts: str | list[str], /, min_ratio: float = 0.7) -> None:
        if isinstance(texts, str):
            texts = [texts]
        self.texts = texts
        self.min_ratio = min_ratio

    def check(self, message_text: Text, ctx: Context) -> bool:
        match = max(difflib.SequenceMatcher(a=message_text, b=text).ratio() for text in self.texts)
        if match < self.min_ratio:
            return False
        ctx.fuzzy_ratio = match
        return True


__all__ = ("FuzzyText",)
