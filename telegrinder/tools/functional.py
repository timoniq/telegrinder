import typing

from fntypes import Nothing, Option, Some

T = typing.TypeVar("T")


def from_optional(value: T | None) -> Option[T]:
    return Some(value) if value is not None else Nothing()


__all__ = ("from_optional",)
