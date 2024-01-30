from telegrinder.bot.cute_types import MessageCute
from telegrinder.bot.dispatch.return_manager import MessageReturnManager

from .abc import BaseStateView


class MessageView(BaseStateView[MessageCute]):
    def __init__(self):
        self.auto_rules = []
        self.handlers = []
        self.middlewares = []
        self.return_manager = MessageReturnManager()

    def get_state_key(self, event: MessageCute) -> int | None:
        return event.chat.id


__all__ = ("MessageView",)
