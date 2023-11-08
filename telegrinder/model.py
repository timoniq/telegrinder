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


def convert(d: typing.Any, serialize: bool = True) -> typing.Any:
    if isinstance(d, Model):
        converted_dct = convert(d.to_dict(), serialize=False)
        if serialize is True:
            return json.dumps(converted_dct)
        return converted_dct
    if isinstance(d, dict):
        return {
            k: convert(v, serialize=serialize) for k, v in d.items() if v is not None
        }
    if isinstance(d, list):
        converted_lst = [convert(x, serialize=False) for x in d]
        if serialize is True:
            return json.dumps(converted_lst)
        return converted_lst
    return d


def get_params(params: dict[str, typing.Any]) -> dict[str, typing.Any]:
    return {
        k: v
        for k, v in (
            *params.items(),
            *params.pop("other").items(),
        )
        if k != "self" and v is not None
    }


class Model(msgspec.Struct, omit_defaults=True, rename={"from_": "from"}):
    def to_dict(
        self,
        *,
        exclude_fields: set[str] | None = None,
    ):
        return {
            k: v
            for k, v in msgspec.structs.asdict(self).items()
            if k not in (exclude_fields or ())
        }


__all__ = (
    "convert",
    "encoder",
    "full_result",
    "msgspec",
    "Model",
    "Raw",
    "get_params",
)
