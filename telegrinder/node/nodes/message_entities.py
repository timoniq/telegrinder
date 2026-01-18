from nodnod.error import NodeError
from nodnod.interface.scalar import scalar_node

from telegrinder.bot.cute_types.message import MessageCute
from telegrinder.types.objects import MessageEntity


@scalar_node
class MessageEntities:
    @classmethod
    def __compose__(cls, message: MessageCute) -> list[MessageEntity]:
        return message.entities.expect(NodeError("Message has no entities."))


__all__ = ("MessageEntities",)
