from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.types.objects import Poll


class PollCute(BaseCute[Poll], Poll, kw_only=True):
    pass


__all__ = ("PollCute",)
