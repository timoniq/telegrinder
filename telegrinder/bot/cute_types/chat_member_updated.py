import typing
from datetime import datetime

from fntypes.result import Result

from telegrinder.api.api import API, APIError
from telegrinder.bot.cute_types.base import BaseCute, compose_method_params
from telegrinder.model import get_params
from telegrinder.tools.magic import shortcut
from telegrinder.types.objects import *


async def chat_member_interaction(
    update: BaseCute[typing.Any],
    method_name: str,
    params: dict[str, typing.Any],
) -> Result[typing.Any, APIError]:
    params = compose_method_params(
        get_params(locals()),
        update,
        default_params={"chat_id", "user_id"},
    )
    return await getattr(update.ctx_api, method_name)(**params)


class ChatMemberShortcuts:
    """Shortcut methods for `ChatMemberUpdatedCute`, `ChatJoinRequestCute` objects."""

    @shortcut("ban_chat_member", executor=chat_member_interaction, custom_params={"chat_id", "user_id"})
    async def ban_chat_member(
        self,
        *,
        chat_id: int | str | None = None,
        revoke_messages: bool | None = None,
        until_date: datetime | int | None = None,
        user_id: int | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Shortcut `API.ban_chat_member()`, see the [documentation](https://core.telegram.org/bots/api#banchatmember)

        Use this method to ban a user in a group, a supergroup or a channel. In the case
        of supergroups and channels, the user will not be able to return to the chat
        on their own using invite links, etc., unless unbanned first. The bot must
        be an administrator in the chat for this to work and must have the appropriate
        administrator rights. Returns True on success."""
        ...

    @shortcut("unban_chat_member", executor=chat_member_interaction, custom_params={"chat_id", "user_id"})
    async def unban_chat_member(
        self,
        *,
        chat_id: int | str | None = None,
        only_if_banned: bool | None = None,
        user_id: int | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Shortcut `API.unban_chat_member()`, see the [documentation](https://core.telegram.org/bots/api#unbanchatmember)

        Use this method to unban a previously banned user in a supergroup or channel.
        The user will not return to the group or channel automatically, but will
        be able to join via link, etc. The bot must be an administrator for this to
        work. By default, this method guarantees that after the call the user is
        not a member of the chat, but will be able to join it. So if the user is a member
        of the chat they will also be removed from the chat. If you don't want this,
        use the parameter only_if_banned. Returns True on success."""
        ...

    @shortcut(
        "restrict_chat_member",
        executor=chat_member_interaction,
        custom_params={"chat_id", "user_id"},
    )
    async def restrict_chat_member(
        self,
        *,
        permissions: ChatPermissions,
        chat_id: int | str | None = None,
        until_date: datetime | int | None = None,
        use_independent_chat_permissions: bool | None = None,
        user_id: int | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Shortcut `API.restrict_chat_member()`, see the [documentation](https://core.telegram.org/bots/api#restrictchatmember)

        Use this method to restrict a user in a supergroup. The bot must be an administrator
        in the supergroup for this to work and must have the appropriate administrator
        rights. Pass True for all permissions to lift restrictions from a user.
        Returns True on success."""
        ...

    @shortcut("promote_chat_member", executor=chat_member_interaction, custom_params={"chat_id", "user_id"})
    async def promote_chat_member(
        self,
        *,
        can_change_info: bool | None = None,
        can_delete_messages: bool | None = None,
        can_delete_stories: bool | None = None,
        can_edit_messages: bool | None = None,
        can_edit_stories: bool | None = None,
        can_invite_users: bool | None = None,
        can_manage_chat: bool | None = None,
        can_manage_topics: bool | None = None,
        can_manage_video_chats: bool | None = None,
        can_pin_messages: bool | None = None,
        can_post_messages: bool | None = None,
        can_post_stories: bool | None = None,
        can_promote_members: bool | None = None,
        can_restrict_members: bool | None = None,
        chat_id: int | str | None = None,
        is_anonymous: bool | None = None,
        user_id: int | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Shortcut `API.promote_chat_member()`, see the [documentation](https://core.telegram.org/bots/api#promotechatmember)

        Use this method to promote or demote a user in a supergroup or a channel. The
        bot must be an administrator in the chat for this to work and must have the
        appropriate administrator rights. Pass False for all boolean parameters
        to demote a user. Returns True on success."""
        ...

    @shortcut(
        "set_chat_administrator_custom_title",
        executor=chat_member_interaction,
        custom_params={"chat_id", "user_id"},
    )
    async def set_chat_administrator_custom_title(
        self,
        *,
        custom_title: str,
        chat_id: int | str | None = None,
        user_id: int | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Shortcut `API.set_chat_administrator_custom_title()`, see the [documentation](https://core.telegram.org/bots/api#setchatadministratorcustomtitle)

        Use this method to set a custom title for an administrator in a supergroup
        promoted by the bot. Returns True on success."""
        ...


class ChatMemberUpdatedCute(BaseCute[ChatMemberUpdated], ChatMemberUpdated, ChatMemberShortcuts, kw_only=True):
    api: API

    @property
    def from_user(self) -> User:
        return self.from_

    @property
    def user_id(self) -> int:
        return self.from_user.id


__all__ = (
    "ChatMemberShortcuts",
    "ChatMemberUpdatedCute",
)
