from .abc import Message, MessageRule


class IsPrivate(MessageRule):
    async def check(self, message: Message, ctx: dict) -> bool:
        return message.chat.id > 0


class IsChat(MessageRule):
    async def check(self, message: Message, ctx: dict) -> bool:
        return message.chat.id < 0
