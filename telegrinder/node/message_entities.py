from telegrinder.bot.cute_types.message import MessageCute
from telegrinder.node.base import scalar_node
from telegrinder.node.error import ComposeError
from telegrinder.types.objects import MessageEntity


@scalar_node
class MessageEntities:
    @classmethod
    def compose(cls, message: MessageCute) -> list[MessageEntity]:
        return message.entities.expect(ComposeError("Message has no entities."))


__all__ = ("MessageEntities",)
