from .base import ScalarNode
from .message import MessageNode


class Text(ScalarNode, str):
    @classmethod
    async def compose(cls, message: MessageNode) -> "Text":
        if not message.text:
            cls.compose_error("Message has no text")
        return Text(message.text.unwrap())
