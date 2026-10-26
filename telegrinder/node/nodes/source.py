import dataclasses
import typing

from kungfu.library.monad.option import Nothing, Option, Some
from nodnod.error import NodeError
from nodnod.interface.polymorphic import case, polymorphic
from nodnod.interface.scalar import scalar_node

from telegrinder.api.api import API
from telegrinder.bot.cute_types import (
    BotSubscriptionUpdatedCute,
    BusinessConnectionCute,
    BusinessMessagesDeletedCute,
    CallbackQueryCute,
    ChatJoinRequestCute,
    ChatMemberUpdatedCute,
    ChosenInlineResultCute,
    InlineQueryCute,
    ManagedBotUpdatedCute,
    MessageCute,
    MessageGenerationStoppedCute,
    MessageReactionCountUpdatedCute,
    MessageReactionUpdatedCute,
    PaidMediaPurchasedCute,
    PollAnswerCute,
    PreCheckoutQueryCute,
    ShippingQueryCute,
)
from telegrinder.types.objects import Chat, Message, User


@scalar_node
@polymorphic["Source"]
@dataclasses.dataclass(kw_only=True)
class Source:
    api: API
    from_: Option[User] = dataclasses.field(default_factory=Nothing)
    chat: Option[Chat] = dataclasses.field(default_factory=Nothing)
    thread_id: Option[int] = dataclasses.field(default_factory=Nothing)

    @property
    def from_user(self) -> User:
        return self.from_.unwrap()

    @case
    def compose_message(cls, message: MessageCute) -> typing.Self:
        return cls(
            api=message.api,
            from_=message.from_,
            chat=Some(message.chat),
            thread_id=message.message_thread_id,
        )

    @case
    def compose_callback_query(cls, callback_query: CallbackQueryCute) -> typing.Self:
        return cls(
            api=callback_query.api,
            from_=Some(callback_query.from_user),
            chat=callback_query.chat,
            thread_id=callback_query.message_thread_id,
        )

    @case
    def compose_inline_query(cls, inline_query: InlineQueryCute) -> typing.Self:
        return cls(
            api=inline_query.api,
            from_=Some(inline_query.from_user),
        )

    @case
    def compose_chosen_inline_result(cls, chosen_inline_result: ChosenInlineResultCute) -> typing.Self:
        return cls(
            api=chosen_inline_result.api,
            from_=Some(chosen_inline_result.from_user),
        )

    @case
    def compose_chat_member_updated(cls, chat_member_updated: ChatMemberUpdatedCute) -> typing.Self:
        return cls(
            api=chat_member_updated.api,
            from_=Some(chat_member_updated.from_user),
            chat=Some(chat_member_updated.chat),
        )

    @case
    def compose_chat_join_request(cls, chat_join_request: ChatJoinRequestCute) -> typing.Self:
        return cls(
            api=chat_join_request.api,
            from_=Some(chat_join_request.from_user),
            chat=Some(chat_join_request.chat),
        )

    @case
    def compose_pre_checkout_query(cls, pre_checkout_query: PreCheckoutQueryCute) -> typing.Self:
        return cls(
            api=pre_checkout_query.api,
            from_=Some(pre_checkout_query.from_user),
        )

    @case
    def compose_message_reaction_updated(cls, message_reaction_updated: MessageReactionUpdatedCute) -> typing.Self:
        return cls(
            api=message_reaction_updated.api,
            from_=message_reaction_updated.user,
            chat=Some(message_reaction_updated.chat),
        )

    @case
    def compose_message_reaction_count_updated(
        cls,
        message_reaction_count_updated: MessageReactionCountUpdatedCute,
    ) -> typing.Self:
        return cls(
            api=message_reaction_count_updated.api,
            chat=Some(message_reaction_count_updated.chat),
        )

    @case
    def compose_paid_media_purchased(cls, paid_media_purchased: PaidMediaPurchasedCute) -> typing.Self:
        return cls(
            api=paid_media_purchased.api,
            from_=Some(paid_media_purchased.from_user),
        )

    @case
    def compose_poll_answer(cls, poll_answer: PollAnswerCute) -> typing.Self:
        return cls(
            api=poll_answer.api,
            from_=poll_answer.user,
            chat=poll_answer.voter_chat,
        )

    @case
    def compose_shipping_query(cls, shipping_query: ShippingQueryCute) -> typing.Self:
        return cls(
            api=shipping_query.api,
            from_=Some(shipping_query.from_user),
        )

    @case
    def compose_managed_bot_updated(cls, managed_bot: ManagedBotUpdatedCute) -> typing.Self:
        return cls(
            api=managed_bot.api,
            from_=Some(managed_bot.from_user),
        )

    @case
    def compose_business_messages_deleted(cls, business_messages_deleted: BusinessMessagesDeletedCute) -> typing.Self:
        return cls(
            api=business_messages_deleted.api,
            chat=Some(business_messages_deleted.chat),
        )

    @case
    def compose_business_connection(cls, business_connection: BusinessConnectionCute) -> typing.Self:
        return cls(
            api=business_connection.api,
            from_=Some(business_connection.user),
        )

    @case
    def compose_subscription(cls, subscrption: BotSubscriptionUpdatedCute) -> typing.Self:
        return cls(
            api=subscrption.api,
            from_=Some(subscrption.from_user),
        )

    @case
    def compose_generation_stopped(cls, generation_stopped: MessageGenerationStoppedCute) -> typing.Self:
        return cls(
            api=generation_stopped.api,
            chat=Some(generation_stopped.chat),
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
        return source.from_.expect(NodeError("Source has no user."))


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
