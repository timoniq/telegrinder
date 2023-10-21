from .text import Message, TextMessageRule


class Integer(TextMessageRule):
    async def check(self, message: Message, ctx: dict) -> bool:
        return message.text.isdigit()


class IntegerInRange(TextMessageRule, requires=[Integer()]):
    def __init__(self, rng: range):
        self.rng = rng

    async def check(self, message: Message, ctx: dict) -> bool:
        return int(message.text) in self.rng
