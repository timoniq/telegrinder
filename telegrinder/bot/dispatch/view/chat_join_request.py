from telegrinder.bot.cute_types.chat_join_request import ChatJoinRequestCute
from telegrinder.bot.dispatch.view.base import BaseStateView


class ChatJoinRequestView(BaseStateView[ChatJoinRequestCute]):
    @classmethod
    def get_state_key(cls, event: ChatJoinRequestCute) -> int | None:
        return event.chat_id


__all__ = ("ChatJoinRequestView",)
