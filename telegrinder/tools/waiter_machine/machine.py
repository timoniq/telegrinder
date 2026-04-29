import datetime
import typing

from telegrinder.modules import logger
from telegrinder.tools.aio import maybe_awaitable
from telegrinder.tools.lifespan import Lifespan
from telegrinder.tools.limited_dict import LimitedDict
from telegrinder.tools.magic.function import bundle
from telegrinder.tools.waiter_machine.hasher import Hasher
from telegrinder.tools.waiter_machine.short_state import (
    ShortState,
    ShortStateContext,
)

if typing.TYPE_CHECKING:
    from telegrinder.bot.cute_types.base import BaseCute
    from telegrinder.bot.dispatch.context import Context
    from telegrinder.bot.dispatch.middleware.waiter import WaiterMiddleware
    from telegrinder.bot.dispatch.view.base import View
    from telegrinder.bot.rules.abc import ABCRule
    from telegrinder.tools.waiter_machine.actions import WaiterActions

type Storage[Event: BaseCute, HasherData] = dict[
    Hasher[Event, HasherData],
    LimitedDict[typing.Hashable, ShortState[Event]],
]
type HasherWithData[Event: BaseCute, Data] = tuple[Hasher[Event, Data], Data]
type HasherWithViewAndData[Event: BaseCute, ViewType: View, Data] = tuple[Hasher[Event, Data], Data, ViewType]
type HasherType[Event: BaseCute, ViewType: View, Data] = (
    Hasher[Event, Data] | HasherWithData[Event, Data] | HasherWithViewAndData[Event, ViewType, Data]
)

_NODATA: typing.Final = object()
MAX_STORAGE_SIZE: typing.Final = 100_000
WEEK: typing.Final = datetime.timedelta(days=7)


def unpack_to_context(context: Context, /) -> tuple[Context]:
    return (context,)


def no_unpack(_: Context, /) -> tuple[()]:
    return ()


class ContextUnpackProto[*Ts](typing.Protocol):
    __name__: str

    def __call__(self, context: Context, /) -> tuple[*Ts]: ...


