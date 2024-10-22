import abc
import dataclasses
import enum

from fntypes.option import Option

from telegrinder.bot.rules.state import State, StateMeta


@dataclasses.dataclass(frozen=True, slots=True)
class StateData[Payload]:
    key: str | enum.Enum
    payload: Payload


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
