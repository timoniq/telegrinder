import typing
from contextlib import suppress
from functools import cached_property

import msgspec

from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.bot.rules.markup import Markup, PatternLike, check_string
from telegrinder.msgspec_json import loads
from telegrinder.node.base import Node
from telegrinder.node.payload import Payload, PayloadData
from telegrinder.tools.callback_data_serilization.abc import ABCDataSerializer, ModelType
from telegrinder.tools.callback_data_serilization.json_ser import JSONSerializer


class PayloadRule[Data](ABCRule):
    def __init__(
        self,
        data_type: type[Data],
        serializer: type[ABCDataSerializer[Data]],
        *,
        alias: str | None = None,
    ) -> None:
        self.data_type = data_type
        self.serializer = serializer
        self.alias = alias or "data"

    @cached_property
    def required_nodes(self) -> dict[str, type[Node]]:
        return {"payload": PayloadModel[self.data_type, self.serializer]}  # type: ignore

    def check(self, payload: PayloadData[Data], context: Context) -> typing.Literal[True]:
        context.set(self.alias, payload)
        return True


class PayloadModelRule[Model: ModelType](PayloadRule[Model]):
    def __init__(
        self,
        model_t: type[Model],
        *,
        serializer: type[ABCDataSerializer[Model]] | None = None,
        alias: str | None = None,
    ) -> None:
        super().__init__(model_t, serializer or JSONSerializer, alias=alias or "model")


class PayloadEqRule(PayloadRule):
    def __init__(self, payload: str, /) -> None:
        self.payload = payload
    
    def check(self, payload: Payload) -> bool:
        return self.payload == payload


class PayloadMarkupRule(PayloadRule):
    def __init__(self, pattern: PatternLike | list[PatternLike], /) -> None:
        self.patterns = Markup(pattern).patterns

    def check(self, payload: Payload, context: Context) -> bool:
        return check_string(self.patterns, payload, context)


class PayloadJsonEqRule(PayloadRule):
    def __init__(self, payload: dict[str, typing.Any], /) -> None:
        self.payload = payload

    def check(self, payload: Payload) -> bool:
        with suppress(msgspec.DecodeError, msgspec.ValidationError):
            return self.payload == loads(payload)
        return False


__all__ = (
    "PayloadEqRule",
    "PayloadJsonEqRule",
    "PayloadMarkupRule",
    "PayloadModelRule",
    "PayloadRule",
)
