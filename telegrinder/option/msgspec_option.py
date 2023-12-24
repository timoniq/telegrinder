import typing

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

    def __eq__(self, __value: typing.Self) -> bool:
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
