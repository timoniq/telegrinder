import msgspec
from telegrinder.result import Result
from msgspec import Raw
import typing

if typing.TYPE_CHECKING:
    from telegrinder.api.error import APIError

T = typing.TypeVar("T")
encoder = msgspec.json.Encoder()


def full_result(
    result: Result[msgspec.Raw, "APIError"], full_t: typing.Type[T]
) -> Result[T, "APIError"]:
    if not result.is_ok:
        return result
    return Result(True, value=msgspec.json.decode(result.value, type=full_t))


def convert(d: typing.Any) -> typing.Any:
    if isinstance(d, Model):
        return msgspec.json.encode(d).decode()
    elif isinstance(d, dict):
        return {k: convert(v) for k, v in d.items() if v is not None}
    elif isinstance(d, list):
        li = [convert(el) for el in d]
        return li
    return d


model_config = {"rename": {"from_": "from"}, "omit_defaults": True}


class Model(msgspec.Struct, **model_config):
    _dict_cached: typing.Optional[dict] = None

    def to_dict(self) -> dict:
        if self._dict_cached is not None:
            return self._dict_cached
        self._dict_cached = {k: getattr(self, k) for k in self.__struct_fields__}
        return self._dict_cached


__all__ = (
    "convert",
    "model_config",
    "encoder",
    "full_result",
    "msgspec",
    "Model",
    "Raw",
)
