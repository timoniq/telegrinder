from __future__ import annotations

import dataclasses

import typing_extensions as typing
from fntypes import Nothing, Option, Some
from vbml.patcher import Patcher

from telegrinder.api.api import API
from telegrinder.bot.dispatch.abc import ABCDispatch
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.handler.func import ErrorHandlerT, Func, FuncHandler
from telegrinder.bot.dispatch.middleware.abc import run_middleware
from telegrinder.bot.dispatch.middleware.global_middleware import GlobalMiddleware
from telegrinder.bot.dispatch.view.box import (
    CallbackQueryView,
    ChatJoinRequestView,
    ChatMemberView,
    InlineQueryView,
    MessageView,
    PreCheckoutQueryView,
    RawEventView,
    ViewBox,
)
from telegrinder.modules import logger
from telegrinder.tools.error_handler.error_handler import ErrorHandler
from telegrinder.tools.global_context import TelegrinderContext
from telegrinder.types.enums import UpdateType
from telegrinder.types.objects import Update

if typing.TYPE_CHECKING:
    from telegrinder.bot.cute_types.base import BaseCute
    from telegrinder.bot.cute_types.update import UpdateCute
    from telegrinder.bot.rules.abc import ABCRule

T = typing.TypeVar("T", default=typing.Any)
R = typing.TypeVar("R", covariant=True, default=typing.Any)
Event = typing.TypeVar("Event", bound="BaseCute")
P = typing.ParamSpec("P", default=...)

DEFAULT_DATACLASS: typing.Final[type[Update]] = Update


@dataclasses.dataclass(repr=False, kw_only=True)
class Dispatch(
    ViewBox[
        CallbackQueryView,
        ChatJoinRequestView,
        ChatMemberView,
        InlineQueryView,
        MessageView,
        PreCheckoutQueryView,
        RawEventView,
    ],
    ABCDispatch,
):
    _global_context: TelegrinderContext = dataclasses.field(
        init=False,
        default_factory=TelegrinderContext,
    )
    global_middleware: "GlobalMiddleware" = dataclasses.field(
        default_factory=lambda: GlobalMiddleware(),
    )

    def __repr__(self) -> str:
        return "Dispatch(%s)" % ", ".join(f"{k}={v!r}" for k, v in self.get_views().items())

    @property
    def global_context(self) -> TelegrinderContext:
        return self._global_context

    @property
    def patcher(self) -> Patcher:
        """Alias `patcher` to get `vbml.Patcher` from the global context."""

        return self.global_context.vbml_patcher

    @typing.overload
    def handle(
        self,
        *rules: "ABCRule",
        is_blocking: bool = True,
    ) -> typing.Callable[[Func[P, R]], FuncHandler["UpdateCute", Func[P, R], ErrorHandler[UpdateCute]]]: ...

    @typing.overload
    def handle(
        self,
        *rules: "ABCRule",
        dataclass: type[T],
        is_blocking: bool = True,
    ) -> typing.Callable[[Func[P, R]], FuncHandler["UpdateCute", Func[P, R], ErrorHandler[T]]]: ...

    @typing.overload
    def handle(
        self,
        *rules: "ABCRule",
        update_type: UpdateType,
        is_blocking: bool = True,
    ) -> typing.Callable[[Func[P, R]], FuncHandler["UpdateCute", Func[P, R], ErrorHandler[UpdateCute]]]: ...

    @typing.overload
    def handle(
        self,
        *rules: "ABCRule",
        dataclass: type[T],
        update_type: UpdateType,
        is_blocking: bool = True,
    ) -> typing.Callable[[Func[P, R]], FuncHandler["UpdateCute", Func[P, R], ErrorHandler[T]]]: ...

    @typing.overload
    def handle(
        self,
        *rules: "ABCRule",
        error_handler: ErrorHandlerT,
        is_blocking: bool = True,
    ) -> typing.Callable[[Func[P, R]], FuncHandler["UpdateCute", Func[P, R], ErrorHandlerT]]: ...

    @typing.overload
    def handle(
        self,
        *rules: "ABCRule",
        update_type: UpdateType,
        error_handler: ErrorHandlerT,
        is_blocking: bool = True,
    ) -> typing.Callable[[Func[P, R]], FuncHandler["UpdateCute", Func[P, R], ErrorHandlerT]]: ...

    @typing.overload
    def handle(
        self,
        *rules: "ABCRule",
        dataclass: type[T],
        error_handler: ErrorHandlerT,
        is_blocking: bool = True,
    ) -> typing.Callable[[Func[P, R]], FuncHandler[T, Func[P, R], ErrorHandlerT]]: ...

    @typing.overload
    def handle(
        self,
        *rules: "ABCRule",
        dataclass: type[T],
        update_type: UpdateType,
        error_handler: ErrorHandlerT,
        is_blocking: bool = True,
    ) -> typing.Callable[[Func[P, R]], FuncHandler[T, Func[P, R], ErrorHandlerT]]: ...

    @typing.overload
    def handle(
        self,
        *rules: "ABCRule",
        update_type: UpdateType | None = None,
        dataclass: type[T] = DEFAULT_DATACLASS,
        error_handler: typing.Literal[None] = None,
        is_blocking: bool = True,
    ) -> typing.Callable[[Func[P, R]], FuncHandler[T, Func[P, R], ErrorHandler[T]]]: ...

    def handle(
        self,
        *rules: "ABCRule",
        update_type: UpdateType | None = None,
        dataclass: type[typing.Any] = DEFAULT_DATACLASS,
        error_handler: ErrorHandlerT | None = None,
        is_blocking: bool = True,
    ) -> typing.Callable[..., typing.Any]:
        def wrapper(func):
            handler = FuncHandler(
                func,
                list(rules),
                is_blocking=is_blocking,
                dataclass=dataclass,
                error_handler=error_handler or ErrorHandler(),
                update_type=update_type,
            )
            self.raw_event.handlers.append(handler)
            return handler

        return wrapper

    async def feed(self, event: Update, api: API) -> bool:
        logger.debug(
            "Processing update (update_id={}, update_type={!r})",
            event.update_id,
            event.update_type.name,
        )
        context = Context(raw_update=event)

        if (
            await run_middleware(
                self.global_middleware.pre,
                api,
                event,  # type: ignore
                raw_event=event,
                ctx=context,
                adapter=self.global_middleware.adapter,
            )
            is False
        ):
            return False

        for view in self.get_views().values():
            if await view.check(event):
                logger.debug(
                    "Update (update_id={}, update_type={!r}) matched view {!r}.",
                    event.update_id,
                    event.update_type.name,
                    view,
                )
                if await view.process(event, api, context):
                    return True

        await run_middleware(
            self.global_middleware.post,
            api,
            event,
            raw_event=event,
            ctx=context,
            adapter=self.global_middleware.adapter,
            responses=[],
        )

        return False

    def load(self, external: typing.Self) -> None:
        view_external = external.get_views()
        for name, view in self.get_views().items():
            assert name in view_external, f"View {name!r} is undefined in external dispatch."
            view.load(view_external[name])
            setattr(external, name, view)

    def get_view(self, of_type: type[T]) -> Option[T]:
        for view in self.get_views().values():
            if isinstance(view, of_type):
                return Some(view)
        return Nothing()

    __call__ = handle


__all__ = ("Dispatch",)
