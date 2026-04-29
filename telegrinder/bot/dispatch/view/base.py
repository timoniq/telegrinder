import typing
from collections import deque

from kungfu import Error, Ok, Pulse, Result

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.handler.abc import ABCHandler
from telegrinder.bot.dispatch.handler.func import FuncHandler, Function
from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware
from telegrinder.bot.dispatch.middleware.box import ViewMiddlewareBox
from telegrinder.bot.dispatch.middleware.waiter import WaiterMiddleware
from telegrinder.bot.dispatch.process import check_rule, process_inner
from telegrinder.bot.dispatch.return_manager.abc import ABCReturnManager
from telegrinder.bot.dispatch.view.abc import ABCView
from telegrinder.bot.rules.abc import ABCRule, Always
from telegrinder.bot.rules.update import IsUpdateModelType, IsUpdateType
from telegrinder.tools.global_context.builtin_context import TelegrinderContext
from telegrinder.tools.waiter_machine.machine import WaiterMachine
from telegrinder.types.enums import UpdateType
from telegrinder.types.objects import (
    BusinessConnection,
    BusinessMessagesDeleted,
    CallbackQuery,
    ChatBoostRemoved,
    ChatBoostUpdated,
    ChatJoinRequest,
    ChatMemberUpdated,
    ChosenInlineResult,
    InlineQuery,
    ManagedBotCreated,
    Message,
    MessageReactionCountUpdated,
    MessageReactionUpdated,
    PaidMediaPurchased,
    Poll,
    PollAnswer,
    PreCheckoutQuery,
    ShippingQuery,
    Update,
)

if typing.TYPE_CHECKING:
    import datetime

    from nodnod.agent.base import Agent

    from telegrinder.bot.cute_types.base import BaseCute
    from telegrinder.tools.lifespan import Lifespan
    from telegrinder.tools.waiter_machine.machine import HasherWithData, ShortStateContext, WaiterActions

type AnyNode = typing.Any
type UpdateModel = typing.Union[
    BusinessConnection,
    BusinessMessagesDeleted,
    CallbackQuery,
    ChatBoostRemoved,
    ChatBoostUpdated,
    ChatJoinRequest,
    ChatMemberUpdated,
    ChosenInlineResult,
    InlineQuery,
    Message,
    MessageReactionCountUpdated,
    MessageReactionUpdated,
    PaidMediaPurchased,
    Poll,
    PollAnswer,
    PreCheckoutQuery,
    ShippingQuery,
    ManagedBotCreated,
]
type ViewResult = Result[str, str] | Result[str, BaseException]

VIEW_IS_OK: typing.Final = Ok()
VIEW_IS_EMPTY_ERROR: typing.Final = Error("View is empty.")
VIEW_FILTER_IS_FAILED_ERROR: typing.Final = Error("Filter is failed.")
TELEGRINDER_CONTEXT: typing.Final = TelegrinderContext()


