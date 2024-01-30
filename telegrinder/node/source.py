import dataclasses
import typing

from telegrinder.api import API
from telegrinder.option.msgspec_option import Option
from telegrinder.option.option import Nothing
from telegrinder.types import Chat, Message

from .base import DataNode
from .message import MessageNode


@dataclasses.dataclass
class Source(DataNode):
    api: API
    chat: Chat
    thread_id: Option[int] = dataclasses.field(default_factory=lambda: Nothing)

    @classmethod
    async def compose(cls, message: MessageNode) -> typing.Self:
        return cls(
            api=message.ctx_api,
            chat=message.chat,
            thread_id=message.message_thread_id,
        )
    
    async def send(self, text: str) -> Message:
        result = await self.api.send_message(self.chat.id, message_thread_id=self.thread_id, text=text)
        return result.unwrap()


__all__ = ("Source",)
