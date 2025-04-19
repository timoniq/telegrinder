import typing


def separate_by_plus_char(iterable: typing.Iterable[str] | None = None, /) -> str | None:
    return None if not iterable else "+".join(iterable)


__all__ = ("separate_by_plus_char",)
