import contextlib
import time
import typing
from collections import deque

from nodnod.interface.inject import inject_internals

from telegrinder.api.api import API
from telegrinder.bot.cute_types.update import UpdateCute
from telegrinder.bot.dispatch.abc import ABCDispatch
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware, run_post_middleware, run_pre_middleware
from telegrinder.bot.dispatch.middleware.box import MiddlewareBox
from telegrinder.bot.dispatch.middleware.waiter import WaiterMiddleware
from telegrinder.bot.dispatch.router.base import Router
from telegrinder.bot.dispatch.view.base import ErrorView, View
from telegrinder.bot.dispatch.view.box import ViewBox
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.modules import log_buffer, logger
from telegrinder.node.scope import create_per_event_scope
from telegrinder.scenario.checkbox import Checkbox
from telegrinder.scenario.choice import Choice
from telegrinder.tools.fullname import fullname
from telegrinder.tools.global_context import TelegrinderContext
from telegrinder.tools.waiter_machine.machine import (
    ContextUnpackProto,
    HasherWithData,
    ShortStateContext,
    WaiterMachine,
    unpack_to_context,
)
from telegrinder.types.objects import Update

if typing.TYPE_CHECKING:
    import datetime

    from vbml.patcher.abc import ABCPatcher

    from telegrinder.bot.cute_types.base import BaseCute
    from telegrinder.bot.dispatch.middleware.filter import FilterMiddleware
    from telegrinder.bot.dispatch.router.base import Injections
    from telegrinder.bot.dispatch.view.base import EventView, RawEventView, View
    from telegrinder.bot.dispatch.view.media_group import MediaGroupView
    from telegrinder.tools.lifespan import Lifespan
    from telegrinder.tools.waiter_machine.actions import WaiterActions
    from telegrinder.tools.waiter_machine.hasher.hasher import Hasher

    class RouterParams(typing.TypedDict):
        name: typing.NotRequired[str]
        injections: typing.NotRequired[Injections]
        filter: typing.NotRequired[ABCRule]

    class DispatchParams[E](typing.TypedDict):
        error_handler: typing.NotRequired[E]
        waiter_machine: typing.NotRequired[WaiterMachine]
        middleware_box: typing.NotRequired[MiddlewareBox]

    class DispatchParamsWithRouter[R, E](DispatchParams[E]):
        router: typing.NotRequired[R]

    class DispatchParamsWithRouterParams[E](RouterParams, DispatchParams[E]): ...


NANOSECONDS_PER_MILLISECOND: typing.Final = 1_000_000


