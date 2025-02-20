import typing

from fntypes.option import Option

from telegrinder.tools.functional import from_optional
from telegrinder.tools.state_storage.abc import ABCStateStorage, StateData

type Payload = dict[str, typing.Any]


class MemoryStateStorage(ABCStateStorage[Payload]):
    def __init__(self) -> None:
        self.storage: dict[int, StateData[Payload]] = {}

    async def get(self, user_id: int) -> Option[StateData[Payload]]:
        return from_optional(self.storage.get(user_id))

    async def set(self, user_id: int, key: str, payload: Payload) -> None:
        self.storage[user_id] = StateData(key, payload)

    async def delete(self, user_id: int) -> None:
        self.storage.pop(user_id)


__all__ = ("MemoryStateStorage",)
