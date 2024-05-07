import typing

from telegrinder.bot.cute_types import ChatMemberUpdatedCute
from telegrinder.types.enums import UpdateType

from .abc import BaseStateView

ChatMemberUpdateType: typing.TypeAlias = typing.Literal[
    UpdateType.CHAT_MEMBER,
    UpdateType.MY_CHAT_MEMBER,
]


class ChatMemberView(BaseStateView[ChatMemberUpdatedCute]):
    def __init__(self, *, update_type: ChatMemberUpdateType | None = None) -> None:
        self.auto_rules = []
        self.handlers = []
        self.middlewares = []
        self.return_manager = None
        self.update_type = update_type

    def get_state_key(self, event: ChatMemberUpdatedCute) -> int | None:
        return event.chat_id


__all__ = ("ChatMemberView",)
