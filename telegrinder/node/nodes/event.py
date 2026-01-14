import dataclasses
import typing

import msgspec
from nodnod.error import NodeError
from nodnod.interface.generic import generic_node

from telegrinder.api.api import API
from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.bot.cute_types.update import UpdateCute
from telegrinder.msgspec_utils import decoder
from telegrinder.tools.fullname import fullname
from telegrinder.types.objects import Model, Update

if typing.TYPE_CHECKING:
    from _typeshed import DataclassInstance

type DataclassType = DataclassInstance | msgspec.Struct | dict[str, typing.Any]


@generic_node
class EventNode[Dataclass: DataclassType]:  # type: ignore[reportRedeclaration]
    @classmethod
    def __compose__(
        cls,
        api: API,
        raw_update: Update,
        dataclass: type[Dataclass],
        update_cute: UpdateCute,
    ) -> DataclassType:
        orig_dataclass = typing.get_origin(dataclass) or dataclass

        if orig_dataclass is UpdateCute:
            return update_cute

        if issubclass(orig_dataclass, BaseCute | Model):
            incoming_update = (
                update_cute.incoming_update if issubclass(orig_dataclass, BaseCute) else raw_update.incoming_update
            )

            if type(incoming_update) is not orig_dataclass:
                raise NodeError(f"Incoming update is not `{fullname(orig_dataclass)}`.")

            return incoming_update

        try:
            if issubclass(orig_dataclass, msgspec.Struct) or dataclasses.is_dataclass(
                orig_dataclass,
            ):
                obj = decoder.convert(
                    obj=raw_update.incoming_update,
                    type=dataclass,
                    from_attributes=True,
                )
            else:
                obj = dataclass(**raw_update.incoming_update.to_full_dict())

            return obj
        except Exception as exc:
            raise NodeError(
                f"Cannot parse an update object into `{fullname(dataclass)}`",
                from_error=NodeError(exc),
            )


if typing.TYPE_CHECKING:
    type EventNode[Dataclass: DataclassType] = Dataclass


__all__ = ("EventNode",)
