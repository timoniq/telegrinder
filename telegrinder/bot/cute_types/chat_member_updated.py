import typing
from datetime import datetime

from fntypes.result import Result

from telegrinder.api import ABCAPI, APIError
from telegrinder.model import get_params
from telegrinder.types.objects import ChatMemberUpdated, ChatPermissions, User

from .base import BaseCute, compose_method_params, shortcut
from .utils import compose_chat_permissions


async def chat_member_interaction(
    update: BaseCute[typing.Any],
    method_name: str,
    params: dict[str, typing.Any],
) -> Result[typing.Any, APIError]:
    if isinstance(params.get("permissions"), dict):
        params["permissions"] = compose_chat_permissions(**params["permissions"])
    params = compose_method_params(
        get_params(locals()),
        update,
        default_params={"chat_id", "user_id"},
    )
    return await getattr(update.ctx_api, method_name)(**params)


class ChatMemberShortcuts:
    """Shortcut methods for `ChatMemberUpdatedCute`, `ChatJoinRequestCute` objects."""

    @shortcut("ban_chat_member", executor=chat_member_interaction)
    async def ban_chat_member(
        self,
        chat_id: int | str | None = None,
        user_id: int | None = None,
        until_date: datetime | int | None = None,
        revoke_messages: bool | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Shortcut `API.ban_chat_member()`, see the [documentation](https://core.telegram.org/bots/api#banchatmember)

        Use this method to ban a user in a group, a supergroup or a channel. In the case 
        of supergroups and channels, the user will not be able to return to the chat 
        on their own using invite links, etc., unless unbanned first. The bot must 
        be an administrator in the chat for this to work and must have the appropriate 
        administrator rights. Returns True on success.

        :param chat_id: Unique identifier for the target group or username of the target supergroup \
        or channel (in the format @channelusername).

        :param user_id: Unique identifier of the target user.

        :param until_date: Date when the user will be unbanned; Unix time. If user is banned for more \
        than 366 days or less than 30 seconds from the current time they are considered \
        to be banned forever. Applied for supergroups and channels only.

        :param revoke_messages: Pass True to delete all messages from the chat for the user that is being removed. \
        If False, the user will be able to see messages in the group that were sent \
        before the user was removed. Always True for supergroups and channels. \
        """

        ...

    @shortcut("unban_chat_member", executor=chat_member_interaction)
    async def unban_chat_member(
        self,
        chat_id: int | str | None = None,
        user_id: int | None = None,
        only_if_banned: bool | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Shortcut `API.unban_chat_member()`, see the [documentation](https://core.telegram.org/bots/api#unbanchatmember)

        Use this method to unban a previously banned user in a supergroup or channel. 
        The user will not return to the group or channel automatically, but will 
        be able to join via link, etc. The bot must be an administrator for this to 
        work. By default, this method guarantees that after the call the user is 
        not a member of the chat, but will be able to join it. So if the user is a member 
        of the chat they will also be removed from the chat. If you don't want this, 
        use the parameter only_if_banned. Returns True on success.

        :param chat_id: Unique identifier for the target group or username of the target supergroup \
        or channel (in the format @channelusername).

        :param user_id: Unique identifier of the target user.

        :param only_if_banned: Do nothing if the user is not banned.
        """

        ...

    @shortcut(
        "restrict_chat_member",
        executor=chat_member_interaction,
        custom_params={"permissions"},
    )
    async def restrict_chat_member(
        self,
        permissions: ChatPermissions | dict[str, typing.Any],
        chat_id: int | str | None = None,
        user_id: int | None = None,
        use_independent_chat_permissions: bool | None = None,
        until_date: datetime | int | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Shortcut `API.restrict_chat_member()`, see the [documentation](https://core.telegram.org/bots/api#restrictchatmember)

        Use this method to restrict a user in a supergroup. The bot must be an administrator 
        in the supergroup for this to work and must have the appropriate administrator 
        rights. Pass True for all permissions to lift restrictions from a user. 
        Returns True on success.

        :param chat_id: Unique identifier for the target chat or username of the target supergroup \
        (in the format @supergroupusername).

        :param user_id: Unique identifier of the target user.

        :param permissions: A JSON-serialized object for new user permissions.

        :param use_independent_chat_permissions: Pass True if chat permissions are set independently. Otherwise, the can_send_other_messages \
        and can_add_web_page_previews permissions will imply the can_send_messages, \
        can_send_audios, can_send_documents, can_send_photos, can_send_videos, \
        can_send_video_notes, and can_send_voice_notes permissions; the can_send_polls \
        permission will imply the can_send_messages permission.

        :param until_date: Date when restrictions will be lifted for the user; Unix time. If user is \
        restricted for more than 366 days or less than 30 seconds from the current \
        time, they are considered to be restricted forever.
        """

        ...

    @shortcut("promote_chat_member", executor=chat_member_interaction)
    async def promote_chat_member(
        self,
        chat_id: int | str | None = None,
        user_id: int | None = None,
        is_anonymous: bool | None = None,
        can_manage_chat: bool | None = None,
        can_delete_messages: bool | None = None,
        can_manage_video_chats: bool | None = None,
        can_restrict_members: bool | None = None,
        can_promote_members: bool | None = None,
        can_change_info: bool | None = None,
        can_invite_users: bool | None = None,
        can_post_stories: bool | None = None,
        can_edit_stories: bool | None = None,
        can_delete_stories: bool | None = None,
        can_post_messages: bool | None = None,
        can_edit_messages: bool | None = None,
        can_pin_messages: bool | None = None,
        can_manage_topics: bool | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Shortcut `API.promote_chat_member()`, see the [documentation](https://core.telegram.org/bots/api#promotechatmember)

        Use this method to promote or demote a user in a supergroup or a channel. The 
        bot must be an administrator in the chat for this to work and must have the 
        appropriate administrator rights. Pass False for all boolean parameters 
        to demote a user. Returns True on success.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param user_id: Unique identifier of the target user.

        :param is_anonymous: Pass True if the administrator's presence in the chat is hidden.

        :param can_manage_chat: Pass True if the administrator can access the chat event log, get boost list, \
        see hidden supergroup and channel members, report spam messages and ignore \
        slow mode. Implied by any other administrator privilege.

        :param can_delete_messages: Pass True if the administrator can delete messages of other users.

        :param can_manage_video_chats: Pass True if the administrator can manage video chats.

        :param can_restrict_members: Pass True if the administrator can restrict, ban or unban chat members, \
        or access supergroup statistics.

        :param can_promote_members: Pass True if the administrator can add new administrators with a subset \
        of their own privileges or demote administrators that they have promoted, \
        directly or indirectly (promoted by administrators that were appointed \
        by him).

        :param can_change_info: Pass True if the administrator can change chat title, photo and other settings. \

        :param can_invite_users: Pass True if the administrator can invite new users to the chat.

        :param can_post_stories: Pass True if the administrator can post stories to the chat.

        :param can_edit_stories: Pass True if the administrator can edit stories posted by other users.

        :param can_delete_stories: Pass True if the administrator can delete stories posted by other users. \

        :param can_post_messages: Pass True if the administrator can post messages in the channel, or access \
        channel statistics; for channels only.

        :param can_edit_messages: Pass True if the administrator can edit messages of other users and can pin \
        messages; for channels only.

        :param can_pin_messages: Pass True if the administrator can pin messages; for supergroups only. \

        :param can_manage_topics: Pass True if the user is allowed to create, rename, close, and reopen forum \
        topics; for supergroups only.
        """

        ...

    @shortcut("set_chat_administrator_custom_title", executor=chat_member_interaction)
    async def set_chat_administrator_custom_title(
        self,
        custom_title: str,
        chat_id: int | str | None = None,
        user_id: int | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Shortcut `API.set_chat_administrator_custom_title()`, see the [documentation](https://core.telegram.org/bots/api#setchatadministratorcustomtitle)

        Use this method to set a custom title for an administrator in a supergroup 
        promoted by the bot. Returns True on success.

        :param chat_id: Unique identifier for the target chat or username of the target supergroup \
        (in the format @supergroupusername).

        :param user_id: Unique identifier of the target user.

        :param custom_title: New custom title for the administrator; 0-16 characters, emoji are not \
        allowed.
        """

        ...


class ChatMemberUpdatedCute(BaseCute[ChatMemberUpdated], ChatMemberUpdated, ChatMemberShortcuts, kw_only=True):
    api: ABCAPI

    @property
    def from_user(self) -> User:
        return self.from_

    @property
    def user_id(self) -> int:
        return self.from_user.id
