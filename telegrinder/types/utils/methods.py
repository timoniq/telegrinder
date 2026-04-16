import dataclasses
import typing

import msgspec
from kungfu.library.monad.option import NOTHING, Option, Some
from kungfu.library.monad.result import Result
from msgspex.decoder import decoder
from msgspex.encoder import encoder
from typing_extensions import TypeForm

from telegrinder.types.utils.lazy_result import lazy_result

if typing.TYPE_CHECKING:
    from telegrinder.api.error import APIError


def decode_full_result[T](raw: msgspec.Raw, full_t: TypeForm[T], /) -> T:
    return decoder.decode(raw, type=full_t)


def full_result[T](res: Result[msgspec.Raw, APIError], full_t: TypeForm[T]) -> Result[T, APIError]:
    return lazy_result(res, lambda raw: decode_full_result(raw, full_t))


def get_params(params: dict[str, typing.Any], /) -> dict[str, typing.Any]:
    return {
        key: encoder.cast(value)
        for key, val in (
            *params.pop("other", {}).items(),
            *params.items(),
        )
        if key != "self"
        and not (
            (value := val.get() if isinstance(val, Proxy) else val) is None
            or value is NOTHING
            or value is msgspec.UNSET
        )
    }


@dataclasses.dataclass(frozen=True)
class Proxy[T]:
    cfg: ProxiedDict[T]
    key: str

    def get(self) -> typing.Any | None:
        return self.cfg._defaults.get(self.key)

    def get_or_default(self, default: typing.Any) -> typing.Any:
        if self.key not in self.cfg._defaults:
            return default
        return self.cfg._defaults[self.key]

    def get_or_error(self) -> typing.Any:
        if self.key not in self.cfg._defaults:
            raise ValueError(f"Value for default parameter `{self.key}` is not defined.")
        return self.cfg._defaults[self.key]

    def get_or_nothing(self) -> Option[typing.Any]:
        if self.key not in self.cfg._defaults:
            return NOTHING
        return Some(self.cfg._defaults[self.key])


class ProxiedDict[T]:
    if typing.TYPE_CHECKING:

        def __new__(cls, tp: type[T], /) -> T | typing.Self: ...

    def __init__(self, tp: type[T], /) -> None:
        self.tp = tp
        self._defaults: dict[str, typing.Any] = {}

    def __setattribute__(self, name: str, value: typing.Any, /) -> None:
        self._defaults[name] = value

    def __getitem__(self, key: str, /) -> typing.Any:
        return Proxy(self, key)

    def __setitem__(self, key: str, value: typing.Any, /) -> None:
        self._defaults[key] = value


__all__ = ("ProxiedDict", "decode_full_result", "full_result", "get_params")
