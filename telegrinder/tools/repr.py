import typing


def fullname(obj: typing.Any, /) -> str:
    obj = type(obj) if not isinstance(obj, type) else obj
    return ".".join((obj.__module__, obj.__name__))


__all__ = ("fullname",)
