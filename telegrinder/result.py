from __future__ import annotations

import dataclasses
import typing

T = typing.TypeVar("T")
Err = typing.TypeVar("Err", covariant=True)
Value = typing.TypeVar("Value", covariant=True)


@dataclasses.dataclass(frozen=True, repr=False)
class Ok(typing.Generic[Value]):
    """`Result.Ok` representing success and containing a value."""

    value: Value

    def __repr__(self) -> str:
        return f"<Result: Ok({self.value!r})>"

    def unwrap(self) -> Value:
        return self.value

    def unwrap_or(self, alternate_value: object, /) -> Value:
        return self.unwrap()

    def unwrap_or_else(self, f: object, /) -> Value:
        return self.value

    def unwrap_or_other(self, other: object, /) -> Value:
        return self.value

    def map(self, op: typing.Callable[[Value], T], /) -> Ok[T]:
        return Ok(op(self.value))

    def map_or(self, default: T, f: typing.Callable[[Value], T], /) -> T:
        return f(self.value)

    def map_or_else(self, default: object, f: typing.Callable[[Value], T], /) -> T:
        return f(self.value)

    def expect(self, msg: str, /) -> Value:
        return self.value


@dataclasses.dataclass(frozen=True, repr=False)
class Error(typing.Generic[Err]):
    """`Result.Error` representing error and containing an error value."""

    error: Err

    def __repr__(self) -> str:
        return (
            "<Result: Error({}: {})>".format(
                self.error.__class__.__name__,
                str(self.error),
            )
            if isinstance(self.error, BaseException)
            else f"<Result: Error({self.error!r})>"
        )

    def unwrap(self) -> typing.NoReturn:
        raise (
            self.error
            if isinstance(self.error, BaseException)
            else Exception(self.error)
        )

    def unwrap_or(self, alternate_value: T, /) -> T:
        return alternate_value

    def unwrap_or_else(self, f: typing.Callable[[Err], T], /) -> T:
        return f(self.error)

    def unwrap_or_other(self, other: Result[T, object], /) -> T:
        return other.unwrap()

    def map(self, op: object, /) -> typing.Self:
        return self

    def map_or(self, default: T, f: object, /) -> T:
        return default

    def map_or_else(self, default: typing.Callable[[Err], T], f: object, /) -> T:
        return default(self.error)

    def expect(self, msg: str, /) -> typing.NoReturn:
        raise Exception(msg)


Result = Ok[Value] | Error[Err]
