import typing
from contextlib import contextmanager

import fntypes.option
import fntypes.result
import msgspec
from fntypes.co import Error, Ok, Variative

if typing.TYPE_CHECKING:
    from datetime import datetime

    from fntypes.option import Option

    from telegrinder.tools.magic import magic_bundle
    from telegrinder.tools.repr import fullname

    def get_class_annotations(obj: typing.Any, /) -> dict[str, typing.Any]: ...

    def get_type_hints(obj: typing.Any, /) -> dict[str, typing.Any]: ...

else:
    from datetime import datetime as dt

    from msgspec._utils import get_class_annotations, get_type_hints

    datetime = type("datetime", (dt,), {})

    class OptionMeta(type):
        def __instancecheck__(cls, __instance: typing.Any) -> bool:
            return isinstance(__instance, (fntypes.option.Some | fntypes.option.Nothing, msgspec.UnsetType))

    class Option[Value](metaclass=OptionMeta):
        pass

    def magic_bundle(*args, **kwargs):
        from telegrinder.tools.magic import magic_bundle

        return magic_bundle(*args, **kwargs)

    def fullname(*args, **kwargs):
        from telegrinder.tools.repr import fullname

        return fullname(*args, **kwargs)


type DecHook[T] = typing.Callable[typing.Concatenate[type[T], typing.Any, ...], typing.Any]
type EncHook[T] = typing.Callable[typing.Concatenate[T, ...], typing.Any]


def get_origin[T](t: type[T], /) -> type[T]:
    t_ = typing.get_origin(t) or t
    t_ = type(t_) if not isinstance(t_, type) else t_
    return typing.cast("type[T]", t_)


def is_common_type(type_: typing.Any) -> typing.TypeGuard[type[typing.Any]]:
    if not isinstance(type_, type):
        return False
    return (
        type_ in (str, int, float, bool, None, Variative)
        or issubclass(type_, msgspec.Struct)
        or hasattr(type_, "__dataclass_fields__")
    )


def struct_as_dict(struct: msgspec.Struct, /) -> dict[str, typing.Any]:
    return {
        k: v
        for k, v in msgspec.structs.asdict(struct).items()
        if not isinstance(v, msgspec.UnsetType | type(None) | fntypes.option.Nothing)
    }


def type_check(obj: typing.Any, t: typing.Any) -> bool:
    return (
        isinstance(obj, t)
        if isinstance(t, type) and issubclass(t, msgspec.Struct)
        else type(obj) in t
        if isinstance(t, tuple)
        else type(obj) is t
    )


def msgspec_convert[T](obj: typing.Any, t: type[T]) -> fntypes.result.Result[T, str]:
    try:
        return Ok(decoder.convert(obj, type=t, strict=True))
    except msgspec.ValidationError:
        return Error(
            "Expected object of type `{}`, got `{}`.".format(
                fullname(t),
                fullname(obj),
            )
        )


def msgspec_to_builtins(
    obj: typing.Any,
    *,
    str_keys: bool = False,
    builtin_types: typing.Iterable[type[typing.Any]] | None = None,
    order: typing.Literal["deterministic", "sorted"] | None = None,
) -> fntypes.result.Result[typing.Any, msgspec.ValidationError]:
    try:
        return Ok(encoder.to_builtins(**locals()))
    except msgspec.ValidationError as exc:
        return Error(exc)


def option_dec_hook(
    tp: type[Option[typing.Any]],
    obj: typing.Any,
) -> fntypes.option.Option[typing.Any] | msgspec.UnsetType:
    if obj is msgspec.UNSET:
        return obj

    if obj is None or isinstance(obj, fntypes.option.Nothing):
        return fntypes.option.Nothing()

    (value_type,) = typing.get_args(tp) or (typing.Any,)
    orig_value_type = typing.get_origin(value_type) or value_type
    orig_obj = obj

    if not isinstance(orig_obj, dict | list) and is_common_type(orig_value_type):
        if orig_value_type is Variative:
            obj = value_type(orig_obj)  # type: ignore
            orig_value_type = typing.get_args(value_type)

        if not type_check(orig_obj, orig_value_type):
            raise TypeError(f"Expected `{fullname(orig_value_type)}`, got `{fullname(orig_obj)}`.")

        return fntypes.option.Some(obj)

    return fntypes.option.Some(decoder.convert(orig_obj, type=value_type))


