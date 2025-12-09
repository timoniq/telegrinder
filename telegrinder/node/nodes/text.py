import typing

from nodnod.error import NodeError
from nodnod.interface.generic import generic_node
from nodnod.interface.scalar import scalar_node

from telegrinder.bot.cute_types.message import MessageCute


@scalar_node
class Caption:
    @classmethod
    def __compose__(cls, message: MessageCute) -> str:
        if not message.caption:
            raise NodeError("Message has no caption.")
        return message.caption.unwrap()


@scalar_node
class Text:
    @classmethod
    def __compose__(cls, message: MessageCute) -> str:
        if not message.text:
            raise NodeError("Message has no text.")
        return message.text.unwrap()


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

    @generic_node
    class TextLiteral[*Ts]:
        @classmethod
        def compose(cls, text: Text, texts: tuple[typing.Unpack[Ts]]) -> str:
            if text in cls.texts:
                return text
            raise NodeError("Text mismatched literal.")


__all__ = ("Caption", "Text", "TextInteger", "TextLiteral")
