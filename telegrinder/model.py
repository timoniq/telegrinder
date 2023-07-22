import typing

import msgspec
from msgspec import Raw

from telegrinder.modules import json
from telegrinder.result import Result

if typing.TYPE_CHECKING:
    from telegrinder.api.error import APIError

T = typing.TypeVar("T")
encoder = msgspec.json.Encoder()


def full_result(
    result: Result[msgspec.Raw, "APIError"], full_t: typing.Type[T]
) -> Result[T, "APIError"]:
    return result.map(lambda v: msgspec.json.decode(v, type=full_t))


def convert(d: typing.Any) -> typing.Any:
    if isinstance(d, Model):
        return msgspec.json.encode(d).decode()
    elif isinstance(d, dict):
        return {k: convert(v) for k, v in d.items() if v is not None}
    elif isinstance(d, list):
        return json.dumps(d)
    return d


model_config = {"rename": {"from_": "from"}, "omit_defaults": True}


class Model(msgspec.Struct, **model_config):
    _dict_cached: dict | None = None

    def to_dict(self) -> dict:
        if self._dict_cached is not None:
            return self._dict_cached
        self._dict_cached = {k: getattr(self, k) for k in self.__struct_fields__}
        return self._dict_cached


def get_params(params: dict) -> dict:
    return {
        k: v
        for k, v in (*params.items(), *params.pop("other").items())
        if k != "self" and v is not None
    }


__all__ = (
    "convert",
    "model_config",
    "encoder",
    "full_result",
    "msgspec",
    "Model",
    "Raw",
    "get_params",
)
