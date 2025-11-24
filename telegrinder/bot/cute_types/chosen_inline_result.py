from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.types.objects import ChosenInlineResult


class ChosenInlineResultCute(BaseCute[ChosenInlineResult], ChosenInlineResult, kw_only=True):
    pass


__all__ = ("ChosenInlineResultCute",)
