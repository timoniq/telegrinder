from __future__ import annotations

import typing
from collections import deque

from nodnod.scope import Scope

from telegrinder.api.api import API
from telegrinder.bot.dispatch.abc import ABCDispatch
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.middleware.abc import run_post_middleware, run_pre_middleware
from telegrinder.bot.dispatch.middleware.global_middleware import GlobalMiddleware
from telegrinder.bot.dispatch.router.base import Router
from telegrinder.bot.dispatch.view.base import View
from telegrinder.bot.dispatch.view.box import ViewBox
from telegrinder.modules import logger
from telegrinder.node.compose import inject_internals
from telegrinder.node.scope import PER_EVENT
from telegrinder.tools.global_context import TelegrinderContext
from telegrinder.types.objects import Update

if typing.TYPE_CHECKING:
    from vbml.patcher.abc import ABCPatcher

    from telegrinder.bot.dispatch.view.base import ErrorView, EventView, RawEventView, View
    from telegrinder.bot.dispatch.view.media_group import MediaGroupView
    from telegrinder.tools.loop_wrapper import LoopWrapper

NANOSECONDS_PER_MILLISECOND: typing.Final = 1_000_000_000


class ViewGetter:
    main_router: Router

    def __getattr__(self, name: str, /) -> typing.Any:
        if name in ViewBox.__dataclass_fields__ or name in ViewBox.__dict__:
            return getattr(self.main_router, name)
        return super().__getattribute__(name)


