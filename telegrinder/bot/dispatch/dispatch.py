import asyncio
import dataclasses
import typing

from vbml.patcher import Patcher

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.bot.rules import ABCRule
from telegrinder.modules import logger
from telegrinder.tools.global_context import TelegrinderCtx
from telegrinder.types import Update

from .abc import ABCDispatch
from .handler import ABCHandler, FuncHandler
from .handler.func import ErrorHandlerT

from .view.box import CallbackQueryViewT, InlineQueryViewT, MessageViewT, ViewBox

T = typing.TypeVar("T")

Event = typing.TypeVar("Event", bound=BaseCute)
R = typing.TypeVar("R")
P = typing.ParamSpec("P")

DEFAULT_DATACLASS = Update


@dataclasses.dataclass(repr=False, frozen=True, kw_only=True)
class Dispatch(
    ABCDispatch,
    ViewBox[CallbackQueryViewT, InlineQueryViewT, MessageViewT],
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
        return "Dispatch(%s)" % ", ".join(
            f"{k}={v!r}" for k, v in self.__dict__.items()
        )

    @property
    def patcher(self) -> Patcher:
        """Alias `patcher` to get `vbml.Patcher` from the global context"""
        return self.global_context.vbml_patcher

    def handle(
        self,
        *rules: ABCRule,
        is_blocking: bool = True,
        dataclass: type[typing.Any] = DEFAULT_DATACLASS,
        error_handler: ErrorHandlerT | None = None,
    ):
        def wrapper(func: typing.Callable):
            handler = FuncHandler(
                func, list(rules), is_blocking, dataclass, error_handler,
            )
            self.default_handlers.append(handler)
            return handler

        return wrapper

    async def feed(self, event: Update, api: ABCAPI) -> bool:
        logger.debug("Processing update (update_id={})", event.update_id)
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
        found = False
        for handler in self.default_handlers:
            if await handler.check(api, event):
                found = True
                loop.create_task(handler.run(event))
                if handler.is_blocking:
                    break
        return found

    def load(self, external: typing.Self):
        view_external = external.get_views()
        for name, view in self.get_views().items():
            assert (
                name in view_external
            ), f"View {name!r} is undefined in external dispatch."
            view.load(view_external[name])
            setattr(external, name, view)
    
    @classmethod
    def to_handler(
        cls,
        *rules: ABCRule[BaseCute],
        is_blocking: bool = True,
        error_handler: ErrorHandlerT | None = None,
    ):
        def wrapper(
            func: typing.Callable[typing.Concatenate[T, P], typing.Awaitable[R]]
        ) -> FuncHandler[
            BaseCute,
            typing.Callable[typing.Concatenate[T, P], typing.Awaitable[R]],
            ErrorHandlerT,
        ]:
            return FuncHandler(
                func,
                list(rules),
                is_blocking=is_blocking,
                dataclass=None,
                error_handler=error_handler,
            )

        return wrapper
