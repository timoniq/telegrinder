from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.types.objects import ChosenInlineResult, User


class ChosenInlineResultCute(BaseCute[ChosenInlineResult], ChosenInlineResult, kw_only=True):
    @property
    def from_user(self) -> User:
        return self.from_


__all__ = ("ChosenInlineResultCute",)
