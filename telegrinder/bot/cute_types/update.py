import typing

from fntypes.co import Nothing, Some

from telegrinder.api import ABCAPI
from telegrinder.msgspec_utils import Option
from telegrinder.types import Model, Update

from .base import BaseCute
from .callback_query import CallbackQueryCute
from .chat_join_request import ChatJoinRequestCute
from .chat_member_updated import ChatMemberUpdatedCute
from .inline_query import InlineQueryCute
from .message import MessageCute

ModelT = typing.TypeVar("ModelT", bound=Model)


class UpdateCute(BaseCute[Update], Update, kw_only=True):
    api: ABCAPI

    message: Option[MessageCute] = Nothing()
    """Optional. New incoming message of any kind - text, photo, sticker, etc."""

    edited_message: Option[MessageCute] = Nothing()
    """Optional. New version of a message that is known to the bot and was edited.
    This update may at times be triggered by changes to message fields that are
    either unavailable or not actively used by your bot."""

    channel_post: Option[MessageCute] = Nothing()
    """Optional. New incoming channel post of any kind - text, photo, sticker,
    etc."""

    edited_channel_post: Option[MessageCute] = Nothing()
    """Optional. New version of a channel post that is known to the bot and was edited.
    This update may at times be triggered by changes to message fields that are
    either unavailable or not actively used by your bot."""

    business_message: Option[MessageCute] = Nothing()
    """Optional. New message from a connected business account."""

    edited_business_message: Option[MessageCute] = Nothing()
    """Optional. New version of a message from a connected business account."""

    inline_query: Option[InlineQueryCute] = Nothing()
    """Optional. New incoming inline query."""

    callback_query: Option[CallbackQueryCute] = Nothing()
    """Optional. New incoming callback query."""

    my_chat_member: Option[ChatMemberUpdatedCute] = Nothing()
    """Optional. The bot's chat member status was updated in a chat. For private
    chats, this update is received only when the bot is blocked or unblocked
    by the user."""

    chat_member: Option[ChatMemberUpdatedCute] = Nothing()
    """Optional. A chat member's status was updated in a chat. The bot must be an
    administrator in the chat and must explicitly specify `chat_member` in
    the list of allowed_updates to receive these updates."""

    chat_join_request: Option[ChatJoinRequestCute] = Nothing()
    """Optional. A request to join the chat has been sent. The bot must have the can_invite_users
    administrator right in the chat to receive these updates."""

    @property
    def incoming_update(self) -> Model:
        return getattr(self, self.update_type.value).unwrap()

    def get_event(self, event_model: type[ModelT]) -> Option[ModelT]:
        if isinstance(self.incoming_update, event_model):
            return Some(self.incoming_update)
        return Nothing()


__all__ = ("UpdateCute",)
