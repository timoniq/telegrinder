import typing

from telegrinder.api import API
from telegrinder.bot.cute_types import UpdateCute
from telegrinder.bot.dispatch.handler.func import FuncHandler
from telegrinder.bot.dispatch.process import process_inner
from telegrinder.bot.dispatch.view.abc import ABCEventRawView, BaseView, ErrorHandlerT
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.tools.error_handler.error_handler import ABCErrorHandler, ErrorHandler
from telegrinder.types.enums import UpdateType
from telegrinder.types.objects import Update

T = typing.TypeVar("T")

FuncType: typing.TypeAlias = typing.Callable[
    typing.Concatenate[T, ...],
    typing.Coroutine[typing.Any, typing.Any, typing.Any],
]


class RawEventView(ABCEventRawView[UpdateCute], BaseView[UpdateCute]):
    def __init__(self) -> None:
        self.auto_rules = []
        self.handlers = []
        self.middlewares = []
        self.return_manager = None

    @typing.overload
    def __call__(
        self,
        update_type: UpdateType,
        *rules: ABCRule,
    ) -> typing.Callable[
        [FuncType[UpdateCute]],
        FuncHandler[UpdateCute, FuncType[UpdateCute], ErrorHandler[UpdateCute]],
    ]: ...

    @typing.overload
    def __call__(
        self,
        update_type: UpdateType,
        *rules: ABCRule,
        dataclass: type[T],
    ) -> typing.Callable[[FuncType[T]], FuncHandler[UpdateCute, FuncType[T], ErrorHandler[T]]]: ...

    @typing.overload
    def __call__(
        self,
        update_type: UpdateType,
        *rules: ABCRule,
        error_handler: ErrorHandlerT,
    ) -> typing.Callable[
        [FuncType[UpdateCute]],
        FuncHandler[UpdateCute, FuncType[UpdateCute], ErrorHandlerT],
    ]: ...

    @typing.overload
    def __call__(
        self,
        update_type: UpdateType,
        *rules: ABCRule,
        dataclass: type[T],
        error_handler: ErrorHandlerT,
        is_blocking: bool = True,
    ) -> typing.Callable[[FuncType[T]], FuncHandler[UpdateCute, FuncType[T], ErrorHandlerT]]: ...

    @typing.overload
    def __call__(
        self,
        update_type: UpdateType,
        *rules: ABCRule,
        dataclass: typing.Literal[None] = None,
        error_handler: typing.Literal[None] = None,
        is_blocking: bool = True,
    ) -> typing.Callable[
        [FuncType[UpdateCute]],
        FuncHandler[UpdateCute, FuncType[UpdateCute], ErrorHandler[UpdateCute]],
    ]: ...

    def __call__(  # type: ignore
        self,
        update_type: UpdateType,
        *rules: ABCRule,
        dataclass: type[typing.Any] | None = None,
        error_handler: ABCErrorHandler | None = None,
        is_blocking: bool = True,
    ):
        def wrapper(func: FuncType[typing.Any]):
            func_handler = FuncHandler(
                func,
                rules=[*self.auto_rules, *rules],
                is_blocking=is_blocking,
                dataclass=dataclass,
                error_handler=error_handler or ErrorHandler(),
                update_type=update_type,
            )
            self.handlers.append(func_handler)
            return func_handler

        return wrapper

    async def check(self, event: Update) -> bool:
        return bool(self.handlers) or bool(self.middlewares)

    async def process(self, event: Update, api: API) -> bool:
        return await process_inner(
            api,
            UpdateCute.from_update(event, bound_api=api),
            event,
            self.middlewares,
            self.handlers,
            self.return_manager,
        )
