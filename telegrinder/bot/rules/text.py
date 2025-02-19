import typing

from telegrinder import node
from telegrinder.tools.i18n.abc import ABCTranslator

from .abc import ABCRule, with_caching_translations
from .node import NodeRule


class HasText(NodeRule):
    def __init__(self) -> None:
        super().__init__(node.as_node(node.text.Text))


class HasCaption(NodeRule):
    def __init__(self) -> None:
        super().__init__(node.as_node(node.text.Caption))


class Text(ABCRule):
    def __init__(self, texts: str | list[str], /, *, ignore_case: bool = False) -> None:
        if not isinstance(texts, list):
            texts = [texts]
        self.texts = texts if not ignore_case else list(map(str.lower, texts))
        self.ignore_case = ignore_case

    def check(self, text: node.either.Either[node.text.Text, node.text.Caption]) -> bool:
        return (text if not self.ignore_case else text.lower()) in self.texts

    @with_caching_translations
    async def translate(self, translator: ABCTranslator) -> typing.Self:
        return self.__class__(
            [translator.get(text) for text in self.texts],
            ignore_case=self.ignore_case,
        )


__all__ = ("HasCaption", "HasText", "Text")
