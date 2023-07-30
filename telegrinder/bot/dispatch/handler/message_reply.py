import typing
from telegrinder.bot.cute_types import MessageCute
from telegrinder.api.abc import ABCAPI
from .abc import ABCHandler


class MessageReplyHandler(ABCHandler[MessageCute]):
    def __init__(
        self,
        text: str,
        as_reply: bool = False,
        is_blocking: bool = True,
    ):
        self.text = text
        self.as_reply = as_reply
        self.is_blocking = is_blocking
        self.dataclass = MessageCute

    async def check(self, api, event) -> bool:
        return True

    async def run(self, event: MessageCute) -> typing.Any:
        await event.answer(
            text=self.text,
            reply_to_message_id=(event.message_id if self.as_reply else None),
        )
