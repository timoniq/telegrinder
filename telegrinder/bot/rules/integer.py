from .text import ABCTextMessageRule, Message


class Integer(ABCTextMessageRule):
    async def check(self, message: Message, ctx: dict) -> bool:
        return message.text.isdigit()


class IntegerInRange(ABCTextMessageRule, require=[Integer()]):
    def __init__(self, rng: range):
        self.rng = rng

    async def check(self, message: Message, ctx: dict) -> bool:
        return int(message.text) in self.rng
