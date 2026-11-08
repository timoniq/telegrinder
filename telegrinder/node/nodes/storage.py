import typing

from nodnod.interface import generic_node, scalar_node
from nodnod.scope import Scope
from nodnod.value import Value

from telegrinder.node.scope import global_node
from telegrinder.tools.state_storage.abc import ABCStateStorage
from telegrinder.tools.state_storage.memory import MemoryStateStorage

type DefaultMemoryStateStorage = MemoryStateStorage[str]


@global_node
@scalar_node
class MemoryStateStorageNode:
    @classmethod
    def __compose__(cls) -> typing.Generator[DefaultMemoryStateStorage, typing.Any, None]:
        storage = MemoryStateStorage[str]()

        try:
            yield storage
        finally:
            storage.clear()


@scalar_node
@generic_node
class StateStorageNode[Storage: ABCStateStorage[typing.Any] = DefaultMemoryStateStorage]:  # type: ignore
    @classmethod
    def __compose__(
        cls,
        storage_сlass: type[Storage],
        default_storage: MemoryStateStorageNode,
        scope: Scope,
    ) -> Storage:
        return typing.cast(
            "Storage",
            scope.retrieve(storage_сlass).map_or(default_storage, Value.unbox).unwrap()
            if storage_сlass is not DefaultMemoryStateStorage
            else default_storage,
        )


if typing.TYPE_CHECKING:
    type StateStorageNode[Storage: ABCStateStorage[typing.Any] = DefaultMemoryStateStorage] = Storage


__all__ = ("MemoryStateStorageNode", "StateStorageNode")