class Dispatch[
    MessageView: EventView = EventView,
    EditedMessageView: EventView = EventView,
    ChannelPostView: EventView = EventView,
    EditedChannelPostView: EventView = EventView,
    BusinessConnectionView: EventView = EventView,
    BusinessMessageView: EventView = EventView,
    EditedBusinessMessageView: EventView = EventView,
    DeletedBusinessMessagesView: EventView = EventView,
    MessageReactionView: EventView = EventView,
    MessageReactionCountView: EventView = EventView,
    InlineQueryView: EventView = EventView,
    ChosenInlineResultView: EventView = EventView,
    CallbackQueryView: EventView = EventView,
    ShippingQueryView: EventView = EventView,
    PreCheckoutQueryView: EventView = EventView,
    PurchasedPaidMediaView: EventView = EventView,
    PollView: EventView = EventView,
    PollAnswerView: EventView = EventView,
    MyChatMemberView: EventView = EventView,
    ChatMemberView: EventView = EventView,
    ChatJoinRequestView: EventView = EventView,
    ChatBoostView: EventView = EventView,
    RemovedChatBoostView: EventView = EventView,
    MediaGroup: View = MediaGroupView,
    Error: ErrorView = ErrorView,
    RawEvent: RawEventView = RawEventView,
](
    ABCDispatch,
    ViewBox[
        MessageView,
        EditedMessageView,
        ChannelPostView,
        EditedChannelPostView,
        BusinessConnectionView,
        BusinessMessageView,
        EditedBusinessMessageView,
        DeletedBusinessMessagesView,
        MessageReactionView,
        MessageReactionCountView,
        InlineQueryView,
        ChosenInlineResultView,
        CallbackQueryView,
        ShippingQueryView,
        PreCheckoutQueryView,
        PurchasedPaidMediaView,
        PollView,
        PollAnswerView,
        MyChatMemberView,
        ChatMemberView,
        ChatJoinRequestView,
        ChatBoostView,
        RemovedChatBoostView,
        MediaGroup,
        Error,
        RawEvent,
    ]
    if typing.TYPE_CHECKING
    else ViewGetter,
):
    type MainRouter = Router[
        MessageView,
        EditedMessageView,
        ChannelPostView,
        EditedChannelPostView,
        BusinessConnectionView,
        BusinessMessageView,
        EditedBusinessMessageView,
        DeletedBusinessMessagesView,
        MessageReactionView,
        MessageReactionCountView,
        InlineQueryView,
        ChosenInlineResultView,
        CallbackQueryView,
        ShippingQueryView,
        PreCheckoutQueryView,
        PurchasedPaidMediaView,
        PollView,
        PollAnswerView,
        MyChatMemberView,
        ChatMemberView,
        ChatJoinRequestView,
        ChatBoostView,
        RemovedChatBoostView,
        MediaGroup,
        Error,
        RawEvent,
    ]

    main_router: MainRouter
    global_middleware: GlobalMiddleware
    global_context: TelegrinderContext
    _routers: deque[Router] | None

    def __init__(
        self,
        *,
        router: MainRouter | None = None,
        global_middleware: GlobalMiddleware | None = None,
    ) -> None:
        self.main_router = router or Router()  # type: ignore
        self.global_middleware = global_middleware or GlobalMiddleware()
        self.global_context = TelegrinderContext()
        self._routers = None

    @property
    def routers(self) -> deque[Router]:
        if self._routers is None:
            self._routers = deque((self.main_router,) if self.main_router else ())  # type: ignore
        return self._routers  # type: ignore

    @property
    def raw_views(self) -> tuple[View, ...]:
        return tuple(filter(None, (router.raw for router in self.routers)))

    @property
    def patcher(self) -> ABCPatcher:
        """Alias `patcher` to get a vbml patcher from the global context."""
        return self.global_context.vbml_patcher

    @property
    def loop_wrapper(self) -> LoopWrapper:
        """Alias `loop_wrapper` to get `telegrinder.tools.loop_wrapper.LoopWrapper` from the global context."""
        return self.global_context.loop_wrapper

    @property
    def global_scope(self) -> Scope:
        """Alias `global_scope` to get `nodnod.scope.Scope` from the global context."""
        return self.global_context.node_global_scope

    async def _process_views(
        self,
        views: typing.Iterable[View],
        api: API,
        update: Update,
        context: Context,
    ) -> bool:
        if not views:
            return False

        async with self.global_context.loop_wrapper.create_task_group() as task_group:
            for view in views:
                task_group.create_task(self.main_router.route_view(view, api, update, context))

        return any(task_group.results())

    async def _process_update_exceptions(
        self,
        api: API,
        update: Update,
        context: Context,
    ) -> bool:
        if not context.exceptions_update:
            return False

        await logger.adebug(
            "Processing error views with exceptions [{}] for update (id={}, type={!r})",
            ", ".join(f"{type(e).__name__}" for e in context.exceptions_update.values()),
            update.update_id,
            update.update_type,
        )

        found = False

        async with self.global_context.loop_wrapper.create_task_group() as task_group:
            for router, exception in context.exceptions_update.items():
                if not router.error:
                    try:
                        raise exception from None
                    except Exception:
                        await logger.aexception(
                            "Exception update (id={}, type={!r}) from router `{!r}` is not processed, traceback message below:",
                            update.update_id,
                            update.update_type,
                            router,
                        )
                    continue

                found = True
                await logger.adebug(
                    "Routing exception update (id={}, type={!r}) to router `{!r}`",
                    update.update_id,
                    update.update_type,
                    router,
                )
                task_group.create_task(
                    router.route_view(
                        router.error,
                        api,
                        update,
                        context.copy().add_exception_update(exception),
                    ),
                )

        return True if not found else any(task_group.results())

    async def _route_update(self, api: API, update: Update, context: Context) -> bool:
        if not self.routers:
            return False

        async with self.global_context.loop_wrapper.create_task_group() as task_group:
            for router in self.routers:
                await logger.adebug(
                    "Routing update (id={}, type={!r}) to router `{!r}`", update.update_id, update.update_type, router
                )
                task_group.create_task(router.route(api, update, context))

        return any(task_group.results())

    async def feed(self, api: API, update: Update) -> None:
        await logger.ainfo("New Update(id={}, type={!r})", update.update_id, update.update_type)

        per_event_scope = self.global_scope.create_child(detail=PER_EVENT)
        context = Context().add_roots(api, update, per_event_scope)

        inject_internals(
            per_event_scope,
            {API: api, Update: update, Context: context},
        )

        failed = False
        start_time = self.global_context.loop_wrapper.loop.time()

        try:
            if await run_pre_middleware(self.global_middleware, context) is False:
                return

            if not self.routers:
                await logger.adebug(
                    "Dispatch doesn't provide routers. Skipping update (id={}, type={!r})",
                    update.update_id,
                    update.update_type,
                )
            elif not await self._route_update(api, update, context):
                await self._process_views(self.raw_views, api, update, context)

            await run_post_middleware(self.global_middleware, context)
        except BaseException as e:
            failed = True

            if not isinstance(e, Exception) and not isinstance(e, BaseExceptionGroup):
                raise  # Throwing control flow exceptions

            #if not await self._process_update_exceptions(api, update, context):
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

            await per_event_scope.close()

    def load(self, external: typing.Self) -> None:
        self.routers.extend(filter(None, external.routers))
        self.global_middleware.filters.difference_update(external.global_middleware.filters)


__all__ = ("Dispatch",)
