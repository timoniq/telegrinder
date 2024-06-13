import dataclasses
import typing

from fntypes import Nothing, Option

from telegrinder.api import API
from telegrinder.types import Chat, Message

from .base import ComposeError, DataNode
from .callback_query import CallbackQueryNode
from .message import MessageNode
from .polymorphic import Polymorphic, impl


@dataclasses.dataclass
class Source(Polymorphic, DataNode):
    api: API
    chat: Chat
    thread_id: Option[int] = dataclasses.field(default_factory=Nothing)

    @impl
    async def compose_message(cls, message: MessageNode) -> typing.Self:
        return cls(
            api=message.ctx_api,
            chat=message.chat,
            thread_id=message.message_thread_id,
        )
    
    @impl
    async def compose_callback_query(cls, callback_query: CallbackQueryNode) -> typing.Self:
        return cls(
            api=callback_query.ctx_api,
            chat=callback_query.message.expect(ComposeError).only(Message).expect(ComposeError).chat,
            thread_id=callback_query.message_thread_id,
        )

    async def send(self, text: str) -> Message:
        result = await self.api.send_message(
            chat_id=self.chat.id,
            message_thread_id=self.thread_id.unwrap_or_none(),
            text=text,
        )
        return result.unwrap()


__all__ = ("Source",)
