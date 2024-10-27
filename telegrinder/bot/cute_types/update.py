import typing

from fntypes.co import Nothing, Some

from telegrinder.api.api import API
from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.bot.cute_types.callback_query import CallbackQueryCute
from telegrinder.bot.cute_types.chat_join_request import ChatJoinRequestCute
from telegrinder.bot.cute_types.chat_member_updated import ChatMemberUpdatedCute
from telegrinder.bot.cute_types.inline_query import InlineQueryCute
from telegrinder.bot.cute_types.message import MessageCute
from telegrinder.bot.cute_types.pre_checkout_query import PreCheckoutQueryCute
from telegrinder.model import From, field
from telegrinder.msgspec_utils import Option
from telegrinder.types.objects import *

EventModel = typing.TypeVar("EventModel", bound=Model)


class UpdateCute(BaseCute[Update], Update, kw_only=True):
    api: API

    message: Option[MessageCute] = field(
        default=Nothing(),
        converter=From[MessageCute | None],
    )
    """Optional. New incoming message of any kind - text, photo, sticker, etc."""

    edited_message: Option[MessageCute] = field(
        default=Nothing(),
        converter=From[MessageCute | None],
    )
    """Optional. New version of a message that is known to the bot and was edited.
    This update may at times be triggered by changes to message fields that are
    either unavailable or not actively used by your bot."""

    channel_post: Option[MessageCute] = field(
        default=Nothing(),
        converter=From[MessageCute | None],
    )
    """Optional. New incoming channel post of any kind - text, photo, sticker,
    etc."""

    edited_channel_post: Option[MessageCute] = field(
        default=Nothing(),
        converter=From[MessageCute | None],
    )
    """Optional. New version of a channel post that is known to the bot and was edited.
    This update may at times be triggered by changes to message fields that are
    either unavailable or not actively used by your bot."""

    business_message: Option[MessageCute] = field(
        default=Nothing(),
        converter=From[MessageCute | None],
    )
    """Optional. New message from a connected business account."""

    edited_business_message: Option[MessageCute] = field(
        default=Nothing(),
        converter=From[MessageCute | None],
    )
    """Optional. New version of a message from a connected business account."""

    inline_query: Option[InlineQueryCute] = field(
        default=Nothing(),
        converter=From[InlineQueryCute | None],
    )
    """Optional. New incoming inline query."""

    callback_query: Option[CallbackQueryCute] = field(
        default=Nothing(),
        converter=From[CallbackQueryCute | None],
    )
    """Optional. New incoming callback query."""

    my_chat_member: Option[ChatMemberUpdatedCute] = field(
        default=Nothing(),
        converter=From[ChatMemberUpdatedCute | None],
    )
    """Optional. The bot's chat member status was updated in a chat. For private
    chats, this update is received only when the bot is blocked or unblocked
    by the user."""

    chat_member: Option[ChatMemberUpdatedCute] = field(
        default=Nothing(),
        converter=From[ChatMemberUpdatedCute | None],
    )
    """Optional. A chat member's status was updated in a chat. The bot must be an
    administrator in the chat and must explicitly specify `chat_member` in
    the list of allowed_updates to receive these updates."""

    chat_join_request: Option[ChatJoinRequestCute] = field(
        default=Nothing(),
        converter=From[ChatJoinRequestCute | None],
    )
    """Optional. A request to join the chat has been sent. The bot must have the can_invite_users
    administrator right in the chat to receive these updates."""

    pre_checkout_query: Option[PreCheckoutQueryCute] = field(
        default=Nothing,
        converter=From[PreCheckoutQueryCute | None],
    )
    """Optional. New incoming pre-checkout query. Contains full information
    about checkout."""

    def get_event(self, event_model: type[EventModel]) -> Option[EventModel]:
        if isinstance(self.incoming_update, event_model):
            return Some(self.incoming_update)
        return Nothing()


__all__ = ("UpdateCute",)
