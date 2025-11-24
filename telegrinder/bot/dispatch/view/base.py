import typing
from collections import deque

from kungfu import Result

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.handler.abc import ABCHandler
from telegrinder.bot.dispatch.handler.func import FuncHandler, Function
from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware
from telegrinder.bot.dispatch.process import check_rule, process_inner
from telegrinder.bot.dispatch.return_manager.abc import ABCReturnManager
from telegrinder.bot.dispatch.view.abc import ABCView
from telegrinder.bot.rules.abc import ABCRule, Always
from telegrinder.modules import logger
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


class View(ABCView):
    filter: ABCRule
    handlers: deque[ABCHandler]
    middlewares: deque[ABCMiddleware]
    return_manager: ABCReturnManager | None

    def __init__(self, *, return_manager: ABCReturnManager | None = None) -> None:
        self.filter = Always()
        self.handlers = deque()
        self.middlewares = deque()
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

    def __call__[T: Function](self, *rules: ABCRule, final: bool = True) -> typing.Callable[[T], T]:
        def decorator(function: T, /) -> T:
            self.handlers.append(
                FuncHandler(
                    function=function,
                    rules=rules,
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

    async def check(self, api: API, update: Update, context: Context) -> bool:
        await logger.adebug(
            "Checking view `{!r}` for update (id={}, type={!r})", self, update.update_id, update.update_type
        )

        if not self:
            await logger.adebug("View `{!r}` is empty", self)
            return False

        if not await check_rule(api, self.filter, update, context):
            await logger.adebug("Filter for view `{!r}` is failed", self)
            return False

        await logger.adebug(
            "View `{!r}` for update (id={}, type={!r}) is okay",
            self,
            update.update_id,
            update.update_type,
        )
        return True

    async def process(self, api: API, update: Update, context: Context) -> Result[str, str]:
        return await process_inner(
            api,
            update,
            context,
            self,
        )


class EventView(View):
    def __init__(self, update_type: UpdateType, return_manager: ABCReturnManager | None = None) -> None:
        super().__init__(return_manager=return_manager)
        self.update_type = update_type

    def __repr__(self) -> str:
        return "<{}: {!r}>".format(type(self).__name__, self.update_type)

    async def check(self, api: API, update: Update, context: Context) -> bool:
        # If update is not of the expected, instantly skip checking the view
        return update.update_type == self.update_type and await super().check(api, update, context)


class EventModelView[T: (UpdateModel)](View):
    def __init__(self, model: type[T], return_manager: ABCReturnManager | None = None) -> None:
        super().__init__(return_manager=return_manager)
        self.model = model

    def __repr__(self) -> str:
        return "<{}: {}>".format(type(self).__name__, self.model.__name__)

    async def check(self, api: API, update: Update, context: Context) -> bool:
        # If update object is not of the expected type of object, instantly skip checking the view
        return update.incoming_update.__class__ is self.model and await super().check(api, update, context)


class ErrorView(View):
    pass


class RawEventView(View):
    pass


__all__ = (
    "ErrorView",
    "EventView",
    "RawEventView",
    "View",
)
