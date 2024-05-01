from telegrinder.bot.cute_types import InlineQueryCute
from telegrinder.bot.dispatch.return_manager import InlineQueryReturnManager

from .abc import BaseStateView


class InlineQueryView(BaseStateView[InlineQueryCute]):
    def __init__(self) -> None:
        self.auto_rules = []
        self.handlers = []
        self.middlewares = []
        self.return_manager = InlineQueryReturnManager()

    def get_state_key(self, event: InlineQueryCute) -> int | None:
        return event.from_user.id


__all__ = ("InlineQueryView",)
