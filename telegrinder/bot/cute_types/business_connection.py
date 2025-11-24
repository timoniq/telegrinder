from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.types.objects import BusinessConnection, User


class BusinessConnectionCute(BaseCute[BusinessConnection], BusinessConnection, kw_only=True):
    @property
    def from_user(self) -> User:
        return self.user


__all__ = ("BusinessConnectionCute",)
