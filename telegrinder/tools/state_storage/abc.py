from __future__ import annotations

import abc
import dataclasses
import enum

from fntypes.option import Option

from telegrinder.bot.rules.state import State, StateMeta


@dataclasses.dataclass
class StateData[Payload]:
    key: str | enum.Enum
    payload: Payload

    async def save(self, user_id: int, storage: ABCStateStorage[Payload]) -> None:
        await storage.set(user_id, key=self.key, payload=self.payload)


class ABCStateStorage[Payload](abc.ABC):
    @abc.abstractmethod
    async def get(self, user_id: int) -> Option[StateData[Payload]]: ...

    @abc.abstractmethod
    async def delete(self, user_id: int) -> None: ...

    @abc.abstractmethod
    async def set(self, user_id: int, key: str | enum.Enum, payload: Payload) -> None: ...

    def State(self, key: str | StateMeta | enum.Enum = StateMeta.ANY, /) -> State[Payload]:  # noqa: N802
        """Can be used as a shortcut to get a state rule dependant on current storage."""
        return State(storage=self, key=key)


__all__ = ("ABCStateStorage", "StateData")
