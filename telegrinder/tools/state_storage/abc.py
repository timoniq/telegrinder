import abc
import enum
import typing
from dataclasses import dataclass

from fntypes import Option

from telegrinder.bot.rules.state import State, StateMeta

Payload = typing.TypeVar("Payload")


@dataclass
class StateData(typing.Generic[Payload]):
    key: str
    payload: Payload


class ABCStateStorage(abc.ABC, typing.Generic[Payload]):
    @abc.abstractmethod
    async def get(self, user_id: int) -> Option[StateData[Payload]]: ...

    @abc.abstractmethod
    async def delete(self, user_id: int) -> None: ...

    @abc.abstractmethod
    async def set(self, user_id: int, key: str, payload: Payload) -> None: ...

    def State(self, key: str | StateMeta | enum.Enum = StateMeta.ANY, /) -> State[Payload]:  # noqa: N802
        """Can be used as a shortcut to get a state rule dependant on current storage."""

        return State(storage=self, key=key)


__all__ = ("ABCStateStorage", "StateData")
