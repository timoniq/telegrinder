import typing

from nodnod.error import NodeError
from nodnod.node import Node

from telegrinder.node.nodes.source import Source
from telegrinder.tools.fullname import fullname
from telegrinder.tools.serialization import (
    ABCDataSerializer,
    JSONSerializer,
)
from telegrinder.tools.state_storage.memory import ABCStateStorage, MemoryStateStorage


class StateMutator(Node):
    STORAGE = MemoryStateStorage[str]()  # TODO: use nodnod injection to get storage inside StateMutator.compose
    # TODO: use nodnod injection to set custom StateMutator
    KEY_MAP: dict[str, type["State"]] = {}

    def __init__(self, storage: ABCStateStorage[str], user_id: int) -> None:
        self.storage = storage
        self.user_id = user_id

    async def get(self) -> "State | None":
        result = await self.storage.get(self.user_id)
        if not result:
            return None

        state_data = result.unwrap()

        if state_data.key not in self.KEY_MAP:
            return None

        state_cls = self.KEY_MAP[state_data.key]
        result = state_cls.__serializer__(state_cls).deserialize(state_data.payload)

        if not result:
            return None

        state = result.unwrap()
        return state.bind(self)

    async def set(self, state: "State"):
        state_cls = state.__class__
        key = fullname(state_cls)

        self.KEY_MAP[key] = state_cls

        payload = state.__serializer__(state.__class__).serialize(state)
        await self.storage.set(self.user_id, key, payload)

    @classmethod
    def __compose__(cls, src: Source) -> typing.Self:
        return cls(cls.STORAGE, src.from_user.id)


class State(Node):
    __serializer__: type[ABCDataSerializer] = (
        JSONSerializer  # TODO: [OPTIMIZATION] can be initialized with cls after cls is created
    )

    def bind(self, mutator: StateMutator) -> typing.Self:
        self.__mutator__ = mutator
        return self

    async def enter(self) -> None:
        await self.__mutator__.set(state=self)

    async def exit(self) -> None:
        pass

    @classmethod
    async def compose(cls, mutator: StateMutator) -> typing.Self:
        current_state = await mutator.get()
        if current_state is None or not isinstance(current_state, cls):
            raise NodeError("State mismatch")
        return current_state


__all__ = ("State", "StateMutator")
