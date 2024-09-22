import typing

from telegrinder.node.base import ComposeError, ContextNode, ScalarNode
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
    from abc import ABCMeta

    String = typing.TypeVar("String", bound=typing.LiteralString)

    class TextLiteralMeta(type):
        def __getitem__(cls, texts: String | tuple[String, ...], /) -> String: ...

    class ABCTextLiteralMeta(TextLiteralMeta, ABCMeta): ...

    class TextLiteral(ContextNode, metaclass=ABCTextLiteralMeta):
        texts: tuple[str, ...]

        def __class_getitem__(cls): ...

        @classmethod
        def compose(cls, text: Text) -> str: ...

else:

    class TextLiteral(ContextNode):
        def __class_getitem__(cls, texts, /):
            return cls(texts=(texts,) if not isinstance(texts, tuple) else texts)

        @classmethod
        def compose(cls, text: Text) -> str:
            if text in cls.texts:
                return text
            raise ComposeError("Text matching failed.")


__all__ = ("Text", "TextInteger", "TextLiteral")
