import typing
from abc import ABC, abstractmethod
from functools import cached_property

from fntypes.option import Nothing, Some

from telegrinder.api.api import API
from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.bot.dispatch.handler.abc import ABCHandler
from telegrinder.bot.dispatch.handler.func import FuncHandler
from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware
from telegrinder.bot.dispatch.process import process_inner
from telegrinder.bot.dispatch.return_manager.abc import ABCReturnManager
from telegrinder.bot.dispatch.view.abc import ABCStateView, ABCView
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.model import Model
from telegrinder.msgspec_utils import Option
from telegrinder.tools.error_handler.error_handler import ABCErrorHandler, ErrorHandler
from telegrinder.types.objects import Update

Event = typing.TypeVar("Event", bound=BaseCute)
ErrorHandlerT = typing.TypeVar("ErrorHandlerT", bound=ABCErrorHandler)
MiddlewareT = typing.TypeVar("MiddlewareT", bound=ABCMiddleware)

FuncType: typing.TypeAlias = typing.Callable[
    typing.Concatenate[Event, ...],
    typing.Coroutine[typing.Any, typing.Any, typing.Any],
]


def get_event_model_class(view: "BaseView[Event]") -> Option[type[Event]]:
    for base in view.__class__.__bases__ + (view.__class__,):
        if "__orig_bases__" not in base.__dict__:
            continue

        for orig_base in base.__dict__["__orig_bases__"]:
            origin_base = typing.get_origin(orig_base) or orig_base
            if not isinstance(origin_base, type) and not issubclass(origin_base, object):
                continue

            for generic_type in typing.get_args(orig_base):
                orig_generic_type = typing.get_origin(generic_type) or generic_type
                if isinstance(orig_generic_type, type) and issubclass(orig_generic_type, BaseCute):
                    return Some(generic_type)

    return Nothing()


class BaseView(ABCView, typing.Generic[Event]):
    auto_rules: list[ABCRule]
    handlers: list[ABCHandler[Event]]
    middlewares: list[ABCMiddleware[Event]]
    return_manager: ABCReturnManager[Event] | None = None

    @staticmethod
    def get_raw_event(update: Update) -> Option[Model]:
        return getattr(update, update.update_type.value)

    @cached_property
    def event_model_class(self) -> Option[type[Event]]:
        return get_event_model_class(self)

    @typing.overload
    @classmethod
    def to_handler(
        cls,
        *rules: ABCRule,
    ) -> typing.Callable[
        [FuncType[Event]],
        FuncHandler[Event, FuncType[Event], ErrorHandler[Event]],
    ]: ...

    @typing.overload
    @classmethod
    def to_handler(
        cls,
        *rules: ABCRule,
        error_handler: ErrorHandlerT,
        is_blocking: bool = True,
    ) -> typing.Callable[[FuncType[Event]], FuncHandler[Event, FuncType[Event], ErrorHandlerT]]: ...

    @typing.overload
    @classmethod
    def to_handler(
        cls,
        *rules: ABCRule,
        error_handler: typing.Literal[None] = None,
        is_blocking: bool = True,
    ) -> typing.Callable[
        [FuncType[Event]],
        FuncHandler[Event, FuncType[Event], ErrorHandler[Event]],
    ]: ...

    @classmethod
    def to_handler(  # type: ignore
        cls,
        *rules: ABCRule,
        error_handler: ABCErrorHandler | None = None,
        is_blocking: bool = True,
    ):
        def wrapper(func: FuncType[Event]):
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
        *rules: ABCRule,
    ) -> typing.Callable[
        [FuncType[Event]],
        FuncHandler[Event, FuncType[Event], ErrorHandler[Event]],
    ]: ...

    @typing.overload
    def __call__(  # type: ignore
        self,
        *rules: ABCRule,
        error_handler: ErrorHandlerT,
        is_blocking: bool = True,
    ) -> typing.Callable[[FuncType[Event]], FuncHandler[Event, FuncType[Event], ErrorHandlerT]]: ...

    @typing.overload
    def __call__(
        self,
        *rules: ABCRule,
        error_handler: typing.Literal[None] = None,
        is_blocking: bool = True,
    ) -> typing.Callable[
        [FuncType[Event]],
        FuncHandler[Event, FuncType[Event], ErrorHandler[Event]],
    ]: ...

    def __call__(  # type: ignore
        self,
        *rules: ABCRule,
        error_handler: ABCErrorHandler | None = None,
        is_blocking: bool = True,
    ):
        def wrapper(func: FuncType[Event]):
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
                self.event_model_class.expect(
                    "{!r} has no event model class in generic.".format(self.__class__.__qualname__),
                ),
                e.__class__,
            ) and (self.handlers or self.middlewares):
                return True
            case _:
                return False

    async def process(self, event: Update, api: API) -> bool:
        return await process_inner(
            api,
            self.event_model_class.unwrap().from_update(
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


class BaseStateView(ABCStateView[Event], BaseView[Event], ABC, typing.Generic[Event]):
    @abstractmethod
    def get_state_key(self, event: Event) -> int | None:
        pass