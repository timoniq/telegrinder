import typing
from contextlib import suppress

import msgspec
from msgspec import Raw, ValidationError

from telegrinder.option import Nothing, NothingType, Option, Some
from telegrinder.option.msgspec_option import Option as MsgspecOption

T = typing.TypeVar("T")

DecHook = typing.Callable[[type[T], typing.Any], typing.Any]
EncHook = typing.Callable[[T], typing.Any]

if typing.TYPE_CHECKING:
    from telegrinder.api.error import APIError
    from telegrinder.result import Result

    Union = typing.Union
else:

    @typing.runtime_checkable
    class _Union(typing.Protocol[T]):        
        def __class_getitem__(cls, types):
            return super().__class_getitem__(typing.Union[types])
    
    Union = _Union


def get_origin(t: type[T]) -> type[T]:
    return typing.cast(T, typing.get_origin(t)) or t


def repr_type(t: type) -> str:
    return getattr(t, "__name__", repr(get_origin(t)))


def msgspec_convert(obj: typing.Any, t: type[T]) -> Option[T]:
    with suppress(NotImplementedError, ValidationError):
        return Some(decoder.convert(obj, type=t))
    return Nothing


def option_enc_hook(obj: Option[typing.Any]) -> typing.Any | None:
    return obj.value if isinstance(obj, Some) else None


def option_dec_hook(tp: type, obj: typing.Any) -> typing.Any:
    if obj is None:
        return Nothing
    value_type = (typing.get_args(tp) or (typing.Any,))[0]
    return msgspec_convert({"value": obj}, Some[value_type]).expect(
        TypeError(
            "Expected `{}` for Option.Some, got `{}`".format(
                repr_type(value_type),
                repr_type(type(obj)),
            )
        )
    )


def union_dec_hook(tp: type, obj: typing.Any) -> typing.Any:
    union_types = typing.cast(tuple[type, ...], tp.__args__[0].__args__)
    
    if isinstance(obj, dict):
        counter_fields = {
            m: len([k for k in obj.keys() if k in m.__struct_fields__])
            for m in union_types
            if issubclass(m, Model)
        }
        union_types = tuple(t for t in union_types if t not in counter_fields)
        reverse = False
        
        if len(set(counter_fields.values())) != len(counter_fields.values()):
            counter_fields = {m: len(m.__struct_fields__) for m in counter_fields}
            reverse = True
        
        union_types = (
            *sorted(counter_fields, key=lambda k: counter_fields[k], reverse=reverse),
            *union_types,
        )
        
    for t in union_types:
        if (o := msgspec_convert(obj, t)):
            return o.value

    raise TypeError(
        "Object of type `{}` does not belong to types `{}`".format(
            repr_type(type(obj)),
            " | ".join(map(repr_type, tp.__args__[0].__args__)),
        )
    )


@typing.overload
def full_result(
    result: "Result[msgspec.Raw, APIError]", full_t: type[T]
) -> "Result[T, APIError]":
    ...


@typing.overload
def full_result(
    result: "Result[msgspec.Raw, APIError]",
    full_t: tuple[type[T], ...],
) -> "Result[T, APIError]":
    ...


def full_result(
    result: "Result[msgspec.Raw, APIError]",
    full_t: type[T] | tuple[type[T], ...],
) -> "Result[T, APIError]":
    return result.map(lambda v: decoder.decode(v, type=full_t))  # type: ignore


def convert(d: typing.Any, serialize: bool = True) -> typing.Any:
    if isinstance(d, Model):
        converted_dct = convert(d.to_dict(), serialize=False)
        return encoder.encode(converted_dct) if serialize is True else converted_dct
    
    if isinstance(d, dict):
        return {
            k: convert(v, serialize=serialize)
            for k, v in d.items()
            if v not in (None, Nothing)
        }
    
    if isinstance(d, list):
        converted_lst = [convert(x, serialize=False) for x in d]
        return encoder.encode(converted_lst) if serialize is True else converted_lst
    
    return d


def get_params(params: dict[str, typing.Any]) -> dict[str, typing.Any]:
    return {
        k: v.unwrap() if v and isinstance(v, Some) else v
        for k, v in (
            *params.items(),
            *params.pop("other", {}).items(),
        )
        if k != "self" and v not in (None, Nothing)
    }


class Model(msgspec.Struct, omit_defaults=True, rename={"from_": "from"}):
    def to_dict(
        self,
        *,
        exclude_fields: set[str] | None = None,
    ):
        return {
            k: v
            for k, v in msgspec.structs.asdict(self).items()
            if k not in (exclude_fields or ())
        }


class Decoder:
    def __init__(self) -> None:
        self.dec_hooks: dict[type, DecHook[typing.Any]] = {
            MsgspecOption: option_dec_hook,
            Union: union_dec_hook,  # type: ignore
        }

    def add_dec_hook(self, tp: type[T]):  # type: ignore
        def decorator(func: DecHook[T]) -> DecHook[T]:
            return self.dec_hooks.setdefault(get_origin(tp), func)
        
        return decorator
    
    def dec_hook(self, tp: type, obj: object) -> object:
        origin_type = get_origin(tp)
        if origin_type not in self.dec_hooks:
            raise TypeError(
                f"Unknown type `{repr_type(origin_type)}`. "
                "You can implement decode hook for this type."
            )
        return self.dec_hooks[origin_type](tp, obj)
    
    def convert(
        self,
        obj: object,
        type: type["T"] = typing.Any,
        *,
        strict: bool = True,
        from_attributes: bool = False,
        builtin_types: typing.Iterable[type] | None = None,
        str_keys: bool = False,
    ) -> "T":
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
        type: type[T] = typing.Any,
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
        }

    def add_dec_hook(self, tp: type[T]):  # type: ignore
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


decoder = Decoder()
encoder = Encoder()


__all__ = (
    "convert",
    "msgspec_convert",
    "repr_type",
    "get_origin",
    "decoder",
    "encoder",
    "full_result",
    "get_params",
    "msgspec",
    "Decoder",
    "Encoder",
    "Model",
    "Raw",
)
