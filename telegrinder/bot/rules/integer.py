from telegrinder.bot.dispatch.context import Context

from .text import Message, TextMessageRule


class Integer(TextMessageRule):
    async def check(self, message: Message, ctx: Context) -> bool:
        return message.text.unwrap().isdigit()


class IntegerInRange(TextMessageRule, requires=[Integer()]):
    def __init__(self, rng: range):
        self.rng = rng

    async def check(self, message: Message, ctx: Context) -> bool:
        return int(message.text.unwrap()) in self.rng


__all__ = ("Integer", "IntegerInRange")
