from telegrinder.bot.cute_types.message import MessageCute
from telegrinder.node.base import ComposeError, ScalarNode
from telegrinder.node.update import UpdateNode


class MessageNode(ScalarNode, MessageCute):
    @classmethod
    async def compose(cls, update: UpdateNode) -> MessageCute:
        if not update.message:
            raise ComposeError("Update is not a message.")
        return update.message.unwrap()


__all__ = ("MessageNode",)
