import asyncio
import datetime
import typing

from telegrinder.bot.dispatch.view.base import BaseStateView
from telegrinder.bot.dispatch.waiter_machine.middleware import WaiterMiddleware
from telegrinder.bot.dispatch.waiter_machine.short_state import (
    EventModel,
    ShortState,
    ShortStateContext,
)
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.tools.limited_dict import LimitedDict

from .hasher import Hasher, StateViewHasher

T = typing.TypeVar("T")
HasherData = typing.TypeVar("HasherData")


Storage: typing.TypeAlias = dict[
    Hasher[EventModel, HasherData], LimitedDict[typing.Hashable, ShortState[EventModel]]
]

WEEK: typing.Final[datetime.timedelta] = datetime.timedelta(days=7)


class WaiterMachine:
    def __init__(
        self,
        *,
        max_storage_size: int = 1000,
        base_state_lifetime: datetime.timedelta = WEEK,
    ) -> None:
        self.max_storage_size = max_storage_size
        self.base_state_lifetime = base_state_lifetime
        self.storage: Storage = {}

    def __repr__(self) -> str:
        return "<{}: max_storage_size={}, {}>".format(
            self.__class__.__name__,
            self.max_storage_size,
            ", ".join(
                f"{view_name}: {len(self.storage[view_name].values())} shortstates"
                for view_name in self.storage
            )
            or "empty",
        )

    async def drop(
        self,
        hasher: Hasher[EventModel, HasherData],
        id: HasherData,
        **context: typing.Any,
    ) -> None:
        if hasher not in self.storage:
            raise LookupError("No record of hasher {!r} found.".format(hasher))

        waiter_id: typing.Hashable = hasher.create_hash(id).expect(
            RuntimeError("Couldn't create hash from data")
        )
        short_state = self.storage[hasher].pop(waiter_id, None)
        if short_state is None:
            raise LookupError(
                "Waiter with identificator {} is not found for hasher {!r}".format(waiter_id, hasher)
            )

        short_state.cancel()

    async def drop_all(self) -> None:
        """Drops all waiters in storage."""

        for hasher in self.storage:
            for ident, short_state in self.storage[hasher].items():
                if short_state.context:
                    await self.drop(
                        hasher,
                        ident,
                    )
                else:
                    short_state.cancel()

    async def wait_from_event(
        self,
        view: BaseStateView[EventModel],
        event: EventModel,
        *,
        filter: ABCRule | None = None,
        release: ABCRule | None = None,
        lifetime: datetime.timedelta | float | None = None,
    ) -> ShortStateContext[EventModel]:
        hasher = StateViewHasher(view)
        return await self.wait(
            hasher=hasher,
            data=hasher.get_data_from_event(event).expect(
                RuntimeError("Hasher couldn't create data from event.")
            ),
            filter=filter,
            release=release,
            lifetime=lifetime,
        )

    async def wait(
        self,
        hasher: Hasher[EventModel, HasherData],
        data: HasherData,
        *,
        filter: ABCRule | None = None,
        release: ABCRule | None = None,
        lifetime: datetime.timedelta | float | None = None,
    ) -> ShortStateContext[EventModel]:
        if isinstance(lifetime, int | float):
            lifetime = datetime.timedelta(seconds=lifetime)

        event = asyncio.Event()
        short_state = ShortState[EventModel](
            filter=filter,
            release=release,
            event=event,
            lifetime=lifetime or self.base_state_lifetime,
        )
        waiter_hash = hasher.create_hash(data).expect(RuntimeError("Hasher couldn't create hash."))

        if hasher not in self.storage:
            hasher.view.middlewares.insert(0, WaiterMiddleware(self, hasher))
            self.storage[hasher] = LimitedDict(maxlimit=self.max_storage_size)

        if (deleted_short_state := self.storage[hasher].set(waiter_hash, short_state)) is not None:
            deleted_short_state.cancel()

        await event.wait()
        self.storage[hasher].pop(waiter_hash, None)
        assert short_state.context is not None
        return short_state.context

    async def clear_storage(
        self,
    ) -> None:
        """Clears storage."""

        for hasher in self.storage:
            now = datetime.datetime.now()
            for ident, short_state in self.storage.get(hasher, {}).copy().items():
                if short_state.expiration_date is not None and now > short_state.expiration_date:
                    await self.drop(
                        hasher,
                        ident,
                        force=True,
                    )


async def clear_wm_storage_worker(
    wm: WaiterMachine,
    interval_seconds: int = 60,
) -> typing.NoReturn:
    while True:
        await wm.clear_storage()
        await asyncio.sleep(interval_seconds)


__all__ = ("WaiterMachine",)
