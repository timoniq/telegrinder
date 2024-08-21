import dataclasses
import typing

from fntypes.option import Nothing, Option

from telegrinder.api.api import API
from telegrinder.bot.cute_types import ChatJoinRequestCute
from telegrinder.node.base import ComposeError, DataNode, ScalarNode
from telegrinder.node.callback_query import CallbackQueryNode
from telegrinder.node.event import EventNode
from telegrinder.node.message import MessageNode
from telegrinder.node.polymorphic import Polymorphic, impl
from telegrinder.types.objects import Chat, Message, User


@dataclasses.dataclass(kw_only=True, slots=True)
class Source(Polymorphic, DataNode):
    api: API
    chat: Chat
    from_user: User
    thread_id: Option[int] = dataclasses.field(default_factory=lambda: Nothing())

    @impl
    async def compose_message(cls, message: MessageNode) -> typing.Self:
        return cls(
            api=message.ctx_api,
            chat=message.chat,
            from_user=message.from_.expect(ComposeError("MessageNode has no from_user")),
            thread_id=message.message_thread_id,
        )

    @impl
    async def compose_callback_query(cls, callback_query: CallbackQueryNode) -> typing.Self:
        return cls(
            api=callback_query.ctx_api,
            chat=callback_query.chat.expect(ComposeError("CallbackQueryNode has no chat")),
            from_user=callback_query.from_user,
            thread_id=callback_query.message_thread_id,
        )

    @impl
    async def compose_chat_join_request(cls, chat_join_request: EventNode[ChatJoinRequestCute]) -> typing.Self:
        return cls(
            api=chat_join_request.ctx_api,
            chat=chat_join_request.chat,
            from_user=chat_join_request.from_user,
            thread_id=Nothing(),
        )

    async def send(self, text: str) -> Message:
        result = await self.api.send_message(
            chat_id=self.chat.id,
            message_thread_id=self.thread_id.unwrap_or_none(),
            text=text,
        )
        return result.unwrap()


class ChatSource(ScalarNode, Chat):
    @classmethod
    async def compose(cls, source: Source) -> Chat:
        return source.chat


class UserSource(ScalarNode, User):
    @classmethod
    async def compose(cls, source: Source) -> User:
        return source.from_user


__all__ = ("Source", "ChatSource", "UserSource")
