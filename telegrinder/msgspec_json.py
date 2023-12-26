from .model import decoder, encoder


def loads(s: str | bytes) -> dict | list:
    return decoder.decode(s)


def dumps(o: dict | list) -> str:
    return encoder.encode(o)
