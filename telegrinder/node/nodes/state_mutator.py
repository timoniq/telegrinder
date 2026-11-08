import dataclasses
import enum
from functools import cache

import typing_extensions as typing
from kungfu.library.monad.option import Some
from nodnod.error import NodeError
from nodnod.node import Node

from telegrinder.node.nodes.payload import PayloadSerializer
from telegrinder.node.nodes.source import UserId
from telegrinder.node.nodes.storage import DefaultMemoryStateStorage, StateStorageNode
from telegrinder.node.scope import per_call
from telegrinder.node.utils import create_node_from_scratch
from telegrinder.tools.fullname import fullname
from telegrinder.tools.magic.annotations import get_type_args_from_orig_base_generic, unwrap_type_alias_value
from telegrinder.tools.serialization import ABCDataSerializer
from telegrinder.tools.state_storage.memory import ABCStateStorage

type AnyStorage = typing.Any
type AnyMutator = typing.Any


@dataclasses.dataclass
class StateMutator[Storage: ABCStateStorage[str] = DefaultMemoryStateStorage](Node):
    KEY_MAP: typing.ClassVar[dict[str | enum.Enum, type[State[AnyMutator]]]] = {}

    if not typing.TYPE_CHECKING:
        Storage = StateStorageNode[DefaultMemoryStateStorage]

    storage: Storage
    user_id: int
    serializer: type[ABCDataSerializer[State[typing.Self]]]

    @classmethod
    @cache
    def __class_getitem__(cls, item: typing.Any, /) -> typing.Any:
        return create_node_from_scratch(
            cls.__name__,
            (cls,),
            {
                "__map__": {getattr(__class__, "Storage", Storage): StateStorageNode[unwrap_type_alias_value(item)]},
                "__module__": cls.__module__,
            },
        )

    @classmethod
    def __compose__(
        cls,
        storage: Storage,
        user_id: UserId,
        serializer: PayloadSerializer,
    ) -> typing.Self:
        return cls(storage, user_id, serializer.serializer)

    def bind_state[T: State[AnyMutator]](self, state: T, /) -> T:
        return state.bind(self)

    @typing.overload
    async def get(self) -> State[typing.Self] | None: ...

    @typing.overload
    async def get[T: State[AnyMutator]](self, state_class: type[T], /) -> T | None: ...

    async def get(
        self,
        state_class: type[State[typing.Self]] | None = None,
    ) -> typing.Any:
        match await self.storage.get(self.user_id):
            case Some(state_data) if (state_class is not None and state_data.key == state_class.__state_key__) or (
                state_class is None and (state_class := StateMutator.KEY_MAP.get(state_data.key)) is not None
            ):
                return (
                    self.serializer(state_class).deserialize(state_data.payload).map(self.bind_state).unwrap_or_none()
                )

        return None

    async def set(self, state: State[AnyMutator]) -> None:
        state_class = type(state)
        await self.storage.set(
            user_id=self.user_id,
            key=state_class.__state_key__,
            payload=self.serializer(state_class).serialize(state),
        )

    async def unset(self) -> None:
        await self.storage.delete(user_id=self.user_id)


@per_call
class State[Mutator: StateMutator[AnyStorage] = StateMutator](Node, abstract=True):
    __state_key__: typing.ClassVar[str | enum.Enum]
    __mutator__: Mutator | None = None

    def __init_subclass__(cls, *args: typing.Any, **kwargs: typing.Any) -> None:
        if not hasattr(cls, "__state_key__"):
            raise LookupError("State must have a state key defined using the class variable `__state_key__`.")

        if not isinstance(cls.__state_key__, str | enum.Enum):
            raise LookupError(
                f"Type of the state key must be `str` or `Enum`, not `{type(cls.__state_key__).__name__}`."
            )

        if cls.__state_key__ in StateMutator.KEY_MAP:
            raise LookupError(
                f"State key {cls.__state_key__!r} conflict between the `{fullname(cls)}` and "
                f"`{fullname(StateMutator.KEY_MAP[cls.__state_key__])}` state classes.",
            )

        StateMutator.KEY_MAP[cls.__state_key__] = cls
        type_args = get_type_args_from_orig_base_generic(State, cls)

        if (mutator_node := type_args.get(Mutator)) is None:
            raise LookupError(f"Could not get a mutator from generic types of `{cls!r}`.")

        cls.__map__ = {Mutator: unwrap_type_alias_value(mutator_node)}
        return super().__init_subclass__(*args, **kwargs)

    def bind(self, mutator: Mutator) -> typing.Self:
        self.__mutator__ = mutator
        return self

    async def enter(self) -> typing.Self:
        if self.__mutator__ is not None:
            await self.__mutator__.set(state=self)

        return self

    async def exit(self) -> None:
        if self.__mutator__ is not None:
            await self.__mutator__.unset()

    async def __aenter__(self) -> typing.Self:
        await self.enter()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException],
        exc_val: BaseException,
        exc_tb: typing.Any,
    ) -> None:
        await self.exit()

    @classmethod
    async def __compose__(cls, mutator: Mutator) -> typing.Self:
        current_state = await mutator.get(cls)

        if current_state is None:
            raise NodeError(f"State `{cls!r}` (key={cls.__state_key__!r}) mismatch.")

        return current_state


__all__ = ("State", "StateMutator")
