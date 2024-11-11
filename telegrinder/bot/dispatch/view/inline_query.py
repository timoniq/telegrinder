from telegrinder.bot.cute_types.inline_query import InlineQueryCute
from telegrinder.bot.dispatch.return_manager import InlineQueryReturnManager
from telegrinder.bot.dispatch.view.base import BaseStateView


class InlineQueryView(BaseStateView[InlineQueryCute]):
    def __init__(self) -> None:
        self.auto_rules = []
        self.handlers = []
        self.middlewares = []
        self.return_manager = InlineQueryReturnManager()

    @classmethod
    def get_state_key(cls, event: InlineQueryCute) -> int | None:
        return event.from_user.id


__all__ = ("InlineQueryView",)
