from telegrinder.bot.dispatch.context import Context
from telegrinder.tools.i18n.base import ABCTranslator

from .abc import ABC, Message, MessageRule, with_caching_translations


class HasText(MessageRule):
    async def check(self, message: Message, ctx: Context) -> bool:
        return bool(message.text)


class TextMessageRule(MessageRule, ABC, requires=[HasText()]):
    pass


class Text(TextMessageRule):
    def __init__(self, texts: str | list[str], *, ignore_case: bool = False) -> None:
        if not isinstance(texts, list):
            texts = [texts]
        self.texts = texts if not ignore_case else list(map(str.lower, texts))
        self.ignore_case = ignore_case

    async def check(self, message: Message, ctx: Context) -> bool:
        text = message.text.unwrap()
        return (text if not self.ignore_case else text.lower()) in self.texts

    @with_caching_translations
    async def translate(self, translator: ABCTranslator) -> "Text":
        return Text(
            texts=[translator.get(text) for text in self.texts],
            ignore_case=self.ignore_case,
        )


__all__ = ("HasText", "Text", "TextMessageRule")
