from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.types.objects import BotSubscriptionUpdated, User


class BotSubscriptionUpdatedCute(BaseCute[BotSubscriptionUpdated], BotSubscriptionUpdated, kw_only=True):
    @property
    def from_user(self) -> User:
        return self.user


__all__ = ("BotSubscriptionUpdatedCute",)
