import datetime as dt
import typing
from contextlib import contextmanager

import fntypes.co
import msgspec
from fntypes.result import Error, Ok, Result
from fntypes.variative import Variative

from telegrinder.msgspec_utils.abc import SupportsCast
from telegrinder.msgspec_utils.custom_types.datetime import datetime, timedelta
from telegrinder.msgspec_utils.custom_types.enum_meta import BaseEnumMeta
from telegrinder.msgspec_utils.custom_types.literal import _Literal
from telegrinder.msgspec_utils.custom_types.option import Option
from telegrinder.msgspec_utils.tools import (
    bundle,
    fullname,
    get_origin,
    is_common_type,
    type_check,
)

type Context = dict[str, typing.Any]
type DecHook[T] = typing.Callable[typing.Concatenate[type[T], typing.Any, ...], typing.Any]


def option_dec_hook(
    tp: type[Option[typing.Any]],
    obj: typing.Any,
    /,
) -> fntypes.co.Option[typing.Any] | msgspec.UnsetType:
    if obj is msgspec.UNSET:
        return obj

    if obj is None or isinstance(obj, fntypes.co.Nothing):
        return fntypes.co.Nothing()

    (value_type,) = typing.get_args(tp) or (typing.Any,)
    orig_value_type = typing.get_origin(value_type) or value_type
    orig_obj = obj

    if not isinstance(orig_obj, dict | list) and is_common_type(orig_value_type):
        if orig_value_type is Variative:
            obj = value_type(orig_obj)  # type: ignore
            orig_value_type = typing.get_args(value_type)

        if not type_check(orig_obj, orig_value_type):
            raise msgspec.ValidationError(
                f"Expected `{fullname(orig_value_type)}` or `builtins.None`, got `{fullname(orig_obj)}`.",
            )

        return fntypes.co.Some(obj)

    return fntypes.co.Some(decoder.convert(orig_obj, type=value_type))


def variative_dec_hook(tp: type[Variative], obj: typing.Any, /) -> Variative:
    union_types = typing.get_args(tp)

    if isinstance(obj, dict):
        reverse = False
        models_fields_count: dict[type[msgspec.Struct], int] = {
            m: sum(1 for k in obj if k in m.__struct_fields__)
            for m in union_types
            if issubclass(get_origin(m), msgspec.Struct)
        }
        union_types = tuple(t for t in union_types if t not in models_fields_count)

        if len(set(models_fields_count.values())) != len(models_fields_count.values()):
            models_fields_count = {m: len(m.__struct_fields__) for m in models_fields_count}
            reverse = True

        union_types = (
            *sorted(
                models_fields_count,
                key=lambda k: models_fields_count[k],
                reverse=reverse,
            ),
            *union_types,
        )

    if (
        not isinstance(obj, dict | list)
        and any(is_common_type(t) and type_check(obj, t) for t in union_types)
    ):
        return tp(obj)

    for t in union_types:
        match convert(obj, t):
            case Ok(value):
                return tp(value)
            case Error(_):
                continue
            case _ as arg:
                typing.assert_never(arg)

    raise msgspec.ValidationError(
        "Object of type `{}` doesn't belong to `{}[{}]`.".format(
            fullname(obj),
            fullname(Variative),
            ", ".join(fullname(get_origin(x)) for x in union_types),
        )
    )


def datetime_dec_hook(tp: type[datetime], obj: typing.Any, /) -> datetime:
    if isinstance(obj, datetime):
        return obj

    if isinstance(obj, dt.datetime):
        assert issubclass(tp, SupportsCast)
        return tp.cast(obj)

    if isinstance(obj, int | float):
        return tp.fromtimestamp(timestamp=obj)

    raise TypeError(
        "Cannot validate object of type `{}` into `datetime.datetime`".format(
            fullname(obj),
        ),
    )


def timedelta_dec_hook(tp: type[timedelta], obj: typing.Any, /) -> timedelta:
    if isinstance(obj, timedelta):
        return obj

    if isinstance(obj, dt.timedelta):
        assert issubclass(tp, SupportsCast)
        return tp.cast(obj)

    if isinstance(obj, int | float):
        return tp(seconds=obj)

    raise TypeError(
        "Cannot validate object of type `{}` into `datetime.timedelta`".format(
            fullname(obj),
        ),
    )


def convert[T](
    obj: typing.Any,
    t: type[T],
    /,
    *,
    context: Context | None = None,
) -> Result[T, str]:
    try:
        return Ok(decoder.convert(obj, type=t, strict=True, context=context))
    except msgspec.ValidationError:
        return Error(
            "Expected object of type `{}`, got `{}`.".format(
                fullname(t),
                fullname(obj),
            )
        )


