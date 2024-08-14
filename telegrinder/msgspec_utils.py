import dataclasses
import typing

import fntypes.option
import fntypes.result
import msgspec
from fntypes.co import Error, Ok, Result, Variative

if typing.TYPE_CHECKING:
    from datetime import datetime

    from fntypes.option import Option
    from fntypes.result import Result
else:
    from datetime import datetime as dt

    Value = typing.TypeVar("Value")
    Err = typing.TypeVar("Err")

    datetime = type("datetime", (dt,), {})

    class OptionMeta(type):
        def __instancecheck__(cls, __instance: typing.Any) -> bool:
            return isinstance(__instance, fntypes.option.Some | fntypes.option.Nothing)

    class ResultMeta(type):
        def __instancecheck__(cls, __instance: typing.Any) -> bool:
            return isinstance(__instance, fntypes.result.Ok | fntypes.result.Error)

    class Option(typing.Generic[Value], metaclass=OptionMeta):
        pass

    class Result(typing.Generic[Value, Err], metaclass=ResultMeta):
        pass


T = typing.TypeVar("T")

DecHook: typing.TypeAlias = typing.Callable[[type[T], typing.Any], typing.Any]
EncHook: typing.TypeAlias = typing.Callable[[T], typing.Any]

Nothing: typing.Final[fntypes.option.Nothing] = fntypes.option.Nothing()


def get_origin(t: type[T]) -> type[T]:
    return typing.cast(T, typing.get_origin(t)) or t


def repr_type(t: type) -> str:
    return getattr(t, "__name__", repr(get_origin(t)))


def msgspec_convert(obj: typing.Any, t: type[T]) -> Result[T, str]:
    try:
        return Ok(decoder.convert(obj, type=t, strict=True))
    except msgspec.ValidationError:
        return Error(
            "Expected object of type `{}`, got `{}`.".format(
                repr_type(t),
                repr_type(type(obj)),
            )
        )


def msgspec_to_builtins(
    obj: typing.Any,
    *,
    str_keys: bool = False,
    builtin_types: typing.Iterable[type[typing.Any]] | None = None,
    order: typing.Literal["deterministic", "sorted"] | None = None,
) -> typing.Any:
    return encoder.to_builtins(**locals())


def option_dec_hook(tp: type[Option[typing.Any]], obj: typing.Any) -> Option[typing.Any]:
    orig_type = get_origin(tp)
    (value_type,) = typing.get_args(tp) or (typing.Any,)

    if obj is None and orig_type in (fntypes.option.Nothing, Option):
        return fntypes.option.Nothing()
    return fntypes.option.Some(decoder.convert(obj, type=value_type))


def result_dec_hook(
    tp: type[Result[typing.Any, typing.Any]], obj: typing.Any
) -> Result[typing.Any, typing.Any]:
    if not isinstance(obj, dict):
        raise TypeError(f"Cannot parse to `fntypes.Result` object of type `{repr_type(type(obj))}`.")

    orig_type = get_origin(tp)
    (first_type, second_type) = (
        typing.get_args(tp) + (typing.Any,) if len(typing.get_args(tp)) == 1 else typing.get_args(tp)
    ) or (typing.Any, typing.Any)

    if orig_type is Ok and "ok" in obj:
        return Ok(decoder.convert(obj["ok"], type=first_type))

    if orig_type is Error and "error" in obj:
        return Error(decoder.convert(obj["error"], type=first_type))

    if orig_type is Result:
        match obj:
            case {"ok": ok}:
                return Ok(decoder.convert(ok, type=first_type))
            case {"error": error}:
                return Error(decoder.convert(error, type=second_type))

    raise msgspec.ValidationError(f"Cannot parse object `{obj!r}` to `fntypes.Result`.")


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
            *sorted(
                struct_fields_match_sums,
                key=lambda k: struct_fields_match_sums[k],
                reverse=reverse,
            ),
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


@typing.runtime_checkable
class DataclassInstance(typing.Protocol):
    __dataclass_fields__: typing.ClassVar[dict[str, dataclasses.Field[typing.Any]]]


