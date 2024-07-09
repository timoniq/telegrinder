import typing
from abc import ABC, abstractmethod

from fntypes.co import Nothing, Some

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.bot.dispatch.handler.abc import ABCHandler
from telegrinder.bot.dispatch.handler.func import FuncHandler
from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware
from telegrinder.bot.dispatch.process import process_inner
from telegrinder.bot.dispatch.return_manager.abc import ABCReturnManager
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.model import Model
from telegrinder.msgspec_utils import Option
from telegrinder.tools.error_handler.error_handler import ABCErrorHandler, ErrorHandler
from telegrinder.types.objects import Update

EventType = typing.TypeVar("EventType", bound=BaseCute)
ErrorHandlerT = typing.TypeVar("ErrorHandlerT", bound=ABCErrorHandler)
MiddlewareT = typing.TypeVar("MiddlewareT", bound=ABCMiddleware)

FuncType: typing.TypeAlias = typing.Callable[
    typing.Concatenate[EventType, ...],
    typing.Coroutine[typing.Any, typing.Any, typing.Any],
]


class ABCView(ABC):
    def __repr__(self) -> str:
        return "<{!r}: {}>".format(
            self.__class__.__name__,
            ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items()),
        )

    @abstractmethod
    async def check(self, event: Update) -> bool:
        pass

    @abstractmethod
    async def process(self, event: Update, api: ABCAPI) -> None:
        pass

    @abstractmethod
    def load(self, external: typing.Self) -> None:
        pass


class ABCStateView(ABCView, typing.Generic[EventType]):
    @abstractmethod
    def get_state_key(self, event: EventType) -> int | None:
        pass


class BaseView(ABCView, typing.Generic[EventType]):
    auto_rules: list[ABCRule[EventType]]
    handlers: list[ABCHandler[EventType]]
    middlewares: list[ABCMiddleware[EventType]]
    return_manager: ABCReturnManager[EventType] | None

    @classmethod
    def get_event_type(cls) -> Option[type[EventType]]:
        for base in cls.__dict__.get("__orig_bases__", ()):
            if issubclass(typing.get_origin(base) or base, ABCView):
                for generic_type in typing.get_args(base):
                    if issubclass(typing.get_origin(generic_type) or generic_type, BaseCute):
                        return Some(generic_type)
        return Nothing()

    @staticmethod
    def get_raw_event(update: Update) -> Option[Model]:
        return getattr(update, update.update_type.value)

    @typing.overload
    @classmethod
    def to_handler(
        cls,
        *rules: ABCRule[EventType],
    ) -> typing.Callable[
        [FuncType[EventType]],
        FuncHandler[EventType, FuncType[EventType], ErrorHandler[EventType]],
    ]: ...

    @typing.overload
    @classmethod
    def to_handler(
        cls,
        *rules: ABCRule[EventType],
        error_handler: ErrorHandlerT,
        is_blocking: bool = True,
    ) -> typing.Callable[
        [FuncType[EventType]], FuncHandler[EventType, FuncType[EventType], ErrorHandlerT]
    ]: ...

    @typing.overload
    @classmethod
    def to_handler(
        cls,
        *rules: ABCRule[EventType],
        error_handler: typing.Literal[None] = None,
        is_blocking: bool = True,
    ) -> typing.Callable[
        [FuncType[EventType]],
        FuncHandler[EventType, FuncType[EventType], ErrorHandler[EventType]],
    ]: ...

    @classmethod
    def to_handler(  # type: ignore
        cls,
        *rules: ABCRule[EventType],
        error_handler: ABCErrorHandler | None = None,
        is_blocking: bool = True,
    ):
        def wrapper(func: FuncType[EventType]):
            return FuncHandler(
                func,
                list(rules),
                is_blocking=is_blocking,
                dataclass=None,
                error_handler=error_handler or ErrorHandler(),
            )

        return wrapper

    @typing.overload
    def __call__(
        self,
        *rules: ABCRule[EventType],
    ) -> typing.Callable[
        [FuncType[EventType]],
        FuncHandler[EventType, FuncType[EventType], ErrorHandler[EventType]],
    ]: ...

    @typing.overload
    def __call__(
        self,
        *rules: ABCRule[EventType],
        error_handler: ErrorHandlerT,
        is_blocking: bool = True,
    ) -> typing.Callable[
        [FuncType[EventType]], FuncHandler[EventType, FuncType[EventType], ErrorHandlerT]
    ]: ...

    @typing.overload
    def __call__(
        self,
        *rules: ABCRule[EventType],
        error_handler: typing.Literal[None] = None,
        is_blocking: bool = True,
    ) -> typing.Callable[
        [FuncType[EventType]],
        FuncHandler[EventType, FuncType[EventType], ErrorHandler[EventType]],
    ]: ...

    def __call__(  # type: ignore
        self,
        *rules: ABCRule[EventType],
        error_handler: ABCErrorHandler | None = None,
        is_blocking: bool = True,
    ):
        def wrapper(func: FuncType[EventType]):
            func_handler = FuncHandler(
                func,
                [*self.auto_rules, *rules],
                is_blocking=is_blocking,
                dataclass=None,
                error_handler=error_handler or ErrorHandler(),
            )
            self.handlers.append(func_handler)
            return func_handler

        return wrapper

    def register_middleware(self, *args: typing.Any, **kwargs: typing.Any):
        def wrapper(cls: type[MiddlewareT]) -> type[MiddlewareT]:
            self.middlewares.append(cls(*args, **kwargs))
            return cls

        return wrapper

    async def check(self, event: Update) -> bool:
        match self.get_raw_event(event):
            case Some(e) if issubclass(
                self.get_event_type().expect(
                    "{!r} has no event type in generic.".format(self.__class__.__name__),
                ),
                e.__class__,
            ):
                return True
            case _:
                return False

    async def process(self, event: Update, api: ABCAPI) -> None:
        await process_inner(
            self.get_event_type()
            .unwrap()
            .from_update(
                update=self.get_raw_event(event).unwrap(),
                bound_api=api,
            ),
            event,
            self.middlewares,
            self.handlers,
            self.return_manager,
        )

    def load(self, external: typing.Self) -> None:
        self.auto_rules.extend(external.auto_rules)
        self.handlers.extend(external.handlers)
        self.middlewares.extend(external.middlewares)


class BaseStateView(ABCStateView[EventType], BaseView[EventType], ABC, typing.Generic[EventType]):
    @abstractmethod
    def get_state_key(self, event: EventType) -> int | None:
        pass


__all__ = (
    "ABCStateView",
    "ABCView",
    "BaseStateView",
    "BaseView",
)
