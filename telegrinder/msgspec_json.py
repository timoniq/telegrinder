import typing

from .msgspec_utils import decoder, encoder


def loads(s: str | bytes) -> typing.Any:
    return decoder.decode(s)


def dumps(o: typing.Any) -> str:
    return encoder.encode(o)


__all__ = ("dumps", "loads")
