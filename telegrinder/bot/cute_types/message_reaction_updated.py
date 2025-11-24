from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.types.objects import MessageReactionUpdated


class MessageReactionUpdatedCute(BaseCute[MessageReactionUpdated], MessageReactionUpdated, kw_only=True):
    pass


__all__ = ("MessageReactionUpdatedCute",)
