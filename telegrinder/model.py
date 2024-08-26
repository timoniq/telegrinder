import dataclasses
import enum
import keyword
import secrets
import typing
from datetime import datetime
from types import NoneType

import msgspec
from fntypes.co import Nothing, Result, Some

from telegrinder.msgspec_utils import decoder, encoder, get_origin

if typing.TYPE_CHECKING:
    from telegrinder.api.error import APIError

T = typing.TypeVar("T")


def rename_field(name: str) -> str:
    if name.endswith("_") and name.removesuffix("_") in keyword.kwlist:
        return name.removesuffix("_")
    return name if not keyword.iskeyword(name) else name + "_"


MODEL_CONFIG: typing.Final[dict[str, typing.Any]] = {
    "omit_defaults": True,
    "dict": True,
    "rename": rename_field,
}


@typing.overload
def full_result(
    result: Result[msgspec.Raw, "APIError"],
    full_t: type[T],
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
    validated_params = {}
    for k, v in (
        *params.pop("other", {}).items(),
        *params.items(),
    ):
        if isinstance(v, Proxy):
            v = v.get()
        if k == "self" or type(v) in (NoneType, Nothing):
            continue
        validated_params[k] = v.unwrap() if isinstance(v, Some) else v
    return validated_params


class Model(msgspec.Struct, **MODEL_CONFIG):
    @classmethod
    def from_data(cls, data: dict[str, typing.Any]) -> typing.Self:
        return decoder.convert(data, type=cls)

    @classmethod
    def from_bytes(cls, data: bytes) -> typing.Self:
        return decoder.decode(data, type=cls)

    def _to_dict(
        self,
        dct_name: str,
        exclude_fields: set[str],
        full: bool,
    ) -> dict[str, typing.Any]:
        if dct_name not in self.__dict__:
            self.__dict__[dct_name] = (
                msgspec.structs.asdict(self)
                if not full
                else encoder.to_builtins(self.to_dict(exclude_fields=exclude_fields), order="deterministic")
            )

        if not exclude_fields:
            return self.__dict__[dct_name]

        return {key: value for key, value in self.__dict__[dct_name].items() if key not in exclude_fields}

    def to_dict(
        self,
        *,
        exclude_fields: set[str] | None = None,
    ) -> dict[str, typing.Any]:
        """
        :param exclude_fields: Model field names to exclude from the dictionary representation of this model.
        :return: A dictionary representation of this model.
        """

        return self._to_dict("model_as_dict", exclude_fields or set(), full=False)

    def to_full_dict(
        self,
        *,
        exclude_fields: set[str] | None = None,
    ) -> dict[str, typing.Any]:
        """
        :param exclude_fields: Model field names to exclude from the dictionary representation of this model.
        :return: A dictionary representation of this model including all models, structs, custom types.
        """

        return self._to_dict("model_as_full_dict", exclude_fields or set(), full=True)


@dataclasses.dataclass(kw_only=True, frozen=True, slots=True, repr=False)
class DataConverter:
    _converters: dict[type[typing.Any], typing.Callable[..., typing.Any]] = dataclasses.field(
        init=False,
        default_factory=lambda: {},
    )
    _files: dict[str, tuple[str, bytes]] = dataclasses.field(default_factory=lambda: {})

    def __repr__(self) -> str:
        return "<{}: {}>".format(
            self.__class__.__name__,
            ", ".join(f"{k}={v.__name__!r}" for k, v in self._converters.items()),
        )

    def __post_init__(self) -> None:
        self._converters.update(
            {
                get_origin(value.__annotations__["data"]): value
                for key, value in vars(self.__class__).items()
                if key.startswith("convert_") and callable(value)
            }
        )

    def __call__(self, data: typing.Any, *, serialize: bool = True) -> typing.Any:
        converter = self.get_converter(get_origin(type(data)))
        if converter is not None:
            if isinstance(converter, staticmethod):
                return converter(data, serialize)
            return converter(self, data, serialize)
        return data

    @property
    def converters(self) -> dict[type[typing.Any], typing.Callable[..., typing.Any]]:
        return self._converters.copy()

    @property
    def files(self) -> dict[str, tuple[str, bytes]]:
        return self._files.copy()

    @staticmethod
    def convert_enum(data: enum.Enum, _: bool = False) -> typing.Any:
        return data.value

    @staticmethod
    def convert_datetime(data: datetime, _: bool = False) -> int:
        return int(data.timestamp())

    def get_converter(self, t: type[typing.Any]):
        for type_, converter in self._converters.items():
            if issubclass(t, type_):
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
            k: self(v, serialize=serialize) for k, v in data.items() if type(v) not in (NoneType, Nothing)
        }

    def convert_lst(
        self,
        data: list[typing.Any],
        serialize: bool = True,
    ) -> str | list[typing.Any]:
        converted_lst = [self(x, serialize=False) for x in data]
        return encoder.encode(converted_lst) if serialize is True else converted_lst

    def convert_tpl(self, data: tuple[typing.Any, ...], _: bool = False) -> str | tuple[typing.Any, ...]:
        match data:
            case (str(filename), bytes(content)):
                attach_name = secrets.token_urlsafe(16)
                self._files[attach_name] = (filename, content)
                return "attach://{}".format(attach_name)

        return data


class Proxy:
    def __init__(self, cfg: "_ProxiedDict", key: str) -> None:
        self.key = key
        self.cfg = cfg

    def get(self) -> typing.Any | None:
        return self.cfg._defaults.get(self.key)


class _ProxiedDict(typing.Generic[T]):
    def __init__(self, tp: type[T]) -> None:
        self.type = tp
        self._defaults = {}

    def __setattribute__(self, name: str, value: typing.Any, /) -> None:
        self._defaults[name] = value

    def __getitem__(self, key: str, /) -> None:
        return Proxy(self, key)  # type: ignore

    def __setitem__(self, key: str, value: typing.Any, /) -> None:
        self._defaults[key] = value


if typing.TYPE_CHECKING:

    def ProxiedDict(typed_dct: type[T]) -> T | _ProxiedDict[T]:  # noqa: N802
        ...

else:
    ProxiedDict = _ProxiedDict


__all__ = (
    "DataConverter",
    "MODEL_CONFIG",
    "Model",
    "ProxiedDict",
    "Proxy",
    "full_result",
    "get_params",
)
