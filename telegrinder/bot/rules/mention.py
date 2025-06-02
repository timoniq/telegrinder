from telegrinder.bot.cute_types.message import MessageCute
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.bot.rules.text import HasText
from telegrinder.types.enums import MessageEntityType


class HasMention(ABCRule, requires=[HasText()]):
    def check(self, message: MessageCute) -> bool:
        entities = message.entities.unwrap_or_none()
        if not entities:
            return False
        return any(entity.type == MessageEntityType.MENTION for entity in entities)


__all__ = ("HasMention",)
