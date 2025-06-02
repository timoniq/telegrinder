import dataclasses
import typing

import msgspec
from fntypes.option import Some

from telegrinder.api.api import API
from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.bot.cute_types.update import UpdateCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.msgspec_utils import decoder
from telegrinder.node.base import ComposeError, FactoryNode, scalar_node
from telegrinder.tools.fullname import fullname
from telegrinder.types.objects import Model, Update

if typing.TYPE_CHECKING:
    from _typeshed import DataclassInstance

type DataclassType = DataclassInstance | msgspec.Struct | dict[str, typing.Any]


@scalar_node
class UpdateNode:
    @classmethod
    def compose(cls, update: Update, api: API, context: Context) -> UpdateCute:
        match context.update_cute:
            case Some(update_cute):
                return update_cute
            case _:
                return context.add_update_cute(update, api).update_cute.unwrap()


class _EventNode(FactoryNode):
    dataclass: type[DataclassType]
    orig_dataclass: type[DataclassType]

    def __class_getitem__(cls, dataclass: type[DataclassType], /) -> typing.Self:
        return cls(dataclass=dataclass, orig_dataclass=typing.get_origin(dataclass) or dataclass)

    @classmethod
    def compose(cls, update_cute: UpdateNode, raw_update: Update, api: API) -> DataclassType:
        if issubclass(cls.orig_dataclass, UpdateCute):
            return update_cute

        if (
            (
                issubclass(cls.orig_dataclass, BaseCute)
                and isinstance(update_cute.incoming_update, cls.orig_dataclass)
            )
            or issubclass(cls.orig_dataclass, Model)
            and isinstance(raw_update.incoming_update, cls.orig_dataclass)
        ):
            return update_cute.incoming_update

        try:
            if issubclass(cls.orig_dataclass, msgspec.Struct) or dataclasses.is_dataclass(
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
            raise ComposeError(f"Cannot parse an update object into `{fullname(cls.dataclass)}`, error: {exc}")


if typing.TYPE_CHECKING:
    type EventNode[Dataclass: DataclassType] = Dataclass
else:
    EventNode = type("EventNode", (_EventNode,), {"__module__": __name__})


__all__ = ("EventNode",)
