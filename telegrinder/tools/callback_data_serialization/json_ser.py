import typing

import msgspec
from fntypes.library.monad.result import Error, Ok, Result

from telegrinder.modules import json
from telegrinder.msgspec_utils import decoder
from telegrinder.tools.callback_data_serialization.abc import ABCDataSerializer, ModelType
from telegrinder.tools.callback_data_serialization.utils import get_model_ident_key

type Json = dict[str, typing.Any] | ModelType


class JSONSerializer[JsonT: Json](ABCDataSerializer[JsonT]):
    @typing.overload
    def __init__(self, model_t: type[JsonT]) -> None: ...

    @typing.overload
    def __init__(self, model_t: type[JsonT], *, ident_key: str | None = ...) -> None: ...

    def __init__(
        self,
        model_t: type[JsonT] = dict[str, typing.Any],
        *,
        ident_key: str | None = None,
    ) -> None:
        self.model_t = model_t
        self.ident_key = ident_key or get_model_ident_key(model_t)

    @classmethod
    def serialize_from_json(cls, data: JsonT, *, ident_key: str | None = None) -> str:
        return cls(type(data), ident_key=ident_key).serialize(data)

    @classmethod
    def deserialize_to_json(cls, serialized_data: str, model_t: type[JsonT]) -> Result[JsonT, str]:
        return cls(model_t).deserialize(serialized_data)

    def serialize(self, data: JsonT) -> str:
        return self.key + json.dumps(data)

    def deserialize(self, serialized_data: str) -> Result[JsonT, str]:
        if not serialized_data.startswith(self.key):
            return Error("Data is not corresponding to key.")

        data = serialized_data.removeprefix(self.key)
        try:
            data_obj = json.loads(data)
        except (msgspec.ValidationError, msgspec.DecodeError):
            return Error("Cannot decode json.")

        if not issubclass(self.model_t, dict):
            try:
                return Ok(decoder.convert(data_obj, type=self.model_t))
            except (msgspec.ValidationError, msgspec.DecodeError):
                return Error("Incorrect data.")

        return Ok(data_obj)


__all__ = ("JSONSerializer",)
