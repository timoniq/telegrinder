import typing
from contextlib import suppress

import msgspec

from .option import Nothing, NothingType, Some

T = typing.TypeVar("T")
Value = typing.TypeVar("Value")

OptionSome = Some
OptionNothing = Nothing


class Option(typing.Generic[Value]):
    """Option monad for `msgspec.Struct`."""

    __match_args__ = Some.__match_args__
    Nothing: typing.ClassVar = typing.cast(typing.Self, OptionNothing)

    def __init__(self, value: Value | None = None) -> None:
        self.value = value

    def __repr__(self) -> str:
        return self.__get_variant().__repr__()

    def __bool__(self) -> bool:
        return self.__get_variant().__bool__()

    def __eq__(self, __value: object) -> bool:
        return self.__get_variant().__eq__(__value)

    def __get_variant(self) -> OptionSome[Value] | NothingType:
        if self.value is None:
            return OptionNothing
        return OptionSome(self.value)

    def unwrap(self) -> Value:
        return self.__get_variant().unwrap()

    def unwrap_or(self, alternate_value: Value, /) -> Value:
        return self.__get_variant().unwrap_or(alternate_value)

    def unwrap_or_other(self, other: OptionSome[Value], /) -> Value:
        return self.__get_variant().unwrap_or_other(other)

    def map(self, op: typing.Callable[[Value], T], /) -> "Option[T]":
        return self.__get_variant().map(op)  # type: ignore

    def map_or(self, default: T, f: typing.Callable[[Value], T], /) -> T:
        return self.__get_variant().map_or(default, f)

    def map_or_else(self, default: typing.Callable[[], T], f: typing.Callable[[Value], T], /) -> T:
        return self.__get_variant().map_or_else(default, f)

    def expect(self, error: str | BaseException, /) -> Value:
        return self.__get_variant().expect(error)


def enc_hook(obj: typing.Any) -> typing.Any:
    if isinstance(obj, NothingType):
        return None
    if isinstance(obj, Option):
        return obj.value
    raise NotImplementedError(f"Not implemented for object of type `{repr_type(type(obj))}`.")


def repr_type(t: type) -> str:
    t = typing.get_origin(t) or t
    return getattr(t, "__name__", repr(t))


def dec_hook(tp: type, obj: typing.Any) -> typing.Any:
    origin_type = typing.get_origin(tp) or tp
    if origin_type is Option:
        if obj is None:
            return Option()
        value_type = (typing.get_args(tp) + (typing.Any,))[0]
        with suppress(msgspec.ValidationError):
            value_type = (typing.get_args(tp) + (typing.Any,))[0]
            some = msgspec.json.decode(
                msgspec.json.encode({"value": obj}, enc_hook=enc_hook),
                type=OptionSome[value_type],
                dec_hook=dec_hook,
            )
            return Option(some.value)
        raise TypeError(
            "Expected `{}` for Option.Some, got `{}`".format(
                repr_type(value_type),
                repr_type(type(obj)),
            )
        )
    raise TypeError(f"Unknown type `{repr_type(tp)}`.")
