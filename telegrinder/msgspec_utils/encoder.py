import datetime as dt
import typing
from contextlib import contextmanager

import fntypes.library
import msgspec

from telegrinder.msgspec_utils.abc import SupportsCast
from telegrinder.msgspec_utils.custom_types.datetime import datetime, timedelta
from telegrinder.msgspec_utils.custom_types.enum_meta import BaseEnumMeta
from telegrinder.msgspec_utils.tools import bundle, fullname, get_origin

type Context = dict[str, typing.Any]
type Order = typing.Literal["deterministic", "sorted"]
type EncHook[T] = typing.Callable[typing.Concatenate[T, ...], typing.Any]


def to_builtins(
    obj: typing.Any,
    *,
    str_keys: bool = False,
    builtin_types: typing.Iterable[type[typing.Any]] | None = None,
    order: Order | None = None,
    context: Context | None = None,
) -> fntypes.library.Result[typing.Any, msgspec.ValidationError]:
    try:
        return fntypes.library.Ok(
            encoder.to_builtins(
                obj,
                str_keys=str_keys,
                builtin_types=builtin_types,
                order=order,
                context=context,
            ),
        )
    except msgspec.ValidationError as error:
        return fntypes.library.Error(error)


class Encoder:
    """Class `Encoder` for `msgspec` module with encode hooks for objects.

    ```
    from datetime import datetime

    class MyDatetime(datetime):
        ...

    encoder = Encoder()
    encoder.enc_hooks[MyDatetime] = lambda d: int(d.timestamp())

    encoder.enc_hook(MyDatetime.now())  #> 1713354732
    encoder.encode({"digit": Digit.ONE})  #> '{"digit":1}'
    ```
    """

    cast_types: dict[type[typing.Any], type[SupportsCast]]
    enc_hooks: dict[typing.Any, EncHook[typing.Any]]
    abstract_enc_hooks: dict[typing.Any, EncHook[typing.Any]]

    def __init__(self) -> None:
        self.cast_types = {  # type: ignore
            dt.datetime: datetime,
            dt.timedelta: timedelta,
        }
        self.enc_hooks = {
            fntypes.library.Some: lambda some: some.value,
            fntypes.library.Nothing: lambda _: None,
            fntypes.library.Variative: lambda variative: variative.v,
            datetime: lambda date: int(date.timestamp()),
            timedelta: lambda time: time.total_seconds(),
        }
        self.abstract_enc_hooks = {
            BaseEnumMeta: lambda enum_member: enum_member.value,
        }

    def __repr__(self) -> str:
        return "<{}: cast_types={!r}, enc_hooks={!r}, abstract_enc_hooks={!r}>".format(
            type(self).__name__,
            self.cast_types,
            self.enc_hooks,
            self.abstract_enc_hooks,
        )

    @contextmanager
    def __call__(
        self,
        *,
        decimal_format: typing.Literal["string", "number"] = "string",
        uuid_format: typing.Literal["canonical", "hex"] = "canonical",
        order: Order | None = None,
        context: Context | None = None,
    ) -> typing.Generator[msgspec.json.Encoder, typing.Any, None]:
        """Context manager returns the `msgspec.json.Encoder` object with passed the `enc_hook`."""
        yield msgspec.json.Encoder(
            enc_hook=self.enc_hook(context),
            decimal_format=decimal_format,
            uuid_format=uuid_format,
            order=order,
        )

    def add_enc_hook[T](self, t: type[T], /) -> typing.Callable[[EncHook[T]], EncHook[T]]:
        def decorator(func: EncHook[T], /) -> EncHook[T]:
            encode_hook = self.enc_hooks.setdefault(get_origin(t), func)
            return func if encode_hook is not func else encode_hook

        return decorator

    def add_abstract_enc_hook[T](self, abstract_type: type[T], /) -> typing.Callable[[EncHook[T]], EncHook[T]]:
        def decorator(func: EncHook[T], /) -> EncHook[T]:
            return self.abstract_enc_hooks.setdefault(get_origin(abstract_type), func)

        return decorator

    def get_abstract_enc_hook(self, subtype: type[typing.Any], /) -> EncHook[typing.Any] | None:
        for abstract, enc_hook in self.abstract_enc_hooks.items():
            if issubclass(subtype, abstract) or issubclass(type(subtype), abstract):
                return enc_hook

        return None

    def enc_hook(self, context: Context | None = None, /) -> EncHook[typing.Any]:
        def inner(obj: typing.Any, /) -> typing.Any:
            origin_type = get_origin(obj)

            if (enc_hook_func := self.enc_hooks.get(origin_type)) is None and (
                enc_hook_func := self.get_abstract_enc_hook(origin_type)
            ) is None:
                raise NotImplementedError(
                    f"Not implemented encode hook for object of type `{fullname(origin_type)}`. "
                    "You can implement encode hook for this object.",
                )

            return bundle(enc_hook_func, context or {}, start_idx=1)(obj)

        return inner

    @typing.overload
    def encode(
        self,
        obj: typing.Any,
        *,
        order: Order | None = None,
        context: Context | None = None,
    ) -> str: ...

    @typing.overload
    def encode(
        self,
        obj: typing.Any,
        *,
        as_str: typing.Literal[True],
        order: Order | None = None,
        context: Context | None = None,
    ) -> str: ...

    @typing.overload
    def encode(
        self,
        obj: typing.Any,
        *,
        as_str: typing.Literal[False],
        order: Order | None = None,
        context: Context | None = None,
    ) -> bytes: ...

    def encode(
        self,
        obj: typing.Any,
        *,
        as_str: bool = True,
        order: Order | None = None,
        context: Context | None = None,
    ) -> str | bytes:
        buf = msgspec.json.encode(obj, enc_hook=self.enc_hook(context), order=order)
        return buf.decode() if as_str else buf

    def to_builtins(
        self,
        obj: typing.Any,
        *,
        str_keys: bool = False,
        builtin_types: typing.Iterable[type[typing.Any]] | None = None,
        order: Order | None = None,
        context: Context | None = None,
    ) -> typing.Any:
        return msgspec.to_builtins(
            obj,
            str_keys=str_keys,
            builtin_types=builtin_types,
            enc_hook=self.enc_hook(context),
            order=order,
        )

    def cast(self, obj: typing.Any, /) -> typing.Any:
        if (caster := self.cast_types.get(get_origin(obj))) is not None:
            return caster.cast(obj)
        return obj


encoder: typing.Final[Encoder] = Encoder()


__all__ = ("Encoder", "encoder", "to_builtins")
