import dataclasses
import typing

from fntypes.option import Nothing, Option, Some

from telegrinder.api.api import API
from telegrinder.bot.cute_types import ChatJoinRequestCute
from telegrinder.node.base import ComposeError, DataNode, scalar_node
from telegrinder.node.callback_query import CallbackQueryNode
from telegrinder.node.event import EventNode
from telegrinder.node.message import MessageNode
from telegrinder.node.polymorphic import Polymorphic, impl
from telegrinder.node.pre_checkout_query import PreCheckoutQueryNode
from telegrinder.types.objects import Chat, Message, User


@dataclasses.dataclass(kw_only=True, slots=True)
class Source(Polymorphic, DataNode):
    api: API
    from_user: User
    chat: Option[Chat] = dataclasses.field(default_factory=Nothing)
    thread_id: Option[int] = dataclasses.field(default_factory=Nothing)

    @impl
    def compose_message(cls, message: MessageNode) -> typing.Self:
        return cls(
            api=message.ctx_api,
            from_user=message.from_user,
            chat=Some(message.chat),
            thread_id=message.message_thread_id,
        )

    @impl
    def compose_callback_query(cls, callback_query: CallbackQueryNode) -> typing.Self:
        return cls(
            api=callback_query.ctx_api,
            from_user=callback_query.from_user,
            chat=callback_query.chat,
            thread_id=callback_query.message_thread_id,
        )

    @impl
    def compose_chat_join_request(cls, chat_join_request: EventNode[ChatJoinRequestCute]) -> typing.Self:
        return cls(
            api=chat_join_request.ctx_api,
            from_user=chat_join_request.from_user,
            chat=Some(chat_join_request.chat),
            thread_id=Nothing(),
        )

    @impl
    def compose_pre_checkout_query(cls, pre_checkout_query: PreCheckoutQueryNode) -> typing.Self:
        return cls(
            api=pre_checkout_query.ctx_api,
            from_user=pre_checkout_query.from_user,
            chat=Nothing(),
            thread_id=Nothing(),
        )

    async def send(self, text: str, **kwargs: typing.Any) -> Message:
        result = await self.api.send_message(
            chat_id=self.chat.map_or(self.from_user.id, lambda chat: chat.id).unwrap(),
            message_thread_id=self.thread_id.unwrap_or_none(),
            text=text,
            **kwargs,
        )
        return result.unwrap()


@scalar_node()
class ChatSource:
    @classmethod
    def compose(cls, source: Source) -> Chat:
        return source.chat.expect(ComposeError("Source has no chat."))


@scalar_node()
class UserSource:
    @classmethod
    def compose(cls, source: Source) -> User:
        return source.from_user


@scalar_node()
class UserId:
    @classmethod
    def compose(cls, user: UserSource) -> int:
        return user.id


__all__ = ("ChatSource", "Source", "UserId", "UserSource")
