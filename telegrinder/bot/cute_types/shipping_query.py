from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.tools.waiter_machine.hasher import SHIPPING_QUERY, SHIPPING_QUERY_FROM_USER
from telegrinder.types.objects import ShippingQuery, User


class ShippingQueryCute(BaseCute[ShippingQuery], ShippingQuery, kw_only=True):
    @property
    def from_user(self) -> User:
        return self.from_

    def QUERY(self, query_id: str | None = None):
        return SHIPPING_QUERY(self.id if query_id is None else query_id)

    def FROM_USER(self, user_id: int | None = None):
        return SHIPPING_QUERY_FROM_USER(self.from_user.id if user_id is None else user_id)


__all__ = ("ShippingQueryCute",)
