import typing

from telegrinder.msgspec_utils.decoder import decoder
from telegrinder.msgspec_utils.encoder import encoder


def dumps(o: typing.Any) -> str:
    return encoder.encode(o)


def loads(s: str | bytes) -> typing.Any:
    return decoder.decode(s)


__all__ = ("dumps", "loads")
