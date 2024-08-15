import typing

from telegrinder.bot.cute_types import ChatMemberUpdatedCute
from telegrinder.bot.dispatch.view.abc import BaseStateView
from telegrinder.types.enums import UpdateType
from telegrinder.types.objects import Update

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

    def __repr__(self) -> str:
        return "<{}: {!r}>".format(
            self.__class__.__name__,
            "chat_member_updated" if self.update_type is None else self.update_type.value,
        )

    def get_state_key(self, event: ChatMemberUpdatedCute) -> int | None:
        return event.chat_id


    async def check(self, event: Update) -> bool:
        return not (
            self.update_type is not None
            and self.update_type != event.update_type
            or not await super().check(event)
        )


__all__ = ("ChatMemberView",)
