from telegrinder.bot.cute_types.message import MessageCute
from telegrinder.node.base import ComposeError, scalar_node
from telegrinder.node.update import UpdateNode


@scalar_node()
class MessageNode:
    @classmethod
    def compose(cls, update: UpdateNode) -> MessageCute:
        if not update.message:
            raise ComposeError("Update is not a message.")
        return update.message.unwrap()


__all__ = ("MessageNode",)