class WaiterMachine:
    storage: Storage[typing.Any, typing.Any]
    view: View | None

    def __init__(
        self,
        *,
        max_storage_size: int = MAX_STORAGE_SIZE,
        base_state_lifetime: datetime.timedelta = WEEK,
    ) -> None:
        self.max_storage_size = max_storage_size
        self.base_state_lifetime = base_state_lifetime
        self.view = None
        self.storage = {}

    def __bool__(self) -> bool:
        return any(self.storage.values())

    def __repr__(self) -> str:
        return "<{} with {} waiters: max_storage_size={}, base_state_lifetime={}>".format(
            type(self).__name__,
            len(self.storage),
            self.max_storage_size,
            self.base_state_lifetime,
        )

    def add_hasher[Event: BaseCute, HasherData](
        self,
        hasher: Hasher[Event, HasherData],
        view: View | None = None,
        waiter_middleware: WaiterMiddleware | None = None,
    ) -> None:
        view = self.view if view is None else view

        if view is None and waiter_middleware is None:
            raise ValueError("Hasher requires view or waiter middleware.")

        if hasher not in self.storage:
            self.storage[hasher] = LimitedDict(maxlimit=self.max_storage_size)

        if view is not None:
            view.middlewares.waiter.add_hasher(hasher)

        elif waiter_middleware is not None:
            waiter_middleware.add_hasher(hasher)

    def bind_view(self, view: View, /) -> typing.Self:
        self.view = view
        return self

    async def drop_all(self) -> None:
        if not self.storage:
            return

        fallback_storage: typing.Mapping[typing.Hashable, ShortState] = {}

        for hasher in self.storage:
            for ident, short_state in self.storage.get(hasher, fallback_storage).items():
                await self.drop_state(short_state, hasher, data=ident)

    async def drop[Event: BaseCute, HasherData](
        self,
        hasher: Hasher[Event, HasherData],
        data: HasherData,
        **context: typing.Any,
    ) -> None:
        if hasher not in self.storage:
            raise LookupError("No record of hasher {!r} found.".format(hasher))

        waiter_hash: typing.Hashable = hasher.get_hash_from_data(data).expect(
            RuntimeError("Couldn't create hash from data."),
        )
        short_state = self.storage[hasher].pop(waiter_hash, None)

        if short_state is None:
            raise LookupError("Waiter with hash `{}` is not found for hasher `{}`.".format(waiter_hash, hasher))

        try:
            await short_state.cancel()
        finally:
            if on_drop := short_state.actions.get("on_drop"):
                context["short_state"] = short_state
                await maybe_awaitable(bundle(on_drop, context)())

    async def drop_state[Event: BaseCute, HasherData](
        self,
        short_state: ShortState[Event],
        hasher: Hasher[Event, HasherData],
        data: HasherData,
        **context: typing.Any,
    ) -> None:
        try:
            await self.drop(
                hasher,
                data,
                **(short_state.context.context | context) if short_state.context is not None else context,
            )
        except Exception as e:
            logger.error("Error dropping state for hasher {!r}: {}", hasher, e)

    async def drop_state_many[Event: BaseCute, ViewType: View, HasherData](
        self,
        short_state: ShortState[Event],
        *hashers: HasherWithData[Event, HasherData] | HasherWithViewAndData[Event, ViewType, HasherData],
        expired: bool = False,
        **context: typing.Any,
    ) -> None:
        for hasher, *rest in hashers:
            await self.drop_state(short_state, hasher, rest[0], expired=expired, **context)

    async def wait[Event: BaseCute, ViewType: View, HasherData](
        self,
        hasher: HasherType[Event, ViewType, HasherData],
        view: ViewType | None = None,
        data: HasherData = _NODATA,
        *,
        filter: ABCRule | None = None,
        release: ABCRule | None = None,
        lifetime: datetime.timedelta | float | None = None,
        lifespan: Lifespan | None = None,
        **actions: typing.Unpack[WaiterActions[Event]],
    ) -> ShortStateContext[Event]:
        if not isinstance(hasher, Hasher):
            hasher, data, view = (*hasher, view) if len(hasher) == 2 else hasher

        if data is _NODATA:
            raise ValueError("Hasher requires data.")

        if isinstance(lifetime, int | float):
            lifetime = datetime.timedelta(seconds=lifetime)
        elif lifetime is None:
            lifetime = self.base_state_lifetime

        short_state = ShortState(
            actions,
            release_rule=release,
            filter=filter,
            expiration=lifetime,
        )
        waiter_hash = hasher.get_hash_from_data(data).expect(RuntimeError("Hasher couldn't create hash."))

        self.add_hasher(hasher, view)

        if (deleted_short_state := self.storage[hasher].set(waiter_hash, short_state)) is not None:
            await deleted_short_state.cancel()

        async with lifespan or Lifespan():
            try:
                await short_state.acquire(self.drop_state_many, (hasher, data), lifetime=lifetime)
            finally:
                if hasher in self.storage:
                    self.storage[hasher].pop(waiter_hash, None)

        if short_state.context is None:
            raise LookupError("No context in `short_state`.")

        return short_state.context

    async def wait_many[Event: BaseCute[typing.Any], ViewType: View, Data, *Ts](
        self,
        *hashers: HasherWithData[Event, Data] | HasherWithViewAndData[Event, ViewType, Data],
        waiter_middleware: WaiterMiddleware | None = None,
        filter: ABCRule | None = None,
        release: ABCRule | None = None,
        lifetime: datetime.timedelta | float | None = None,
        lifespan: Lifespan | None = None,
        unpack: ContextUnpackProto[*Ts] = unpack_to_context,
        **actions: typing.Unpack[WaiterActions[Event]],
    ) -> tuple[Hasher[Event, Data], Event, *Ts]:
        data: typing.Any

        if isinstance(lifetime, int | float):
            lifetime = datetime.timedelta(seconds=lifetime)
        elif lifetime is None:
            lifetime = self.base_state_lifetime

        short_state = ShortState(
            actions,
            filter=filter,
            release_rule=release,
            expiration=lifetime,
        )
        waiter_hashes: dict[Hasher[Event, Data], list[typing.Hashable]] = {}

        for hasher, *rest in hashers:
            data, view = (rest[0], None) if len(rest) != 2 else rest
            waiter_hash = hasher.get_hash_from_data(data).expect(RuntimeError("Hasher couldn't create hash."))

            self.add_hasher(hasher, view=view, waiter_middleware=waiter_middleware)  # type: ignore

            if (deleted_short_state := self.storage[hasher].set(waiter_hash, short_state)) is not None:
                await deleted_short_state.cancel()

            waiter_hashes.setdefault(hasher, []).append(waiter_hash)

        async with lifespan or Lifespan():
            try:
                await short_state.acquire(self.drop_state_many, *hashers, lifetime=lifetime)
            finally:
                for h, hashes in waiter_hashes.items():
                    for waiter_hash in hashes:
                        if h in self.storage:
                            self.storage[h].pop(waiter_hash, None)

        if short_state.context is None:
            raise LookupError("No context in `short_state`.")

        initiator = short_state.context.context.pop("initiator", None)
        if initiator is None:
            raise LookupError("Initiator not found in `short_state` context.")

        return (
            initiator,
            short_state.context.event,
            *unpack(short_state.context.context),
        )


__all__ = ("WaiterMachine",)
