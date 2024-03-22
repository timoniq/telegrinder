import abc
import typing

from telegrinder.bot.cute_types import InlineQueryCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.bot.rules.adapter import EventAdapter
from telegrinder.types.enums import ChatType

from .markup import Markup, PatternLike, check_string

InlineQuery: typing.TypeAlias = InlineQueryCute


class InlineQueryRule(ABCRule[InlineQuery], abc.ABC):
    adapter = EventAdapter("inline_query", InlineQuery)

    @abc.abstractmethod
    async def check(self, query: InlineQuery, ctx: Context) -> bool:
        pass


class HasLocation(InlineQueryRule):
    async def check(self, query: InlineQuery, ctx: Context) -> bool:
        return bool(query.location)


class InlineQueryChatType(InlineQueryRule):
    def __init__(self, chat_type: ChatType, /) -> None:
        self.chat_type = chat_type

    async def check(self, query: InlineQuery, ctx: Context) -> bool:
        return query.chat_type.map(lambda x: x == self.chat_type).unwrap_or(False)


class InlineQueryText(InlineQueryRule):
    def __init__(self, texts: str | list[str], *, lower_case: bool = False) -> None:
        self.texts = [
            text.lower() if lower_case else text
            for text in ([texts] if isinstance(texts, str) else texts)
        ]
        self.lower_case = lower_case

    async def check(self, query: InlineQuery, ctx: Context) -> bool:
        return (query.query.lower() if self.lower_case else query.query) in self.texts


class InlineQueryMarkup(InlineQueryRule):
    def __init__(self, patterns: PatternLike | list[PatternLike], /) -> None:
        self.patterns = Markup(patterns).patterns
    
    async def check(self, query: InlineQuery, ctx: Context) -> bool:
        return check_string(self.patterns, query.query, ctx)


__all__ = (
    "HasLocation",
    "InlineQueryRule",
    "InlineQueryText",
    "InlineQueryMarkup",
    "InlineQueryChatType",
)
