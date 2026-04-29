import typing

from msgspex import decoder, encoder


def dumps(o: typing.Any, /) -> str:
    return encoder.encode(o)


def loads(s: str | bytes, /) -> typing.Any:
    return decoder.decode(s)


__all__ = ("dumps", "loads")
