from telegrinder.bot.cute_types.message import MessageCute
from telegrinder.bot.cute_types.utils import MEDIA_TYPES
from telegrinder.bot.rules.abc import ABCRule


class IsMediaGroup(ABCRule):
    def check(self, message: MessageCute) -> bool:
        if not message.media_group_id:
            return False
        return message.content_type in MEDIA_TYPES


__all__ = ("IsMediaGroup",)
