from telegrinder.bot.dispatch.view.base import BaseView
from telegrinder.types.enums import UpdateType


class ChatJoinRequestView(BaseView):
    def __init__(self) -> None:
        super().__init__(UpdateType.CHAT_JOIN_REQUEST)


__all__ = ("ChatJoinRequestView",)
