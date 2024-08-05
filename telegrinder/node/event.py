import typing

import msgspec

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.model import DataclassInstance, Model
from telegrinder.node.base import ComposeError, DataNode, Node
from telegrinder.node.update import UpdateNode

Dataclass = typing.TypeVar("Dataclass", bound="DataclassType")

DataclassType: typing.TypeAlias = (
    "DataclassInstance | DataNode | DataNodeCute | msgspec.Struct | dict[str, typing.Any]"
)

EVENT_NODE_KEY = "_event_node"


if typing.TYPE_CHECKING:
    EventNode: typing.TypeAlias = typing.Annotated[Dataclass, ...]

else:

    class EventNode(Node):
        dataclass: type[DataclassType]

        def __new__(cls, dataclass: type[DataclassType], /) -> type[typing.Self]:
            namespace = dict(**cls.__dict__)
            namespace.pop("__new__", None)
            new_cls = type("EventNode", (cls,), {"dataclass": dataclass, **namespace})
            return new_cls  # type: ignore

        def __class_getitem__(cls, dataclass: type[DataclassType], /) -> type[typing.Self]:
            return cls(dataclass)

        @classmethod
        async def compose(cls, raw_update: UpdateNode, ctx: Context) -> DataclassType:
            try:
                if issubclass(typing.get_origin(cls.dataclass) or cls.dataclass, DataNodeCute):
                    dataclass = cls.dataclass.from_update(
                        update=raw_update.incoming_update, bound_api=raw_update.api
                    )
                else:
                    dataclass = cls.dataclass(**raw_update.incoming_update.to_dict())

                ctx[EVENT_NODE_KEY] = cls
                return dataclass
            except Exception:
                raise ComposeError(f"Cannot parse update to {cls.dataclass.__name__!r}.")


class DataNodeCute(DataNode, BaseCute[Model]):
    api: ABCAPI


__all__ = ("DataNodeCute", "EventNode")
