from __future__ import annotations

import dataclasses
import sys
import traceback
import typing

from telegrinder.modules import logger

T = typing.TypeVar("T")
Err = typing.TypeVar("Err", covariant=True)
Value = typing.TypeVar("Value", covariant=True)
ErrorType: typing.TypeAlias = str | BaseException | type[BaseException]


@dataclasses.dataclass
class ErrorTypeFormatter(typing.Generic[T]):
    error_types: tuple[type[T], ...]
    formatter: typing.Callable[[Error[T]], str]


class ResultLoggingFactoryClass:
    """ Sigleton for logging result errors """
    def __init__(self, log: typing.Callable[[typing.Any], None] = lambda _: None):
        self.log = log

    def __call__(self, err: typing.Any) -> None:
        self.log(err)

    def set_log(self, log: typing.Callable[[typing.Any], None]) -> None:
        self.log = log

    @staticmethod
    def format_traceback():
        summary = traceback.extract_stack()
        while len(summary) > 2:
            if summary[-1].filename in (__file__, "<string>"):
                summary.pop()
            else:
                break

        trace = traceback.format_list(summary)
        return "\n".join(trace)


RESULT_ERROR_LOGGER = ResultLoggingFactoryClass()


@dataclasses.dataclass(frozen=True, repr=False)
class Ok(typing.Generic[Value]):
    """`Result.Ok` representing success and containing a value."""

    value: Value

    def __repr__(self) -> str:
        return f"<Result: Ok({self.value!r})>"

    def __bool__(self) -> typing.Literal[True]:
        return True

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

    def expect(self, error: ErrorType, /) -> Value:
        return self.value


@dataclasses.dataclass(repr=False)
class Error(typing.Generic[Err]):
    """`Result.Error` representing error and containing an error value."""

    error: Err

    tb: str | None = None

    def __repr__(self) -> str:
        return (
            "<Result: Error({}: {!r})>".format(
                self.error.__class__.__name__,
                str(self.error),
            )
            if isinstance(self.error, BaseException)
            else f"<Result: Error({self.error!r})>"
        )
    
    def __post_init__(self):
        self.tb = RESULT_ERROR_LOGGER.format_traceback()

    def __bool__(self) -> typing.Literal[False]:
        return False

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

    def expect(self, error: ErrorType, /) -> typing.NoReturn:
        raise error if not isinstance(error, str) else Exception(error)
    
    def __del__(self):
        # TODO: interaction with Error object must update .tb to None
        if self.tb:
            RESULT_ERROR_LOGGER(
                self.tb + "\n  " + repr(self.error),
            )


Result: typing.TypeAlias = Ok[Value] | Error[Err]

__all__ = ("Ok", "Error", "Result")
