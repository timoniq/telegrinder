import typing

from fntypes import Nothing, Option, Some

from .abc import ABCStateStorage, StateData

Payload = dict[str, typing.Any]


class MemoryStateStorage(ABCStateStorage[Payload]):
    def __init__(self):
        self.storage: dict[int, StateData[Payload]] = {}

    async def get(self, user_id: int) -> Option[StateData[Payload]]:
        state = self.storage.get(user_id)
        return Some(state) if state is not None else Nothing()

    async def set(self, user_id: int, key: str, payload: Payload) -> None:
        self.storage[user_id] = StateData(key, payload)

    async def delete(self, user_id: int) -> None:
        self.storage.pop(user_id)
