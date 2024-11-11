from telegrinder.bot.cute_types.callback_query import CallbackQueryCute
from telegrinder.bot.dispatch.return_manager.callback_query import CallbackQueryReturnManager
from telegrinder.bot.dispatch.view.base import BaseStateView


class CallbackQueryView(BaseStateView[CallbackQueryCute]):
    def __init__(self) -> None:
        self.auto_rules = []
        self.handlers = []
        self.middlewares = []
        self.return_manager = CallbackQueryReturnManager()

    @classmethod
    def get_state_key(cls, event: CallbackQueryCute) -> int | None:
        return event.message_id.unwrap_or_none()


__all__ = ("CallbackQueryView",)
