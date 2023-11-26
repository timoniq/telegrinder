import typing
from contextlib import suppress

import msgspec

from .option import NothingType, Some

T = typing.TypeVar("T")
Value = typing.TypeVar("Value")


@typing.runtime_checkable
class Option(typing.Generic[Value], typing.Protocol):
    """Option protocol for `msgspec.Struct`."""
    
    def __repr__(self) -> str:
        ...

    def __bool__(self) -> bool:
        ...

    def __eq__(self, __value: object) -> bool:
        ...

    def unwrap(self) -> Value:
        ...

    def unwrap_or(self, alternate_value: Value, /) -> Value:
        ...

    def unwrap_or_other(self, other: Some[Value], /) -> Value:
        ...

    def map(self, op: typing.Callable[[Value], T], /) -> Some[T] | NothingType:
        ...

    def map_or(self, default: T, f: typing.Callable[[Value], T], /) -> T:
        ...

    def map_or_else(self, default: typing.Callable[[], T], f: typing.Callable[[Value], T], /) -> T:
        ...

    def expect(self, error: str | BaseException, /) -> Value:
        ...


def enc_hook(obj: typing.Any) -> typing.Any:
    if isinstance(obj, NothingType):
        return None
    if isinstance(obj, Some):
        return obj.value
    raise NotImplementedError(f"Not implemented for object of type `{repr_type(type(obj))}`.")


def repr_type(t: type) -> str:
    t = typing.get_origin(t) or t
    return getattr(t, "__name__", repr(t))


def dec_hook(tp: type, obj: typing.Any) -> typing.Any:
    origin_type = typing.get_origin(tp) or tp
    if origin_type is Option:
        if obj is None:
            return NothingType()
        value_type = (typing.get_args(tp) + (typing.Any,))[0]
        with suppress(msgspec.ValidationError):
            value_type = (typing.get_args(tp) + (typing.Any,))[0]
            return msgspec.json.decode(
                msgspec.json.encode({"value": obj}, enc_hook=enc_hook),
                type=Some[value_type],
                dec_hook=dec_hook,
            )
        raise TypeError(
            "Expected `{}` for Option.Some, got `{}`".format(
                repr_type(value_type),
                repr_type(type(obj)),
            )
        )
    raise TypeError(f"Unknown type `{repr_type(tp)}`.")
