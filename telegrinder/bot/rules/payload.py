import typing
from contextlib import suppress
from functools import cached_property

import msgspec

from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.bot.rules.markup import Markup, PatternLike, check_string
from telegrinder.msgspec_utils.json import loads
from telegrinder.node.base import Node
from telegrinder.node.payload import Payload, PayloadData
from telegrinder.tools.callback_data_serialization.abc import ABCDataSerializer, ModelType
from telegrinder.tools.callback_data_serialization.json_ser import JSONSerializer
from telegrinder.tools.callback_data_serialization.utils import get_model_serializer

_ANY: typing.Final[object] = object()


class PayloadRule[Data](ABCRule):
    def __init__(
        self,
        data_type: type[Data],
        serializer: type[ABCDataSerializer[Data]] | None = None,
        *,
        alias: str | None = None,
    ) -> None:
        self.data_type = data_type
        self.serializer = serializer or get_model_serializer(data_type) or JSONSerializer
        self.alias = alias or "data"

    @cached_property
    def required_nodes(self) -> dict[str, type[Node]]:
        return {"payload": PayloadData[self.data_type, self.serializer]}  # type: ignore

    def check(self, payload: PayloadData[Data], context: Context) -> typing.Literal[True]:
        context.set(self.alias, payload)
        return True


class PayloadModelRule[Model: ModelType](PayloadRule):
    def __init__(
        self,
        model_t: type[Model],
        /,
        *,
        payload: typing.Any = _ANY,
        serializer: type[ABCDataSerializer[Model]] | None = None,
        alias: str | None = None,
    ) -> None:
        super().__init__(model_t, serializer, alias=alias or "model")
        self.payload = payload

    def check(self, payload: PayloadData[Model], context: Context) -> bool:
        if self.payload is not _ANY and payload != self.payload:
            return False

        context.set(self.alias, payload)
        return True


class PayloadEqRule(ABCRule):
    def __init__(self, payloads: str | list[str], /) -> None:
        self.payloads = [payloads] if isinstance(payloads, str) else payloads

    def check(self, payload: Payload) -> bool:
        return any(p == payload for p in self.payloads)


class PayloadMarkupRule(ABCRule):
    def __init__(self, pattern: PatternLike | list[PatternLike], /) -> None:
        self.patterns = Markup(pattern).patterns

    def check(self, payload: Payload, context: Context) -> bool:
        return check_string(self.patterns, payload, context)


class PayloadJsonEqRule(ABCRule):
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
