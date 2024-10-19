from __future__ import annotations

import abc
import typing
from functools import cached_property

import msgspec
from fntypes.result import Result

if typing.TYPE_CHECKING:
    from dataclasses import Field

    from _typeshed import DataclassInstance

P = typing.ParamSpec("P")
T = typing.TypeVar("T")
Data = typing.TypeVar("Data")

ModelType: typing.TypeAlias = "DataclassWithIdentKey | ModelWithIdentKey | msgspec.Struct | DataclassInstance"


@typing.runtime_checkable
class DataclassWithIdentKey(typing.Protocol):
    __key__: str
    __dataclass_fields__: typing.ClassVar[dict[str, Field[typing.Any]]]


@typing.runtime_checkable
class ModelWithIdentKey(typing.Protocol):
    __key__: str
    __struct_fields__: typing.ClassVar[tuple[str, ...]]


class ABCDataSerializer(abc.ABC, typing.Generic[Data]):
    ident_key: str | None = None

    @abc.abstractmethod
    def __init__(self, data_type: type[Data], /) -> None:
        pass

    @cached_property
    def key(self) -> str:
        return self.ident_key + "_" if self.ident_key else ""

    @abc.abstractmethod
    def serialize(self, data: Data) -> str:
        pass

    @abc.abstractmethod
    def deserialize(self, serialized_data: str) -> Result[Data, str]:
        pass


__all__ = ("ABCDataSerializer",)
