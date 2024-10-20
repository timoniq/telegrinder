import base64
import binascii
import dataclasses
import typing
from collections import deque
from contextlib import suppress
from functools import cached_property

import msgspec
from fntypes.result import Error, Ok, Result

from telegrinder.msgspec_utils import decoder, encoder, get_class_annotations

from .abc import ABCDataSerializer, ModelType

ModelT = typing.TypeVar("ModelT", bound=ModelType)


def is_model_type(obj: typing.Any, /) -> typing.TypeGuard[type[ModelType]]:
    return isinstance(obj, type) and issubclass(obj, msgspec.Struct) or dataclasses.is_dataclass(obj)


class MsgPackSerializer(ABCDataSerializer[ModelT]):
    @typing.overload
    def __init__(self, model_t: type[ModelT], /) -> None: ...

    @typing.overload
    def __init__(self, model_t: type[ModelT], /, *, ident_key: str | None = ...) -> None: ...

    def __init__(self, model_t: type[ModelT], /, *, ident_key: str | None = None) -> None:
        self.model_t = model_t
        self.ident_key: str | None = ident_key or getattr(model_t, "__key__", None)

    @classmethod
    def serialize_from_model(cls, model: ModelT, *, ident_key: str | None = None) -> str:
        return cls(model.__class__, ident_key=ident_key).serialize(model)

    @classmethod
    def deserialize_to_json(cls, serialized_data: str, model_t: type[ModelT]) -> Result[ModelT, str]:
        return cls(model_t).deserialize(serialized_data)

    @cached_property
    def key(self) -> bytes:
        if self.ident_key:
            return msgspec.msgpack.encode(super().key)
        return b""

    @staticmethod
    def parse(model: ModelT) -> list[typing.Any]:
        """Returns a parsed model as linked list."""

        linked: list[typing.Any] = []
        stack: list[typing.Any] = [(list(encoder.to_builtins(model).values()), linked)]

        while stack:
            current_obj, current = stack.pop()

            for item in current_obj:
                if isinstance(item, dict):
                    new_list = []
                    current.append(new_list)
                    stack.append((list(item.values()), new_list))
                elif isinstance(item, list | tuple):
                    new_list = []
                    current.append(new_list)
                    stack.append((item, new_list))
                else:
                    current.append(item)

        return linked

    def compose_data(self, data: list[typing.Any], model: type[ModelType]) -> dict[str, typing.Any]:
        """Compose data to dictionary for model type."""

        root_converted_data = {}
        stack = deque([(data, model, root_converted_data)])

        while stack:
            current_data, current_model, converted_data = stack.pop()

            for index, (field, annotation) in enumerate(get_class_annotations(current_model).items()):
                obj = current_data[index]
                origin_type = typing.get_origin(annotation) or annotation

                if (
                    isinstance(obj, list)
                    and isinstance(origin_type, type)
                    and issubclass(origin_type, (list, tuple, set, frozenset))
                    and (type_args := typing.get_args(annotation))
                ):
                    origin_type = type_args[0]

                if is_model_type(origin_type):
                    if isinstance(obj, list):
                        converted_data[field] = []
                        for item in obj:
                            new_converted_data = {}
                            converted_data[field].append(new_converted_data)
                            stack.append((item, origin_type, new_converted_data))
                    else:
                        new_converted_data = {}
                        converted_data[field] = new_converted_data
                        stack.append((obj, origin_type, new_converted_data))
                else:
                    converted_data[field] = obj

        return root_converted_data

    def serialize(self, data: ModelT) -> str:
        return base64.urlsafe_b64encode(
            self.key + msgspec.msgpack.encode(self.parse(data), enc_hook=encoder.enc_hook),
        ).decode()

    def deserialize(self, serialized_data: str) -> Result[ModelT, str]:
        with suppress(msgspec.DecodeError, msgspec.ValidationError, binascii.Error):
            ser_data = base64.urlsafe_b64decode(serialized_data)
            if self.ident_key and not ser_data.startswith(self.key):
                return Error("Data is not corresponding to key.")

            data: list[typing.Any] = msgspec.msgpack.decode(
                ser_data.removeprefix(self.key),
                dec_hook=decoder.dec_hook,
            )
            return Ok(decoder.convert(self.compose_data(data, self.model_t), type=self.model_t))

        return Error("Incorrect data.")


__all__ = ("MsgPackSerializer",)
