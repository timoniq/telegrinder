import typing

from nodnod.error import NodeError
from nodnod.interface.node_constructor import NodeConstructor
from nodnod.interface.scalar import scalar_node

from telegrinder.bot.cute_types.message import MessageCute


@scalar_node
class Caption:
    @classmethod
    def __compose__(cls, message: MessageCute) -> str:
        return message.caption.expect(NodeError("Message has no caption."))


@scalar_node
class Text:
    @classmethod
    def __compose__(cls, message: MessageCute) -> str:
        return message.text.expect(NodeError("Message has no text."))


@scalar_node
class TextInteger:
    @classmethod
    def __compose__(cls, text: Text | Caption) -> int:
        if not text.isdigit():
            raise NodeError("Text is not digit.")
        return int(text)


if typing.TYPE_CHECKING:
    from typing import Literal as TextLiteral

else:

    class TextLiteral(NodeConstructor):
        def __init__(self, *texts: str) -> None:
            self.texts = texts

        def __compose__(self, text: Text | Caption) -> str:
            if text in self.texts:
                return text
            raise NodeError("Text mismatched literal.")


__all__ = ("Caption", "Text", "TextInteger", "TextLiteral")
