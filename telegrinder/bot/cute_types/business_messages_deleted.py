from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.types.objects import BusinessMessagesDeleted


class BusinessMessagesDeletedCute(BaseCute[BusinessMessagesDeleted], BusinessMessagesDeleted, kw_only=True):
    pass


__all__ = ("BusinessMessagesDeletedCute",)
