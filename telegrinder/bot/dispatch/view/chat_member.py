import typing

from telegrinder.bot.dispatch.view.base import BaseView
from telegrinder.types.enums import UpdateType

type ChatMemberUpdateType = typing.Literal[
    UpdateType.CHAT_MEMBER,
    UpdateType.MY_CHAT_MEMBER,
]


class ChatMemberView(BaseView):
    def __init__(self, update_type: ChatMemberUpdateType) -> None:
        super().__init__(update_type)


__all__ = ("ChatMemberView",)
