from .base import ScalarNode
from .message import MessageNode


class Text(ScalarNode, str):
    async def compose(self, message: MessageNode) -> "Text":
        if not message.text:
            self.compose_error("Message has no text")
        return Text(message.text)
