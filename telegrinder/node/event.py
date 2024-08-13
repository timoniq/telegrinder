import typing

import msgspec

from telegrinder.bot.dispatch.context import Context
from telegrinder.msgspec_utils import DataclassInstance
from telegrinder.node.base import BaseNode, ComposeError, DataNode
from telegrinder.node.update import UpdateNode

if typing.TYPE_CHECKING:
    Dataclass = typing.TypeVar("Dataclass", bound="DataclassType")

    DataclassType: typing.TypeAlias = DataclassInstance | DataNode | msgspec.Struct | dict[str, typing.Any]

EVENT_NODE_KEY = "_event_node"


if typing.TYPE_CHECKING:
    EventNode: typing.TypeAlias = typing.Annotated["Dataclass", ...]

else:
    from telegrinder.msgspec_utils import decoder

    class EventNode(BaseNode):
        dataclass: type["DataclassType"]

        def __new__(cls, dataclass: type["DataclassType"], /) -> type[typing.Self]:
            namespace = dict(**cls.__dict__)
            namespace.pop("__new__", None)
            new_cls = type("EventNode", (cls,), {"dataclass": dataclass, **namespace})
            return new_cls  # type: ignore

        def __class_getitem__(cls, dataclass: type["DataclassType"], /) -> type[typing.Self]:
            return cls(dataclass)

        @classmethod
        async def compose(cls, raw_update: UpdateNode, ctx: Context) -> "DataclassType":
            dataclass_type = typing.get_origin(cls.dataclass) or cls.dataclass

            try:
                if issubclass(dataclass_type, dict):
                    dataclass = cls.dataclass(**raw_update.incoming_update.to_full_dict())

                elif issubclass(dataclass_type, msgspec.Struct | DataclassInstance):
                    dataclass = decoder.convert(
                        raw_update.incoming_update.to_full_dict(),
                        type=cls.dataclass,
                    )

                else:
                    dataclass = cls.dataclass(**raw_update.incoming_update.to_dict())

                ctx[EVENT_NODE_KEY] = cls
                return dataclass
            except Exception:
                raise ComposeError(f"Cannot parse update to {cls.dataclass.__name__!r}.")


__all__ = ("EventNode",)
