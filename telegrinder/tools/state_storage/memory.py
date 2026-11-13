import typing

from kungfu.library.misc import from_optional
from kungfu.library.monad.option import Option

from telegrinder.tools.state_storage.abc import ABCStateStorage, Key, StateData

type Payload = dict[str, typing.Any]


class MemoryStateStorage[T = Payload](ABCStateStorage[T]):
    storage: dict[int, StateData[T]]

    def __init__(self) -> None:
        self.storage = {}

    def clear(self) -> None:
        self.storage.clear()

    async def get(self, user_id: int) -> Option[StateData[T]]:
        return from_optional(self.storage.get(user_id))

    async def set(self, user_id: int, key: Key, payload: T) -> None:
        self.storage[user_id] = StateData(key, payload)

    async def delete(self, user_id: int) -> None:
        self.storage.pop(user_id, None)


__all__ = ("MemoryStateStorage",)
