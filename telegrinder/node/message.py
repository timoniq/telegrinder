from telegrinder.bot.cute_types import MessageCute
from telegrinder.node.base import ComposeError, ScalarNode
from telegrinder.node.update import UpdateNode


class MessageNode(ScalarNode, MessageCute):
    @classmethod
    async def compose(cls, update: UpdateNode) -> "MessageNode":
        if not update.message:
            raise ComposeError
        return MessageNode(
            **update.message.unwrap().to_dict(),
            api=update.api,
        )


__all__ = ("MessageNode",)
