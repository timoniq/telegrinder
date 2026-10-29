from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.tools.magic.descriptors import magic_property
from telegrinder.tools.waiter_machine.hasher import (
    BOT_SUBSCRIPTION,
    BOT_SUBSCRIPTION_FOR_PAYLOAD_FROM_USER,
    BOT_SUBSCRIPTION_FROM_USER,
)
from telegrinder.types.objects import BotSubscriptionUpdated, User


class BotSubscriptionUpdatedCute(BaseCute[BotSubscriptionUpdated], BotSubscriptionUpdated, kw_only=True):
    @magic_property
    def from_user(self) -> User:
        return self.user

    def SUBSCRIPTION(self, invoice_payload: str | None = None):
        return BOT_SUBSCRIPTION(self.invoice_payload if invoice_payload is None else invoice_payload)

    def FROM_USER(self, user_id: int | None = None):
        return BOT_SUBSCRIPTION_FROM_USER(self.user.id if user_id is None else user_id)

    def FOR_PAYLOAD_FROM_USER(self, invoice_payload: str | None = None, user_id: int | None = None):
        return BOT_SUBSCRIPTION_FOR_PAYLOAD_FROM_USER(
            (
                self.invoice_payload if invoice_payload is None else invoice_payload,
                self.user.id if user_id is None else user_id,
            ),
        )


__all__ = ("BotSubscriptionUpdatedCute",)
