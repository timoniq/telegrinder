from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.tools.waiter_machine.hasher import (
    PAID_MEDIA_PURCHASED,
    PAID_MEDIA_PURCHASED_FOR_PAYLOAD_FROM_USER,
    PAID_MEDIA_PURCHASED_FROM_USER,
)
from telegrinder.types.objects import PaidMediaPurchased, User


class PaidMediaPurchasedCute(BaseCute[PaidMediaPurchased], PaidMediaPurchased, kw_only=True):
    @property
    def from_user(self) -> User:
        return self.from_

    def FROM_USER(self, user_id: int | None = None):
        return PAID_MEDIA_PURCHASED_FROM_USER(self.from_user.id if user_id is None else user_id)

    def PAYLOAD(self, paid_media_payload: str | None = None):
        return PAID_MEDIA_PURCHASED(
            paid_media_payload if paid_media_payload is not None else self.paid_media_payload,
        )

    def FOR_PAYLOAD_FROM_USER(self, paid_media_payload: str | None = None, user_id: int | None = None):
        return PAID_MEDIA_PURCHASED_FOR_PAYLOAD_FROM_USER(
            (
                paid_media_payload if paid_media_payload is not None else self.paid_media_payload,
                user_id if user_id is not None else self.from_user.id,
            ),
        )


__all__ = ("PaidMediaPurchasedCute",)
