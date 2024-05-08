import dataclasses
import typing

from telegrinder.api import API
from telegrinder.types import Chat, Message

from .base import DataNode
from .message import MessageNode


@dataclasses.dataclass
class Source(DataNode):
    api: API
    chat: Chat
    thread_id: int | None = None

    @classmethod
    async def compose(cls, message: MessageNode) -> typing.Self:
        return cls(
            api=message.ctx_api,
            chat=message.chat,
            thread_id=message.message_thread_id.unwrap_or_none(),
        )

    async def send(self, text: str) -> Message:
        result = await self.api.send_message(
            chat_id=self.chat.id,
            message_thread_id=self.thread_id,
            text=text,
        )
        return result.unwrap()


__all__ = ("Source",)
