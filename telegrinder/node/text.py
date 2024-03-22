import typing

from .base import ComposeError, ScalarNode
from .message import MessageNode


class Text(ScalarNode, str):
    @classmethod
    async def compose(cls, message: MessageNode) -> typing.Self:
        return cls(message.text.expect(ComposeError("Message has no text")))


__all__ = ("Text",)