class View(ABCView):
    _filter: ABCRule
    handlers: deque[ABCHandler]
    waiter_machine: WaiterMachine
    middlewares: ViewMiddlewareBox
    agent_cls: type[Agent] | None
    return_manager: ABCReturnManager | None

    def __init__(
        self,
        *,
        middlewares: ViewMiddlewareBox | None = None,
        waiter_machine: WaiterMachine | None = None,
        return_manager: ABCReturnManager | None = None,
        agent_cls: type[Agent] | None = None,
    ) -> None:
        self._filter = Always()
        self.handlers = deque()
        self.agent_cls = agent_cls
        self.return_manager = return_manager
        self.waiter_machine = (waiter_machine or WaiterMachine()).bind_view(self)
        self.middlewares = (
            ViewMiddlewareBox(waiter=WaiterMiddleware(machine=self.waiter_machine))
            if middlewares is None
            else middlewares
        )

    def __bool__(self) -> bool:
        return bool(self.handlers) or bool(self.middlewares)

    def __repr__(self) -> str:
        return "<{}>".format(type(self).__name__)

    @property
    def filter(self) -> ABCRule:
        return self._filter

    @filter.setter
    def filter(self, value: ABCRule, /) -> None:
        self._filter &= value

    @property
    def auto_rules(self) -> ABCRule:
        return self._filter

    @auto_rules.setter
    def auto_rules(self, value: ABCRule | typing.Iterable[ABCRule], /) -> None:
        for rule in (value,) if isinstance(value, ABCRule) else value:
            self.filter = rule

    def __call__[T: Function](
        self,
        *rules: ABCRule,
        final: bool = True,
        agent: type[Agent] | None = None,
    ) -> typing.Callable[[T], T]:
        def decorator(function: T, /) -> T:
            self.handlers.append(
                FuncHandler(
                    function=function,
                    rules=rules,
                    agent=agent or self.agent_cls,
                    final=final,
                ),
            )
            return function

        return decorator

    @typing.overload
    def register_middleware[T: ABCMiddleware](self, middleware_cls: type[T], /) -> type[T]: ...

    @typing.overload
    def register_middleware(self, middleware: ABCMiddleware, /) -> None: ...

    def register_middleware(
        self,
        middleware: type[ABCMiddleware] | ABCMiddleware,
    ) -> typing.Callable[..., typing.Any] | None:
        self.middlewares.put(middleware() if isinstance(middleware, type) else middleware)
        return middleware if isinstance(middleware, type) else None

    def load(self, external: typing.Self, /) -> None:
        if not external:
            return

        self.handlers.extend(external.handlers)
        self.middlewares.extend(external.middlewares)

        if not isinstance(external.filter, Always):
            self.filter &= external.filter

        if external.waiter_machine.storage:
            self.waiter_machine.storage.update(external.waiter_machine.storage)

        if external.return_manager is not None and self.return_manager is None:
            self.return_manager = external.return_manager

        elif self.return_manager is not None and external.return_manager is not None:
            self.return_manager.managers.extend(external.return_manager.managers)

    async def wait[Event: BaseCute, Data](
        self,
        hasher: HasherWithData[Event, Data],
        *,
        filter: ABCRule | None = None,
        release: ABCRule | None = None,
        lifetime: datetime.timedelta | float | None = None,
        lifespan: Lifespan | None = None,
        **actions: typing.Unpack[WaiterActions[Event]],
    ) -> ShortStateContext[Event]:
        return await self.waiter_machine.wait(
            hasher=hasher,
            view=self,
            filter=filter,
            release=release,
            lifetime=lifetime,
            lifespan=lifespan,
            **actions,
        )

    async def check(self, api: API, update: Update, context: Context) -> Pulse[str]:
        if not self:
            return VIEW_IS_EMPTY_ERROR

        if not await check_rule(self.filter, context):
            return VIEW_FILTER_IS_FAILED_ERROR

        return VIEW_IS_OK

    async def process(self, api: API, update: Update, context: Context) -> ViewResult:
        return await process_inner(api, update, context, self)


class EventView(View):
    def __init__(
        self,
        update_type: UpdateType,
        *,
        middlewares: ViewMiddlewareBox | None = None,
        waiter_machine: WaiterMachine | None = None,
        return_manager: ABCReturnManager | None = None,
        agent_cls: type[Agent] | None = None,
    ) -> None:
        super().__init__(
            agent_cls=agent_cls,
            middlewares=middlewares,
            waiter_machine=waiter_machine,
            return_manager=return_manager,
        )
        self.update_type = update_type
        self._filter = self._update_filter = IsUpdateType(update_type)

    def __str__(self) -> str:
        return f"@{self.update_type.value}"

    def __repr__(self) -> str:
        return "<{}: {!r}>".format(type(self).__name__, self.update_type)

    def hold(
        self,
        source_node: AnyNode,
        source_value: typing.Any,
        /,
        *filters: ABCRule,
        agent: type[Agent] | None = None,
    ) -> typing.ContextManager[None]:
        return TELEGRINDER_CONTEXT.middleware_box.filter.hold(
            source_node,
            source_value,
            self._update_filter,
            *filters,
            agent_cls=agent,
        )


class EventModelView[T: (UpdateModel)](View):
    def __init__(
        self,
        model: type[T],
        *,
        middlewares: ViewMiddlewareBox | None = None,
        waiter_machine: WaiterMachine | None = None,
        return_manager: ABCReturnManager | None = None,
        agent_cls: type[Agent] | None = None,
    ) -> None:
        super().__init__(
            agent_cls=agent_cls,
            middlewares=middlewares,
            waiter_machine=waiter_machine,
            return_manager=return_manager,
        )
        self.model = model
        self._filter = self._update_filter = IsUpdateModelType(model)

    def __repr__(self) -> str:
        return "<{}: {}>".format(type(self).__name__, self.model.__name__)

    def hold(
        self,
        source_node: AnyNode,
        source_value: typing.Any,
        /,
        *filters: ABCRule,
        agent: type[Agent] | None = None,
    ) -> typing.ContextManager[None]:
        return TELEGRINDER_CONTEXT.middleware_box.filter.hold(
            source_node,
            source_value,
            self._update_filter,
            *filters,
            agent_cls=agent,
        )


class ErrorView(View):
    async def process(self, api: API, update: Update, context: Context) -> ViewResult:
        result = await super().process(api, update, context)

        if not result and context.exception_update:
            return Error(context.exception_update.unwrap())

        return result


class RawEventView(View):
    pass


__all__ = ("ErrorView", "EventView", "RawEventView", "View")
