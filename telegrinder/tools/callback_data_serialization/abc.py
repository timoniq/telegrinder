from __future__ import annotations

import abc
import typing
from functools import cached_property

import msgspec
from fntypes.library.monad.result import Result

if typing.TYPE_CHECKING:
    from _typeshed import DataclassInstance

type ModelType = msgspec.Struct | DataclassInstance


class ABCDataSerializer[Data = typing.Any](abc.ABC):
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
