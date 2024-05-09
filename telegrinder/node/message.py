import typing

from telegrinder.bot.cute_types import MessageCute

from .base import ComposeError, ScalarNode
from .update import UpdateNode


class MessageNode(ScalarNode, MessageCute):
    @classmethod
    async def compose(cls, update: UpdateNode) -> typing.Self:
        if not update.message:
            raise ComposeError
        return cls(
            **update.message.unwrap().to_dict(),
            api=update.api,
        )


__all__ = ("MessageNode",)
