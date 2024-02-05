import typing
from types import NoneType

import msgspec
from fntypes.co import Nothing, Result, Some

from .msgspec_utils import decoder, encoder

T = typing.TypeVar("T")

if typing.TYPE_CHECKING:
    from telegrinder.api.error import APIError
    

MODEL_CONFIG: typing.Final[dict[str, typing.Any]] = {
    "omit_defaults": True,
    "dict": True,
    "rename": {"from_": "from"},
}


@typing.overload
def full_result(
    result: Result[msgspec.Raw, "APIError"], full_t: type[T]
) -> Result[T, "APIError"]:
    ...


@typing.overload
def full_result(
    result: Result[msgspec.Raw, "APIError"],
    full_t: tuple[type[T], ...],
) -> Result[T, "APIError"]:
    ...


def full_result(
    result: Result[msgspec.Raw, "APIError"],
    full_t: type[T] | tuple[type[T], ...],
) -> Result[T, "APIError"]:
    return result.map(lambda v: decoder.decode(v, type=full_t))  # type: ignore


def convert(d: typing.Any, serialize: bool = True) -> typing.Any:
    if isinstance(d, Model):
        converted_dct = convert(d.to_dict(), serialize=False)
        return encoder.encode(converted_dct) if serialize is True else converted_dct
    
    if isinstance(d, dict):
        return {
            k: convert(v, serialize=serialize)
            for k, v in d.items()
            if type(v) not in (NoneType, Nothing)
        }
    
    if isinstance(d, list):
        converted_lst = [convert(x, serialize=False) for x in d]
        return encoder.encode(converted_lst) if serialize is True else converted_lst
    
    return d


def get_params(params: dict[str, typing.Any]) -> dict[str, typing.Any]:
    return {
        k: v.unwrap() if v and isinstance(v, Some) else v
        for k, v in (
            *params.items(),
            *params.pop("other", {}).items(),
        )
        if k != "self" and type(v) not in (NoneType, Nothing)
    }


class Model(msgspec.Struct, **MODEL_CONFIG):
    def to_dict(
        self,
        *,
        exclude_fields: set[str] | None = None,
    ) -> dict[str, typing.Any]:  
        exclude_fields = exclude_fields or set()
        if "model_as_dict" not in self.__dict__:
            self.__dict__["model_as_dict"] = msgspec.structs.asdict(self)
        return {
            key: value
            for key, value in self.__dict__["model_as_dict"].items()
            if key not in exclude_fields
        }


__all__ = (
    "Model",
    "convert",
    "full_result",
    "get_params",
    "MODEL_CONFIG",
)
