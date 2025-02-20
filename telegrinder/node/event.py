import dataclasses
import typing

import msgspec

from telegrinder.api.api import API
from telegrinder.bot.cute_types import BaseCute
from telegrinder.msgspec_utils import decoder
from telegrinder.node.base import ComposeError, FactoryNode
from telegrinder.types.objects import Update

if typing.TYPE_CHECKING:
    from _typeshed import DataclassInstance

type DataclassType = DataclassInstance | msgspec.Struct | dict[str, typing.Any]


class _EventNode(FactoryNode):
    dataclass: type[DataclassType]
    orig_dataclass: type[DataclassType]

    def __class_getitem__(cls, dataclass: type[DataclassType], /) -> typing.Self:
        return cls(dataclass=dataclass, orig_dataclass=typing.get_origin(dataclass) or dataclass)

    @classmethod
    def compose(cls, raw_update: Update, api: API) -> DataclassType:
        try:
            if issubclass(cls.orig_dataclass, BaseCute):
                update = raw_update if issubclass(cls.orig_dataclass, Update) else raw_update.incoming_update
                dataclass = cls.orig_dataclass.from_update(update=update, bound_api=api)

            elif issubclass(cls.orig_dataclass, msgspec.Struct) or dataclasses.is_dataclass(
                cls.orig_dataclass,
            ):
                dataclass = decoder.convert(
                    obj=raw_update.incoming_update,
                    type=cls.dataclass,
                    from_attributes=True,
                )
            else:
                dataclass = cls.dataclass(**raw_update.incoming_update.to_full_dict())

            return dataclass
        except Exception as exc:
            raise ComposeError(f"Cannot parse an update object into {cls.dataclass!r}, error: {str(exc)}")


if typing.TYPE_CHECKING:
    type EventNode[Dataclass: DataclassType] = Dataclass
else:
    EventNode = _EventNode


__all__ = ("EventNode",)
