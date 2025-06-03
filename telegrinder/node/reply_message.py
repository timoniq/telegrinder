from telegrinder.bot.cute_types.message import MessageCute
from telegrinder.node import ComposeError, scalar_node


@scalar_node
class ReplyMessage:
    @classmethod
    def compose(cls, message: MessageCute) -> MessageCute:
        return message.reply_to_message.expect(ComposeError("Message doesn't have reply"))
    

__all__ = ("ReplyMessage")
