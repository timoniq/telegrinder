from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.types.objects import ChatBoostRemoved


class ChatBoostRemovedCute(BaseCute[ChatBoostRemoved], ChatBoostRemoved, kw_only=True):
    pass


__all__ = ("ChatBoostRemovedCute",)
