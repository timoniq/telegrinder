from .abc import ABC, MessageRule, Message
import typing


class HasText(MessageRule):
    async def check(self, message: Message, ctx: dict) -> bool:
        return bool(message.text)


class TextMessageRule(MessageRule, ABC, require=[HasText()]):
    pass


class Text(TextMessageRule):
    def __init__(self, texts: str | list[str], ignore_case: bool = False):
        if not isinstance(texts, list):
            texts = [texts]
        self.texts = texts
        self.ignore_case = ignore_case

    async def check(self, message: Message, ctx: dict) -> bool:
        if self.ignore_case:
            return message.text.lower() in list(map(str.lower, self.texts))
        return message.text in self.texts
