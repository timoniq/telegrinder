import dataclasses
import typing

import msgspec
from msgspec import Raw

from telegrinder.option import Nothing, Some, enc_hook
from telegrinder.option import dec_hook as option_dec_hook
from telegrinder.option.msgspec_option import Option as MsgspecOption
from telegrinder.result import Result

if typing.TYPE_CHECKING:
    from telegrinder.api.error import APIError

DecHook = typing.Callable[[type[typing.Any], typing.Any], typing.Any]
T = typing.TypeVar("T")
encoder = msgspec.json.Encoder(enc_hook=enc_hook)


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


@dataclasses.dataclass(frozen=True, repr=False)
class Decoder:
    dec_hooks: list[DecHook] = dataclasses.field(default_factory=lambda: [])
    strict: bool = dataclasses.field(default=False, kw_only=True)

    def add_dec_hook(self, dec_hook: DecHook) -> None:
        if dec_hook not in self.dec_hooks:
            self.dec_hooks.append(dec_hook)

    def decode(self, buf: str | bytes, *, type: type[T] = typing.Any) -> T:
        if not self.dec_hooks:
            return msgspec.json.decode(
                buf,
                type=type,
                strict=self.strict,
            )
        errors: list[BaseException] = []
        for dec_hook in self.dec_hooks:
            try:
                return msgspec.json.decode(
                    buf,
                    type=type,
                    strict=self.strict,
                    dec_hook=dec_hook,
                )
            except (TypeError, msgspec.ValidationError, msgspec.DecodeError) as e:
                errors.append(e)
        raise BaseExceptionGroup("Failed to decode with msgspec.json.decode", errors)


def full_result(
    result: Result[msgspec.Raw, "APIError"], full_t: typing.Type[T]
) -> Result[T, "APIError"]:
    return result.map(lambda v: decoder.decode(v, type=full_t))


def convert(d: typing.Any, serialize: bool = True) -> typing.Any:
    if isinstance(d, Model):
        converted_dct = convert(d.to_dict(), serialize=False)
        if serialize is True:
            return encoder.encode(converted_dct).decode()
        return converted_dct
    if isinstance(d, dict):
        return {
            k: convert(v, serialize=serialize)
            for k, v in d.items()
            if v not in (None, Nothing)
        }
    if isinstance(d, list):
        converted_lst = [convert(x, serialize=False) for x in d]
        if serialize is True:
            return encoder.encode(converted_lst).decode()
        return converted_lst
    return d


def get_params(params: dict[str, typing.Any]) -> dict[str, typing.Any]:
    return {
        k: v.unwrap() if v and isinstance(v, Some | MsgspecOption) else v
        for k, v in (
            *params.items(),
            *params.pop("other", {}).items(),
        )
        if k != "self" and v not in (None, Nothing)
    }


decoder = Decoder([option_dec_hook], strict=True)


__all__ = (
    "convert",
    "decoder",
    "encoder",
    "full_result",
    "get_params",
    "msgspec",
    "Decoder",
    "Model",
    "Raw",
)
