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
    callback_query: CallbackQueryView = dataclasses.field(
        default_factory=lambda: typing.cast(
            CallbackQueryView,
            callback_query.CallbackQueryView(),
        ),
    )
    chat_join_request: ChatJoinRequestView = dataclasses.field(
        default_factory=lambda: typing.cast(
            ChatJoinRequestView,
            chat_join_request.ChatJoinRequestView(),
        ),
    )
    chat_member: ChatMemberView = dataclasses.field(
        default_factory=lambda: typing.cast(
            ChatMemberView,
            chat_member.ChatMemberView(update_type=UpdateType.CHAT_MEMBER),
        ),
    )
    my_chat_member: ChatMemberView = dataclasses.field(
        default_factory=lambda: typing.cast(
            ChatMemberView,
            chat_member.ChatMemberView(update_type=UpdateType.MY_CHAT_MEMBER),
        ),
    )
    inline_query: InlineQueryView = dataclasses.field(
        default_factory=lambda: typing.cast(InlineQueryView, inline_query.InlineQueryView()),
    )
    message: MessageView = dataclasses.field(
        default_factory=lambda: typing.cast(
            MessageView,
            message.MessageView(update_type=UpdateType.MESSAGE),
        ),
    )
    business_message: MessageView = dataclasses.field(
        default_factory=lambda: typing.cast(
            MessageView,
            message.MessageView(update_type=UpdateType.BUSINESS_MESSAGE),
        ),
    )
    channel_post: MessageView = dataclasses.field(
        default_factory=lambda: typing.cast(
            MessageView,
            message.MessageView(update_type=UpdateType.CHANNEL_POST),
        ),
    )
    edited_message: MessageView = dataclasses.field(
        default_factory=lambda: typing.cast(
            MessageView,
            message.MessageView(update_type=UpdateType.EDITED_MESSAGE),
        ),
    )
    edited_business_message: MessageView = dataclasses.field(
        default_factory=lambda: typing.cast(
            MessageView,
            message.MessageView(update_type=UpdateType.EDITED_BUSINESS_MESSAGE),
        ),
    )
    edited_channel_post: MessageView = dataclasses.field(
        default_factory=lambda: typing.cast(
            MessageView,
            message.MessageView(update_type=UpdateType.EDITED_CHANNEL_POST),
        ),
    )
    any_message: MessageView = dataclasses.field(
        default_factory=lambda: typing.cast(MessageView, message.MessageView()),
    )
    chat_member_updated: ChatMemberView = dataclasses.field(
        default_factory=lambda: typing.cast(ChatMemberView, chat_member.ChatMemberView()),
    )
    raw_event: RawEventView = dataclasses.field(
        default_factory=lambda: typing.cast(RawEventView, raw.RawEventView()),
    )

    def get_views(self) -> dict[str, ABCView]:
        """Get all views."""

        return {name: view for name, view in self.__dict__.items() if isinstance(view, ABCView)}


__all__ = ("ViewBox",)