def variative_dec_hook(tp: type[Variative], obj: typing.Any) -> Variative:
    union_types = typing.get_args(tp)

    if isinstance(obj, dict):
        models_struct_fields: dict[type[msgspec.Struct], int] = {
            m: sum(1 for k in obj if k in m.__struct_fields__)
            for m in union_types
            if issubclass(get_origin(m), msgspec.Struct)
        }
        union_types = tuple(t for t in union_types if t not in models_struct_fields)
        reverse = False

        if len(set(models_struct_fields.values())) != len(models_struct_fields.values()):
            models_struct_fields = {m: len(m.__struct_fields__) for m in models_struct_fields}
            reverse = True

        union_types = (
            *sorted(
                models_struct_fields,
                key=lambda k: models_struct_fields[k],
                reverse=reverse,
            ),
            *union_types,
        )

    for t in union_types:
        if not isinstance(obj, dict | list) and is_common_type(t) and type_check(obj, t):
            return tp(obj)
        match msgspec_convert(obj, t):
            case Ok(value):
                return tp(value)
            case Error(_):
                continue

    raise TypeError(
        "Object of type `{}` does not belong to types `{}`".format(
            fullname(obj),
            " | ".join(map(fullname, union_types)),
        )
    )


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

    decoder = Decoder()
    decoder.dec_hooks[dt] = lambda t, timestamp: t.fromtimestamp(timestamp)

    decoder.dec_hook(dt, 1713354732)  #> datetime.datetime(2024, 4, 17, 14, 52, 12)

    decoder.convert("123", type=int, strict=False)  #> 123
    decoder.convert(1, type=Digit)  #> <Digit.ONE: 1>

    decoder.decode(b'{"digit":3}', type=dict[str, Digit])  #> {'digit': <Digit.THREE: 3>}
    ```
    """

    def __init__(self) -> None:
        self.dec_hooks: dict[typing.Any, DecHook[typing.Any]] = {
            Option: option_dec_hook,
            Variative: variative_dec_hook,
            datetime: lambda t, obj: t.fromtimestamp(obj),
            fntypes.option.Some: option_dec_hook,
            fntypes.option.Nothing: option_dec_hook,
        }

    def __repr__(self) -> str:
        return "<{}: dec_hooks={!r}>".format(
            self.__class__.__name__,
            self.dec_hooks,
        )

    @typing.overload
    def __call__[T](
        self,
        type: type[T],
        context: dict[str, typing.Any] | None = None,
    ) -> typing.ContextManager[msgspec.json.Decoder[T]]: ...

    @typing.overload
    def __call__(
        self,
        type: typing.Any,
        context: dict[str, typing.Any] | None = None,
    ) -> typing.ContextManager[msgspec.json.Decoder[typing.Any]]: ...

    @typing.overload
    def __call__[T](
        self,
        type: type[T],
        *,
        strict: bool = True,
        context: dict[str, typing.Any] | None = None,
    ) -> typing.ContextManager[msgspec.json.Decoder[T]]: ...

    @typing.overload
    def __call__(
        self,
        type: typing.Any,
        *,
        strict: bool = True,
        context: dict[str, typing.Any] | None = None,
    ) -> typing.ContextManager[msgspec.json.Decoder[typing.Any]]: ...

    @contextmanager
    def __call__(self, type=object, *, strict=True, context=None):
        """Context manager returns an `msgspec.json.Decoder` object with the `dec_hook`."""
        dec_obj = msgspec.json.Decoder(
            type=typing.Any if type is object else type,
            strict=strict,
            dec_hook=self.dec_hook(context),
        )
        yield dec_obj

    def add_dec_hook[T](self, t: type[T], /) -> typing.Callable[[DecHook[T]], DecHook[T]]:
        def decorator(func: DecHook[T], /) -> DecHook[T]:
            return self.dec_hooks.setdefault(get_origin(t), func)

        return decorator

    def dec_hook(self, context: dict[str, typing.Any] | None = None) -> DecHook[typing.Any]:
        def inner(tp: type[typing.Any], obj: typing.Any, /) -> typing.Any:
            origin_type = t if isinstance((t := get_origin(tp)), type) else type(t)
            if origin_type not in self.dec_hooks:
                raise TypeError(
                    f"Unknown type `{fullname(origin_type)}`. You can implement decode hook for this type."
                )
            dec_hook_func = self.dec_hooks[origin_type]
            kwargs = magic_bundle(dec_hook_func, context or {}, start_idx=2)
            return dec_hook_func(tp, obj, **kwargs)

        return inner

    def convert[T](
        self,
        obj: object,
        *,
        type: type[T] = dict,
        strict: bool = True,
        from_attributes: bool = False,
        builtin_types: typing.Iterable[type[typing.Any]] | None = None,
        str_keys: bool = False,
        context: dict[str, typing.Any] | None = None,
    ) -> T:
        return msgspec.convert(
            obj,
            type,
            strict=strict,
            from_attributes=from_attributes,
            dec_hook=self.dec_hook(context),
            builtin_types=builtin_types,
            str_keys=str_keys,
        )

    @typing.overload
    def decode(
        self,
        buf: str | bytes,
        *,
        context: dict[str, typing.Any] | None = None,
    ) -> typing.Any: ...

    @typing.overload
    def decode[T](
        self,
        buf: str | bytes,
        *,
        type: type[T],
        context: dict[str, typing.Any] | None = None,
    ) -> T: ...

    @typing.overload
    def decode(
        self,
        buf: str | bytes,
        *,
        type: typing.Any,
        context: dict[str, typing.Any] | None = None,
    ) -> typing.Any: ...

    @typing.overload
    def decode[T](
        self,
        buf: str | bytes,
        *,
        type: type[T],
        strict: bool = True,
        context: dict[str, typing.Any] | None = None,
    ) -> T: ...

    @typing.overload
    def decode(
        self,
        buf: str | bytes,
        *,
        type: typing.Any,
        strict: bool = True,
        context: dict[str, typing.Any] | None = None,
    ) -> typing.Any: ...

    def decode(self, buf, *, type=object, strict=True, context=None):
        return msgspec.json.decode(
            buf,
            type=typing.Any if type is object else type,
            strict=strict,
            dec_hook=self.dec_hook(context),
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
            Variative: lambda variative: variative.v,
            datetime: lambda date: int(date.timestamp()),
        }

    def __repr__(self) -> str:
        return "<{}: enc_hooks={!r}>".format(
            self.__class__.__name__,
            self.enc_hooks,
        )

    @contextmanager
    def __call__(
        self,
        *,
        decimal_format: typing.Literal["string", "number"] = "string",
        uuid_format: typing.Literal["canonical", "hex"] = "canonical",
        order: typing.Literal[None, "deterministic", "sorted"] = None,
        context: dict[str, typing.Any] | None = None,
    ) -> typing.Generator[msgspec.json.Encoder, typing.Any, None]:
        """Context manager returns an `msgspec.json.Encoder` object with the `enc_hook`."""
        enc_obj = msgspec.json.Encoder(enc_hook=self.enc_hook(context))
        yield enc_obj

    def add_enc_hook[T](self, t: type[T], /) -> typing.Callable[[EncHook[T]], EncHook[T]]:
        def decorator(func: EncHook[T], /) -> EncHook[T]:
            encode_hook = self.enc_hooks.setdefault(get_origin(t), func)
            return func if encode_hook is not func else encode_hook

        return decorator

    def enc_hook(self, context: dict[str, typing.Any] | None = None) -> EncHook[typing.Any]:
        def inner(obj: typing.Any, /) -> typing.Any:
            origin_type = get_origin(obj.__class__)
            if origin_type not in self.enc_hooks:
                raise NotImplementedError(
                    f"Not implemented encode hook for object of type `{fullname(origin_type)}`.",
                )
            enc_hook_func = self.enc_hooks[origin_type]
            kwargs = magic_bundle(enc_hook_func, context or {}, start_idx=1)
            return enc_hook_func(obj, **kwargs)

        return inner

    @typing.overload
    def encode(
        self,
        obj: typing.Any,
        *,
        context: dict[str, typing.Any] | None = None,
    ) -> str: ...

    @typing.overload
    def encode(
        self,
        obj: typing.Any,
        *,
        as_str: typing.Literal[True],
        context: dict[str, typing.Any] | None = None,
    ) -> str: ...

    @typing.overload
    def encode(
        self,
        obj: typing.Any,
        *,
        as_str: typing.Literal[False],
        context: dict[str, typing.Any] | None = None,
    ) -> bytes: ...

    def encode(
        self,
        obj: typing.Any,
        *,
        as_str: bool = True,
        context: dict[str, typing.Any] | None = None,
    ) -> str | bytes:
        buf = msgspec.json.encode(obj, enc_hook=self.enc_hook(context))
        return buf.decode() if as_str else buf

    def to_builtins(
        self,
        obj: typing.Any,
        *,
        str_keys: bool = False,
        builtin_types: typing.Iterable[type[typing.Any]] | None = None,
        order: typing.Literal["deterministic", "sorted"] | None = None,
        context: dict[str, typing.Any] | None = None,
    ) -> typing.Any:
        return msgspec.to_builtins(
            obj,
            str_keys=str_keys,
            builtin_types=builtin_types,
            enc_hook=self.enc_hook(context),
            order=order,
        )


decoder: typing.Final[Decoder] = Decoder()
encoder: typing.Final[Encoder] = Encoder()


__all__ = (
    "Decoder",
    "Encoder",
    "Option",
    "datetime",
    "decoder",
    "encoder",
    "get_class_annotations",
    "get_type_hints",
    "msgspec_convert",
    "msgspec_to_builtins",
    "struct_as_dict",
)
