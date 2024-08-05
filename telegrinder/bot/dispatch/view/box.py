import dataclasses

import typing_extensions as typing

from telegrinder.bot.dispatch.view import (
    callback_query,
    chat_join_request,
    chat_member,
    inline_query,
    message,
    raw,
)
from telegrinder.bot.dispatch.view.abc import ABCView
from telegrinder.types.enums import UpdateType

CallbackQueryView = typing.TypeVar(
    "CallbackQueryView", bound=ABCView, default=callback_query.CallbackQueryView
)
ChatJoinRequestView = typing.TypeVar(
    "ChatJoinRequestView", bound=ABCView, default=chat_join_request.ChatJoinRequestView
)
ChatMemberView = typing.TypeVar("ChatMemberView", bound=ABCView, default=chat_member.ChatMemberView)
InlineQueryView = typing.TypeVar("InlineQueryView", bound=ABCView, default=inline_query.InlineQueryView)
MessageView = typing.TypeVar("MessageView", bound=ABCView, default=message.MessageView)
RawEventView = typing.TypeVar("RawEventView", bound=ABCView, default=raw.RawEventView)


@dataclasses.dataclass(kw_only=True)
class ViewBox(
    typing.Generic[
        CallbackQueryView,
        ChatJoinRequestView,
        ChatMemberView,
        InlineQueryView,
        MessageView,
        RawEventView,
    ],
):
    callback_query_view: dataclasses.InitVar[CallbackQueryView | None] = None
    chat_join_request_view: dataclasses.InitVar[ChatJoinRequestView | None] = None
    chat_member_view: dataclasses.InitVar[ChatMemberView | None] = None
    my_chat_member_view: dataclasses.InitVar[ChatMemberView | None] = None
    inline_query_view: dataclasses.InitVar[InlineQueryView | None] = None
    message_view: dataclasses.InitVar[MessageView | None] = None
    business_message_view: dataclasses.InitVar[MessageView | None] = None
    channel_post_view: dataclasses.InitVar[MessageView | None] = None
    edited_message_view: dataclasses.InitVar[MessageView | None] = None
    edited_business_message_view: dataclasses.InitVar[MessageView | None] = None
    edited_channel_post_view: dataclasses.InitVar[MessageView | None] = None
    any_message_view: dataclasses.InitVar[MessageView | None] = None
    chat_member_updated_view: dataclasses.InitVar[ChatMemberView | None] = None
    raw_event_view: dataclasses.InitVar[RawEventView | None] = None

    def __post_init__(
        self,
        callback_query_view: CallbackQueryView | None = None,
        chat_join_request_view: ChatJoinRequestView | None = None,
        chat_member_view: ChatMemberView | None = None,
        my_chat_member_view: ChatMemberView | None = None,
        inline_query_view: InlineQueryView | None = None,
        message_view: MessageView | None = None,
        business_message_view: MessageView | None = None,
        channel_post_view: MessageView | None = None,
        edited_message_view: MessageView | None = None,
        edited_business_message_view: MessageView | None = None,
        edited_channel_post_view: MessageView | None = None,
        any_message_view: MessageView | None = None,
        chat_member_updated_view: ChatMemberView | None = None,
        raw_event_view: RawEventView | None = None,
    ) -> None:
        self.callback_query = typing.cast(
            CallbackQueryView,
            callback_query_view or callback_query.CallbackQueryView(),
        )
        self.chat_join_request = typing.cast(
            ChatJoinRequestView,
            chat_join_request_view or chat_join_request.ChatJoinRequestView(),
        )
        self.chat_member = typing.cast(
            ChatMemberView,
            chat_member_view or chat_member.ChatMemberView(update_type=UpdateType.CHAT_MEMBER),
        )
        self.my_chat_member = typing.cast(
            ChatMemberView,
            my_chat_member_view or chat_member.ChatMemberView(update_type=UpdateType.MY_CHAT_MEMBER),
        )
        self.inline_query = typing.cast(
            InlineQueryView,
            inline_query_view or inline_query.InlineQueryView(),
        )
        self.message = typing.cast(
            MessageView,
            message_view or message.MessageView(update_type=UpdateType.MESSAGE),
        )
        self.business_message = typing.cast(
            MessageView,
            business_message_view or message.MessageView(update_type=UpdateType.BUSINESS_MESSAGE),
        )
        self.channel_post = typing.cast(
            MessageView,
            channel_post_view or message.MessageView(update_type=UpdateType.CHANNEL_POST),
        )
        self.edited_message = typing.cast(
            MessageView,
            edited_message_view or message.MessageView(update_type=UpdateType.EDITED_MESSAGE),
        )
        self.edited_business_message = typing.cast(
            MessageView,
            edited_business_message_view
            or message.MessageView(update_type=UpdateType.EDITED_BUSINESS_MESSAGE),
        )
        self.edited_channel_post = typing.cast(
            MessageView,
            edited_channel_post_view or message.MessageView(update_type=UpdateType.EDITED_CHANNEL_POST),
        )
        self.any_message = typing.cast(MessageView, any_message_view or message.MessageView())
        self.chat_member_updated = typing.cast(
            ChatMemberView,
            chat_member_updated_view or chat_member.ChatMemberView(),
        )
        self.raw_event = typing.cast(RawEventView, raw_event_view or raw.RawEventView())

    def get_views(self) -> dict[str, ABCView]:
        """Get all views."""

        return {name: view for name, view in self.__dict__.items() if isinstance(view, ABCView)}


__all__ = ("ViewBox",)
