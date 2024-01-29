import typing
from contextlib import suppress

import msgspec
from msgspec import Raw, ValidationError

from telegrinder.option import Nothing, NothingType, Option, Some
from telegrinder.option.msgspec_option import Option as MsgspecOption
from telegrinder.result import Error, Ok, Result

T = typing.TypeVar("T")

DecHook = typing.Callable[[type[T], typing.Any], typing.Any]
EncHook = typing.Callable[[T], typing.Any]

if typing.TYPE_CHECKING:
    from telegrinder.api.error import APIError
    
    Union = typing.Union
else:

    @typing.runtime_checkable
    class _Union(typing.Protocol[T]):        
        def __class_getitem__(cls, types):
            obj = super().__class_getitem__(typing.Any)
            obj.__args__ = types
            return obj
    
    Union = _Union

MODEL_CONFIG: typing.Final[dict[str, typing.Any]] = {
    "omit_defaults": True,
    "dict": True,
    "rename": {"from_": "from"},
}


def get_origin(t: type[T]) -> type[T]:
    return typing.cast(T, typing.get_origin(t)) or t


def repr_type(t: type) -> str:
    return getattr(t, "__name__", repr(get_origin(t)))


def msgspec_convert(obj: typing.Any, t: type[T]) -> Result[T, ValidationError]:
    try:
        return Ok(decoder.convert(obj, type=t, strict=True))
    except ValidationError as exc:
        return Error(exc)


def option_enc_hook(obj: Option[typing.Any]) -> typing.Any | None:
    return obj.value if isinstance(obj, Some) else None


def option_dec_hook(tp: type, obj: typing.Any) -> typing.Any:
    if obj is None:
        return Nothing
    value_type = (typing.get_args(tp) or (typing.Any,))[0]
    return msgspec_convert({"value": obj}, Some[value_type]).unwrap()


def union_dec_hook(tp: type, obj: typing.Any) -> typing.Any:
    union_types = typing.get_args(tp)

    if isinstance(obj, dict):
        counter_fields = {
            m: sum(1 for k in obj if k in m.__struct_fields__)
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
        match msgspec_convert(obj, t):
            case Ok(value):
                return value

    raise TypeError(
        "Object of type `{}` does not belong to types `{}`".format(
            repr_type(type(obj)),
            " | ".join(map(repr_type, tp.__args__[0].__args__)),
        )
    )


@typing.overload
def full_result(
    result: Result[msgspec.Raw, "APIError"], full_t: type[T]
) -> Result[T, "APIError"]:
    ...


@typing.overload
def full_result(
    result: Result[msgspec.Raw, "APIError"],
    full_t: tuple[type[T], ...],
) -> Result[T, "APIError"]:
    ...


def full_result(
    result: Result[msgspec.Raw, "APIError"],
    full_t: type[T] | tuple[type[T], ...],
) -> Result[T, "APIError"]:
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


class Model(msgspec.Struct, **MODEL_CONFIG):
    def to_dict(
        self,
        *,
        exclude_fields: set[str] | None = None,
    ):  
        exclude_fields = exclude_fields or set()
        if "model_to_dict" not in self.__dict__:
            self.__dict__["model_to_dict"] = msgspec.structs.asdict(self)
        return {
            key: value
            for key, value in self.__dict__["model_to_dict"].items()
            if key not in exclude_fields
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
        *,
        type: type["T"] = dict,
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


decoder: typing.Final[Decoder] = Decoder()
encoder: typing.Final[Encoder] = Encoder()


__all__ = (
    "Decoder",
    "Encoder",
    "Model",
    "Raw",
    "convert",
    "decoder",
    "encoder",
    "full_result",
    "get_origin",
    "get_params",
    "msgspec",
    "msgspec_convert",
    "repr_type",
)
