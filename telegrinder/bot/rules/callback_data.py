import abc
import typing

import msgspec
import vbml

from telegrinder.bot.cute_types import CallbackQueryCute
from telegrinder.bot.rules.adapter import EventAdapter
from telegrinder.modules import json
from telegrinder.tools.buttons import IsDataclass

from .abc import ABCRule
from .markup import Markup, check_string

CallbackQuery = CallbackQueryCute
PatternLike = str | vbml.Pattern


class CallbackQueryRule(ABCRule[CallbackQuery], abc.ABC):
    adapter = EventAdapter("callback_query", CallbackQuery)  # type: ignore

    @abc.abstractmethod
    async def check(self, event: CallbackQuery, ctx: dict) -> bool:
        pass


class CallbackDataEq(CallbackQueryRule):
    def __init__(self, value: str):
        self.value = value

    async def check(self, event: CallbackQuery, ctx: dict) -> bool:
        return event.data == self.value


class CallbackDataJsonEq(CallbackQueryRule):
    def __init__(self, d: dict):
        self.d = d

    async def check(self, event: CallbackQuery, ctx: dict) -> bool:
        if not event.data:
            return False
        try:
            # todo: use msgspec
            return json.loads(event.data) == self.d
        except:  # noqa
            return False


class CallbackDataJsonModel(CallbackQueryRule):
    def __init__(self, model: typing.Type[msgspec.Struct] | typing.Type[IsDataclass]):
        self.decoder = msgspec.json.Decoder(type=model)

    async def check(self, event: CallbackQuery, ctx: dict) -> bool:
        try:
            ctx["data"] = self.decoder.decode(event.data.encode())
            return True
        except msgspec.DecodeError:
            return False


class CallbackDataMarkup(CallbackQueryRule):
    def __init__(self, patterns: PatternLike | list[PatternLike]):
        self.patterns = Markup(patterns).patterns

    async def check(self, event: CallbackQuery, ctx: dict) -> bool:
        return check_string(self.patterns, event.data, ctx)
