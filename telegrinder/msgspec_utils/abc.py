from __future__ import annotations

import abc
import typing


def is_supports_cast(obj: typing.Any, /) -> typing.TypeGuard[SupportsCast]:
    return isinstance(obj, SupportsCast)


@typing.runtime_checkable
class SupportsCast(typing.Protocol):
    @classmethod
    @abc.abstractmethod
    def cast(cls, obj: typing.Any) -> typing.Self: ...


__all__ = ("SupportsCast", "is_supports_cast")
