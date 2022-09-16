from .abc import Message
from .text import ABCTextMessageRule
import difflib
import typing


class FuzzyText(ABCTextMessageRule):
    def __init__(
        self,
        texts: typing.Union[str, typing.List[str]],
        min_ratio: float = 0.7
    ):
        if isinstance(texts, str):
            texts = [texts]
        self.texts = texts
        self.min_ratio = min_ratio

    async def check(self, message: Message, ctx: dict) -> bool:
        match = max(
            difflib.SequenceMatcher(
                a=message.text,
                b=text
            ).ratio()
            for text in self.texts
        )
        if match < self.min_ratio:
            return False
        ctx["fuzzy_ratio"] = match
        return True

