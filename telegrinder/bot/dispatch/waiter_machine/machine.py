import asyncio
import datetime
import typing

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.tools.limited_dict import LimitedDict
from telegrinder.types import Update

from .middleware import WaiterMiddleware
from .short_state import Behaviour, EventModel, ShortState

if typing.TYPE_CHECKING:
    from telegrinder.bot.dispatch.view.abc import ABCStateView, BaseStateView

T = typing.TypeVar("T")

Identificator: typing.TypeAlias = str | int
Storage: typing.TypeAlias = dict[str, LimitedDict[Identificator, ShortState[EventModel]]]


class WaiterMachine:
    def __init__(self) -> None:
        self.storage: Storage = {}

    def __repr__(self) -> str:
        return "<{}: storage={!r}>".format(
            self.__class__.__name__,
            self.storage,
        )

    async def drop(
        self,
        state_view: "ABCStateView[EventModel]",
        id: Identificator,
        update: Update,
        **context: typing.Any,
    ) -> None:
        view_name = state_view.__class__.__name__
        if view_name not in self.storage:
            raise LookupError("No record of view {!r} found".format(view_name))

        short_state = self.storage[view_name].pop(id, None)
        if short_state is None:
            raise LookupError(
                "Waiter with identificator {} is not found for view {!r}".format(
                    id, view_name
                )
            )

        waiters = typing.cast(
            typing.Iterable[asyncio.Future[typing.Any]],
            short_state.event._waiters,  # type: ignore
        )
        for future in waiters:
            future.cancel()

        await self.call_behaviour(
            state_view,
            short_state.event,
            update,
            behaviour=short_state.on_drop_behaviour,
            **context,
        )

    async def wait(
        self,
        state_view: "BaseStateView[EventModel]",
        linked: EventModel | tuple[ABCAPI, Identificator],
        *rules: ABCRule[EventModel],
        default: Behaviour = None,
        on_drop: Behaviour = None,
        expiration: datetime.timedelta | int | None = None,
    ) -> tuple[EventModel, Context]:
        if isinstance(expiration, int | float):
            expiration = datetime.timedelta(seconds=expiration)

        api: ABCAPI
        key: Identificator
        api, key = (
            linked
            if isinstance(linked, tuple)
            else (linked.ctx_api, state_view.get_state_key(linked))
        )  # type: ignore
        if not key:
            raise RuntimeError("Unable to get state key.")

        event = asyncio.Event()
        short_state = ShortState(
            key,
            api,
            event,
            rules,
            expiration=expiration,
            default_behaviour=default,
            on_drop_behaviour=on_drop,
        )
        view_name = state_view.__class__.__name__
        if view_name not in self.storage:
            state_view.middlewares.insert(0, WaiterMiddleware(self, state_view))
            self.storage[view_name] = LimitedDict()

        self.storage[view_name][key] = short_state
        await event.wait()

        e, ctx = getattr(event, "context")
        self.storage[view_name].pop(key, None)
        return e, ctx

    async def call_behaviour(
        self,
        view: "ABCStateView[EventModel]",
        event: asyncio.Event | EventModel,
        update: Update,
        behaviour: Behaviour[EventModel] | None = None,
        **context: typing.Any,
    ) -> None:
        # TODO: support param view as a behaviour

        ctx = Context(**context)

        if isinstance(event, asyncio.Event):
            event, preset_ctx = typing.cast(
                tuple[EventModel, Context],
                getattr(event, "context"),
            )
            ctx.update(preset_ctx)

        if behaviour is None:
            return

        if await behaviour.check(event.api, update, ctx):
            await behaviour.run(event, ctx)
        

__all__ = ("WaiterMachine",)
