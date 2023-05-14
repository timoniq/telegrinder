import dataclasses
import typing
import typing_extensions

T = typing.TypeVar("T")
T_co = typing.TypeVar("T_co", covariant=True)
E_co = typing.TypeVar("E_co", covariant=True, bound=BaseException)


@dataclasses.dataclass(frozen=True)
class Ok(typing.Generic[T_co]):
    value: T_co

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"<Result: Ok({self.value!r})>"

    def unwrap(self) -> T_co:
        return self.value

    def unwrap_or(self, alternate_value: object) -> T_co:
        return self.unwrap()

    def map(self, op: typing.Callable[[T_co], T_co]) -> typing_extensions.Self[T_co]:
        return Ok(op(self.value))


@dataclasses.dataclass(frozen=True)
class Error(typing.Generic[E_co]):
    error: E_co

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return "<Result: Error({}: {})>".format(
            self.error.__class__.__name__,
            str(self.error),
        )

    def unwrap(self) -> typing.NoReturn:
        raise self.error

    def unwrap_or(self, alternate_value: T) -> T:
        return alternate_value

    def map(self, op: object) -> typing_extensions.Self[E_co]:
        return self


Result = Ok[T_co] | Error[E_co]
