from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.types.objects import PollAnswer


class PollAnswerCute(BaseCute[PollAnswer], PollAnswer, kw_only=True):
    pass


__all__ = ("PollAnswerCute",)
