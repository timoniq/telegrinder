from __future__ import annotations

import dataclasses
import keyword
import typing

import msgspec
from fntypes.co import Nothing, Result

from telegrinder.msgspec_utils import decoder, encoder, struct_as_dict

if typing.TYPE_CHECKING:
    from telegrinder.api.error import APIError

MODEL_CONFIG: typing.Final[dict[str, typing.Any]] = {
    "dict": True,
    "rename": {kw + "_": kw for kw in keyword.kwlist},
}
UNSET = typing.cast("typing.Any", msgspec.UNSET)
"""Docs: https://jcristharif.com/msgspec/api.html#unset

During decoding, if a field isn't explicitly set in the model,
the default value of `UNSET` will be set instead. This lets downstream
consumers determine whether a field was left unset, or explicitly set a value."""


def full_result[T](
    result: Result[msgspec.Raw, APIError],
    full_t: type[T],
) -> Result[T, APIError]:
    return result.map(lambda v: decoder.decode(v, type=full_t))


def is_none(value: typing.Any, /) -> typing.TypeGuard[None | Nothing]:
    return value is None or isinstance(value, Nothing)


def get_params(params: dict[str, typing.Any], /) -> dict[str, typing.Any]:
    return {
        key: value
        for key, val in (
            *params.pop("other", {}).items(),
            *params.items(),
        )
        if key != "self" and (value := val.get() if isinstance(val, Proxy) else val) is not None
    }


if typing.TYPE_CHECKING:

    @typing.overload
    def field(*, name: str | None = ...) -> typing.Any: ...

    @typing.overload
    def field(*, default: typing.Any, name: str | None = ...) -> typing.Any: ...

    @typing.overload
    def field(
        *,
        default_factory: typing.Callable[[], typing.Any],
        name: str | None = None,
    ) -> typing.Any: ...

    @typing.overload
    def field(
        *,
        converter: typing.Callable[[typing.Any], typing.Any],
        name: str | None = ...,
    ) -> typing.Any: ...

    @typing.overload
    def field(
        *,
        default: typing.Any,
        converter: typing.Callable[[typing.Any], typing.Any],
        name: str | None = ...,
    ) -> typing.Any: ...

    @typing.overload
    def field(
        *,
        default_factory: typing.Callable[[], typing.Any],
        converter: typing.Callable[[typing.Any], typing.Any],
        name: str | None = None,
    ) -> typing.Any: ...

    def field(
        *,
        default=...,
        default_factory=...,
        name=...,
        converter=...,
    ) -> typing.Any: ...

    class From[T]:
        def __new__(cls, _: T, /) -> typing.Any: ...
else:
    from msgspec import field as _field

    type From[T] = T

    def field(**kwargs):
        kwargs.pop("converter", None)
        return _field(**kwargs)


@typing.dataclass_transform(field_specifiers=(field,))
class Model(msgspec.Struct, **MODEL_CONFIG):
    if not typing.TYPE_CHECKING:

        def __post_init__(self):
            for field in self.__struct_fields__:
                if is_none(getattr(self, field)):
                    setattr(self, field, UNSET)

        def __getattribute__(self, name, /):
            val = super().__getattribute__(name)
            return Nothing() if val is UNSET else val

    @classmethod
    def from_data[**P, T](cls: typing.Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
        return decoder.convert(msgspec.structs.asdict(cls(*args, **kwargs)), type=cls)  # type: ignore

    @classmethod
    def from_dict(cls, obj: dict[str, typing.Any], /) -> typing.Self:
        return decoder.convert(obj, type=cls)

    @classmethod
    def from_raw(cls, raw: str | bytes, /) -> typing.Self:
        return decoder.decode(raw, type=cls)

    def _to_dict(
        self,
        dct_name: str,
        exclude_fields: set[str],
        full: bool,
    ) -> dict[str, typing.Any]:
        if dct_name not in self.__dict__:
            self.__dict__[dct_name] = (
                struct_as_dict(self)
                if not full
                else encoder.to_builtins(self.to_dict(exclude_fields=exclude_fields), order="deterministic")
            )

        if not exclude_fields:
            return self.__dict__[dct_name]

        return {key: value for key, value in self.__dict__[dct_name].items() if key not in exclude_fields}

    def to_raw(self) -> str:
        return encoder.encode(self)

    def to_dict(
        self,
        *,
        exclude_fields: set[str] | None = None,
    ) -> dict[str, typing.Any]:
        """:param exclude_fields: Model field names to exclude from the dictionary representation of this model.
        :return: A dictionary representation of this model.
        """
        return self._to_dict("model_as_dict", exclude_fields or set(), full=False)

    def to_full_dict(
        self,
        *,
        exclude_fields: set[str] | None = None,
    ) -> dict[str, typing.Any]:
        """:param exclude_fields: Model field names to exclude from the dictionary representation of this model.
        :return: A dictionary representation of this model including all models, structs, custom types.
        """
        return self._to_dict("model_as_full_dict", exclude_fields or set(), full=True)


@dataclasses.dataclass(frozen=True)
class Proxy[T]:
    cfg: ProxiedDict[T]
    key: str

    def get(self) -> typing.Any | None:
        return self.cfg._defaults.get(self.key)


class ProxiedDict[T]:
    if typing.TYPE_CHECKING:

        def __new__(cls, tp: type[T], /) -> T | typing.Self: ...

    def __init__(self, tp: type[T], /) -> None:
        self.tp = tp
        self._defaults: dict[str, typing.Any] = {}

    def __setattribute__(self, name: str, value: typing.Any, /) -> None:
        self._defaults[name] = value

    def __getitem__(self, key: str, /) -> None:
        return Proxy(self, key)  # type: ignore

    def __setitem__(self, key: str, value: typing.Any, /) -> None:
        self._defaults[key] = value


__all__ = (
    "MODEL_CONFIG",
    "Model",
    "ProxiedDict",
    "Proxy",
    "full_result",
    "get_params",
)
