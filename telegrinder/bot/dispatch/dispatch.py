import asyncio
import dataclasses
import typing

from vbml.patcher import Patcher

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.rules import ABCRule
from telegrinder.modules import logger
from telegrinder.tools.error_handler.error_handler import ErrorHandler
from telegrinder.tools.global_context import TelegrinderCtx
from telegrinder.types import Update

from .abc import ABCDispatch
from .handler import ABCHandler, FuncHandler
from .handler.func import ErrorHandlerT
from .view.box import (
    CallbackQueryViewT,
    ChatJoinRequestViewT,
    ChatMemberViewT,
    InlineQueryViewT,
    MessageViewT,
    RawEventViewT,
    ViewBox,
)

T = typing.TypeVar("T")
R = typing.TypeVar("R")
P = typing.ParamSpec("P")
Handler = typing.Callable[
    typing.Concatenate[T, ...], typing.Coroutine[typing.Any, typing.Any, typing.Any]
]
Event = typing.TypeVar("Event", bound=BaseCute)

DEFAULT_DATACLASS: typing.Final[type[Update]] = Update


@dataclasses.dataclass(repr=False, kw_only=True)
class Dispatch(
    ABCDispatch,
    ViewBox[
        CallbackQueryViewT,
        ChatJoinRequestViewT,
        ChatMemberViewT,
        InlineQueryViewT,
        MessageViewT,
        RawEventViewT,
    ],
):
    global_context: TelegrinderCtx = dataclasses.field(
        init=False,
        default_factory=lambda: TelegrinderCtx(),
    )
    default_handlers: list[ABCHandler] = dataclasses.field(
        init=False,
        default_factory=lambda: [],
    )

    def __repr__(self) -> str:
        return "Dispatch(%s)" % ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())

    @property
    def patcher(self) -> Patcher:
        """Alias `patcher` to get `vbml.Patcher` from the global context"""
        return self.global_context.vbml_patcher

    @typing.overload
    def handle(
        self,
        *rules: ABCRule[Event],
    ) -> typing.Callable[[Handler[T]], FuncHandler[Event, Handler[T], ErrorHandler]]: ...

    @typing.overload
    def handle(
        self,
        *rules: ABCRule[Event],
        is_blocking: bool = True,
    ) -> typing.Callable[[Handler[T]], FuncHandler[Event, Handler[T], ErrorHandler]]: ...

    @typing.overload
    def handle(
        self,
        *rules: ABCRule[Event],
        dataclass: type[T],
        is_blocking: bool = True,
    ) -> typing.Callable[[Handler[T]], FuncHandler[Event, Handler[T], ErrorHandler]]: ...

    @typing.overload
    def handle(  # type: ignore
        self,
        *rules: ABCRule[Event],
        error_handler: ErrorHandlerT,
        is_blocking: bool = True,
    ) -> typing.Callable[[Handler[T]], FuncHandler[Event, Handler[T], ErrorHandlerT]]: ...

    @typing.overload
    def handle(
        self,
        *rules: ABCRule[Event],
        dataclass: type[T],
        error_handler: ErrorHandlerT,
        is_blocking: bool = True,
    ) -> typing.Callable[[Handler[T]], FuncHandler[Event, Handler[T], ErrorHandlerT]]: ...

    @typing.overload
    def handle(
        self,
        *rules: ABCRule[Event],
        dataclass: type[T] = DEFAULT_DATACLASS,
        error_handler: typing.Literal[None] = None,
        is_blocking: bool = True,
    ) -> typing.Callable[[Handler[T]], FuncHandler[Event, Handler[T], ErrorHandler]]: ...

    def handle(  # type: ignore
        self,
        *rules: ABCRule,
        dataclass: type[typing.Any] = DEFAULT_DATACLASS,
        error_handler: ErrorHandlerT | None = None,
        is_blocking: bool = True,
    ):
        def wrapper(func: typing.Callable):
            handler = FuncHandler(
                func,
                list(rules),
                is_blocking=is_blocking,
                dataclass=dataclass,
                error_handler=error_handler or ErrorHandler(),
            )
            self.default_handlers.append(handler)
            return handler

        return wrapper

    async def feed(self, event: Update, api: ABCAPI) -> bool:
        logger.debug("Processing update (update_id={})", event.update_id)
        await self.raw_event.process(event, api)
        for view in self.get_views().values():
            if await view.check(event):
                logger.debug(
                    "Update (update_id={}) matched view {!r}",
                    event.update_id,
                    view.__class__.__name__,
                )
                await view.process(event, api)
                return True

        loop = asyncio.get_running_loop()
        ctx = Context()
        found = False
        for handler in self.default_handlers:
            if await handler.check(api, event, ctx):
                found = True
                loop.create_task(handler.run(event, ctx))
                if handler.is_blocking:
                    break
        return found

    def load(self, external: typing.Self) -> None:
        view_external = external.get_views()
        for name, view in self.get_views().items():
            assert (
                name in view_external
            ), f"View {name!r} is undefined in external dispatch."
            view.load(view_external[name])
            setattr(external, name, view)


__all__ = ("Dispatch",)
