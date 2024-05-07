import asyncio
import datetime
import typing
from collections import deque

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.rules.abc import ABCRule

from .middleware import WaiterMiddleware
from .short_state import Behaviour, EventModel, ShortState

T = typing.TypeVar("T")

Storage: typing.TypeAlias = dict[str, "ShortStateStorage"]
Identificator: typing.TypeAlias = str | int

if typing.TYPE_CHECKING:
    from telegrinder.bot.dispatch.view.abc import ABCStateView, BaseStateView


class ShortStateStorage(dict[Identificator, ShortState[EventModel]]):
    def __init__(self, *, maxlimit: int = 1000) -> None:
        super().__init__()
        self.maxlimit = maxlimit
        self.queue: deque[Identificator] = deque(maxlen=maxlimit)
    
    def __repr__(self) -> str:
        return "<{}: {}, (current={} | maxlimit={})>".format(
            self.__class__.__name__,
            super().__repr__(),
            len(self.queue),
            self.maxlimit,
        )
    
    def __setitem__(self, key: Identificator, value: ShortState[EventModel], /) -> None:
        self.add(key, value)
    
    def __delitem__(self, key: Identificator, /) -> None:
        self.pop(key, None)

    def add(self, id: Identificator, short_state: ShortState[EventModel]) -> None:
        if len(self.queue) >= self.maxlimit:
            self.pop(self.queue.popleft(), None)
        if id not in self.queue:
            self.queue.append(id)
        super().__setitem__(id, short_state)

    def clear(self) -> None:
        self.queue.clear()
        super().clear()
    
    def setdefault(self, id: Identificator, default: ShortState[EventModel]) -> ShortState[EventModel]:
        if id in self:
            return self[id]
        self.add(id, default)
        return default
    
    def pop(self, id: Identificator, default: T):  # type: ignore
        if id in self.queue:
            self.queue.remove(id)
        return super().pop(id, default)
    
    def popitem(self) -> tuple[Identificator, ShortState[EventModel]]:
        item = super().popitem()
        self.queue.remove(item[0])
        return item
    
    def update(
        self,
        mapping: typing.Mapping[Identificator, ShortState[EventModel]] | None = None,
        /,
        **kwargs: ShortState[EventModel],
    ) -> None:
        for key, value in (mapping if mapping is not None else kwargs).items():
            self.add(key, value)


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
        **context: typing.Any,
    ) -> None:
        view_name = state_view.__class__.__name__
        if view_name not in self.storage:
            raise LookupError("No record of view {!r} found".format(view_name))

        short_state = self.storage[view_name].pop(id, None)
        if short_state is None:
            raise LookupError(
                "Waiter with identificator {} is not found for view {!r}".format(
                    id,
                    view_name,
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
            short_state.on_drop_behaviour,
            short_state.event,
            **context,
        )

    async def wait(
        self,
        state_view: "BaseStateView[EventModel]",
        linked: EventModel | tuple[ABCAPI, Identificator],
        *rules: ABCRule[EventModel],
        default: Behaviour = None,
        on_drop: Behaviour = None,
        expiration: datetime.timedelta | int | float | None = None,
        short_state_storage: ShortStateStorage[EventModel] | None = None,
    ) -> tuple[EventModel, Context]:
        if isinstance(expiration, int | float):
            expiration = datetime.timedelta(seconds=expiration)

        api: ABCAPI; key: Identificator
        api, key = linked if isinstance(linked, tuple) else (linked.ctx_api, state_view.get_state_key(linked))  # type: ignore
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
            self.storage[view_name] = short_state_storage or ShortStateStorage()

        self.storage[view_name].add(key, short_state)
        await event.wait()

        e, ctx = getattr(event, "context")
        self.storage[view_name].pop(key, None)
        return e, ctx

    async def call_behaviour(
        self,
        view: "ABCStateView[EventModel]",
        behaviour: Behaviour,
        event: asyncio.Event | EventModel,
        **context: typing.Any,
    ) -> None:
        if behaviour is None:
            return
        # TODO: add behaviour check
        # TODO: support view as a behaviour
        await behaviour.run(event, context)  # type: ignore


__all__ = ("WaiterMachine",)
