from telegrinder.types.enums import MessageEntityType

from .text import Message, TextMessageRule


class HasMention(TextMessageRule):
    async def check(self, message: Message, ctx: dict) -> bool:
        if not message.entities.unwrap_or([]):
            return False
        return any(
            entity.type == MessageEntityType.MENTION
            for entity in message.entities.unwrap()
        )
