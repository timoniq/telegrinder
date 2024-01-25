from __future__ import annotations

import dataclasses
import traceback
import typing

T = typing.TypeVar("T")
Err = typing.TypeVar("Err", covariant=True)
Value = typing.TypeVar("Value", covariant=True)
ErrorType: typing.TypeAlias = str | BaseException | type[BaseException]


class ResultLoggingFactory:
    """Sigleton for logging result errors."""

    def __init__(
        self,
        log: typing.Callable[[str], None] = lambda _: None,
        traceback_formatter: typing.Callable[[], str] | None = None,
    ):
        self._log = log
        self._traceback_formatter = traceback_formatter or self.base_traceback_formatter
 
    def __call__(self, err: typing.Any) -> None:
        self._log(str(err))
    
    @staticmethod
    def base_traceback_formatter() -> str:
        summary = traceback.extract_stack()
        while len(summary) > 2:
            if summary[-1].filename in (__file__, "<string>", "<module>"):
                summary.pop()
            else:
                break
        trace = traceback.format_list(summary)
        return "\n".join(trace)

    def format_traceback(self, error: typing.Any) -> str: 
        return self._traceback_formatter() + "\n\n  " + repr(error)
    
    def set_log(self, log: typing.Callable[[str], None]) -> None:
        self._log = log
    
    def set_traceback_formatter(self, formatter: typing.Callable[[], str]) -> None:
        self._traceback_formatter = formatter


RESULT_ERROR_LOGGER: typing.Final[ResultLoggingFactory] = ResultLoggingFactory()


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
    is_controlled: bool = False

    def __post_init__(self) -> None:
        tb = RESULT_ERROR_LOGGER.format_traceback(self.error)
        self.tb = "Result log\n" + tb

    def __repr__(self) -> str:
        return (
            "<Result: Error({}: {!r})>".format(
                self.error.__class__.__name__,
                str(self.error),
            )
            if isinstance(self.error, BaseException)
            else f"<Result: Error({self.error!r})>"
        )
    
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
    
    def __getattribute__(self, __name: str) -> typing.Any:
        """
        If control over .error was passed to another logic 
        (which is considered passed as soon as .error field is accessed) 
        then there is no need to log on event of result deletion."""

        if __name == "error" and self.tb is not None:
            self.is_controlled = True
        
        return super().__getattribute__(__name)
    
    def __del__(self):
        if self.tb and not self.is_controlled:
            RESULT_ERROR_LOGGER(self.tb)


Result: typing.TypeAlias = Ok[Value] | Error[Err]

__all__ = ("Ok", "Error", "Result", "RESULT_ERROR_LOGGER")
