from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.types.objects import BusinessConnection


class BusinessConnectionCute(BaseCute[BusinessConnection], BusinessConnection, kw_only=True):
    pass


__all__ = ("BusinessConnectionCute",)
