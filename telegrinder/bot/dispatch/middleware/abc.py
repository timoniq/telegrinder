from __future__ import annotations

from abc import ABC

import typing_extensions as typing
from fntypes import Some

from telegrinder.api import API
from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.model import Model
from telegrinder.modules import logger
from telegrinder.tools.adapter.abc import ABCAdapter, run_adapter
from telegrinder.tools.lifespan import Lifespan
from telegrinder.types.objects import Update

ToEvent = typing.TypeVar("ToEvent", bound=Model, default=typing.Any)


async def run_middleware[Event: Model, R: bool | None](
    method: typing.Callable[typing.Concatenate[Event, Context, ...], typing.Awaitable[R]],
    api: API,
    event: Event,
    ctx: Context,
    raw_event: Update | None = None,
    adapter: "ABCAdapter[Update, Event] | None" = None,
    *args: typing.Any,
    **kwargs: typing.Any,
) -> R:
    if adapter is not None:
        if raw_event is None:
            raise RuntimeError("raw_event must be specified to apply adapter")
        match await run_adapter(adapter, api, raw_event, ctx):
            case Some(val):
                event = val
            case _:
                return False  # type: ignore

    logger.debug("Running {}-middleware {!r}...", method.__name__, method.__qualname__.split(".")[0])
    return await method(event, ctx, *args, **kwargs)  # type: ignore


class ABCMiddleware[Event: Model | BaseCute](ABC):
    adapter: ABCAdapter[Update, Event] | None = None

    def __repr__(self) -> str:
        name = f"middleware {self.__class__.__name__!r}:"
        has_pre = self.pre.__qualname__.split(".")[0] != "ABCMiddleware"
        has_post = self.post.__qualname__.split(".")[0] != "ABCMiddleware"

        if has_post:
            name = "post-" + name
        if has_pre:
            name = "pre-" + name

        return "<{} with adapter={!r}>".format(name, self.adapter)

    async def pre(self, event: Event, ctx: Context) -> bool: ...

    async def post(self, event: Event, ctx: Context) -> None: ...

    @typing.overload
    def to_lifespan(self, event: Event, ctx: Context | None = None, *, api: API) -> Lifespan: ...

    @typing.overload
    def to_lifespan(self, event: Event, ctx: Context | None = None) -> Lifespan: ...

    def to_lifespan(
        self,
        event: Event,
        ctx: Context | None = None,
        api: API | None = None,
        **add_context: typing.Any,
    ) -> Lifespan:
        if api is None:
            if not isinstance(event, BaseCute):
                raise LookupError("Cannot get api, please pass as kwarg or provide BaseCute api-bound event")
            api = event.api

        ctx = ctx or Context()
        ctx |= add_context
        return Lifespan(
            startup_tasks=[run_middleware(self.pre, api, event, raw_event=None, ctx=ctx, adapter=None)],
            shutdown_tasks=[
                run_middleware(
                    self.post,
                    api,
                    event,
                    raw_event=None,
                    ctx=ctx,
                    adapter=None,
                )
            ],
        )


__all__ = ("ABCMiddleware", "run_middleware")
