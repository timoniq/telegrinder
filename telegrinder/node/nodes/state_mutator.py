import typing

from kungfu.library.monad.option import Some
from nodnod.error import NodeError
from nodnod.node import Node

from telegrinder.node.nodes.payload import PayloadSerializer
from telegrinder.node.nodes.source import Source
from telegrinder.tools.fullname import fullname
from telegrinder.tools.serialization import ABCDataSerializer
from telegrinder.tools.state_storage.memory import ABCStateStorage, MemoryStateStorage


class StateMutator(Node):
    STORAGE = MemoryStateStorage[str]()  # TODO: use nodnod injection to get storage inside StateMutator.compose
    KEY_MAP: dict[str, type[State]] = {}

    def __init__(
        self,
        storage: ABCStateStorage[str],
        user_id: int,
        serializer: type[ABCDataSerializer[State]],
    ) -> None:
        self.storage = storage
        self.user_id = user_id
        self.serializer = serializer

    async def get(self) -> State | None:
        match await self.storage.get(self.user_id):
            case Some(state_data) if state_data.key in self.KEY_MAP:
                return (
                    self
                    .serializer(self.KEY_MAP[state_data.key])
                    .deserialize(state_data.payload)
                    .map(lambda state: state.bind(self))
                    .unwrap_or_none()
                )

        return None

    async def set(self, state: State) -> None:
        state_cls = state.__class__
        key = fullname(state_cls)
        payload = self.serializer(state_cls).serialize(state)
        await self.storage.set(self.user_id, key, payload)
        self.KEY_MAP[key] = state_cls

    @classmethod
    def __compose__(cls, src: Source, serializer: PayloadSerializer) -> typing.Self:
        return cls(cls.STORAGE, src.from_user.id, serializer.serializer)


class State:
    def bind(self, mutator: StateMutator) -> typing.Self:
        self.__mutator__ = mutator
        return self

    async def enter(self) -> None:
        await self.__mutator__.set(state=self)

    async def exit(self) -> None:
        pass

    @classmethod
    async def __compose__(cls, mutator: StateMutator) -> typing.Self:
        current_state = await mutator.get()
        if current_state is None or not isinstance(current_state, cls):
            raise NodeError("State mismatch.")
        return current_state


__all__ = ("State", "StateMutator")
