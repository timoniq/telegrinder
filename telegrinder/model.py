import keyword
import types
import typing
from reprlib import recursive_repr

import msgspec
from fntypes.co import Nothing, Some

from telegrinder.msgspec_utils import Option, decoder, encoder, struct_asdict

UNSET: typing.Final[typing.Any] = typing.cast("typing.Any", msgspec.UNSET)
"""See [DOCS](https://jcristharif.com/msgspec/api.html#unset) about `msgspec.UNSET`."""
MODEL_CONFIG: typing.Final[dict[str, typing.Any]] = {
    "dict": True,
    "rename": {kw + "_": kw for kw in keyword.kwlist},
}
INSPECTED_MODEL_FIELDS_KEY: typing.Final[str] = "__inspected_struct_fields__"


def is_none(obj: typing.Any, /) -> typing.TypeGuard[Nothing | None]:
    return isinstance(obj, types.NoneType | Nothing)


if typing.TYPE_CHECKING:

    @typing.overload
    def field() -> typing.Any: ...

    @typing.overload
    def field(*, name: str | None = ...) -> typing.Any: ...

    @typing.overload
    def field(*, default: typing.Any, name: str | None = ...) -> typing.Any: ...

    @typing.overload
    def field(
        *,
        default_factory: typing.Callable[[], typing.Any],
        name: str | None = None,
    ) -> typing.Any: ...

    @typing.overload
    def field(
        *,
        converter: typing.Callable[[typing.Any], typing.Any],
        name: str | None = ...,
    ) -> typing.Any: ...

    @typing.overload
    def field(
        *,
        default: typing.Any,
        converter: typing.Callable[[typing.Any], typing.Any],
        name: str | None = ...,
    ) -> typing.Any: ...

    @typing.overload
    def field(
        *,
        default_factory: typing.Callable[[], typing.Any],
        converter: typing.Callable[[typing.Any], typing.Any],
        name: str | None = None,
    ) -> typing.Any: ...

    def field(
        *,
        default=...,
        default_factory=...,
        name=...,
        converter=...,
    ) -> typing.Any: ...

    class From[T]:
        def __new__(cls, _: T, /) -> typing.Any: ...
else:
    from msgspec import field as _field

    type From[T] = T

    def field(**kwargs):
        if "default" in kwargs and (default := kwargs["default"]) is Ellipsis:
            kwargs["default"] = UNSET

        kwargs.pop("converter", None)
        return _field(**kwargs)


@typing.dataclass_transform(field_specifiers=(field,))
class Model(msgspec.Struct, **MODEL_CONFIG):
    if not typing.TYPE_CHECKING:

        def __post_init__(self):
            for field in self.__struct_fields__:
                if is_none(getattr(self, field)):
                    setattr(self, field, UNSET)

        def __getattribute__(self, name, /):
            val = super().__getattribute__(name)
            field_info = super().__getattribute__("get_field")(name).unwrap_or_none()

            if (
                field_info is not None
                and isinstance(field_info.type, msgspec.inspect.CustomType)
                and issubclass(field_info.type.cls, Option)
            ):
                return Nothing() if val is UNSET else val

            if val is UNSET:
                raise AttributeError(f"{self.__class__.__name__!r} object has no attribute {name!r}")

            return val

        @recursive_repr()
        def __repr__(self) -> str:
            return "{}({})".format(
                type(self).__name__,
                ", ".join(
                    f"{f}={value!r}"
                    for f in self.__struct_fields__
                    if (value := getattr(self, f)) is not UNSET  # excluding UNSET fields
                ),
            )

    @classmethod
    def get_fields(cls) -> types.MappingProxyType[str, msgspec.inspect.Field]:
        if (model_fields := getattr(cls, INSPECTED_MODEL_FIELDS_KEY, None)) is not None:
            return model_fields

        model_fields = types.MappingProxyType[str, msgspec.inspect.Field](
            {f.name: f for f in msgspec.inspect.type_info(cls).fields},  # type: ignore
        )
        setattr(cls, INSPECTED_MODEL_FIELDS_KEY, model_fields)
        return model_fields

    @classmethod
    def get_field(cls, field_name: str, /) -> Option[msgspec.inspect.Field]:
        if (f := cls.get_fields().get(field_name)) is not None:
            return Some(f)
        return Nothing()

    @classmethod
    def from_data[**P, T](cls: typing.Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
        return decoder.convert(msgspec.structs.asdict(cls(*args, **kwargs)), type=cls)  # type: ignore

    @classmethod
    def from_dict(cls, obj: dict[str, typing.Any], /) -> typing.Self:
        return decoder.convert(obj, type=cls)

    @classmethod
    def from_raw(cls, raw: str | bytes, /) -> typing.Self:
        return decoder.decode(raw, type=cls)

    def _to_dict(
        self,
        dct_name: str,
        exclude_fields: set[str],
        full: bool,
    ) -> dict[str, typing.Any]:
        if dct_name not in self.__dict__:
            self.__dict__[dct_name] = (
                struct_asdict(self)
                if not full
                else encoder.to_builtins(self.to_dict(exclude_fields=exclude_fields), order="deterministic")
            )

        if not exclude_fields:
            return self.__dict__[dct_name]

        return {key: value for key, value in self.__dict__[dct_name].items() if key not in exclude_fields}

    def to_raw(self) -> str:
        return encoder.encode(self)

    def to_dict(
        self,
        *,
        exclude_fields: set[str] | None = None,
    ) -> dict[str, typing.Any]:
        """:param exclude_fields: Model field names to exclude from the dictionary representation of this model.
        :return: A dictionary representation of this model.
        """
        return self._to_dict("model_as_dict", exclude_fields or set(), full=False)

    def to_full_dict(
        self,
        *,
        exclude_fields: set[str] | None = None,
    ) -> dict[str, typing.Any]:
        """:param exclude_fields: Model field names to exclude from the dictionary representation of this model.
        :return: A dictionary representation of this model including all models, structs, custom types.
        """
        return self._to_dict("model_as_full_dict", exclude_fields or set(), full=True)


__all__ = ("MODEL_CONFIG", "Model", "UNSET", "field")