class _ViewGetter:
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
    GuestMessageView: EventView = EventView,
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
    BotSubscriptionUpdatedView: EventView = EventView,
    MessageGenerationStoppedView: EventView = EventView,
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
        GuestMessageView,
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
        BotSubscriptionUpdatedView,
        MessageGenerationStoppedView,
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
        GuestMessageView,
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
        BotSubscriptionUpdatedView,
        MessageGenerationStoppedView,
        MediaGroup,
        EventError,
        RawEvent,
    ]

    main_router: MainRouter
    error_handler: ErrorHandler
    middlewares: T
    waiter_machine: WaiterMachine
    _routers: deque[Router] | None

    @typing.overload
    def __init__(self) -> None: ...

    @typing.overload
    def __init__(self, **params: typing.Unpack[RouterParams]) -> None: ...

    @typing.overload
    def __init__(self, **params: typing.Unpack[DispatchParams[ErrorHandler]]) -> None: ...

    @typing.overload
    def __init__(self, **params: typing.Unpack[DispatchParamsWithRouter[MainRouter, ErrorHandler]]) -> None: ...

    @typing.overload
    def __init__(self, **params: typing.Unpack[DispatchParamsWithRouterParams[ErrorHandler]]) -> None: ...

    def __init__(
        self,
        *,
        name: str | None = None,
        injections: Injections | None = None,
        filter: ABCRule | None = None,
        router: MainRouter | None = None,
        waiter_machine: WaiterMachine | None = None,
        error_handler: ErrorHandler | None = None,
        middleware_box: MiddlewareBox | None = None,
    ) -> None:
        self.global_context = TelegrinderContext()
        self.main_router = typing.cast(
            "typing.Any",
            router
            or Router(
                name=name,
                injections=injections or {},
                filter=filter,
            ),
        )
        self.error_handler = error_handler or ErrorView()  # type: ignore
        self.global_scope = self.global_context.node_global_scope
        self.loop_wrapper = self.global_context.loop_wrapper
        self.waiter_machine = self.global_context.setdefault_value(
            "waiter_machine",
            (WaiterMachine() if "waiter_machine" not in self.global_context else self.global_context.waiter_machine)
            if waiter_machine is None
            else waiter_machine,
        )
        self.middlewares = self.global_context.setdefault_value(
            "middleware_box",
            (
                MiddlewareBox(waiter=WaiterMiddleware(machine=self.waiter_machine))
                if "middleware_box" not in self.global_context
                else self.global_context.middleware_box
            )
            if middleware_box is None
            else middleware_box,
        )
        self._routers = None

    def __setitem__(self, injection_type: typing.Any, injection_value: typing.Any, /) -> None:
        self.global_scope.inject(injection_type, injection_value)

    @property
    def routers(self) -> deque[Router]:
        if self._routers is None:
            self._routers = deque((self.main_router,) if self.main_router else ())  # type: ignore
        return self._routers  # type: ignore

    @property
    def injections(self) -> Injections:
        """Alias `injections` to get an injections container from the main router."""
        return self.main_router.injections

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

    @property
    def choice(self) -> type[Choice[typing.Any]]:
        """Alias `choice` to create a choice scenario."""
        return lambda *args, **kwargs: Choice(  # type: ignore
            *args,
            waiter_machine=self.main_router.callback_query.waiter_machine,
            **kwargs,
        )

    @property
    def checkbox(self) -> type[Checkbox[typing.Any]]:
        """Alias `checkbox` to create a checkbox scenario."""
        return lambda *args, **kwargs: Checkbox(  # type: ignore
            *args,
            waiter_machine=self.main_router.callback_query.waiter_machine,
            **kwargs,
        )

    async def _process_exception(
        self,
        exception: BaseException,
        api: API,
        update: Update,
        context: Context,
    ) -> None:
        if context.exceptions_update:
            try:
                await self._process_exceptions_update(api, update, context)
                return
            except BaseExceptionGroup as group:
                if not self.error_handler:
                    raise

                exceptions = group.exceptions
        else:
            exceptions = (exception,)

        if self.error_handler:
            logger.debug("Caught unhandled exceptions, running the dispatch's error handler...")
            await self._handle_exceptions(api, update, context, exceptions)
            return

        raise exception from None

    async def _handle_exceptions(
        self,
        api: API,
        update: Update,
        context: Context,
        exceptions: typing.Iterable[BaseException | BaseExceptionGroup[BaseException]],
    ) -> None:
        for exception in exceptions:
            if isinstance(exception, KeyboardInterrupt | SystemExit):
                raise exception from None

        unhandled_exceptions: list[BaseException] = []

        try:
            async with self.loop_wrapper.create_task_group() as task_group:
                for exception in exceptions:
                    if isinstance(exception, BaseExceptionGroup):
                        await self._handle_exceptions(api, update, context, exception.exceptions)
                    elif await self.main_router.check_view(
                        self.error_handler,
                        api,
                        update,
                        copy_context := context.copy().add_exception_update(exception),
                    ):
                        task_group.create_task(
                            self.main_router.process_view(
                                self.error_handler,
                                api,
                                update,
                                copy_context,
                            ),
                        )
                    else:
                        unhandled_exceptions.append(exception)
        except KeyboardInterrupt, SystemExit:
            raise
        except BaseException as e:
            raise BaseExceptionGroup("Unhandled exceptions:", (e, *unhandled_exceptions)) from None

    async def _process_exceptions_update(
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

    @staticmethod
    @contextlib.asynccontextmanager
    async def _create_update_context(api: API, update: Update) -> typing.AsyncGenerator[Context]:
        inject_internals(per_event_scope := create_per_event_scope(), {API: api, Update: update})

        async with per_event_scope:
            with log_buffer(f"Update:{update.update_id} > Bot:{api.id}"):
                yield Context().add_roots(api, update, per_event_scope)

    async def feed(self, api: API, update: Update) -> None:
        async with self._create_update_context(api, update) as context:
            start_time = time.perf_counter_ns()
            ok = False

            try:
                for middleware in self.middlewares:
                    if await run_pre_middleware(middleware, context) is not True:
                        logger.info(
                            "Dispatch pre-middleware `{}` raised failure.",
                            fullname(middleware),
                        )
                        ok = True
                        return

                if self.routers:
                    await self._route_update(api, update, context)

                for middleware in self.middlewares:
                    await run_post_middleware(middleware, context)

                ok = True
            except KeyboardInterrupt, SystemExit:
                raise
            except BaseException as exception:
                await self._process_exception(exception, api, update, context)
            finally:
                if ok:
                    elapsed_ns = time.perf_counter_ns() - start_time
                    elapsed_ms = elapsed_ns / NANOSECONDS_PER_MILLISECOND
                    logger.debug(
                        "Processed in {:,} {}.",
                        elapsed_ns
                        if elapsed_ms < 1
                        else int(elapsed_ms)
                        if elapsed_ms < 1000
                        else int(elapsed_ms // 1000),
                        "ns" if elapsed_ms < 1 else "ms" if elapsed_ms < 1000 else "s",
                    )

    async def feed_raw(self, api: API, raw_update: str | bytes) -> None:
        await self.feed(api, UpdateCute.from_raw(raw_update, api))

    async def feed_cute(self, api: API, update_cute: UpdateCute) -> None:
        await self.feed(api, update_cute)

    async def wait[Event: BaseCute[typing.Any], Data](
        self,
        hasher: HasherWithData[Event, Data],
        *,
        filter: ABCRule | None = None,
        release: ABCRule | None = None,
        lifetime: datetime.timedelta | float | None = None,
        lifespan: Lifespan | None = None,
        **actions: typing.Unpack[WaiterActions[Event]],
    ) -> ShortStateContext[Event]:
        _, event, context = await self.wait_many(
            hasher,
            filter=filter,
            release=release,
            lifetime=lifetime,
            lifespan=lifespan,
            **actions,
        )
        return ShortStateContext(event, context)

    async def wait_many[Event: BaseCute[typing.Any], Data, *Ts](
        self,
        *hashers: HasherWithData[Event, Data],
        filter: ABCRule | None = None,
        release: ABCRule | None = None,
        lifetime: datetime.timedelta | float | None = None,
        lifespan: Lifespan | None = None,
        unpack: ContextUnpackProto[*Ts] = unpack_to_context,
        **actions: typing.Unpack[WaiterActions[typing.Any]],
    ) -> tuple[Hasher[Event, Data], Event, *Ts]:
        return await self.waiter_machine.wait_many(
            *hashers,
            waiter_middleware=self.middlewares.waiter,
            filter=filter,
            release=release,
            lifetime=lifetime,
            lifespan=lifespan,
            unpack=unpack,
            **actions,
        )

    def load(self, external: typing.Self) -> None:
        self.routers.extend(filter(None, external.routers))
        self.error_handler.load(external.error_handler)


__all__ = ("Dispatch",)
