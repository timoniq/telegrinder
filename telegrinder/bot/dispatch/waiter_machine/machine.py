from __future__ import annotations

import asyncio
import datetime
import typing

from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.bot.dispatch.abc import ABCDispatch
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.waiter_machine.actions import WaiterActions
from telegrinder.bot.dispatch.waiter_machine.hasher import Hasher
from telegrinder.bot.dispatch.waiter_machine.middleware import WaiterMiddleware
from telegrinder.bot.dispatch.waiter_machine.short_state import (
    ShortState,
    ShortStateContext,
)
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.tools.global_context.builtin_context import TelegrinderContext
from telegrinder.tools.lifespan import Lifespan
from telegrinder.tools.limited_dict import LimitedDict

type Storage[Event: BaseCute, HasherData] = dict[
    Hasher[Event, HasherData],
    LimitedDict[typing.Hashable, ShortState[Event]],
]
type HasherWithData[Event: BaseCute, Data] = tuple[Hasher[Event, Data], Data]

_NODATA: typing.Final[typing.Any] = object()
MAX_STORAGE_SIZE: typing.Final[int] = 10000
ONE_MINUTE: typing.Final[datetime.timedelta] = datetime.timedelta(minutes=1)
WEEK: typing.Final[datetime.timedelta] = datetime.timedelta(days=7)
CONTEXT: typing.Final[TelegrinderContext] = TelegrinderContext()


async def clear_wm_storage_worker(wm: WaiterMachine, interval: float) -> None:
    await wm.clear_storage()
    await asyncio.sleep(interval)


def unpack_to_context(context: Context, /) -> tuple[Context]:
    return (context,)


def no_unpack(_: Context, /) -> tuple[()]:
    return ()


class ContextUnpackProto[*Ts](typing.Protocol):
    __name__: str

    def __call__(self, context: Context, /) -> tuple[*Ts]: ...


