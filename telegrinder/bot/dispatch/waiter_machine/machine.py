import asyncio
import typing
import datetime

from telegrinder.bot.rules.abc import ABCRule
from telegrinder.api.abc import ABCAPI

from .middleware import WaiterMiddleware
from .short_state import Behaviour, EventModel, ShortState

Identificator = str | int
Storage = dict[str, dict[Identificator, "ShortState"]]


if typing.TYPE_CHECKING:
    from telegrinder.bot.dispatch.view.abc import ABCStateView


class WaiterMachine:
    def __init__(self) -> None:
        self.storage: Storage = {}

    async def drop(
        self,
        state_view: "ABCStateView",
        id: Identificator,
        **context,
    ) -> None:
        view_name = state_view.__class__.__name__
        if view_name not in self.storage:
            raise LookupError("No record of view {} found".format(view_name))

        short_state = self.storage[view_name].pop(id, None)
        if not short_state:
            raise LookupError(
                "Waiter with identificator {} is not found for view {!r}".format(
                    id, view_name
                )
            )

        waiters: typing.Iterable[asyncio.Future] = short_state.event._waiters  # type: ignore

        for future in waiters:
            future.cancel()

        await self.call_behaviour(
            state_view,  # type: ignore
            short_state.on_drop_behaviour,
            short_state.event,
            **context,
        )

    async def wait(
        self,
        state_view: "ABCStateView",
        linked: EventModel | tuple[ABCAPI, Identificator],
        *rules: ABCRule[EventModel],
        default: Behaviour = None,
        on_drop: Behaviour = None,
        expiration: typing.Union[datetime.timedelta, int, None] = None,
    ) -> typing.Tuple[EventModel, dict]:
        if isinstance(expiration, int):
            expiration = datetime.timedelta(seconds=expiration)

        event = asyncio.Event()

        api: ABCAPI
        key: Identificator

        if isinstance(linked, tuple):
            api, key = linked
        else:
            api = linked.ctx_api
            key = state_view.get_state_key(linked)
            if not key:
                raise RuntimeError("Unable to get state key")

        short_state = ShortState(
            key,
            ctx_api=api,
            event=event,
            rules=rules,
            expiration=expiration,
            default_behaviour=default,
            on_drop_behaviour=on_drop,
        )

        view_name = state_view.__class__.__name__
        if view_name not in self.storage:
            state_view.middlewares.append(WaiterMiddleware(self, state_view))  # type: ignore
            self.storage[view_name] = {}

        self.storage[view_name][key] = short_state

        await event.wait()

        e, ctx = getattr(event, "context")
        self.storage[view_name].pop(key)

        return e, ctx

    async def call_behaviour(
        self,
        view: "ABCStateView",
        behaviour: Behaviour,
        event: EventModel,
        **context,
    ) -> None:
        if behaviour is None:
            return
        # todo: add behaviour check
        # todo: support view as a behaviour
        await behaviour.run(event)
