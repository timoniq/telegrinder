import typing

from telegrinder.node.base import ComposeError, FactoryNode, ScalarNode
from telegrinder.node.message import MessageNode


class Text(ScalarNode, str):
    @classmethod
    def compose(cls, message: MessageNode) -> str:
        if not message.text:
            raise ComposeError("Message has no text.")
        return message.text.unwrap()


class TextInteger(ScalarNode, int):
    @classmethod
    def compose(cls, text: Text) -> int:
        if not text.isdigit():
            raise ComposeError("Text is not digit.")
        return int(text)


if typing.TYPE_CHECKING:
    from typing import Literal as TextLiteral

else:

    class TextLiteral(FactoryNode):
        texts: tuple[str, ...]

        def __class_getitem__(cls, texts, /):
            return cls(texts=(texts,) if not isinstance(texts, tuple) else texts)

        @classmethod
        def compose(cls, text: Text) -> str:
            if text in cls.texts:
                return text
            raise ComposeError("Text mismatched literal.")


__all__ = ("Text", "TextInteger", "TextLiteral")
