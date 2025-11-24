from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.types.objects import MessageReactionCountUpdated


class MessageReactionCountUpdatedCute(BaseCute[MessageReactionCountUpdated], MessageReactionCountUpdated, kw_only=True):
    pass


__all__ = ("MessageReactionCountUpdatedCute",)
