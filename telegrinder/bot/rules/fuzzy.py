import difflib

from telegrinder.bot.dispatch.context import Context

from .abc import Message
from .text import TextMessageRule


class FuzzyText(TextMessageRule):
    def __init__(self, texts: str | list[str], min_ratio: float = 0.7):
        if isinstance(texts, str):
            texts = [texts]
        self.texts = texts
        self.min_ratio = min_ratio

    async def check(self, message: Message, ctx: Context) -> bool:
        match = max(
            difflib.SequenceMatcher(a=message.text.unwrap(), b=text).ratio() for text in self.texts
        )
        if match < self.min_ratio:
            return False
        ctx.fuzzy_ratio = match
        return True


__all__ = ("FuzzyText",)
