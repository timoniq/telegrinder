import keyword
import types
import typing
from functools import cache
from reprlib import recursive_repr

import msgspec
from kungfu.library.monad.option import NOTHING
from msgspec import UNSET

from telegrinder.msgspec_utils import Option, decoder, encoder, is_none, struct_asdict

type From[T] = T

MODEL_CONFIG: typing.Final[dict[str, typing.Any]] = {
    "dict": True,
    "rename": {kw + "_": kw for kw in keyword.kwlist},
}


def field(**kwargs: typing.Any) -> typing.Any:
    if kwargs.get("default") is Ellipsis:
        kwargs["default"] = UNSET

    kwargs.pop("converter", None)
    return msgspec.field(**kwargs)


class Model(msgspec.Struct, **MODEL_CONFIG):
    def __init_subclass__(cls, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        from telegrinder.tools.member_descriptor_proxy import MemberDescriptorProxy

        result = super().__init_subclass__(*args, **kwargs)

        for field_name in getattr(cls, "__slots__", ()):
            setattr(cls, field_name, MemberDescriptorProxy(getattr(cls, field_name)))

        return result

    def __getattribute__(self, name: str, /) -> typing.Any:
        class_ = type(self)
        val = object.__getattribute__(self, name)

        if name not in class_.__struct_fields__:
            return val

        if name in class_.get_optional_fields():
            return NOTHING if val is UNSET else val

        if val is UNSET:
            raise AttributeError(f"{class_.__name__!r} object has no attribute {name!r}")

        return val

    def __post_init__(self) -> None:
        for field, value in struct_asdict(self, exclude_unset=False).items():
            if is_none(value):
                setattr(self, field, UNSET)

    @recursive_repr()
    def __repr__(self) -> str:
        return "{}({})".format(
            type(self).__name__,
            ", ".join(
                f"{f}={val!r}" for f, val in struct_asdict(self, exclude_unset=False, unset_as_nothing=True).items()
            ),
        )

    @classmethod
    @cache
    def get_fields(cls) -> types.MappingProxyType[str, msgspec.inspect.Field]:
        return types.MappingProxyType(
            mapping={f.name: f for f in msgspec.inspect.type_info(cls).fields},  # type: ignore
        )

    @classmethod
    @cache
    def get_optional_fields(cls) -> frozenset[str]:
        return frozenset(
            f.name
            for f in cls.get_fields().values()
            if isinstance(f.type, msgspec.inspect.CustomType) and issubclass(f.type.cls, Option)  # type: ignore
        )

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
            self.__dict__[dct_name] = (  # type: ignore
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
        return self._to_dict("model_as_dict", exclude_fields or set(), full=False)

    def to_full_dict(
        self,
        *,
        exclude_fields: set[str] | None = None,
    ) -> dict[str, typing.Any]:
        return self._to_dict("model_as_full_dict", exclude_fields or set(), full=True)


__all__ = ("UNSET", "From", "Model", "field", "is_none")
