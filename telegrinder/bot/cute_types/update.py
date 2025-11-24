import typing
from functools import cached_property

from kungfu.library.monad.option import Nothing, Some

from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.bot.cute_types.business_connection import BusinessConnectionCute
from telegrinder.bot.cute_types.business_messages_deleted import BusinessMessagesDeletedCute
from telegrinder.bot.cute_types.callback_query import CallbackQueryCute
from telegrinder.bot.cute_types.chat_boost_removed import ChatBoostRemovedCute
from telegrinder.bot.cute_types.chat_boost_updated import ChatBoostUpdatedCute
from telegrinder.bot.cute_types.chat_join_request import ChatJoinRequestCute
from telegrinder.bot.cute_types.chat_member_updated import ChatMemberUpdatedCute
from telegrinder.bot.cute_types.chosen_inline_result import ChosenInlineResultCute
from telegrinder.bot.cute_types.inline_query import InlineQueryCute
from telegrinder.bot.cute_types.message import MessageCute
from telegrinder.bot.cute_types.message_reaction_count_updated import MessageReactionCountUpdatedCute
from telegrinder.bot.cute_types.message_reaction_updated import MessageReactionUpdatedCute
from telegrinder.bot.cute_types.paid_media_purchased import PaidMediaPurchasedCute
from telegrinder.bot.cute_types.poll import PollCute
from telegrinder.bot.cute_types.poll_answer import PollAnswerCute
from telegrinder.bot.cute_types.pre_checkout_query import PreCheckoutQueryCute
from telegrinder.bot.cute_types.shipping_query import ShippingQueryCute
from telegrinder.model import From, field
from telegrinder.msgspec_utils import Option
from telegrinder.types.objects import *


