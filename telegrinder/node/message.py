from telegrinder.bot.cute_types import MessageCute

from .base import ScalarNode
from .update import UpdateNode


class MessageNode(ScalarNode, MessageCute):
    @classmethod
    async def compose(cls, update: UpdateNode) -> "MessageCute":
        if not update.message:
            return cls.compose_error()
        return MessageCute(
            **update.message.unwrap().to_dict(), 
            api=update.api,  # type: ignore
        )

