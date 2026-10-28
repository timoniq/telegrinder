from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.tools.waiter_machine.hasher import POLL
from telegrinder.types.objects import Poll


class PollCute(BaseCute[Poll], Poll, kw_only=True):
    def POLL(self, poll_id: str | None = None):
        return POLL(self.id if poll_id is None else poll_id)


__all__ = ("PollCute",)