class UpdateCute(BaseCute[Update], Update, kw_only=True):
    """Cute version of the object [Update](https://core.telegram.org/bots/api#update).

    This object represents an incoming "cute" update.
    At most one of the optional parameters can be present in any given cute update.
    """

    message: Option[MessageCute] = field(
        default=...,
        converter=From[MessageCute | None],
    )
    """Optional. New incoming message of any kind - text, photo, sticker, etc."""

    edited_message: Option[MessageCute] = field(
        default=...,
        converter=From[MessageCute | None],
    )
    """Optional. New version of a message that is known to the bot and was edited.
    This update may at times be triggered by changes to message fields that are
    either unavailable or not actively used by your bot."""

    channel_post: Option[MessageCute] = field(
        default=...,
        converter=From[MessageCute | None],
    )
    """Optional. New incoming channel post of any kind - text, photo, sticker,
    etc."""

    edited_channel_post: Option[MessageCute] = field(
        default=...,
        converter=From[MessageCute | None],
    )
    """Optional. New version of a channel post that is known to the bot and was edited.
    This update may at times be triggered by changes to message fields that are
    either unavailable or not actively used by your bot."""

    business_connection: Option[BusinessConnectionCute] = field(
        default=...,
        converter=From["BusinessConnectionCute | None"],
    )
    """Optional. The bot was connected to or disconnected from a business account,
    or a user edited an existing connection with the bot."""

    business_message: Option[MessageCute] = field(
        default=...,
        converter=From[MessageCute | None],
    )
    """Optional. New message from a connected business account."""

    edited_business_message: Option[MessageCute] = field(
        default=...,
        converter=From[MessageCute | None],
    )
    """Optional. New version of a message from a connected business account."""

    deleted_business_messages: Option[BusinessMessagesDeletedCute] = field(
        default=...,
        converter=From["BusinessMessagesDeletedCute | None"],
    )
    """Optional. Messages were deleted from a connected business account."""

    message_reaction: Option[MessageReactionUpdatedCute] = field(
        default=...,
        converter=From["MessageReactionUpdatedCute | None"],
    )
    """Optional. A reaction to a message was changed by a user. The bot must be an
    administrator in the chat and must explicitly specify `message_reaction`
    in the list of allowed_updates to receive these updates. The update isn't
    received for reactions set by bots."""

    message_reaction_count: Option[MessageReactionCountUpdatedCute] = field(
        default=...,
        converter=From["MessageReactionCountUpdatedCute | None"],
    )
    """Optional. Reactions to a message with anonymous reactions were changed.
    The bot must be an administrator in the chat and must explicitly specify
    `message_reaction_count` in the list of allowed_updates to receive these
    updates. The updates are grouped and can be sent with delay up to a few minutes."""

    inline_query: Option[InlineQueryCute] = field(
        default=...,
        converter=From[InlineQueryCute | None],
    )
    """Optional. New incoming inline query."""

    chosen_inline_result: Option[ChosenInlineResultCute] = field(
        default=...,
        converter=From["ChosenInlineResultCute | None"],
    )
    """Optional. The result of an inline query that was chosen by a user and sent
    to their chat partner. Please see our documentation on the feedback collecting
    for details on how to enable these updates for your bot."""

    callback_query: Option[CallbackQueryCute] = field(
        default=...,
        converter=From[CallbackQueryCute | None],
    )
    """Optional. New incoming callback query."""

    shipping_query: Option[ShippingQueryCute] = field(
        default=...,
        converter=From[ShippingQueryCute | None],
    )
    """Optional. New incoming shipping query. Only for invoices with flexible
    price."""

    pre_checkout_query: Option[PreCheckoutQueryCute] = field(
        default=...,
        converter=From[PreCheckoutQueryCute | None],
    )
    """Optional. New incoming pre-checkout query. Contains full information
    about checkout."""

    purchased_paid_media: Option[PaidMediaPurchasedCute] = field(
        default=...,
        converter=From["PaidMediaPurchasedCute | None"],
    )
    """Optional. A user purchased paid media with a non-empty payload sent by the
    bot in a non-channel chat."""

    poll: Option[PollCute] = field(
        default=...,
        converter=From["PollCute | None"],
    )
    """Optional. New poll state. Bots receive only updates about manually stopped
    polls and polls, which are sent by the bot."""

    poll_answer: Option[PollAnswerCute] = field(
        default=...,
        converter=From["PollAnswerCute | None"],
    )
    """Optional. A user changed their answer in a non-anonymous poll. Bots receive
    new votes only in polls that were sent by the bot itself."""

    my_chat_member: Option[ChatMemberUpdatedCute] = field(
        default=...,
        converter=From[ChatMemberUpdatedCute | None],
    )
    """Optional. The bot's chat member status was updated in a chat. For private
    chats, this update is received only when the bot is blocked or unblocked
    by the user."""

    chat_member: Option[ChatMemberUpdatedCute] = field(
        default=...,
        converter=From[ChatMemberUpdatedCute | None],
    )
    """Optional. A chat member's status was updated in a chat. The bot must be an
    administrator in the chat and must explicitly specify `chat_member` in
    the list of allowed_updates to receive these updates."""

    chat_join_request: Option[ChatJoinRequestCute] = field(
        default=...,
        converter=From[ChatJoinRequestCute | None],
    )
    """Optional. A request to join the chat has been sent. The bot must have the can_invite_users
    administrator right in the chat to receive these updates."""

    chat_boost: Option[ChatBoostUpdatedCute] = field(
        default=...,
        converter=From["ChatBoostUpdatedCute | None"],
    )
    """Optional. A chat boost was added or changed. The bot must be an administrator
    in the chat to receive these updates."""

    removed_chat_boost: Option[ChatBoostRemovedCute] = field(
        default=...,
        converter=From["ChatBoostRemovedCute | None"],
    )
    """Optional. A boost was removed from a chat. The bot must be an administrator
    in the chat to receive these updates."""

    @cached_property
    def incoming_update(self) -> BaseCute[typing.Any]:
        return getattr(self, self.update_type.value).unwrap()

    def get_event[T: BaseCute[typing.Any]](self, event_model: type[T], /) -> Option[T]:
        if isinstance(self.incoming_update, event_model):
            return Some(self.incoming_update)
        return Nothing()


__all__ = ("UpdateCute",)
