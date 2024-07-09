import dataclasses

import typing_extensions as typing

from telegrinder.types.enums import UpdateType

from .abc import ABCView
from .callback_query import CallbackQueryView
from .chat_join_request import ChatJoinRequestView
from .chat_member import ChatMemberView
from .inline_query import InlineQueryView
from .message import MessageView
from .raw import RawEventView

CallbackQueryViewT = typing.TypeVar("CallbackQueryViewT", bound=ABCView, default=CallbackQueryView)
ChatJoinRequestViewT = typing.TypeVar("ChatJoinRequestViewT", bound=ABCView, default=ChatJoinRequestView)
ChatMemberViewT = typing.TypeVar("ChatMemberViewT", bound=ABCView, default=ChatMemberView)
InlineQueryViewT = typing.TypeVar("InlineQueryViewT", bound=ABCView, default=InlineQueryView)
MessageViewT = typing.TypeVar("MessageViewT", bound=ABCView, default=MessageView)
RawEventViewT = typing.TypeVar("RawEventViewT", bound=ABCView, default=RawEventView)


@dataclasses.dataclass(kw_only=True)
class ViewBox(
    typing.Generic[
        CallbackQueryViewT,
        ChatJoinRequestViewT,
        ChatMemberViewT,
        InlineQueryViewT,
        MessageViewT,
        RawEventViewT,
    ],
):
    callback_query: CallbackQueryViewT = dataclasses.field(
        default_factory=lambda: typing.cast(CallbackQueryViewT, CallbackQueryView()),
    )
    chat_join_request: ChatJoinRequestViewT = dataclasses.field(
        default_factory=lambda: typing.cast(ChatJoinRequestViewT, ChatJoinRequestView()),
    )
    chat_member: ChatMemberViewT = dataclasses.field(
        default_factory=lambda: typing.cast(
            ChatMemberViewT, ChatMemberView(update_type=UpdateType.CHAT_MEMBER)
        ),
    )
    my_chat_member: ChatMemberViewT = dataclasses.field(
        default_factory=lambda: typing.cast(
            ChatMemberViewT, ChatMemberView(update_type=UpdateType.MY_CHAT_MEMBER)
        ),
    )
    inline_query: InlineQueryViewT = dataclasses.field(
        default_factory=lambda: typing.cast(InlineQueryViewT, InlineQueryView()),
    )
    message: MessageViewT = dataclasses.field(
        default_factory=lambda: typing.cast(MessageViewT, MessageView(update_type=UpdateType.MESSAGE)),
    )
    business_message: MessageViewT = dataclasses.field(
        default_factory=lambda: typing.cast(
            MessageViewT, MessageView(update_type=UpdateType.BUSINESS_MESSAGE)
        ),
    )
    channel_post: MessageViewT = dataclasses.field(
        default_factory=lambda: typing.cast(MessageViewT, MessageView(update_type=UpdateType.CHANNEL_POST)),
    )
    edited_message: MessageViewT = dataclasses.field(
        default_factory=lambda: typing.cast(MessageViewT, MessageView(update_type=UpdateType.EDITED_MESSAGE)),
    )
    edited_business_message: MessageViewT = dataclasses.field(
        default_factory=lambda: typing.cast(
            MessageViewT,
            MessageView(update_type=UpdateType.EDITED_BUSINESS_MESSAGE),
        ),
    )
    edited_channel_post: MessageViewT = dataclasses.field(
        default_factory=lambda: typing.cast(
            MessageViewT, MessageView(update_type=UpdateType.EDITED_CHANNEL_POST)
        ),
    )
    any_message: MessageViewT = dataclasses.field(
        default_factory=lambda: typing.cast(MessageViewT, MessageView()),
    )
    chat_member_updated: ChatMemberViewT = dataclasses.field(
        default_factory=lambda: typing.cast(ChatMemberViewT, ChatMemberView()),
    )
    raw_event: RawEventViewT = dataclasses.field(
        default_factory=lambda: typing.cast(RawEventViewT, RawEventView()),
    )

    def get_views(self) -> dict[str, ABCView]:
        """Get all views."""

        return {name: view for name, view in self.__dict__.items() if isinstance(view, ABCView)}


__all__ = ("ViewBox",)
