import typing


class _LiteralMeta(type):
    __args__: tuple[typing.Any, ...]

    def __getitem__[T](cls: type[T], values: typing.Any, /) -> type[T]:
        values = (values,) if not isinstance(values, tuple) else values
        return _LiteralMeta(cls.__name__, (cls,), {"__args__": values})  # type: ignore

    def __instancecheck__(cls, instance: typing.Any, /) -> bool:
        return instance in cls.__args__


class _Literal(metaclass=_LiteralMeta):
    pass


if typing.TYPE_CHECKING:
    from typing import Literal
else:
    Literal = _Literal


__all__ = ("Literal",)
