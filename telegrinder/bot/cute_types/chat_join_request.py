import typing

from fntypes.result import Result

from telegrinder.api.api import API, APIError
from telegrinder.bot.cute_types.base import BaseCute, shortcut
from telegrinder.bot.cute_types.chat_member_updated import ChatMemberShortcuts, chat_member_interaction
from telegrinder.types.objects import *


class ChatJoinRequestCute(BaseCute[ChatJoinRequest], ChatJoinRequest, ChatMemberShortcuts, kw_only=True):
    api: API

    @property
    def from_user(self) -> User:
        return self.from_

    @property
    def user_id(self) -> int:
        return self.from_user.id

    @shortcut(
        "approve_chat_join_request",
        executor=chat_member_interaction,
        custom_params={"chat_id", "user_id"},
    )
    async def approve(
        self,
        chat_id: int | str | None = None,
        user_id: int | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Shortcut `API.approve_chat_join_request()`, see the [documentation](https://core.telegram.org/bots/api#approvechatjoinrequest)

        Use this method to approve a chat join request. The bot must be an administrator
        in the chat for this to work and must have the can_invite_users administrator
        right. Returns True on success."""

        ...

    @shortcut(
        "decline_chat_join_request",
        executor=chat_member_interaction,
        custom_params={"chat_id", "user_id"},
    )
    async def decline(
        self,
        chat_id: int | str | None = None,
        user_id: int | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Shortcut `API.decline_chat_join_request()`, see the [documentation](https://core.telegram.org/bots/api#declinechatjoinrequest)

        Use this method to decline a chat join request. The bot must be an administrator
        in the chat for this to work and must have the can_invite_users administrator
        right. Returns True on success."""

        ...


__all__ = ("ChatJoinRequestCute",)