class Decoder:
    """Class `Decoder` for `msgspec` module with decode hook
    for objects with the specified type.

    ```
    import enum

    from datetime import datetime as dt

    class Digit(enum.IntEnum):
        ONE = 1
        TWO = 2
        THREE = 3

    decoder = Encoder()
    decoder.dec_hooks[dt] = lambda t, timestamp: t.fromtimestamp(timestamp)

    decoder.dec_hook(dt, 1713354732)  #> datetime.datetime(2024, 4, 17, 14, 52, 12)

    decoder.convert("123", type=int, strict=False)  #> 123
    decoder.convert(1, type=Digit)  #> <Digit.ONE: 1>

    decoder.decode(b'{"digit":3}', type=dict[str, Digit])  #> {'digit': <Digit.THREE: 3>}
    ```
    """

    def __init__(self) -> None:
        self.dec_hooks: dict[typing.Any, DecHook[typing.Any]] = {
            Result: result_dec_hook,
            Option: option_dec_hook,
            Variative: variative_dec_hook,
            datetime: lambda t, obj: t.fromtimestamp(obj),
            fntypes.result.Error: result_dec_hook,
            fntypes.result.Ok: result_dec_hook,
            fntypes.option.Some: option_dec_hook,
            fntypes.option.Nothing: option_dec_hook,
        }

    def __repr__(self) -> str:
        return "<{}: dec_hooks={!r}>".format(
            self.__class__.__name__,
            self.dec_hooks,
        )

    def add_dec_hook(self, t: T):  # type: ignore
        def decorator(func: DecHook[T]) -> DecHook[T]:
            return self.dec_hooks.setdefault(get_origin(t), func)  # type: ignore

        return decorator

    def dec_hook(self, tp: type[typing.Any], obj: object) -> object:
        origin_type = t if isinstance((t := get_origin(tp)), type) else type(t)
        if origin_type not in self.dec_hooks:
            raise TypeError(
                f"Unknown type `{repr_type(origin_type)}`. You can implement decode hook for this type."
            )
        return self.dec_hooks[origin_type](tp, obj)

    def convert(
        self,
        obj: object,
        *,
        type: type[T] = dict,
        strict: bool = True,
        from_attributes: bool = False,
        builtin_types: typing.Iterable[type[typing.Any]] | None = None,
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
    def decode(self, buf: str | bytes) -> typing.Any: ...

    @typing.overload
    def decode(self, buf: str | bytes, *, type: type[T]) -> T: ...

    @typing.overload
    def decode(
        self,
        buf: str | bytes,
        *,
        type: type[T],
        strict: bool = True,
    ) -> T: ...

    def decode(self, buf, *, type=object, strict=True):
        return msgspec.json.decode(
            buf,
            type=typing.Any if type is object else type,
            strict=strict,
            dec_hook=self.dec_hook,
        )


class Encoder:
    """Class `Encoder` for `msgspec` module with encode hooks for objects.

    ```
    from datetime import datetime as dt

    encoder = Encoder()
    encoder.enc_hooks[dt] = lambda d: int(d.timestamp())

    encoder.enc_hook(dt.now())  #> 1713354732
    encoder.encode({'digit': Digit.ONE})  #> '{"digit":1}'
    ```
    """

    def __init__(self) -> None:
        self.enc_hooks: dict[typing.Any, EncHook[typing.Any]] = {
            fntypes.option.Some: lambda opt: opt.value,
            fntypes.option.Nothing: lambda _: None,
            fntypes.result.Ok: lambda ok: {"ok": ok.value},
            fntypes.result.Error: lambda err: {
                "error": (str(err.error) if isinstance(err.error, BaseException) else err.error)
            },
            Variative: lambda variative: variative.v,
            datetime: lambda date: int(date.timestamp()),
        }

    def __repr__(self) -> str:
        return "<{}: enc_hooks={!r}>".format(
            self.__class__.__name__,
            self.enc_hooks,
        )

    def add_dec_hook(self, t: type[T]):
        def decorator(func: EncHook[T]) -> EncHook[T]:
            encode_hook = self.enc_hooks.setdefault(get_origin(t), func)
            return func if encode_hook is not func else encode_hook

        return decorator

    def enc_hook(self, obj: object) -> object:
        origin_type = get_origin(obj.__class__)
        if origin_type not in self.enc_hooks:
            raise NotImplementedError(
                f"Not implemented encode hook for object of type `{repr_type(origin_type)}`."
            )
        return self.enc_hooks[origin_type](obj)

    @typing.overload
    def encode(self, obj: typing.Any) -> str: ...

    @typing.overload
    def encode(self, obj: typing.Any, *, as_str: typing.Literal[True]) -> str: ...

    @typing.overload
    def encode(self, obj: typing.Any, *, as_str: typing.Literal[False]) -> bytes: ...

    def encode(self, obj: typing.Any, *, as_str: bool = True) -> str | bytes:
        buf = msgspec.json.encode(obj, enc_hook=self.enc_hook)
        return buf.decode() if as_str else buf

    def to_builtins(
        self,
        obj: typing.Any,
        *,
        str_keys: bool = False,
        builtin_types: typing.Iterable[type[typing.Any]] | None = None,
        order: typing.Literal["deterministic", "sorted"] | None = None,
    ) -> typing.Any:
        return msgspec.to_builtins(
            obj,
            str_keys=str_keys,
            builtin_types=builtin_types,
            enc_hook=self.enc_hook,
            order=order,
        )


decoder: typing.Final[Decoder] = Decoder()
encoder: typing.Final[Encoder] = Encoder()


__all__ = (
    "Decoder",
    "Encoder",
    "Nothing",
    "Option",
    "datetime",
    "decoder",
    "encoder",
    "get_origin",
    "msgspec_convert",
    "msgspec_to_builtins",
    "option_dec_hook",
    "repr_type",
    "variative_dec_hook",
)
