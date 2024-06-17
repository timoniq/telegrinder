from .base import ComposeError, ScalarNode
from .message import MessageNode


class Text(ScalarNode, str):
    @classmethod
    async def compose(cls, message: MessageNode) -> "Text":
        if not message.text:
            raise ComposeError("Message has no text")
        return Text(message.text.unwrap())


__all__ = ("Text",)
