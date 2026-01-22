from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.types.objects import ChatBoostUpdated


class ChatBoostUpdatedCute(BaseCute[ChatBoostUpdated], ChatBoostUpdated, kw_only=True):
    pass


__all__ = ("ChatBoostUpdatedCute",)
