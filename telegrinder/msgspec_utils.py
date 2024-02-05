import typing

import msgspec
from fntypes.co import Error, Ok, Result, Some, Union
from fntypes.option import Nothing as NothingType

T = typing.TypeVar("T")
Value = typing.TypeVar("Value")
Ts = typing.TypeVarTuple("Ts")

DecHook: typing.TypeAlias = typing.Callable[[type[T], object], object]
EncHook: typing.TypeAlias = typing.Callable[[T], object]

Nothing: typing.Final[NothingType] = NothingType()


def get_origin(t: type[T]) -> type[T]:
    return typing.cast(T, typing.get_origin(t)) or t


def repr_type(t: type) -> str:
    return getattr(t, "__name__", repr(get_origin(t)))


def msgspec_convert(obj: typing.Any, t: type[T]) -> Result[T, msgspec.ValidationError]:
    try:
        return Ok(decoder.convert(obj, type=t, strict=True))
    except msgspec.ValidationError as exc:
        return Error(exc)


def option_dec_hook(tp: type["Option[typing.Any]"], obj: typing.Any) -> typing.Any:
    if obj is None:
        return Nothing
    generic_args = typing.get_args(tp)
    value_type: typing.Any | type[typing.Any] = typing.Any if not generic_args else generic_args[0]
    return msgspec_convert({"value": obj}, Some[value_type]).unwrap()


def union_dec_hook(tp: type[Union], obj: typing.Any) -> Union:
    union_types = typing.get_args(tp)
    
    if isinstance(obj, dict):
        struct_fields_match_sums: dict[type[msgspec.Struct], int] = {
            m: sum(1 for k in obj if k in m.__struct_fields__)
            for m in union_types
            if issubclass(get_origin(m), msgspec.Struct)
        }
        union_types = tuple(t for t in union_types if t not in struct_fields_match_sums)
        reverse = False

        if len(set(struct_fields_match_sums.values())) != len(struct_fields_match_sums.values()):
            struct_fields_match_sums = {m: len(m.__struct_fields__) for m in struct_fields_match_sums}
            reverse = True

        union_types = (
            *sorted(struct_fields_match_sums, key=lambda k: struct_fields_match_sums[k], reverse=reverse),
            *union_types,
        )
    
    for t in union_types:
        match msgspec_convert(obj, t):
            case Ok(value):
                return tp(value)

    raise TypeError(
        "Object of type `{}` does not belong to types `{}`".format(
            repr_type(type(obj)),
            " | ".join(map(repr_type, union_types)),
        )
    )


def option_enc_hook(obj: "Option[typing.Any]") -> typing.Any | None:
    return obj.value if isinstance(obj, Some) else None


def union_enc_hook(obj: Union) -> typing.Any:
    return typing.cast(typing.Any, obj.value)


class Decoder:
    def __init__(self) -> None:
        self.dec_hooks: dict[type, DecHook[typing.Any]] = {
            Option: option_dec_hook,
            Union: union_dec_hook,
        }

    def add_dec_hook(self, tp: type[T]):
        def decorator(func: DecHook[T]) -> DecHook[T]:
            return self.dec_hooks.setdefault(get_origin(tp), func)
        
        return decorator
    
    def dec_hook(self, tp: type[typing.Any], obj: object) -> object:
        origin_type = t if isinstance((t := get_origin(tp)), type) else type(t)
        if origin_type not in self.dec_hooks:
            raise TypeError(
                f"Unknown type `{repr_type(origin_type)}`. "
                "You can implement decode hook for this type."
            )
        return self.dec_hooks[origin_type](tp, obj)
    
    def convert(
        self,
        obj: object,
        *,
        type: type[T] = dict,
        strict: bool = True,
        from_attributes: bool = False,
        builtin_types: typing.Iterable[type] | None = None,
        str_keys: bool = False,
    ) -> T:
        return msgspec.convert(
            obj,
            type,
            strict=strict,
            from_attributes=from_attributes,
            dec_hook=self.dec_hook,
            builtin_types=builtin_types,
            str_keys=str_keys,
        )

    def decode(
        self,
        buf: str | bytes,
        *,
        type: type[T] = dict,
        strict: bool = True,
    ) -> T:
        return msgspec.json.decode(
            buf,
            type=type,
            strict=strict,
            dec_hook=self.dec_hook,
        )


class Encoder:
    def __init__(self) -> None:
        self.enc_hooks: dict[type, EncHook] = {
            Some: option_enc_hook,
            NothingType: option_enc_hook,
            Union: union_enc_hook,
        }

    def add_dec_hook(self, tp: type[T]):
        def decorator(func: EncHook[T]) -> EncHook[T]:
            return self.enc_hooks.setdefault(get_origin(tp), func)
        
        return decorator
    
    def enc_hook(self, obj: object) -> object:
        origin_type = get_origin(type(obj))
        if origin_type not in self.enc_hooks:
            raise NotImplementedError(
                "Not implemented encode hook for "
                f"object of type `{repr_type(origin_type)}`."
            )
        return self.enc_hooks[origin_type](obj)
    
    @typing.overload
    def encode(self, obj: typing.Any) -> str:
        ...

    @typing.overload
    def encode(self, obj: typing.Any, *, as_str: bool = False) -> bytes:
        ...

    def encode(self, obj: typing.Any, *, as_str: bool = True) -> str | bytes:
        buf = msgspec.json.encode(obj, enc_hook=self.enc_hook)
        return buf.decode() if as_str else buf


@typing.runtime_checkable
class Option(typing.Protocol[Value]):
    """Option protocol for `msgspec.Struct`."""

    def __repr__(self) -> str:
        ...

    def __bool__(self) -> bool:
        ...

    def __eq__(self, other: typing.Self) -> bool:
        ...

    def unwrap(self) -> Value:
        ...

    def unwrap_or(self, alternate_value: Value, /) -> Value:
        ...

    def unwrap_or_other(self, other: Some[T], /) -> Value | T:
        ...

    def map(self, op: typing.Callable[[Value], T], /) -> Some[T] | NothingType:
        ...

    def map_or(self, default: T, f: typing.Callable[[Value], T], /) -> T:
        ...

    def map_or_else(self, default: typing.Callable[[None], T], f: typing.Callable[[Value], T], /) -> T:
        ...

    def expect(self, error: typing.Any, /) -> Value:
        ...

    def unwrap_or_none(self) -> Value | None:
        ...


decoder: typing.Final[Decoder] = Decoder()
encoder: typing.Final[Encoder] = Encoder()


__all__ = (
    "Decoder",
    "Encoder",
    "Option",
    "Nothing",
    "get_origin",
    "repr_type",
    "msgspec_convert",
    "option_dec_hook",
    "option_enc_hook",
    "union_dec_hook",
    "decoder",
    "encoder",
)
