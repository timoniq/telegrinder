import typing
from collections import deque

from nodnod.interface.inject import inject_internals

from telegrinder.api.api import API
from telegrinder.bot.cute_types.update import UpdateCute
from telegrinder.bot.dispatch.abc import ABCDispatch
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware, run_post_middleware, run_pre_middleware
from telegrinder.bot.dispatch.middleware.box import MiddlewareBox
from telegrinder.bot.dispatch.router.base import Router
from telegrinder.bot.dispatch.view.base import ErrorView, View
from telegrinder.bot.dispatch.view.box import ViewBox
from telegrinder.modules import log_buffer, logger
from telegrinder.node.scope import create_per_event_scope
from telegrinder.tools.fullname import fullname
from telegrinder.tools.global_context import TelegrinderContext
from telegrinder.types.objects import Update

if typing.TYPE_CHECKING:
    from vbml.patcher.abc import ABCPatcher

    from telegrinder.bot.dispatch.middleware.filter import FilterMiddleware
    from telegrinder.bot.dispatch.view.base import EventView, RawEventView, View
    from telegrinder.bot.dispatch.view.media_group import MediaGroupView
    from telegrinder.tools.lifespan import Lifespan

NANOSECONDS_PER_MILLISECOND: typing.Final = 1_000_000_000


class _ViewGetter:  # type: ignore
    main_router: Router

    def __getattr__(self, name: str, /) -> typing.Any:
        if name in ViewBox.__dataclass_fields__ or name in ViewBox.__dict__:
            return getattr(self.main_router, name)
        return super().__getattribute__(name)


