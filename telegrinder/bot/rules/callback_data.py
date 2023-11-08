import abc
import typing
from contextlib import suppress

import msgspec

from telegrinder.bot.cute_types import CallbackQueryCute
from telegrinder.bot.rules.adapter import EventAdapter

from .abc import ABCRule
from .markup import Markup, PatternLike, check_string

CallbackQuery = CallbackQueryCute


class CallbackQueryRule(ABCRule[CallbackQuery], abc.ABC):
    adapter = EventAdapter("callback_query", CallbackQuery)

    @abc.abstractmethod
    async def check(self, event: CallbackQuery, ctx: dict) -> bool:
        pass


class HasData(CallbackQueryRule):
    async def check(self, event: CallbackQuery, ctx: dict) -> bool:
        return bool(event.data)


class CallbackQueryDataRule(CallbackQueryRule, abc.ABC, requires=[HasData()]):
    pass


class CallbackDataEq(CallbackQueryDataRule):
    def __init__(self, value: str):
        self.value = value

    async def check(self, event: CallbackQuery, ctx: dict) -> bool:
        return event.data == self.value


class CallbackDataJsonEq(CallbackQueryDataRule):
    def __init__(self, d: dict[str, typing.Any]):
        self.d = d

    async def check(self, event: CallbackQuery, ctx: dict) -> bool:
        if not event.data:
            return False
        with suppress(BaseException):
            return msgspec.json.decode(event.data, type=dict) == self.d
        return False


class CallbackDataJsonModel(CallbackQueryDataRule):
    def __init__(self, model: typing.Type[msgspec.Struct]):
        self.decoder = msgspec.json.Decoder(type=model)

    async def check(self, event: CallbackQuery, ctx: dict) -> bool:
        with suppress(msgspec.DecodeError):
            ctx["data"] = self.decoder.decode(event.data.encode())
            return True
        return False


class CallbackDataMarkup(CallbackQueryDataRule):
    def __init__(self, patterns: PatternLike | list[PatternLike]):
        self.patterns = Markup(patterns).patterns

    async def check(self, event: CallbackQuery, ctx: dict) -> bool:
        return check_string(self.patterns, event.data, ctx)
