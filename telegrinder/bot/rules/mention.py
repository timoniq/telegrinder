from telegrinder.types.enums import MessageEntityType

from .message import Message, MessageRule
from .text import HasText


class HasMention(MessageRule, requires=[HasText()]):
    async def check(self, message: Message) -> bool:
        if not message.entities.unwrap_or_none():
            return False
        return any(entity.type == MessageEntityType.MENTION for entity in message.entities.unwrap())


__all__ = ("HasMention",)
