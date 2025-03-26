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
from telegrinder.tools.callback_data_serilization.abc import ABCDataSerializer, ModelType

DESERIALIZE_EXCEPTIONS: typing.Final[set[type[BaseException]]]  = {
    msgspec.DecodeError,
    msgspec.ValidationError,
    binascii.Error
}

try:
    import brotli  # type: ignore

    DESERIALIZE_EXCEPTIONS.add(brotli.error)  # type: ignore
except ImportError:
    brotli = None


@dataclasses.dataclass(frozen=True, slots=True)
class ModelParser[Model: ModelType]:
    model_type: type[Model]

    def _is_model(self, obj: typing.Any, /) -> typing.TypeGuard[ModelType]:
        return dataclasses.is_dataclass(obj) or isinstance(obj, msgspec.Struct)

    def _model_to_dict(self, model: ModelType) -> dict[str, typing.Any]:
        if dataclasses.is_dataclass(model):
            return dataclasses.asdict(model)
        return msgspec.structs.asdict(model)  # type: ignore

    def _is_union(self, inspected_type: msgspec.inspect.Type, /) -> typing.TypeGuard[msgspec.inspect.UnionType]:
        return isinstance(inspected_type, msgspec.inspect.UnionType)

    def _is_model_type(
        self,
        inspected_type: msgspec.inspect.Type,
        /,
    ) -> typing.TypeGuard[msgspec.inspect.DataclassType | msgspec.inspect.StructType]:
        return isinstance(inspected_type, msgspec.inspect.DataclassType | msgspec.inspect.StructType)

    def _is_iter_of_model(
        self, inspected_type: msgspec.inspect.Type, /
    ) -> typing.TypeGuard[msgspec.inspect.ListType]:
        return isinstance(
            inspected_type,
            msgspec.inspect.ListType | msgspec.inspect.SetType | msgspec.inspect.FrozenSetType,
        ) and self._is_model_type(inspected_type.item_type)

    def _validate_annotation(self, annotation: typing.Any, /) -> tuple[type[ModelType], bool] | None:
        is_iter_of_model = False
        type_args: tuple[msgspec.inspect.Type, ...] | None = None
        inspected_type = msgspec.inspect.type_info(annotation)

        if self._is_union(inspected_type):
            type_args = inspected_type.types
        elif self._is_iter_of_model(inspected_type):
            type_args = (inspected_type.item_type,)
            is_iter_of_model = True
        elif self._is_model_type(inspected_type):
            type_args = (inspected_type,)

        if type_args is not None:
            for arg in type_args:
                if self._is_union(arg):
                    type_args += arg.types
                if self._is_model_type(arg):
                    return (arg.cls, is_iter_of_model)
                if self._is_iter_of_model(arg):
                    return (arg.item_type.cls, True)  # type: ignore

        return None

    def parse(self, model: Model) -> list[typing.Any]:
        """Returns a parsed model as linked list."""
        linked: list[typing.Any] = []
        stack: list[typing.Any] = [(list(self._model_to_dict(model).values()), linked)]

        while stack:
            current_obj, current = stack.pop()

            for item in current_obj:
                if self._is_model(item):
                    item = self._model_to_dict(item)
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

        return encoder.to_builtins(linked)

    def compose(self, linked: list[typing.Any]) -> dict[str, typing.Any]:
        """Compose linked list to dictionary based on the model class annotations `(without validation)`."""
        root_converted_data: dict[str, typing.Any] = {}
        stack: deque[typing.Any] = deque([(linked, self.model_type, root_converted_data)])

        while stack:
            current_data, current_model, converted_data = stack.pop()

            for index, (field, annotation) in enumerate(get_class_annotations(current_model).items()):
                obj, model_type, is_iter_of_model = current_data[index], None, False

                if isinstance(obj, list) and (validated := self._validate_annotation(annotation)):
                    model_type, is_iter_of_model = validated

                if model_type is not None:
                    if is_iter_of_model:
                        converted_data[field] = []
                        for item in obj:
                            new_converted_data = {}
                            converted_data[field].append(new_converted_data)
                            stack.append((item, model_type, new_converted_data))
                    else:
                        new_converted_data = {}
                        converted_data[field] = new_converted_data
                        stack.append((obj, model_type, new_converted_data))
                else:
                    converted_data[field] = obj

        return root_converted_data


class MsgPackSerializer[Model: ModelType](ABCDataSerializer[Model]):
    @typing.overload
    def __init__(self, model_t: type[Model], /) -> None: ...

    @typing.overload
    def __init__(self, model_t: type[Model], /, *, ident_key: str | None = ...) -> None: ...

    def __init__(self, model_t: type[Model], /, *, ident_key: str | None = None) -> None:
        self.model_t = model_t
        self.ident_key: str | None = ident_key or getattr(model_t, "__key__", None)
        self._model_parser = ModelParser(model_t)

    @classmethod
    def serialize_from_model(cls, model: Model, *, ident_key: str | None = None) -> str:
        return cls(model.__class__, ident_key=ident_key).serialize(model)

    @classmethod
    def deserialize_to_json(cls, serialized_data: str, model_t: type[Model]) -> Result[Model, str]:
        return cls(model_t).deserialize(serialized_data)

    @cached_property
    def key(self) -> bytes:
        if self.ident_key:
            return msgspec.msgpack.encode(super().key)
        return b""

    def serialize(self, data: Model, /) -> str:
        encoded = self.key + msgspec.msgpack.encode(self._model_parser.parse(data), enc_hook=encoder.enc_hook)
        if brotli is not None:
            return base64.b85encode(brotli.compress(encoded, quality=11)).decode()  # type: ignore
        return base64.urlsafe_b64encode(encoded).decode()

    def deserialize(self, serialized_data: str, /) -> Result[Model, str]:
        with suppress(*DESERIALIZE_EXCEPTIONS):
            if brotli is not None:
                ser_data = brotli.decompress(base64.b85decode(serialized_data))
            else:
                ser_data = base64.urlsafe_b64decode(serialized_data)

            if self.ident_key and not ser_data.startswith(self.key):
                return Error("Data is not corresponding to key.")

            data: list[typing.Any] = msgspec.msgpack.decode(
                ser_data.removeprefix(self.key),
                dec_hook=decoder.dec_hook(),
            )
            return Ok(decoder.convert(self._model_parser.compose(data), type=self.model_t))

        return Error("Incorrect data.")


__all__ = ("MsgPackSerializer",)
