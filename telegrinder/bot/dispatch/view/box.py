from __future__ import annotations

import dataclasses
import typing
from functools import cached_property
from types import MappingProxyType

from telegrinder.bot.dispatch.return_manager.callback_query import CallbackQueryReturnManager
from telegrinder.bot.dispatch.return_manager.inline_query import InlineQueryReturnManager
from telegrinder.bot.dispatch.return_manager.message import MessageReturnManager
from telegrinder.bot.dispatch.return_manager.pre_checkout_query import PreCheckoutQueryReturnManager
from telegrinder.bot.dispatch.view.base import (
    ErrorView,
    EventView,
    RawEventView,
    View,
)
from telegrinder.bot.dispatch.view.media_group import MediaGroupView
from telegrinder.types.enums import UpdateType

if typing.TYPE_CHECKING:
    from telegrinder.bot.dispatch.return_manager.abc import ABCReturnManager

EXCLUDE_VIEW_META: typing.Final = dict(exclude_view=True)


def event_view[T: EventView](
    update_type: UpdateType,
    return_manager: ABCReturnManager | None = None,
    /,
) -> typing.Callable[[], T]:
    def factory() -> T:
        return typing.cast("T", EventView(update_type, return_manager))

    return factory


def view[T: View](
    view_class: type[View],
    return_manager: ABCReturnManager | None = None,
    /,
) -> typing.Callable[[], T]:
    def factory() -> T:
        return typing.cast("T", view_class(return_manager=return_manager))

    return factory


event_model_view = view


@dataclasses.dataclass(kw_only=True)
class EventViewBox[
    MessageView: EventView = EventView,
    EditedMessageView: EventView = EventView,
    ChannelPostView: EventView = EventView,
    EditedChannelPostView: EventView = EventView,
    BusinessConnectionView: EventView = EventView,
    BusinessMessageView: EventView = EventView,
    EditedBusinessMessageView: EventView = EventView,
    DeletedBusinessMessagesView: EventView = EventView,
    MessageReactionView: EventView = EventView,
    MessageReactionCountView: EventView = EventView,
    InlineQueryView: EventView = EventView,
    ChosenInlineResultView: EventView = EventView,
    CallbackQueryView: EventView = EventView,
    ShippingQueryView: EventView = EventView,
    PreCheckoutQueryView: EventView = EventView,
    PurchasedPaidMediaView: EventView = EventView,
    PollView: EventView = EventView,
    PollAnswerView: EventView = EventView,
    MyChatMemberView: EventView = EventView,
    ChatMemberView: EventView = EventView,
    ChatJoinRequestView: EventView = EventView,
    ChatBoostView: EventView = EventView,
    RemovedChatBoostView: EventView = EventView,
]:
    message: MessageView = dataclasses.field(default_factory=event_view(UpdateType.MESSAGE, MessageReturnManager()))
    edited_message: EditedMessageView = dataclasses.field(
        default_factory=event_view(UpdateType.EDITED_MESSAGE, MessageReturnManager())
    )
    channel_post: ChannelPostView = dataclasses.field(
        default_factory=event_view(UpdateType.CHANNEL_POST, MessageReturnManager())
    )
    edited_channel_post: EditedChannelPostView = dataclasses.field(
        default_factory=event_view(UpdateType.EDITED_CHANNEL_POST, MessageReturnManager())
    )
    business_connection: BusinessConnectionView = dataclasses.field(
        default_factory=event_view(UpdateType.BUSINESS_CONNECTION)
    )
    business_message: BusinessMessageView = dataclasses.field(
        default_factory=event_view(UpdateType.BUSINESS_MESSAGE, MessageReturnManager())
    )
    edited_business_message: EditedBusinessMessageView = dataclasses.field(
        default_factory=event_view(UpdateType.EDITED_BUSINESS_MESSAGE, MessageReturnManager())
    )
    deleted_business_messages: DeletedBusinessMessagesView = dataclasses.field(
        default_factory=event_view(UpdateType.DELETED_BUSINESS_MESSAGES)
    )
    message_reaction: MessageReactionView = dataclasses.field(default_factory=event_view(UpdateType.MESSAGE_REACTION))
    message_reaction_count: MessageReactionCountView = dataclasses.field(
        default_factory=event_view(UpdateType.MESSAGE_REACTION_COUNT)
    )
    inline_query: InlineQueryView = dataclasses.field(
        default_factory=event_view(UpdateType.INLINE_QUERY, InlineQueryReturnManager())
    )
    chosen_inline_result: ChosenInlineResultView = dataclasses.field(
        default_factory=event_view(UpdateType.CHOSEN_INLINE_RESULT)
    )
    callback_query: CallbackQueryView = dataclasses.field(
        default_factory=event_view(UpdateType.CALLBACK_QUERY, CallbackQueryReturnManager())
    )
    shipping_query: ShippingQueryView = dataclasses.field(default_factory=event_view(UpdateType.SHIPPING_QUERY))
    pre_checkout_query: PreCheckoutQueryView = dataclasses.field(
        default_factory=event_view(UpdateType.PRE_CHECKOUT_QUERY, PreCheckoutQueryReturnManager())
    )
    purchased_paid_media: PurchasedPaidMediaView = dataclasses.field(
        default_factory=event_view(UpdateType.PURCHASED_PAID_MEDIA)
    )
    poll: PollView = dataclasses.field(default_factory=event_view(UpdateType.POLL))
    poll_answer: PollAnswerView = dataclasses.field(default_factory=event_view(UpdateType.POLL_ANSWER))
    my_chat_member: MyChatMemberView = dataclasses.field(default_factory=event_view(UpdateType.MY_CHAT_MEMBER))
    chat_member: ChatMemberView = dataclasses.field(default_factory=event_view(UpdateType.CHAT_MEMBER))
    chat_join_request: ChatJoinRequestView = dataclasses.field(default_factory=event_view(UpdateType.CHAT_JOIN_REQUEST))
    chat_boost: ChatBoostView = dataclasses.field(default_factory=event_view(UpdateType.CHAT_BOOST))
    removed_chat_boost: RemovedChatBoostView = dataclasses.field(
        default_factory=event_view(UpdateType.REMOVED_CHAT_BOOST)
    )


@dataclasses.dataclass(kw_only=True)
class EventModelViewBox[MediaGroup: View = MediaGroupView]:
    media_group: MediaGroup = dataclasses.field(
        default_factory=event_model_view(MediaGroupView, MessageReturnManager())
    )


@dataclasses.dataclass(kw_only=True)
class ViewBox(EventModelViewBox, EventViewBox):
    error: ErrorView = dataclasses.field(default_factory=view(ErrorView), metadata=EXCLUDE_VIEW_META)
    raw: RawEventView = dataclasses.field(default_factory=view(RawEventView), metadata=EXCLUDE_VIEW_META)

    @cached_property
    def views(self) -> MappingProxyType[str, View]:
        return MappingProxyType(
            mapping={
                field.name: obj
                for field in dataclasses.fields(self)
                if isinstance(obj := getattr(self, field.name), View)
                and field.metadata.get("exclude_view", False) is False
            },
        )


__all__ = ("EventModelViewBox", "EventViewBox", "ViewBox")
