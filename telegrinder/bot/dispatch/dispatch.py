import typing
from collections import deque

from kungfu.library.monad.option import Some
from nodnod.interface.inject import inject_internals
from nodnod.scope import Scope

from telegrinder.api.api import API
from telegrinder.bot.dispatch.abc import ABCDispatch
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware, run_post_middleware, run_pre_middleware
from telegrinder.bot.dispatch.middleware.box import MiddlewareBox
from telegrinder.bot.dispatch.router.base import Router
from telegrinder.bot.dispatch.view.base import View
from telegrinder.bot.dispatch.view.box import ViewBox
from telegrinder.modules import logger
from telegrinder.node.scope import PER_EVENT
from telegrinder.tools.fullname import fullname
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
    T: MiddlewareBox = MiddlewareBox,
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
    global_context: TelegrinderContext
    _routers: deque[Router] | None

    @typing.overload
    def __init__(self) -> None: ...

    @typing.overload
    def __init__(self, *, router: MainRouter) -> None: ...

    @typing.overload
    def __init__(self, *, middleware_box: T) -> None: ...

    @typing.overload
    def __init__(self, *, router: MainRouter, middleware_box: T) -> None: ...

    def __init__(
        self,
        *,
        router: MainRouter | None = None,
        middleware_box: MiddlewareBox | None = None,
    ) -> None:
        self.main_router = router or Router()  # type: ignore
        self.global_context = TelegrinderContext()
        self._routers = None

        if not self.global_context.middleware_box or middleware_box is not None:
            self.global_context.middleware_box = Some(middleware_box or MiddlewareBox())

    def __setitem__(self, injection_type: typing.Any, injection_value: typing.Any, /) -> None:
        self.global_scope.inject(injection_type, injection_value)

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

    @property
    def middleware_box(self) -> T:
        """Alias `middleware_box` to get middleware box from the global context."""
        return typing.cast("T", self.global_context.middleware_box.unwrap())

    @property
    def global_middleware[Middleware: ABCMiddleware](self) -> typing.Callable[[type[Middleware]], type[Middleware]]:
        """Decorator to register a custom global middleware in the middleware box."""
        return self.middleware_box.__call__

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
    ) -> None:
        await logger.adebug(
            "Processing error views with exceptions [{}] for update (id={}, type={!r})",
            ", ".join(f"{type(e).__name__}" for e in context.exceptions_update.values()),
            update.update_id,
            update.update_type,
        )

        async with self.global_context.loop_wrapper.create_task_group() as task_group:
            for router, exception in context.exceptions_update.items():
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

    async def _route_update(self, api: API, update: Update, context: Context) -> bool:
        if not self.routers:
            return False

        async with self.global_context.loop_wrapper.create_task_group() as task_group:
            for router in self.routers:
                await logger.adebug(
                    "Routing update (id={}, type={!r}) to router `{!r}`",
                    update.update_id,
                    update.update_type,
                    router,
                )
                task_group.create_task(router.route(api, update, context))

        return any(task_group.results())

    async def feed(self, api: API, update: Update) -> None:
        await logger.ainfo("New Update(id={}, type={!r})", update.update_id, update.update_type)

        per_event_scope = self.global_scope.create_child(detail=PER_EVENT)
        context = Context().add_roots(api, update, per_event_scope)

        inject_internals(per_event_scope, {API: api, Update: update})

        failed = False
        middleware_box = self.middleware_box
        start_time = self.global_context.loop_wrapper.loop.time()

        try:
            for middleware in middleware_box:
                if await run_pre_middleware(middleware, context) is not True:
                    await logger.ainfo(
                        "Update(id={}, type={!r}) processed with global pre-middleware `{}` and raised failure.",
                        update.update_id,
                        update.update_type,
                        fullname(middleware),
                    )
                    return

            if not self.routers:
                await logger.adebug(
                    "Dispatch has empty routers, skipping update (id={}, type={!r}).",
                    update.update_id,
                    update.update_type,
                )
            elif not await self._route_update(api, update, context):
                await self._process_views(self.raw_views, api, update, context)

            for middleware in middleware_box:
                await run_post_middleware(middleware, context)
        except BaseException as e:
            failed = True

            if (
                not isinstance(e, Exception) and not isinstance(e, BaseExceptionGroup)
            ) or not context.exceptions_update:
                raise  # Throwing control flow exceptions

            await self._process_update_exceptions(api, update, context)
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


__all__ = ("Dispatch",)
