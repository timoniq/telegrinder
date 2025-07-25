from __future__ import annotations

import dataclasses
import typing

import msgspec
from fntypes.library.monad.result import Result

from telegrinder.msgspec_utils.decoder import decoder
from telegrinder.msgspec_utils.encoder import encoder

if typing.TYPE_CHECKING:
    from telegrinder.api.error import APIError


def full_result[T](
    result: Result[msgspec.Raw, APIError],
    full_t: type[T],
) -> Result[T, APIError]:
    return result.map(lambda v: decoder.decode(v, type=full_t))


def get_params(params: dict[str, typing.Any], /) -> dict[str, typing.Any]:
    return {
        key: encoder.cast(value)
        for key, val in (
            *params.pop("other", {}).items(),
            *params.items(),
        )
        if key != "self" and (value := val.get() if isinstance(val, Proxy) else val) is not None
    }


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

    def __getitem__(self, key: str, /) -> typing.Any:
        return Proxy(self, key)

    def __setitem__(self, key: str, value: typing.Any, /) -> None:
        self._defaults[key] = value


__all__ = ("ProxiedDict", "full_result", "get_params")
