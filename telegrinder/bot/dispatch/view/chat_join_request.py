from telegrinder.bot.cute_types.chat_join_request import ChatJoinRequestCute
from telegrinder.bot.dispatch.view.base import BaseStateView


class ChatJoinRequestView(BaseStateView[ChatJoinRequestCute]):
    def __init__(self) -> None:
        self.auto_rules = []
        self.handlers = []
        self.middlewares = []
        self.return_manager = None

    @classmethod
    def get_state_key(cls, event: ChatJoinRequestCute) -> int | None:
        return event.chat_id


__all__ = ("ChatJoinRequestView",)
