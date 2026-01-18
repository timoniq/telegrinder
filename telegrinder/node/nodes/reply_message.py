from nodnod.error import NodeError
from nodnod.interface.scalar import scalar_node

from telegrinder.bot.cute_types.message import MessageCute


@scalar_node
class ReplyMessage:
    @classmethod
    def __compose__(cls, message: MessageCute) -> MessageCute:
        return message.reply_to_message.expect(NodeError("Message doesn't have reply"))


__all__ = ("ReplyMessage",)