class WaiterMachine:
    def __init__(
        self,
        dispatch: ABCDispatch,
        *,
        max_storage_size: int = MAX_STORAGE_SIZE,
        base_state_lifetime: datetime.timedelta = WEEK,
        clear_storage_interval: datetime.timedelta = ONE_MINUTE,
    ) -> None:
        self.dispatch = dispatch
        self.max_storage_size = max_storage_size
        self.base_state_lifetime = base_state_lifetime
        self.storage: Storage[typing.Any, typing.Any] = {}

        CONTEXT.loop_wrapper.add_task(
            clear_wm_storage_worker(self, clear_storage_interval.total_seconds()),
        )

    def __repr__(self) -> str:
        return "<{}: with {} storage items and max_storage_size={}, base_state_lifetime={!r}>".format(
            self.__class__.__name__,
            len(self.storage),
            self.max_storage_size,
            self.base_state_lifetime,
        )

    def add_hasher[Event: BaseCute, HasherData](
        self,
        hasher: Hasher[Event, HasherData],
        /,
    ) -> None:
        self.storage[hasher] = LimitedDict(maxlimit=self.max_storage_size)
        view = self.dispatch.get_view(hasher.view_class).expect(
            RuntimeError(f"View {hasher.view_class.__name__!r} is not defined in dispatch."),
        )
        view.middlewares.insert(0, WaiterMiddleware(self, hasher))

    async def drop_all(self) -> None:
        """Drops all waiters in storage."""
        for hasher in self.storage.copy():
            for ident, short_state in self.storage[hasher].items():
                if short_state.context:
                    await self.drop(hasher, data=ident)
                else:
                    await short_state.cancel()

            del self.storage[hasher]

    async def drop[Event: BaseCute, HasherData](
        self,
        hasher: Hasher[Event, HasherData],
        data: HasherData,
        **context: typing.Any,
    ) -> None:
        if hasher not in self.storage:
            raise LookupError("No record of hasher {!r} found.".format(hasher))

        waiter_id: typing.Hashable = hasher.get_hash_from_data(data).expect(
            RuntimeError("Couldn't create hash from data"),
        )
        short_state = self.storage[hasher].pop(waiter_id, None)
        if short_state is None:
            raise LookupError(
                "Waiter with identificator {} is not found for hasher {!r}.".format(waiter_id, hasher)
            )

        if on_drop := short_state.actions.get("on_drop"):
            on_drop(short_state, **context)

        await short_state.cancel()

    async def wait[Event: BaseCute, HasherData](
        self,
        hasher: Hasher[Event, HasherData] | HasherWithData[Event, HasherData],
        data: HasherData = _NODATA,
        *,
        filter: ABCRule | None = None,
        release: ABCRule | None = None,
        lifetime: datetime.timedelta | float | None = None,
        lifespan: Lifespan | None = None,
        **actions: typing.Unpack[WaiterActions[Event]],
    ) -> ShortStateContext[Event]:
        if isinstance(lifetime, int | float):
            lifetime = datetime.timedelta(seconds=lifetime)

        lifespan = lifespan or Lifespan()
        event = asyncio.Event()
        short_state = ShortState(
            event,
            actions,
            release=release,
            filter=filter,
            lifetime=lifetime or self.base_state_lifetime,
        )

        hasher, data = hasher if not isinstance(hasher, Hasher) else (hasher, data)
        assert data is not _NODATA, "Hasher requires data."
        waiter_hash = hasher.get_hash_from_data(data).expect(RuntimeError("Hasher couldn't create hash."))

        if hasher not in self.storage:
            self.add_hasher(hasher)

        if (deleted_short_state := self.storage[hasher].set(waiter_hash, short_state)) is not None:
            await deleted_short_state.cancel()

        async with lifespan:
            await event.wait()

        self.storage[hasher].pop(waiter_hash, None)

        if short_state.context is None:
            raise LookupError("No context in short_state.")
        return short_state.context

    async def wait_many[Event: BaseCute[typing.Any], Data, *Ts](
        self,
        *hashers: HasherWithData[Event, Data],
        filter: ABCRule | None = None,
        release: ABCRule | None = None,
        lifetime: datetime.timedelta | float | None = None,
        lifespan: Lifespan | None = None,
        unpack: ContextUnpackProto[*Ts] = unpack_to_context,
        **actions: typing.Unpack[WaiterActions[Event]],
    ) -> tuple[HasherWithData[Event, Data], Event, *Ts]:
        if isinstance(lifetime, int | float):
            lifetime = datetime.timedelta(seconds=lifetime)

        lifespan = lifespan or Lifespan()
        event = asyncio.Event()
        short_state = ShortState(
            event,
            actions,
            release=release,
            filter=filter,
            lifetime=lifetime or self.base_state_lifetime,
        )
        waiter_hashes: dict[Hasher[Event, Data], typing.Hashable] = {}

        for hasher, data in hashers:
            waiter_hash = hasher.get_hash_from_data(data).expect(RuntimeError("Hasher couldn't create hash."))

            if hasher not in self.storage:
                self.add_hasher(hasher)

            if (deleted_short_state := self.storage[hasher].set(waiter_hash, short_state)) is not None:
                await deleted_short_state.cancel()

            waiter_hashes[hasher] = waiter_hash

        async with lifespan:
            await event.wait()

        if short_state.context is None:
            raise LookupError("No context in short_state.")

        initiator = short_state.context.context.get("initiator")
        if initiator is None:
            raise LookupError("Initiator not found in short_state context.")

        for hasher, waiter_hash in waiter_hashes.items():
            self.storage[hasher].pop(waiter_hash, None)

        return (
            initiator,
            short_state.context.event,
            *unpack(short_state.context.context),
        )

    async def clear_storage(self) -> None:
        """Clears storage."""
        now = datetime.datetime.now()

        for hasher in self.storage:
            for ident, short_state in self.storage.get(hasher, {}).copy().items():
                if short_state.expiration_date is not None and now > short_state.expiration_date:
                    await self.drop(hasher, data=ident, force=True)


__all__ = ("WaiterMachine",)
