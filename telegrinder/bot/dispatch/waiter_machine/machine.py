import asyncio
import datetime
import typing

from telegrinder.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.view.abc import ABCStateView, BaseStateView
from telegrinder.bot.dispatch.waiter_machine.middleware import WaiterMiddleware
from telegrinder.bot.dispatch.waiter_machine.short_state import (
    Behaviour,
    EventModel,
    ShortState,
    ShortStateContext,
)
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.tools.limited_dict import LimitedDict
from telegrinder.types import Update

if typing.TYPE_CHECKING:
    from telegrinder.bot.dispatch import Dispatch

T = typing.TypeVar("T")

Identificator: typing.TypeAlias = str | int
Storage: typing.TypeAlias = dict[str, LimitedDict[Identificator, ShortState[EventModel]]]

WEEK: typing.Final[datetime.timedelta] = datetime.timedelta(days=7)


class WaiterMachine:
    def __init__(self, *, max_storage_size: int = 1000) -> None:
        self.max_storage_size = max_storage_size
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
        state_view: typing.Union["ABCStateView[EventModel]", str],
        id: Identificator,
        event: EventModel,
        update: Update,
        **context: typing.Any,
    ) -> None:
        view_name = state_view if isinstance(state_view, str) else state_view.__class__.__name__
        if view_name not in self.storage:
            raise LookupError("No record of view {!r} found.".format(view_name))

        short_state = self.storage[view_name].pop(id, None)
        if short_state is None:
            raise LookupError("Waiter with identificator {} is not found for view {!r}".format(id, view_name))

        short_state.cancel()
        await self.call_behaviour(
            event,
            update,
            behaviour=short_state.on_drop_behaviour,
            **context,
        )

    async def drop_all(self) -> None:
        """Drops all waiters in storage"""
        for view_name in self.storage:
            for ident, short_state in self.storage[view_name].items():
                if short_state.context:
                    await self.drop(
                        view_name,
                        ident,
                        short_state.context.event,
                        short_state.context.context.raw_update
                    )
                else:
                    short_state.cancel()

    async def wait(
        self,
        state_view: "BaseStateView[EventModel]",
        linked: EventModel | tuple[API, Identificator],
        *rules: ABCRule,
        default: Behaviour[EventModel] | None = None,
        on_drop: Behaviour[EventModel] | None = None,
        exit: Behaviour[EventModel] | None = None,
        expiration: datetime.timedelta | float | None = None,
    ) -> ShortStateContext[EventModel]:
        if isinstance(expiration, int | float):
            expiration = datetime.timedelta(seconds=expiration)

        api: API
        key: Identificator
        api, key = linked if isinstance(linked, tuple) else (linked.ctx_api, state_view.get_state_key(linked))  # type: ignore
        if not key:
            raise RuntimeError("Unable to get state key.")

        view_name = state_view.__class__.__name__
        event = asyncio.Event()
        short_state = ShortState[EventModel](
            key,
            api,
            event,
            rules,
            expiration=expiration,
            default_behaviour=default,
            on_drop_behaviour=on_drop,
            exit_behaviour=exit,
        )

        if view_name not in self.storage:
            state_view.middlewares.insert(0, WaiterMiddleware(self, state_view))
            self.storage[view_name] = LimitedDict(maxlimit=self.max_storage_size)

        if (deleted_short_state := self.storage[view_name].set(key, short_state)) is not None:
            deleted_short_state.cancel()

        await event.wait()
        self.storage[view_name].pop(key, None)
        assert short_state.context is not None
        return short_state.context

    async def call_behaviour(
        self,
        event: EventModel,
        update: Update,
        behaviour: Behaviour[EventModel] | None = None,
        **context: typing.Any,
    ) -> bool:
        # TODO: support view as a behaviour

        if behaviour is None:
            return False

        ctx = Context(**context)
        if await behaviour.check(event.api, update, ctx):
            await behaviour.run(event.api, event, ctx)
            return True

        return False

    async def clear_storage(
        self,
        views: typing.Iterable[ABCStateView[EventModel]],
        absolutely_dead_time: datetime.timedelta = WEEK,
    ) -> None:
        """Clears storage.

        :param absolutely_dead_time: timedelta when state can be forgotten.
        """

        for view in views:
            view_name = view.__class__.__name__
            now = datetime.datetime.now()
            for ident, short_state in self.storage.get(view_name, {}).copy().items():
                if short_state.expiration_date is not None and now > short_state.expiration_date:
                    assert short_state.context  # FIXME: why???
                    await self.drop(
                        view,
                        ident,
                        event=short_state.context.event,
                        update=short_state.context.context.raw_update,
                        force=True,
                    )
                elif short_state.creation_date + absolutely_dead_time < now:
                    short_state.cancel()
                    del self.storage[view_name][short_state.key]


async def clear_wm_storage_worker(
    wm: WaiterMachine,
    dp: "Dispatch",
    interval_seconds: int = 60,
    absolutely_dead_time: datetime.timedelta = WEEK,
) -> typing.NoReturn:
    while True:
        await wm.clear_storage(
            views=[view for view in dp.get_views().values() if isinstance(view, ABCStateView)],
            absolutely_dead_time=absolutely_dead_time,
        )
        await asyncio.sleep(interval_seconds)


__all__ = ("WaiterMachine",)
