import typing
from functools import cached_property

from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.node.base import Node
from telegrinder.node.payload import PayloadData
from telegrinder.tools.callback_data_serilization.abc import ABCDataSerializer, ModelType
from telegrinder.tools.callback_data_serilization.json_ser import JSONSerializer


class PayloadRule[Data](ABCRule):
    def __init__(self, *, alias: str | None = None) -> None:
        self.alias = alias or "data"

    def check(self, payload: PayloadData[Data], ctx: Context) -> typing.Literal[True]:
        ctx.set(self.alias, payload)
        return True


class PayloadDataRule[Data](PayloadRule[Data]):
    def __init__(
        self,
        data_type: type[Data],
        serializer: type[ABCDataSerializer[Data]],
        *,
        alias: str | None = None,
    ) -> None:
        self.data_type = data_type
        self.serializer = serializer
        super().__init__(alias=alias)

    @cached_property
    def required_nodes(self) -> dict[str, type[Node]]:
        return {"payload": PayloadModel[self.model_t, self.serializer]}  # type: ignore


class PayloadModelRule[Model: ModelType](PayloadRule[Model]):
    def __init__(
        self,
        model_t: type[Model],
        *,
        serializer: type[ABCDataSerializer[Model]] | None = None,
        alias: str | None = None,
    ) -> None:
        self.model_t = model_t
        self.serializer = serializer or JSONSerializer[Model]
        super().__init__(alias=alias or "model")

    @cached_property
    def required_nodes(self) -> dict[str, type[Node]]:
        return {"payload": PayloadData[self.model_t, self.serializer]}  # type: ignore


__all__ = ("PayloadDataRule", "PayloadModelRule", "PayloadRule")
