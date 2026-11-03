import typing

from msgspex import decoder, encoder


def dumps(o: typing.Any, /) -> str:
    return encoder.encode(o)


def dumpb(o: typing.Any, /) -> bytes:
    return encoder.encode(o, as_str=False)


def loads(s: str | bytes, /) -> typing.Any:
    return decoder.decode(s)


__all__ = ("dumpb", "dumps", "loads")
