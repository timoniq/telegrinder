from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.types.objects import PaidMediaPurchased


class PaidMediaPurchasedCute(BaseCute[PaidMediaPurchased], PaidMediaPurchased, kw_only=True):
    pass


__all__ = ("PaidMediaPurchasedCute",)
