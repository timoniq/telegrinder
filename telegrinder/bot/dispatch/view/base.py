import typing
from abc import ABC, abstractmethod
from functools import cached_property

from fntypes.option import Nothing, Some

from telegrinder.api.api import API
from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.handler.abc import ABCHandler
from telegrinder.bot.dispatch.handler.func import Func, FuncHandler
from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware
from telegrinder.bot.dispatch.process import process_inner
from telegrinder.bot.dispatch.return_manager.abc import ABCReturnManager
from telegrinder.bot.dispatch.view.abc import ABCStateView, ABCView
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.model import Model
from telegrinder.msgspec_utils import Option
from telegrinder.tools.error_handler.error_handler import ABCErrorHandler, ErrorHandler
from telegrinder.types.objects import Update


def get_event_model_class[Event: BaseCute](
    view: "BaseView[Event] | type[BaseView[Event]]",
) -> Option[type[Event]]:
    view_class = view if isinstance(view, typing.Type) else view.__class__
    for base in view.__class__.__bases__ + (view_class,):
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


class BaseView[Event: BaseCute](ABCView):
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
    def to_handler[**P, R](
        cls,
        *rules: ABCRule,
    ) -> typing.Callable[
        [Func[P, R]],
        FuncHandler[Event, Func[P, R], ErrorHandler[Event]],
    ]: ...

    @typing.overload
    @classmethod
    def to_handler[**P, Dataclass, R](
        cls,
        *rules: ABCRule,
        dataclass: type[Dataclass],
        is_blocking: bool = True,
    ) -> typing.Callable[
        [Func[P, R]],
        FuncHandler[Dataclass, Func[P, R], ErrorHandler[Dataclass]],
    ]: ...

    @typing.overload
    @classmethod
    def to_handler[**P, ErrorHandlerT: ABCErrorHandler, R](
        cls,
        *rules: ABCRule,
        error_handler: ErrorHandlerT,
        is_blocking: bool = True,
    ) -> typing.Callable[[Func[P, R]], FuncHandler[Event, Func[P, R], ErrorHandlerT]]: ...

    @typing.overload
    @classmethod
    def to_handler[**P, Dataclass, ErrorHandlerT: ABCErrorHandler, R](
        cls,
        *rules: ABCRule,
        dataclass: type[Dataclass],
        error_handler: ErrorHandlerT,
        is_blocking: bool = True,
    ) -> typing.Callable[[Func[P, R]], FuncHandler[Dataclass, Func[P, R], ErrorHandlerT]]: ...

    @classmethod
    def to_handler(
        cls,
        *rules: ABCRule,
        dataclass: type[typing.Any] | None = None,
        error_handler: ABCErrorHandler | None = None,
        is_blocking: bool = True,
    ) -> typing.Callable[..., typing.Any]:
        def wrapper(func):
            return FuncHandler(
                func,
                list(rules),
                is_blocking=is_blocking,
                dataclass=dataclass,
                error_handler=error_handler or ErrorHandler(),
            )

        return wrapper

    @typing.overload
    def __call__[**P, R](
        self,
        *rules: ABCRule,
        is_blocking: bool = True,
    ) -> typing.Callable[
        [Func[P, R]],
        FuncHandler[Event, Func[P, R], ErrorHandler[Event]],
    ]: ...

    @typing.overload
    def __call__[**P, Dataclass, R](
        self,
        *rules: ABCRule,
        dataclass: type[Dataclass],
        is_blocking: bool = True,
    ) -> typing.Callable[
        [Func[P, R]],
        FuncHandler[Dataclass, Func[P, R], ErrorHandler[Dataclass]],
    ]: ...

    @typing.overload
    def __call__[**P, ErrorHandlerT: ABCErrorHandler, R](
        self,
        *rules: ABCRule,
        error_handler: ErrorHandlerT,
        is_blocking: bool = True,
    ) -> typing.Callable[[Func[P, R]], FuncHandler[Event, Func[P, R], ErrorHandlerT]]: ...

    def __call__[**P, R](
        self,
        *rules: ABCRule,
        dataclass: type[typing.Any] | None = None,
        error_handler: ABCErrorHandler | None = None,
        is_blocking: bool = True,
    ) -> typing.Callable[..., typing.Any]:
        def wrapper(func):
            func_handler = FuncHandler(
                func,
                [*self.auto_rules, *rules],
                is_blocking=is_blocking,
                dataclass=dataclass,
                error_handler=error_handler or ErrorHandler(),
            )
            self.handlers.append(func_handler)
            return func_handler

        return wrapper

    def register_middleware[Middleware: ABCMiddleware](self, *args: typing.Any, **kwargs: typing.Any):
        def wrapper(cls: type[Middleware]) -> type[Middleware]:
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

    async def process(self, event: Update, api: API, context: Context) -> bool:
        return await process_inner(
            api,
            self.event_model_class.unwrap().from_update(
                update=self.get_raw_event(event).unwrap(),
                bound_api=api,
            ),
            event,
            context,
            self.middlewares,
            self.handlers,
            self.return_manager,
        )

    def load(self, external: typing.Self) -> None:
        self.auto_rules.extend(external.auto_rules)
        self.handlers.extend(external.handlers)
        self.middlewares.extend(external.middlewares)


class BaseStateView[Event: BaseCute](ABCStateView[Event], BaseView[Event], ABC):
    @classmethod
    @abstractmethod
    def get_state_key(cls, event: Event) -> int | None:
        pass


__all__ = ("ABCStateView", "ABCView", "BaseStateView", "BaseView")
