import abc
import inspect
import typing
from contextlib import suppress

import msgspec

from telegrinder.bot.cute_types import CallbackQueryCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.rules.adapter import EventAdapter
from telegrinder.model import decoder
from telegrinder.tools.buttons import DataclassInstance
from telegrinder.types.enums import UpdateType

from .abc import ABCRule
from .markup import Markup, PatternLike, check_string

CallbackQuery: typing.TypeAlias = CallbackQueryCute
Validator: typing.TypeAlias = typing.Callable[[typing.Any], bool | typing.Awaitable[bool]]
MapDict: typing.TypeAlias = dict[str, "typing.Any | type[typing.Any] | Validator | list[MapDict] | MapDict"]
CallbackMap: typing.TypeAlias = list[tuple[str, "typing.Any | type[typing.Any] | Validator | CallbackMap"]]
CallbackMapStrict: typing.TypeAlias = list[tuple[str, "Validator | CallbackMapStrict"]]


class CallbackQueryRule(ABCRule[CallbackQuery], abc.ABC):
    adapter: EventAdapter[CallbackQuery] = EventAdapter(UpdateType.CALLBACK_QUERY, CallbackQuery)

    @abc.abstractmethod
    async def check(self, event: CallbackQuery, ctx: Context) -> bool:
        pass


class HasData(CallbackQueryRule):
    async def check(self, event: CallbackQuery, ctx: Context) -> bool:
        return bool(event.data.unwrap_or_none())


class CallbackQueryDataRule(CallbackQueryRule, abc.ABC, requires=[HasData()]):
    pass


class CallbackDataMap(CallbackQueryDataRule):
    def __init__(self, mapping: MapDict, /) -> None:
        self.mapping = self.transform_to_callbacks(
            self.transform_to_map(mapping),
        )

    @classmethod
    def transform_to_map(cls, mapping: MapDict) -> CallbackMap:
        """Transforms MapDict to CallbackMap."""

        callback_map = []

        for k, v in mapping.items():
            if isinstance(v, dict):
                v = cls.transform_to_map(v)
            callback_map.append((k, v))

        return callback_map

    @classmethod
    def transform_to_callbacks(cls, callback_map: CallbackMap) -> CallbackMapStrict:
        """Transforms `CallbackMap` to `CallbackMapStrict`."""

        callback_map_result = []

        for key, value in callback_map:
            if isinstance(value, type):
                validator = (lambda tp: lambda v: isinstance(v, tp))(value)
            elif isinstance(value, list):
                validator = cls.transform_to_callbacks(value)
            elif not callable(value):
                validator = (lambda val: lambda v: val == v)(value)
            else:
                validator = value
            callback_map_result.append((key, validator))

        return callback_map_result

    @staticmethod
    async def run_validator(value: typing.Any, validator: Validator) -> bool:
        """Run async or sync validator."""

        with suppress(BaseException):
            result = validator(value)
            if inspect.isawaitable(result):
                result = await result
            return result

        return False

    @classmethod
    async def match(cls, callback_data: dict[str, typing.Any], callback_map: CallbackMapStrict) -> bool:
        """Matches callback_data with callback_map recursively."""

        for key, validator in callback_map:
            if key not in callback_data:
                return False

            if isinstance(validator, list):
                if not (
                    isinstance(callback_data[key], dict) and await cls.match(callback_data[key], validator)
                ):
                    return False

            elif not await cls.run_validator(callback_data[key], validator):
                return False

        return True

    async def check(self, event: CallbackQuery, ctx: Context) -> bool:
        callback_data = event.decode_callback_data().unwrap_or_none()
        if callback_data is None:
            return False
        if await self.match(callback_data, self.mapping):
            ctx.update(callback_data)
            return True
        return False


class CallbackDataEq(CallbackQueryDataRule):
    def __init__(self, value: str, /) -> None:
        self.value = value

    async def check(self, event: CallbackQuery, ctx: Context) -> bool:
        return event.data.unwrap() == self.value


class CallbackDataJsonEq(CallbackQueryDataRule):
    def __init__(self, d: dict[str, typing.Any], /) -> None:
        self.d = d

    async def check(self, event: CallbackQuery, ctx: Context) -> bool:
        return event.decode_callback_data().unwrap_or_none() == self.d


class CallbackDataJsonModel(CallbackQueryDataRule):
    def __init__(self, model: type[msgspec.Struct] | type[DataclassInstance], /) -> None:
        self.model = model

    async def check(self, event: CallbackQuery, ctx: Context) -> bool:
        with suppress(BaseException):
            ctx.data = decoder.decode(event.data.unwrap().encode(), type=self.model)
            return True
        return False


class CallbackDataMarkup(CallbackQueryDataRule):
    def __init__(self, patterns: PatternLike | list[PatternLike], /) -> None:
        self.patterns = Markup(patterns).patterns

    async def check(self, event: CallbackQuery, ctx: Context) -> bool:
        return check_string(self.patterns, event.data.unwrap(), ctx)


__all__ = (
    "CallbackDataEq",
    "CallbackDataJsonEq",
    "CallbackDataJsonModel",
    "CallbackDataMap",
    "CallbackDataMarkup",
    "CallbackQueryDataRule",
    "CallbackQueryRule",
    "HasData",
)
