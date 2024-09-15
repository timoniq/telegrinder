from telegrinder.node.base import ComposeError, ScalarNode
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


__all__ = ("Text", "TextInteger")
