from telegrinder.bot.cute_types import InlineQueryCute
from telegrinder.bot.rules.adapter import EventAdapter
from telegrinder.bot.rules.abc import ABCRule
import abc


class InlineQueryRule(ABCRule[InlineQueryCute], abc.ABC):
    adapter = EventAdapter("inline_query", InlineQueryCute)

    @abc.abstractmethod
    async def check(self, query: InlineQueryCute, ctx: dict) -> bool:
        pass


class InlineQueryText(InlineQueryRule):
    def __init__(self, texts: str | list[str]) -> None:
        if isinstance(texts, str):
            texts = [texts]
        self.texts = texts

    async def check(self, query: InlineQueryCute, ctx: dict) -> bool:
        return query.query in self.texts


class LocationInlineQuery(InlineQueryRule):
    async def check(self, query: InlineQueryCute, ctx: dict) -> bool:
        return query.location is not None
