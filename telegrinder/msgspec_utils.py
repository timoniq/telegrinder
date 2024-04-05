import typing

import fntypes.option
import msgspec
from fntypes.co import Error, Ok, Result, Variative

T = typing.TypeVar("T")
Ts = typing.TypeVarTuple("Ts")

if typing.TYPE_CHECKING:
    from datetime import datetime

    from fntypes.option import Option
else:
    from datetime import datetime as dt

    Value = typing.TypeVar("Value")

    datetime = type("datetime", (dt,), {})

    class OptionMeta(type):
        def __instancecheck__(cls, __instance: typing.Any) -> bool:
            return isinstance(__instance, fntypes.option.Some | fntypes.option.Nothing)


    class Option(typing.Generic[Value], metaclass=OptionMeta):
        pass

DecHook: typing.TypeAlias = typing.Callable[[type[T], typing.Any], object]
EncHook: typing.TypeAlias = typing.Callable[[T], typing.Any]

Nothing: typing.Final[fntypes.option.Nothing] = fntypes.option.Nothing()


def get_origin(t: type[T]) -> type[T]:
    return typing.cast(T, typing.get_origin(t)) or t


def repr_type(t: type) -> str:
    return getattr(t, "__name__", repr(get_origin(t)))


def msgspec_convert(obj: typing.Any, t: type[T]) -> Result[T, msgspec.ValidationError]:
    try:
        return Ok(decoder.convert(obj, type=t, strict=True))
    except msgspec.ValidationError as exc:
        return Error(exc)


def option_dec_hook(tp: type[Option[typing.Any]], obj: typing.Any) -> Option[typing.Any]:
    if obj is None:
        return Nothing
    generic_args = typing.get_args(tp)
    value_type: typing.Any | type[typing.Any] = typing.Any if not generic_args else generic_args[0]
    return msgspec_convert({"value": obj}, fntypes.option.Some[value_type]).unwrap()


def variative_dec_hook(tp: type[Variative], obj: typing.Any) -> Variative:
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
            repr_type(obj.__class__),
            " | ".join(map(repr_type, union_types)),
        )
    )


class Decoder:
    def __init__(self) -> None:
        self.dec_hooks: dict[typing.Any, DecHook[typing.Any]] = {
            Option: option_dec_hook,
            Variative: variative_dec_hook,
            datetime: lambda t, obj: t.fromtimestamp(obj),
        }

    def add_dec_hook(self, t: T):  # type: ignore
        def decorator(func: DecHook[T]) -> DecHook[T]:
            return self.dec_hooks.setdefault(get_origin(t), func)  # type: ignore
        
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
    
    @typing.overload
    def decode(self, buf: str | bytes) -> typing.Any:
        ...
    
    @typing.overload
    def decode(self, buf: str | bytes, *, strict: bool = True) -> typing.Any:
        ...

    @typing.overload
    def decode(
        self,
        buf: str | bytes,
        *,
        type: type[T],
        strict: bool = True,
    ) -> T:
        ...

    def decode(
        self,
        buf: str | bytes,
        *,
        type: type[T] = typing.Any,  # type: ignore
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
        self.enc_hooks: dict[typing.Any, EncHook[typing.Any]] = {
            fntypes.option.Some: lambda opt: opt.value,
            fntypes.option.Nothing: lambda _: None,
            Variative: lambda variative: variative.v,
            datetime: lambda date: int(date.timestamp()),
        }

    def add_dec_hook(self, tp: type[T]):
        def decorator(func: EncHook[T]) -> EncHook[T]:
            return self.enc_hooks.setdefault(get_origin(tp), func)
        
        return decorator
    
    def enc_hook(self, obj: object) -> object:
        origin_type = get_origin(obj.__class__)
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
    def encode(self, obj: typing.Any, *, as_str: typing.Literal[True] = True) -> str:
        ...

    @typing.overload
    def encode(self, obj: typing.Any, *, as_str: typing.Literal[False] = False) -> bytes:
        ...

    def encode(self, obj: typing.Any, *, as_str: bool = True) -> str | bytes:
        buf = msgspec.json.encode(obj, enc_hook=self.enc_hook)
        return buf.decode() if as_str else buf


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
    "variative_dec_hook",
    "datetime",
    "decoder",
    "encoder",
)
