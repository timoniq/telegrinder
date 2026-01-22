from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.types.objects import ShippingQuery, User


class ShippingQueryCute(BaseCute[ShippingQuery], ShippingQuery, kw_only=True):
    @property
    def from_user(self) -> User:
        return self.from_


__all__ = ("ShippingQueryCute",)
