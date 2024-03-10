import dataclasses
import enum
import secrets
import typing
from datetime import datetime
from types import NoneType

import msgspec
from fntypes.co import Nothing, Result, Some

from .msgspec_utils import decoder, encoder, get_origin

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


def get_params(params: dict[str, typing.Any]) -> dict[str, typing.Any]:
    return {
        k: v.unwrap() if v and isinstance(v, Some) else v
        for k, v in (
            *params.pop("other", {}).items(),
            *params.items(),
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


@dataclasses.dataclass(kw_only=True)
class DataConverter:
    files: dict[str, tuple[str, bytes]] = dataclasses.field(default_factory=lambda: {})

    @property
    def converters(self) -> dict[
        type[typing.Any], typing.Callable[[typing.Self, typing.Any, bool], typing.Any]
    ]:
        return {
            get_origin(value.__annotations__["d"]): value
            for key, value in vars(self.__class__).items()
            if key.startswith("convert_")
            and callable(value)
        }
    
    def get_converter(
        self, t: type[typing.Any]
    ) -> typing.Callable[[typing.Self, typing.Any, bool], typing.Any] | None:
        for type, converter in self.converters.items():
            if issubclass(t, type):
                return converter
        return None
    
    def convert_model(self, d: Model, serialize: bool = True) -> str | dict[str, typing.Any]:
        converted_dct = self.convert(d.to_dict(), serialize=False)
        return encoder.encode(converted_dct) if serialize is True else converted_dct
    
    def convert_dct(self, d: dict[str, typing.Any], serialize: bool = True) -> dict[str, typing.Any]:
        return {
            k: self.convert(v, serialize=serialize)
            for k, v in d.items()
            if type(v) not in (NoneType, Nothing)
        }
    
    def convert_lst(self, d: list[typing.Any], serialize: bool = True) -> str | list[typing.Any]:
        converted_lst = [self.convert(x, serialize=False) for x in d]
        return encoder.encode(converted_lst) if serialize is True else converted_lst
    
    def convert_tpl(self, d: tuple[typing.Any, ...], serialize: bool = True) -> str | tuple[typing.Any, ...]:
        if (
            isinstance(d, tuple)
            and len(d) == 2
            and isinstance(d[0], str)
            and isinstance(d[1], bytes)
        ):
            attach_name = secrets.token_urlsafe(16)
            self.files[attach_name] = d
            return "attach://{}".format(attach_name)
        return d
    
    def convert_enum(self, d: enum.Enum, serialize: bool = True) -> str:
        return d.value
    
    def convert_datetime(self, d: datetime, serialize: bool = True) -> int:
        return int(d.timestamp())

    def convert(self, data: typing.Any, *, serialize: bool = True) -> typing.Any:
        converter = self.get_converter(get_origin(type(data)))
        if converter is not None:
            return converter(self, data, serialize)
        return data


__all__ = (
    "DataConverter",
    "Model",
    "full_result",
    "get_params",
    "MODEL_CONFIG",
)
