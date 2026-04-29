from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.tools.waiter_machine.hasher import PAID_MEDIA_PURCHASED_FROM_USER
from telegrinder.types.objects import PaidMediaPurchased, User


class PaidMediaPurchasedCute(BaseCute[PaidMediaPurchased], PaidMediaPurchased, kw_only=True):
    @property
    def from_user(self) -> User:
        return self.from_

    def FROM_USER(self, user_id: int | None = None):
        return PAID_MEDIA_PURCHASED_FROM_USER(self.from_user.id if user_id is None else user_id)


__all__ = ("PaidMediaPurchasedCute",)
