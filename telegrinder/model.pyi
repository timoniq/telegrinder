import typing

import msgspec
from kungfu.library.monad.option import Nothing

UNSET: typing.Final = typing.cast("typing.Any", msgspec.UNSET)

def is_none(obj: typing.Any, /) -> typing.TypeIs[Nothing | None]: ...

@typing.overload
def field() -> typing.Any: ...
@typing.overload
def field(*, name: str | None = ...) -> typing.Any: ...
@typing.overload
def field(*, default: typing.Any, name: str | None = ...) -> typing.Any: ...
@typing.overload
def field(*, default_factory: typing.Callable[[], typing.Any], name: str | None = None) -> typing.Any: ...
@typing.overload
def field(*, converter: typing.Callable[[typing.Any], typing.Any], name: str | None = ...) -> typing.Any: ...
@typing.overload
def field(*, default: typing.Any, converter: typing.Callable[[typing.Any], typing.Any], name: str | None = ...) -> typing.Any: ...
@typing.overload
def field(
    *,
    default_factory: typing.Callable[[], typing.Any],
    converter: typing.Callable[[typing.Any], typing.Any],
    name: str | None = None,
) -> typing.Any: ...

class From[T]:
    def __new__(cls, _: T, /) -> typing.Any: ...

@typing.dataclass_transform(field_specifiers=(field,))
class Model(msgspec.Struct, dict=True):
    @classmethod
    def get_fields(cls) -> typing.Mapping[str, msgspec.inspect.Field]: ...
    @classmethod
    def get_optional_fields(cls) -> typing.Iterable[str]: ...
    @classmethod
    def from_data[**P, T](cls: typing.Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T: ...
    @classmethod
    def from_dict(cls, obj: dict[str, typing.Any], /) -> typing.Self: ...
    @classmethod
    def from_raw(cls, raw: str | bytes, /) -> typing.Self: ...
    def to_raw(self) -> str: ...
    def to_dict(
        self,
        *,
        exclude_fields: set[str] | None = None,
    ) -> dict[str, typing.Any]: ...
    def to_full_dict(
        self,
        *,
        exclude_fields: set[str] | None = None,
    ) -> dict[str, typing.Any]: ...

__all__ = ("UNSET", "From", "Model", "field", "is_none")
