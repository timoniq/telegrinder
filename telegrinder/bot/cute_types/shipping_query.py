from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.types.objects import ShippingQuery


class ShippingQueryCute(BaseCute[ShippingQuery], ShippingQuery, kw_only=True):
    pass


__all__ = ("ShippingQueryCute",)