def literal_dec_hook(literal: type[_Literal], obj: typing.Any, /) -> typing.Any:
    if obj in literal.__args__:
        return obj

    raise msgspec.ValidationError(
        "Invalid literal value {!r} of either {}.".format(
            obj,
            literal.__args__[0]
            if len(literal.__args__) == 1
            else (", ".join(f"`{x}`" for x in literal.__args__[:-1])) + f" or `{literal.__args__[-1]}`",
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

    dec_hooks: dict[typing.Any, DecHook[typing.Any]]
    abstract_dec_hooks: dict[typing.Any, DecHook[typing.Any]]

    def __init__(self) -> None:
        self.dec_hooks = {
            Option: option_dec_hook,
            Variative: variative_dec_hook,
            datetime: datetime_dec_hook,
            timedelta: timedelta_dec_hook,
            fntypes.option.Some: option_dec_hook,
            fntypes.option.Nothing: option_dec_hook,
        }
        self.abstract_dec_hooks = {
            BaseEnumMeta: lambda enum_type, member: enum_type(member),
            _Literal: literal_dec_hook,
        }

    def __repr__(self) -> str:
        return "<{}: dec_hooks={!r}, abstract_dec_hooks={!r}>".format(
            type(self).__name__,
            self.dec_hooks,
            self.abstract_dec_hooks,
        )

    @typing.overload
    def __call__[T](
        self,
        type: type[T],
        context: Context | None = None,
    ) -> typing.ContextManager[msgspec.json.Decoder[T]]: ...

    @typing.overload
    def __call__(
        self,
        type: typing.Any,
        context: Context | None = None,
    ) -> typing.ContextManager[msgspec.json.Decoder[typing.Any]]: ...

    @typing.overload
    def __call__[T](
        self,
        type: type[T],
        *,
        strict: bool = True,
        context: Context | None = None,
    ) -> typing.ContextManager[msgspec.json.Decoder[T]]: ...

    @typing.overload
    def __call__(
        self,
        type: typing.Any,
        *,
        strict: bool = True,
        context: Context | None = None,
    ) -> typing.ContextManager[msgspec.json.Decoder[typing.Any]]: ...

    @contextmanager
    def __call__(
        self,
        type: typing.Any = object,
        *,
        strict: bool = True,
        context: Context | None = None,
    ) -> typing.Generator[msgspec.json.Decoder, typing.Any, None]:
        """Context manager returns an `msgspec.json.Decoder` object with passed the `dec_hook`."""
        yield msgspec.json.Decoder(
            type=typing.Any if type is object else type,
            strict=strict,
            dec_hook=self.dec_hook(context),
        )

    def add_dec_hook[T](self, t: type[T], /) -> typing.Callable[[DecHook[T]], DecHook[T]]:
        def decorator(func: DecHook[T], /) -> DecHook[T]:
            return self.dec_hooks.setdefault(get_origin(t), func)

        return decorator

    def add_abstract_dec_hook[T](self, abstract_type: type[T], /) -> typing.Callable[[DecHook[T]], DecHook[T]]:
        def decorator(func: DecHook[T], /) -> DecHook[T]:
            return self.abstract_dec_hooks.setdefault(get_origin(abstract_type), func)

        return decorator

    def get_abstract_dec_hook(self, subtype: type[typing.Any], /) -> DecHook[typing.Any] | None:
        for abstract, dec_hook in self.abstract_dec_hooks.items():
            if issubclass(subtype, abstract) or issubclass(type(subtype), abstract):
                return dec_hook

        return None

    def dec_hook(self, context: Context | None = None, /) -> DecHook[typing.Any]:
        def inner(tp: typing.Any, obj: typing.Any, /) -> typing.Any:
            origin_type = get_origin(tp)

            if (dec_hook_func := self.dec_hooks.get(origin_type)) is None and (
                dec_hook_func := self.get_abstract_dec_hook(origin_type)
            ) is None:
                raise NotImplementedError(
                    f"Not implemented decode hook for type `{fullname(origin_type)}`. "
                    "You can implement decode hook for this type.",
                )

            return bundle(dec_hook_func, context or {}, start_idx=2)(tp, obj)

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
        context: Context | None = None,
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
        context: Context | None = None,
    ) -> typing.Any: ...

    @typing.overload
    def decode[T](
        self,
        buf: str | bytes,
        *,
        type: type[T],
        context: Context | None = None,
    ) -> T: ...

    @typing.overload
    def decode(
        self,
        buf: str | bytes,
        *,
        type: typing.Any,
        context: Context | None = None,
    ) -> typing.Any: ...

    @typing.overload
    def decode[T](
        self,
        buf: str | bytes,
        *,
        type: type[T],
        strict: bool = True,
        context: Context | None = None,
    ) -> T: ...

    @typing.overload
    def decode(
        self,
        buf: str | bytes,
        *,
        type: typing.Any,
        strict: bool = True,
        context: Context | None = None,
    ) -> typing.Any: ...

    def decode(
        self,
        buf: str | bytes,
        *,
        type: typing.Any = object,
        strict: bool = True,
        context: Context | None = None,
    ) -> typing.Any:
        return msgspec.json.decode(
            buf,
            type=typing.Any if type is object else type,
            strict=strict,
            dec_hook=self.dec_hook(context),
        )


decoder: typing.Final[Decoder] = Decoder()


__all__ = ("Decoder", "convert", "decoder")
