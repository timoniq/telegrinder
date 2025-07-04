from telegrinder import node
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.bot.rules.node import NodeRule


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
        self.texts = set(texts) if not ignore_case else set(map(str.lower, texts))
        self.ignore_case = ignore_case

    def check(self, text: node.text.Text | node.text.Caption) -> bool:
        return (text if not self.ignore_case else text.lower()) in self.texts


__all__ = ("HasCaption", "HasText", "Text")
