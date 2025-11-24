from __future__ import annotations

import asyncio
import typing
from collections import deque

from kungfu.library.monad.option import Nothing, Option, Some
from vbml.patcher.abc import ABCPatcher

from telegrinder.api.api import API
from telegrinder.bot.dispatch.abc import ABCDispatch
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.middleware.abc import run_middleware
from telegrinder.bot.dispatch.middleware.global_middleware import GlobalMiddleware
from telegrinder.bot.dispatch.router.base import Router
from telegrinder.bot.dispatch.view.abc import ABCView
from telegrinder.bot.dispatch.view.base import View
from telegrinder.bot.dispatch.view.box import ViewBox
from telegrinder.modules import logger
from telegrinder.node.composer import CONTEXT_STORE_NODES_KEY
from telegrinder.node.scope import NodeScope
from telegrinder.node.session import close_sessions
from telegrinder.tools.aio import get_tasks_results
from telegrinder.tools.global_context import TelegrinderContext
from telegrinder.types.objects import Update

if typing.TYPE_CHECKING:
    from telegrinder.node.composer import Composer

NANOSECONDS_PER_MILLISECOND: typing.Final = 1_000_000_000


class Dispatch(ABCDispatch, ViewBox if typing.TYPE_CHECKING else object):
    main_router: Router
    global_middleware: GlobalMiddleware
    global_context: TelegrinderContext
    _routers: deque[Router] | None

    def __init__(
        self,
        *,
        router: Router | None = None,
        global_middleware: GlobalMiddleware | None = None,
    ) -> None:
        self.main_router = router or Router()
        self.global_middleware = global_middleware or GlobalMiddleware()
        self.global_context = TelegrinderContext()
        self._routers = None

    if not typing.TYPE_CHECKING:

        def __getattr__(self, name: str, /) -> typing.Any:
            if name in ViewBox.__dataclass_fields__ or name in ViewBox.__dict__:
                return getattr(self.main_router, name)
            return super().__getattribute__(name)

    @property
    def routers(self) -> deque[Router]:
        if self._routers is None:
            self._routers = deque((self.main_router,) if self.main_router else ())
        return self._routers

    @property
    def raw_views(self) -> tuple[View, ...]:
        return tuple(filter(None, (router.raw for router in self.routers)))

    @property
    def error_views(self) -> tuple[View, ...]:
        return tuple(filter(None, (router.error for router in self.routers)))

    @property
    def patcher(self) -> ABCPatcher:
        """Alias `patcher` to get `vbml.Patcher` from the global context."""
        return self.global_context.vbml_patcher

    @property
    def composer(self) -> Composer:
        """Alias `composer` to get `telegrinder.node.composer.Composer` from the global context."""
        return self.global_context.composer.unwrap()

    async def _process_views(
        self,
        views: typing.Iterable[View],
        api: API,
        update: Update,
        context: Context,
    ) -> bool:
        if not views:
            return False

        tasks: set[asyncio.Task[bool]] = set()

        async with asyncio.TaskGroup() as task_group:
            for view in views:
                tasks.add(task_group.create_task(self.main_router.route_view(view, api, update, context)))

        return any(get_tasks_results(tasks))

    async def _process_update_exceptions(
        self,
        api: API,
        update: Update,
        context: Context,
    ) -> bool:
        if not context.exceptions_update:
            return False

        tasks: set[asyncio.Task[bool]] = set()

        async with asyncio.TaskGroup() as task_group:
            for router, exception in context.exceptions_update.items():
                await logger.adebug(
                    "Routing exception update (id={}, type={!r}) to router `{!r}`",
                    # type(exception).__name__,
                    update.update_id,
                    update.update_type,
                    router,
                )
                tasks.add(
                    task_group.create_task(
                        router.route_view(router.error, api, update, context.add_exception_update(exception))
                    )
                )

        return any(get_tasks_results(tasks))

    async def _route_update(self, api: API, update: Update, context: Context) -> bool:
        if not self.routers:
            return False

        tasks: set[asyncio.Task[bool]] = set()

        async with asyncio.TaskGroup() as task_group:
            for router in self.routers:
                await logger.adebug(
                    "Routing update (id={}, type={!r}) to router `{!r}`", update.update_id, update.update_type, router
                )
                tasks.add(task_group.create_task(router.route(api, update, context)))

        return any(get_tasks_results(tasks))

    async def feed(self, api: API, update: Update) -> None:
        await logger.ainfo("New Update(id={}, type={!r})", update.update_id, update.update_type)

        failed = False
        context = Context().add_update_cute(update, api)
        start_time = self.global_context.loop_wrapper.loop.time()

        try:
            if (
                await run_middleware(
                    self.global_middleware.pre,
                    api,
                    update,
                    context,
                    required_nodes=self.global_middleware.pre_required_nodes,
                )
                is False
            ):
                return

            if not self.routers:
                await logger.adebug(
                    "Dispatch doesn't provide routers. Skipping update (id={}, type={!r})",
                    update.update_id,
                    update.update_type,
                )
            elif not await self._route_update(api, update, context):
                await self._process_views(self.raw_views, api, update, context)

            await run_middleware(
                self.global_middleware.post,
                api,
                update,
                context,
                required_nodes=self.global_middleware.post_required_nodes,
            )
        except BaseException as e:
            if not context.exceptions_update or not isinstance(e, Exception):
                failed = True
                raise  # Throwing control flow exceptions

            await logger.adebug(
                "Processing error views with exceptions [{}] for update (id={}, type={!r})",
                ", ".join(f"{type(e).__name__}" for e in context.exceptions_update.values()),
                update.update_id,
                update.update_type,
            )

            if await self._process_update_exceptions(api, update, context):
                return

            failed = True
            await logger.aexception(
                "Update (id={}, type={!r}) processed with exception, traceback message below:",
                update.update_id,
                update.update_type,
            )
        finally:
            if not failed:
                elapsed_time = self.global_context.loop_wrapper.loop.time() - start_time
                elapsed_ms = elapsed_time * 1000
                await logger.adebug(
                    "Update (id={}, type={!r}) processed in {} {} by bot (id={})",
                    update.update_id,
                    update.update_type,
                    int(elapsed_time * NANOSECONDS_PER_MILLISECOND) if elapsed_ms < 1 else int(elapsed_ms),
                    "ns" if elapsed_ms < 1 else "ms",
                    api.id,
                )

            await close_sessions(
                context.get(CONTEXT_STORE_NODES_KEY, {}),
                scopes=(NodeScope.PER_CALL, NodeScope.PER_EVENT),
            )

    def load(self, external: typing.Self) -> None:
        self.routers.extend(filter(None, external.routers))
        self.global_middleware.filters.difference_update(external.global_middleware.filters)

    def get_view[T: ABCView](self, of_type: type[T]) -> Option[T]:
        for view in self.main_router.views.values():
            if isinstance(view, of_type):
                return Some(view)

        return Nothing()


__all__ = ("Dispatch",)
