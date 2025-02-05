import typing

from telegrinder.node.base import ComposeError, FactoryNode, scalar_node
from telegrinder.node.either import Either
from telegrinder.node.message import MessageNode


@scalar_node()
class Caption:
    @classmethod
    def compose(cls, message: MessageNode) -> str:
        if not message.caption:
            raise ComposeError("Message has no caption.")
        return message.caption.unwrap()


@scalar_node()
class Text:
    @classmethod
    def compose(cls, message: MessageNode) -> str:
        if not message.text:
            raise ComposeError("Message has no text.")
        return message.text.unwrap()


@scalar_node()
class TextInteger:
    @classmethod
    def compose(cls, text: Either[Text, Caption]) -> int:
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


__all__ = ("Caption", "Text", "TextInteger", "TextLiteral")
