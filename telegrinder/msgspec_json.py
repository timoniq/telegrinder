import typing

from .msgspec_utils import decoder, encoder


def loads(s: str | bytes) -> dict[str, typing.Any] | list[typing.Any]:
    return decoder.decode(s, type=dict[str, typing.Any] | list[typing.Any])  # type: ignore


def dumps(o: dict[str, typing.Any] | list[typing.Any]) -> str:
    return encoder.encode(o)


__all__ = ("dumps", "loads")
