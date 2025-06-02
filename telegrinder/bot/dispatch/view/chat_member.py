import typing

from telegrinder.bot.dispatch.view.base import BaseView
from telegrinder.types.enums import UpdateType

ChatMemberUpdateType: typing.TypeAlias = typing.Literal[
    UpdateType.CHAT_MEMBER,
    UpdateType.MY_CHAT_MEMBER,
]


class ChatMemberView(BaseView):
    def __init__(self, *, update_type: ChatMemberUpdateType) -> None:
        super().__init__(update_type)

    def __repr__(self) -> str:
        return "<{}>".format(type(self).__name__)


__all__ = ("ChatMemberView",)
