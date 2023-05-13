import dataclasses
import typing

T = typing.TypeVar("T")
T_co = typing.TypeVar("T_co", covariant=True)
E_co = typing.TypeVar("E_co", covariant=True, bound=BaseException)


@dataclasses.dataclass(frozen=True)
class Ok(typing.Generic[T_co]):
    value: T_co

    def unwrap(self) -> T_co:
        return self.value
    
    def unwrap_or(self, alternate_value: object) -> T_co:
        return self.unwrap()
    
    def __repr__(self) -> str:
        return f"<Result (Ok: {self.value!r})>"


@dataclasses.dataclass(frozen=True)
class Error(typing.Generic[E_co]):
    error: E_co

    def unwrap(self) -> typing.NoReturn:
        raise self.error
    
    def unwrap_or(self, alternate_value: T) -> T:
        return alternate_value

    def __repr__(self) -> str:
        return f"<Result (Error: {self.error!r})>"


Result = Ok[T_co] | Error[E_co]
