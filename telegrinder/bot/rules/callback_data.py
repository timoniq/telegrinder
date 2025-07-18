import abc
import typing
from contextlib import suppress

from telegrinder.bot.cute_types import CallbackQueryCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.bot.rules.payload import (
    PayloadEqRule,
    PayloadJsonEqRule,
    PayloadMarkupRule,
    PayloadModelRule,
)
from telegrinder.tools.aio import maybe_awaitable

type Validator = typing.Callable[[typing.Any], bool | typing.Awaitable[bool]]
type CallbackMap = dict[str, typing.Any | type[typing.Any] | Validator | CallbackMap]
type CallbackMapStrict = dict[str, Validator | CallbackMapStrict]

CallbackQuery: typing.TypeAlias = CallbackQueryCute
CallbackDataEq: typing.TypeAlias = PayloadEqRule
CallbackDataJsonEq: typing.TypeAlias = PayloadJsonEqRule
CallbackDataMarkup: typing.TypeAlias = PayloadMarkupRule
CallbackDataJsonModel: typing.TypeAlias = PayloadModelRule


class HasData(ABCRule):
    def check(self, event: CallbackQuery) -> bool:
        return bool(event.data)


class CallbackQueryDataRule(ABCRule, abc.ABC, requires=[HasData()]):
    pass


class CallbackDataMap(CallbackQueryDataRule):
    def __init__(self, mapping: CallbackMap, /, *, allow_extra_fields: bool = False) -> None:
        """Callback data map validation.
        :param mapping: A callback data mapping with validators.
        :param allow_extra_fields: Allows extra fields in a callback query data.
        """
        self.mapping = self.transform_to_callbacks(mapping)
        self.allow_extra_fields = allow_extra_fields

    @classmethod
    def transform_to_callbacks(cls, callback_map: CallbackMap) -> CallbackMapStrict:
        """Transforms `CallbackMap` to `CallbackMapStrict`."""
        callback_map_result = []

        for key, value in callback_map.items():
            if isinstance(value, type):
                validator = (lambda tp: lambda v: isinstance(v, tp))(value)
            elif isinstance(value, dict):
                validator = cls.transform_to_callbacks(value)
            elif not callable(value):
                validator = (lambda val: lambda v: val == v)(value)
            else:
                validator = value
            callback_map_result.append((key, validator))

        return dict(callback_map_result)

    @staticmethod
    async def run_validator(value: typing.Any, validator: Validator) -> bool:
        """Runs sync/async validator."""
        with suppress(Exception):
            return await maybe_awaitable(validator(value))
        return False

    @classmethod
    async def match(cls, callback_data: dict[str, typing.Any], callback_map: CallbackMapStrict) -> bool:
        """Matches `callback_data` with `callback_map` recursively."""
        for key, validator in callback_map.items():
            if key not in callback_data:
                return False

            if isinstance(validator, dict):
                if not (isinstance(callback_data[key], dict) and await cls.match(callback_data[key], validator)):
                    return False

            elif not await cls.run_validator(callback_data[key], validator):
                return False

        return True

    async def check(self, event: CallbackQuery, ctx: Context) -> bool:
        callback_data = event.decode_data().unwrap_or_none()
        if callback_data is None:
            return False

        if not self.allow_extra_fields and self.mapping.keys() != callback_data.keys():
            return False

        if await self.match(callback_data, self.mapping):
            ctx.update({k: callback_data[k] for k in self.mapping})
            return True

        return False


__all__ = (
    "CallbackDataEq",
    "CallbackDataJsonEq",
    "CallbackDataJsonModel",
    "CallbackDataMap",
    "CallbackDataMarkup",
    "CallbackQueryDataRule",
    "HasData",
)
