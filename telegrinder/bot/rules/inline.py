import typing

from telegrinder.bot.cute_types import InlineQueryCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.types.enums import ChatType

from .markup import Markup, PatternLike, check_string

InlineQuery: typing.TypeAlias = InlineQueryCute


class HasLocation(ABCRule):
    def check(self, query: InlineQuery) -> bool:
        return bool(query.location)


class InlineQueryChatType(ABCRule):
    def __init__(self, chat_type: ChatType, /) -> None:
        self.chat_type = chat_type

    def check(self, query: InlineQuery) -> bool:
        return query.chat_type.map(lambda x: x == self.chat_type).unwrap_or(False)


class InlineQueryText(ABCRule):
    def __init__(self, texts: str | list[str], *, lower_case: bool = False) -> None:
        self.texts = {
            text.lower() if lower_case else text for text in ([texts] if isinstance(texts, str) else texts)
        }
        self.lower_case = lower_case

    def check(self, query: InlineQuery) -> bool:
        return (query.query.lower() if self.lower_case else query.query) in self.texts


class InlineQueryMarkup(ABCRule):
    def __init__(self, patterns: PatternLike | list[PatternLike], /) -> None:
        self.patterns = Markup(patterns).patterns

    def check(self, query: InlineQuery, ctx: Context) -> bool:
        return check_string(self.patterns, query.query, ctx)


__all__ = (
    "HasLocation",
    "InlineQueryChatType",
    "InlineQueryMarkup",
    "InlineQueryText",
)
