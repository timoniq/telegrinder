import base64
import binascii
import dataclasses
import typing
from collections import deque
from contextlib import suppress
from functools import cache, cached_property

import msgspec
from kungfu.library.monad.result import Error, Ok, Result
from msgspex import decoder, encoder
from msgspex.tools.model import get_class_annotations

from telegrinder.tools.serialization.abc import ABCDataSerializer, ModelType
from telegrinder.tools.serialization.utils import get_model_ident_key

try:
    import brotli  # type: ignore

except ImportError:
    brotli = None

INGORE_TYPE_ANNOTATIONS: typing.Final[frozenset[typing.Any]] = frozenset(
    (
        typing.ClassVar,
        typing.Final,
    ),
)
DESERIALIZE_EXCEPTIONS: typing.Final[frozenset[type[BaseException]]] = frozenset(
    filter(
        None,
        (
            msgspec.DecodeError,
            msgspec.ValidationError,
            binascii.Error,
            ValueError,
            LookupError,
            TypeError,
            brotli.error if brotli is not None else None,  # type: ignore
        ),
    ),
)


@dataclasses.dataclass(frozen=True, slots=True)
class ModelParser[Model: ModelType]:
    model_type: type[Model]

    @staticmethod
    def _is_model(obj: typing.Any, /) -> typing.TypeGuard[ModelType]:
        return dataclasses.is_dataclass(obj) or isinstance(obj, msgspec.Struct)

    @staticmethod
    def _model_to_dict(model: ModelType) -> dict[str, typing.Any]:
        if dataclasses.is_dataclass(model):
            return dataclasses.asdict(model)
        return msgspec.structs.asdict(model)  # type: ignore

    @staticmethod
    def _is_union(inspected_type: msgspec.inspect.Type, /) -> typing.TypeGuard[msgspec.inspect.UnionType]:
        return isinstance(inspected_type, msgspec.inspect.UnionType)

    @staticmethod
    def _is_model_type(
        inspected_type: msgspec.inspect.Type,
        /,
    ) -> typing.TypeGuard[msgspec.inspect.DataclassType | msgspec.inspect.StructType]:
        return isinstance(inspected_type, msgspec.inspect.DataclassType | msgspec.inspect.StructType)

    @staticmethod
    def _is_iter_of_model(
        inspected_type: msgspec.inspect.Type,
        /,
    ) -> typing.TypeGuard[msgspec.inspect.ListType]:
        return isinstance(
            inspected_type,
            msgspec.inspect.ListType | msgspec.inspect.SetType | msgspec.inspect.FrozenSetType,
        ) and ModelParser._is_model_type(inspected_type.item_type)

    @staticmethod
    @cache
    def _inspect_annotation(annotation: typing.Any, /) -> tuple[type[ModelType], bool] | None:
        is_iter_of_model = False
        type_args: tuple[msgspec.inspect.Type, ...] = tuple()
        inspected_type = msgspec.inspect.type_info(annotation)

        if ModelParser._is_union(inspected_type):
            type_args = inspected_type.types
        elif ModelParser._is_iter_of_model(inspected_type):
            type_args = (inspected_type.item_type,)
            is_iter_of_model = True
        elif ModelParser._is_model_type(inspected_type):
            type_args = (inspected_type,)

        for arg in type_args:
            if ModelParser._is_union(arg):
                type_args += arg.types

            if ModelParser._is_model_type(arg):
                return (arg.cls, is_iter_of_model)

            if ModelParser._is_iter_of_model(arg):
                return (arg.item_type.cls, True)  # type: ignore

        return None

    @staticmethod
    @cache
    def _get_model_annotations(model: type[typing.Any], /) -> tuple[tuple[str, typing.Any], ...]:
        return tuple(
            (f, ann)
            for f, ann in get_class_annotations(model).items()
            if not f.startswith("__")
            and not f.endswith("__")
            and not isinstance(orig_annotation := typing.get_origin(ann) or ann, dataclasses.InitVar)
            and orig_annotation not in INGORE_TYPE_ANNOTATIONS
        )

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

            for index, (field, annotation) in enumerate(self._get_model_annotations(current_model)):
                obj, model_type, is_iter_of_model = current_data[index], None, False

                if isinstance(obj, list) and (inspected := self._inspect_annotation(annotation)):
                    model_type, is_iter_of_model = inspected

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
        self.ident_key = ident_key or get_model_ident_key(model_t)
        self._model_parser = ModelParser(model_t)

    @classmethod
    def serialize_from_model(cls, model: Model, *, ident_key: str | None = None) -> str:
        return cls(type(model), ident_key=ident_key).serialize(model)

    @classmethod
    def deserialize_to_json(cls, serialized_data: str, model_t: type[Model]) -> Result[Model, str]:
        return cls(model_t).deserialize(serialized_data)

    @cached_property
    def key(self) -> bytes:
        return msgspec.msgpack.encode(super().key) if self.ident_key else b""

    def serialize(self, data: Model, /) -> str:
        encoded = self.key + msgspec.msgpack.encode(self._model_parser.parse(data), enc_hook=encoder.enc_hook)
        if brotli is not None:
            return base64.b85encode(brotli.compress(encoded, quality=11)).decode()  # type: ignore
        return base64.urlsafe_b64encode(encoded).decode()

    def deserialize(self, serialized_data: str, /) -> Result[Model, str]:
        with suppress(*DESERIALIZE_EXCEPTIONS):
            if brotli is not None:
                ser_data = typing.cast("bytes", brotli.decompress(base64.b85decode(serialized_data)))
            else:
                ser_data = base64.urlsafe_b64decode(serialized_data)

            if not ser_data.startswith(self.key):
                return Error("Data is not corresponding to key.")

            data: list[typing.Any] = msgspec.msgpack.decode(
                ser_data.removeprefix(self.key),
                dec_hook=decoder.dec_hook(),
            )
            return Ok(decoder.convert(self._model_parser.compose(data), type=self.model_t))

        return Error("Incorrect data.")


__all__ = ("MsgPackSerializer",)
