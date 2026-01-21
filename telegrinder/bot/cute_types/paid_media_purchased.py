from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.types.objects import PaidMediaPurchased, User


class PaidMediaPurchasedCute(BaseCute[PaidMediaPurchased], PaidMediaPurchased, kw_only=True):
    @property
    def from_user(self) -> User:
        return self.from_


__all__ = ("PaidMediaPurchasedCute",)
