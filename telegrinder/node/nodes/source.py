import dataclasses
import typing

from kungfu.library.monad.option import Nothing, Option, Some
from nodnod.error import NodeError
from nodnod.interface.polymorphic import case, polymorphic
from nodnod.interface.scalar import scalar_node

from telegrinder.api.api import API
from telegrinder.bot.cute_types import (
    CallbackQueryCute,
    ChatJoinRequestCute,
    ChatMemberUpdatedCute,
    InlineQueryCute,
    MessageCute,
    PreCheckoutQueryCute,
)
from telegrinder.types.objects import Chat, Message, User


@scalar_node
@polymorphic["Source"]
@dataclasses.dataclass(kw_only=True, slots=True)
class Source:
    api: API
    from_user: User
    chat: Option[Chat] = dataclasses.field(default_factory=Nothing)
    thread_id: Option[int] = dataclasses.field(default_factory=Nothing)

    @case
    @classmethod
    def compose_message(cls, message: MessageCute) -> typing.Self:
        return cls(
            api=message.api,
            from_user=message.from_.expect(NodeError("Message is from a channel.")),
            chat=Some(message.chat),
            thread_id=message.message_thread_id,
        )

    @case
    @classmethod
    def compose_callback_query(cls, callback_query: CallbackQueryCute) -> typing.Self:
        return cls(
            api=callback_query.api,
            from_user=callback_query.from_user,
            chat=callback_query.chat,
            thread_id=callback_query.message_thread_id,
        )

    @case
    @classmethod
    def compose_inline_query(cls, inline_query: InlineQueryCute) -> typing.Self:
        return cls(
            api=inline_query.api,
            from_user=inline_query.from_user,
        )

    @case
    @classmethod
    def compose_chat_member_updated(cls, chat_member_updated: ChatMemberUpdatedCute) -> typing.Self:
        return cls(
            api=chat_member_updated.api,
            from_user=chat_member_updated.from_user,
            chat=Some(chat_member_updated.chat),
        )

    @case
    @classmethod
    def compose_chat_join_request(cls, chat_join_request: ChatJoinRequestCute) -> typing.Self:
        return cls(
            api=chat_join_request.api,
            from_user=chat_join_request.from_user,
            chat=Some(chat_join_request.chat),
        )

    @case
    @classmethod
    def compose_pre_checkout_query(cls, pre_checkout_query: PreCheckoutQueryCute) -> typing.Self:
        return cls(
            api=pre_checkout_query.api,
            from_user=pre_checkout_query.from_user,
        )

    async def send(self, text: str, **kwargs: typing.Any) -> Message:
        result = await self.api.send_message(
            chat_id=self.chat.map_or(self.from_user.id, lambda chat: chat.id).unwrap(),
            message_thread_id=self.thread_id.unwrap_or_none(),
            text=text,
            **kwargs,
        )
        return result.unwrap()


@scalar_node
class ChatSource:
    @classmethod
    def __compose__(cls, source: Source) -> Chat:
        return source.chat.expect(NodeError("Source has no chat."))


@scalar_node
class UserSource:
    @classmethod
    def __compose__(cls, source: Source) -> User:
        return source.from_user


@scalar_node
class ChatId:
    @classmethod
    def __compose__(cls, chat: ChatSource) -> int:
        return chat.id


@scalar_node
class UserId:
    @classmethod
    def __compose__(cls, user: UserSource) -> int:
        return user.id


@scalar_node
class Locale:
    @classmethod
    def __compose__(cls, user: UserSource) -> str:
        return user.language_code.expect(NodeError("User has no language code."))


__all__ = (
    "ChatId",
    "ChatSource",
    "Locale",
    "Source",
    "UserId",
    "UserSource",
)