class Dispatch[
    T: MiddlewareBox = MiddlewareBox,
    ErrorHandler: ErrorView = ErrorView,
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
    ManagedBotUpdatedView: EventView = EventView,
    MediaGroup: View = MediaGroupView,
    EventError: ErrorView = ErrorView,
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
        ManagedBotUpdatedView,
        MediaGroup,
        EventError,
        RawEvent,
    ]
    if typing.TYPE_CHECKING
    else _ViewGetter,
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
        ManagedBotUpdatedView,
        MediaGroup,
        EventError,
        RawEvent,
    ]

    main_router: MainRouter
    error_handler: ErrorHandler
    middlewares: T
    _routers: deque[Router] | None = None

    @typing.overload
    def __init__(self) -> None: ...

    @typing.overload
    def __init__(self, *, name: str) -> None: ...

    @typing.overload
    def __init__(self, *, router: MainRouter) -> None: ...

    @typing.overload
    def __init__(self, *, middleware_box: T) -> None: ...

    @typing.overload
    def __init__(self, *, name: str, middleware_box: T) -> None: ...

    @typing.overload
    def __init__(self, *, router: MainRouter, middleware_box: T) -> None: ...

    def __init__(
        self,
        *,
        name: str | None = None,
        router: MainRouter | None = None,
        error_handler: ErrorHandler | None = None,
        middleware_box: MiddlewareBox | None = None,
    ) -> None:
        self.main_router = router or Router(name=name)  # type: ignore
        self.error_handler = error_handler or ErrorView()  # type: ignore
        self.global_context = TelegrinderContext()
        self.global_scope = self.global_context.node_global_scope
        self.loop_wrapper = self.global_context.loop_wrapper
        self.middlewares = self.global_context.setdefault_value("middleware_box", middleware_box or MiddlewareBox())

    def __setitem__(self, injection_type: typing.Any, injection_value: typing.Any, /) -> None:
        self.global_scope.inject(injection_type, injection_value)

    @property
    def routers(self) -> deque[Router]:
        if self._routers is None:
            self._routers = deque((self.main_router,) if self.main_router else ())  # type: ignore
        return self._routers  # type: ignore

    @property
    def patcher(self) -> ABCPatcher:
        """Alias `patcher` to get a vbml patcher from the global context."""
        return self.global_context.vbml_patcher

    @property
    def lifespan(self) -> Lifespan:
        """Alias `lifespan` to get a lifespan from the loop wrapper."""
        return self.global_context.lifespan

    @property
    def register_middleware[Middleware: ABCMiddleware](self) -> typing.Callable[[type[Middleware]], type[Middleware]]:
        """Decorator to register a custom middleware in the dispatch's middleware box."""
        return self.middlewares.__call__

    @property
    def filter(self) -> FilterMiddleware:
        """Alias `filter` to get a filter middleware from the middleware box."""
        return self.middlewares.filter

    async def _handle_exceptions(
        self,
        api: API,
        update: Update,
        context: Context,
        exceptions: tuple[BaseException | BaseExceptionGroup[BaseException], ...],
    ) -> None:
        unhandled_exceptions: list[BaseException] = []

        try:
            async with self.loop_wrapper.create_task_group() as task_group:
                for exception in exceptions:
                    if isinstance(exception, BaseExceptionGroup):
                        task_group.create_task(
                            self._handle_exceptions(api, update, context.copy(), exception.exceptions),
                        )
                    elif isinstance(exception, Exception):
                        task_group.create_task(
                            self.main_router.process_view(
                                self.error_handler,
                                api,
                                update,
                                context.copy().add_exception_update(exception),
                            ),
                        )
                    else:
                        unhandled_exceptions.append(exception)
        except BaseExceptionGroup as group:
            if not unhandled_exceptions:
                raise

            raise BaseExceptionGroup(
                "Unhandled exception groups:",
                (group, BaseExceptionGroup("Unhandled exceptions:", unhandled_exceptions)),
            )

        if unhandled_exceptions:
            raise BaseExceptionGroup("Unhandled exceptions:", unhandled_exceptions)

    async def _process_update_exceptions(
        self,
        api: API,
        update: Update,
        context: Context,
    ) -> None:
        logger.debug(
            "Processing error views with exceptions [{}]",
            ", ".join(fullname(e) for e in context.exceptions_update.values()),
        )

        async with self.loop_wrapper.create_task_group() as task_group:
            for router, exception in context.exceptions_update.items():
                logger.debug("Proccessing exception via router `{!r}`", router)
                task_group.create_task(
                    router.process_view(
                        router.event_error,
                        api,
                        update,
                        context.copy().add_exception_update(exception),
                    ),
                )

    async def _route_update(self, api: API, update: Update, context: Context) -> None:
        async with self.loop_wrapper.create_task_group() as task_group:
            for router in self.routers:
                logger.debug("Routing to router `{!r}`", router)
                task_group.create_task(router.route(api, update, context.copy()))

    async def feed(self, api: API, update: Update) -> None:
        inject_internals(per_event_scope := create_per_event_scope(), {API: api, Update: update})

        with log_buffer(f"Update:{update.update_id} > Bot:{api.id}"):
            logger.info("New update was received, processing...")

            context = Context().add_roots(api, update, per_event_scope)
            failed = False
            middlewares = self.middlewares

            async with per_event_scope:
                start_time = self.loop_wrapper.time

                try:
                    for middleware in middlewares:
                        if await run_pre_middleware(middleware, context) is not True:
                            logger.info(
                                "Dispatch pre-middleware `{}` raised failure.",
                                fullname(middleware),
                            )
                            return

                    if self.routers:
                        await self._route_update(api, update, context)

                    for middleware in middlewares:
                        await run_post_middleware(middleware, context)
                except BaseException as exc:
                    failed = True

                    if context.exceptions_update:
                        try:
                            await self._process_update_exceptions(api, update, context)
                        except BaseExceptionGroup as group:
                            if not self.error_handler:
                                raise

                            logger.debug(
                                "Dispatch caught unhandled exceptions, routing to error handler...",
                            )
                            await self._handle_exceptions(api, update, context, group.exceptions)

                        return

                    if (
                        isinstance(exc, Exception)
                        and self.error_handler
                        and await self.main_router.check_view(self.error_handler, api, update, context)
                    ):
                        logger.debug(
                            "Dispatch caught an exception, routing to error handler...",
                        )
                        await self.main_router.process_view(
                            self.error_handler,
                            api,
                            update,
                            context.copy().add_exception_update(exc),
                        )
                        return

                    raise
                finally:
                    if not failed:
                        elapsed_time = self.loop_wrapper.time - start_time
                        elapsed_ms = elapsed_time * 1000
                        logger.debug(
                            "Update processed in {} {}.",
                            int(elapsed_time * NANOSECONDS_PER_MILLISECOND) if elapsed_ms < 1 else int(elapsed_ms),
                            "ns" if elapsed_ms < 1 else "ms",
                        )

    async def feed_raw(self, api: API, raw_update: str | bytes) -> None:
        await self.feed(api, UpdateCute.from_raw(raw_update))

    async def feed_cute(self, api: API, update_cute: UpdateCute) -> None:
        await self.feed(api, update_cute)

    def load(self, external: typing.Self) -> None:
        self.routers.extend(filter(None, external.routers))
        self.error_handler.load(external.error_handler)


__all__ = ("Dispatch",)
