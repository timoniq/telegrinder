from telegrinder import node
from telegrinder.bot.dispatch.context import Context
from telegrinder.tools.i18n.base import ABCTranslator

from .abc import ABCRule, with_caching_translations
from .node import NodeRule


class HasText(NodeRule):
    def __init__(self) -> None:
        super().__init__(node.text.Text)


class Text(ABCRule):
    def __init__(self, texts: str | list[str], *, ignore_case: bool = False) -> None:
        if not isinstance(texts, list):
            texts = [texts]
        self.texts = texts if not ignore_case else list(map(str.lower, texts))
        self.ignore_case = ignore_case

    async def check(self, text: node.text.Text, ctx: Context) -> bool:
        return (text if not self.ignore_case else text.lower()) in self.texts

    @with_caching_translations
    async def translate(self, translator: ABCTranslator) -> "Text":
        return Text(
            texts=[translator.get(text) for text in self.texts],
            ignore_case=self.ignore_case,
        )


__all__ = ("HasText", "Text")
