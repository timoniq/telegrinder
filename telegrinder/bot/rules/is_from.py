from .abc import ABCMessageRule, Message


class IsPrivate(ABCMessageRule):
    async def check(self, message: Message, ctx: dict) -> bool:
        return message.chat.id > 0


class IsChat(ABCMessageRule):
    async def check(self, message: Message, ctx: dict) -> bool:
        return message.chat.id < 0
