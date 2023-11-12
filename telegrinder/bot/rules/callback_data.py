import abc
import typing
from contextlib import suppress

import msgspec

from telegrinder.bot.cute_types import CallbackQueryCute
from telegrinder.bot.rules.adapter import EventAdapter
from telegrinder.model import decoder
from telegrinder.tools.buttons import DataclassInstance

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
        return bool(event.data or event.data.unwrap())


class CallbackQueryDataRule(CallbackQueryRule, abc.ABC, requires=[HasData()]):
    pass


class CallbackDataEq(CallbackQueryDataRule):
    def __init__(self, value: str):
        self.value = value

    async def check(self, event: CallbackQuery, ctx: dict) -> bool:
        return event.data.unwrap() == self.value


class CallbackDataJsonEq(CallbackQueryDataRule):
    def __init__(self, d: dict[str, typing.Any]):
        self.d = d

    async def check(self, event: CallbackQuery, ctx: dict) -> bool:
        with suppress(BaseException):
            return decoder.decode(event.data.unwrap(), type=dict) == self.d
        return False


class CallbackDataJsonModel(CallbackQueryDataRule):
    def __init__(self, model: type[msgspec.Struct] | type[DataclassInstance]):
        self.model = model

    async def check(self, event: CallbackQuery, ctx: dict) -> bool:
        with suppress(msgspec.ValidationError, msgspec.DecodeError):
            ctx["data"] = decoder.decode(event.data.unwrap().encode(), type=self.model)
            return True
        return False


class CallbackDataMarkup(CallbackQueryDataRule):
    def __init__(self, patterns: PatternLike | list[PatternLike]):
        self.patterns = Markup(patterns).patterns

    async def check(self, event: CallbackQuery, ctx: dict) -> bool:
        return check_string(self.patterns, event.data.unwrap(), ctx)
