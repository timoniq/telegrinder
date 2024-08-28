from telegrinder.bot.cute_types.chat_join_request import ChatJoinRequestCute
from telegrinder.bot.dispatch.view.abc import BaseStateView


class ChatJoinRequestView(BaseStateView[ChatJoinRequestCute]):
    def __init__(self) -> None:
        self.auto_rules = []
        self.handlers = []
        self.middlewares = []
        self.return_manager = None

    def get_state_key(self, event: ChatJoinRequestCute) -> int | None:
        return event.chat_id


__all__ = ("ChatJoinRequestView",)
