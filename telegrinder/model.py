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
) -> Result[T, "APIError"]: ...


@typing.overload
def full_result(
    result: Result[msgspec.Raw, "APIError"],
    full_t: tuple[type[T], ...],
) -> Result[T, "APIError"]: ...


def full_result(
    result: Result[msgspec.Raw, "APIError"],
    full_t: type[T] | tuple[type[T], ...],
) -> Result[T, "APIError"]:
    return result.map(lambda v: decoder.decode(v, type=full_t))  # type: ignore


def get_params(params: dict[str, typing.Any]) -> dict[str, typing.Any]:
    return {
        k: v.unwrap() if isinstance(v, Some) else v
        for k, v in (
            *params.pop("other", {}).items(),
            *params.items(),
        )
        if k != "self" and type(v) not in (NoneType, Nothing)
    }


class Model(msgspec.Struct, **MODEL_CONFIG):
    @classmethod
    def from_bytes(cls, data: bytes) -> typing.Self:
        return decoder.decode(data, type=cls)

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

    def __repr__(self) -> str:
        return "<{}: {}>".format(
            self.__class__.__name__,
            ", ".join(f"{k}={v!r}" for k, v in self.converters),
        )

    @property
    def converters(self) -> dict[type[typing.Any], typing.Callable[..., typing.Any]]:
        return {
            get_origin(value.__annotations__["data"]): value
            for key, value in vars(self.__class__).items()
            if key.startswith("convert_") and callable(value)
        }

    @staticmethod
    def convert_enum(data: enum.Enum, _: bool = True) -> typing.Any:
        return data.value

    @staticmethod
    def convert_datetime(data: datetime, _: bool = True) -> int:
        return int(data.timestamp())

    def __call__(self, data: typing.Any, *, serialize: bool = True) -> typing.Any:
        converter = self.get_converter(get_origin(type(data)))
        if converter is not None:
            if isinstance(converter, staticmethod):
                return converter(data, serialize)
            return converter(self, data, serialize)
        return data

    def get_converter(self, t: type[typing.Any]):
        for type, converter in self.converters.items():
            if issubclass(t, type):
                return converter
        return None

    def convert_model(
        self,
        data: Model,
        serialize: bool = True,
    ) -> str | dict[str, typing.Any]:
        converted_dct = self(data.to_dict(), serialize=False)
        return encoder.encode(converted_dct) if serialize is True else converted_dct

    def convert_dct(
        self,
        data: dict[str, typing.Any],
        serialize: bool = True,
    ) -> dict[str, typing.Any]:
        return {
            k: self(v, serialize=serialize)
            for k, v in data.items()
            if type(v) not in (NoneType, Nothing)
        }

    def convert_lst(
        self,
        data: list[typing.Any],
        serialize: bool = True,
    ) -> str | list[typing.Any]:
        converted_lst = [self(x, serialize=False) for x in data]
        return encoder.encode(converted_lst) if serialize is True else converted_lst

    def convert_tpl(
        self,
        data: tuple[typing.Any, ...],
        _: bool = True,
    ) -> str | tuple[typing.Any, ...]:
        if (
            isinstance(data, tuple)
            and len(data) == 2
            and isinstance(data[0], str)
            and isinstance(data[1], bytes)
        ):
            attach_name = secrets.token_urlsafe(16)
            self.files[attach_name] = data
            return "attach://{}".format(attach_name)
        return data


__all__ = (
    "DataConverter",
    "MODEL_CONFIG",
    "Model",
    "full_result",
    "get_params",
)
