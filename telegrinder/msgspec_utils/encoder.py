import typing
from contextlib import contextmanager

import msgspec
from fntypes.option import Nothing, Some
from fntypes.result import Error, Ok, Result
from fntypes.variative import Variative

from telegrinder.msgspec_utils.tools import datetime, fullname, get_origin, magic_bundle

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
) -> Result[typing.Any, msgspec.ValidationError]:
    try:
        return Ok(
            encoder.to_builtins(
                obj,
                str_keys=str_keys,
                builtin_types=builtin_types,
                order=order,
                context=context,
            ),
        )
    except msgspec.ValidationError as error:
        return Error(error)


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
            Some: lambda some: some.value,
            Nothing: lambda _: None,
            Variative: lambda variative: variative.v,
            datetime: lambda date: int(date.timestamp()),
        }

    def __repr__(self) -> str:
        return "<{}: enc_hooks={!r}>".format(type(self).__name__, self.enc_hooks)

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

    def enc_hook(self, context: Context | None = None, /) -> EncHook[typing.Any]:
        def inner(obj: typing.Any, /) -> typing.Any:
            origin_type = get_origin(obj)
            if origin_type not in self.enc_hooks:
                raise NotImplementedError(
                    f"Not implemented encode hook for object of type `{fullname(origin_type)}`. "
                    "You can implement encode hook for this object."
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


encoder: typing.Final[Encoder] = Encoder()


__all__ = ("Encoder", "encoder", "to_builtins")
