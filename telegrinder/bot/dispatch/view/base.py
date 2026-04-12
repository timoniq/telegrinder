import typing
from collections import deque

from kungfu import Error, Ok, Pulse, Result

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.handler.abc import ABCHandler
from telegrinder.bot.dispatch.handler.func import FuncHandler, Function
from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware
from telegrinder.bot.dispatch.process import check_rule, process_inner
from telegrinder.bot.dispatch.return_manager.abc import ABCReturnManager
from telegrinder.bot.dispatch.view.abc import ABCView
from telegrinder.bot.rules.abc import ABCRule, Always
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
    from nodnod.agent.base import Agent

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
]
type ViewResult = Result[str, str] | Result[str, Exception]

OK_CHECK: typing.Final = Ok()


class View(ABCView):
    filter: ABCRule
    handlers: deque[ABCHandler]
    middlewares: deque[ABCMiddleware]
    return_manager: ABCReturnManager | None

    def __init__(
        self,
        *,
        agent_cls: type[Agent] | None = None,
        return_manager: ABCReturnManager | None = None,
    ) -> None:
        self.filter = Always()
        self.handlers = deque()
        self.middlewares = deque()
        self.agent_cls = agent_cls
        self.return_manager = return_manager

    def __bool__(self) -> bool:
        return bool(self.handlers) or bool(self.middlewares)

    def __repr__(self) -> str:
        return "<{}>".format(type(self).__name__)

    @property
    def auto_rules(self) -> ABCRule:
        return self.filter

    @auto_rules.setter
    def auto_rules(self, value: ABCRule | typing.Iterable[ABCRule], /) -> None:
        for rule in (value,) if isinstance(value, ABCRule) else value:
            self.filter &= rule

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
        self.middlewares.append(middleware() if isinstance(middleware, type) else middleware)
        return middleware if isinstance(middleware, type) else None

    def load(self, external: typing.Self, /) -> None:
        if not external:
            return

        self.handlers.extend(external.handlers)
        self.middlewares.extend(external.middlewares)

        if not isinstance(external.filter, Always):
            self.filter &= external.filter

        if external.return_manager is not None and self.return_manager is None:
            self.return_manager = external.return_manager

        elif self.return_manager is not None and external.return_manager is not None:
            self.return_manager.managers.extend(external.return_manager.managers)

    async def check(self, api: API, update: Update, context: Context) -> Pulse[str]:
        if not bool(self):
            return Error("View is empty.")

        if not await check_rule(self.filter, context):
            return Error("Filter is failed.")

        return OK_CHECK

    async def process(self, api: API, update: Update, context: Context) -> ViewResult:
        return await process_inner(
            api,
            update,
            context,
            self,
        )


class EventView(View):
    def __init__(
        self,
        update_type: UpdateType,
        return_manager: ABCReturnManager | None = None,
        agent_cls: type[Agent] | None = None,
    ) -> None:
        super().__init__(
            agent_cls=agent_cls,
            return_manager=return_manager,
        )
        self.update_type = update_type

    def __str__(self) -> str:
        return f"@{self.update_type.value}"

    def __repr__(self) -> str:
        return "<{}: {!r}>".format(type(self).__name__, self.update_type)

    async def check(self, api: API, update: Update, context: Context) -> Pulse[str]:
        # If update is not of the expected, instantly skip checking the view
        if update.update_type != self.update_type:
            return Error(f"Incoming event `{update.update_type!r}` is not `{self.update_type!r}`.")
        return await super().check(api, update, context)


class EventModelView[T: (UpdateModel)](View):
    def __init__(
        self,
        model: type[T],
        return_manager: ABCReturnManager | None = None,
        agent_cls: type[Agent] | None = None,
    ) -> None:
        super().__init__(
            agent_cls=agent_cls,
            return_manager=return_manager,
        )
        self.model = model

    def __repr__(self) -> str:
        return "<{}: {}>".format(type(self).__name__, self.model.__name__)

    async def check(self, api: API, update: Update, context: Context) -> Pulse[str]:
        # If update object is not of the expected type of object, instantly skip checking the view
        if not issubclass(update.incoming_update.__class__, self.model):
            return Error(
                f"Incoming event model `{update.incoming_update.__class__.__name__!r}`"
                f" is not `{self.model.__name__!r}`.",
            )
        return await super().check(api, update, context)


class ErrorView(View):
    async def process(self, api: API, update: Update, context: Context) -> ViewResult:
        result = await super().process(api, update, context)

        if not result and context.exception_update:
            return Error(context.exception_update.unwrap())

        return result


class RawEventView(View):
    pass


__all__ = ("ErrorView", "EventView", "RawEventView", "View")
