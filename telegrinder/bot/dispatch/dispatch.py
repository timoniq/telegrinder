from __future__ import annotations

import dataclasses

import typing_extensions as typing
from fntypes import Nothing, Option, Some
from vbml.patcher.abc import ABCPatcher

from telegrinder.api.api import API
from telegrinder.bot.dispatch.abc import ABCDispatch
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.handler.func import ErrorHandlerT, Func, FuncHandler
from telegrinder.bot.dispatch.middleware.abc import run_middleware
from telegrinder.bot.dispatch.middleware.global_middleware import GlobalMiddleware
from telegrinder.bot.dispatch.view.abc import ABCView
from telegrinder.bot.dispatch.view.box import (
    CallbackQueryView,
    ChatJoinRequestView,
    ChatMemberView,
    ErrorView,
    InlineQueryView,
    MessageView,
    PreCheckoutQueryView,
    RawEventView,
    ViewBox,
)
from telegrinder.modules import logger
from telegrinder.tools.error_handler.error_handler import ErrorHandler
from telegrinder.tools.global_context import TelegrinderContext
from telegrinder.types.objects import Update

if typing.TYPE_CHECKING:
    from telegrinder.bot.cute_types.base import BaseCute
    from telegrinder.bot.rules.abc import ABCRule
    from telegrinder.node.composer import Composer

T = typing.TypeVar("T", default=typing.Any)
R = typing.TypeVar("R", covariant=True, default=typing.Any)
Event = typing.TypeVar("Event", bound="BaseCute")
P = typing.ParamSpec("P", default=...)


@dataclasses.dataclass(repr=False, kw_only=True)
class Dispatch(
    ABCDispatch,
    ViewBox[
        CallbackQueryView,
        ChatJoinRequestView,
        ChatMemberView,
        InlineQueryView,
        MessageView,
        PreCheckoutQueryView,
        RawEventView,
        ErrorView,
    ],
    typing.Generic[
        CallbackQueryView,
        ChatJoinRequestView,
        ChatMemberView,
        InlineQueryView,
        MessageView,
        PreCheckoutQueryView,
        RawEventView,
        ErrorView,
    ],
):
    global_context: TelegrinderContext = dataclasses.field(
        init=False,
        default_factory=TelegrinderContext,
    )
    global_middleware: "GlobalMiddleware" = dataclasses.field(
        default_factory=lambda: GlobalMiddleware(),
    )

    def __repr__(self) -> str:
        return "Dispatch(%s)" % ", ".join(f"{k}={v!r}" for k, v in self.get_views().items())

    @property
    def patcher(self) -> ABCPatcher:
        """Alias `patcher` to get `vbml.Patcher` from the global context."""
        return self.global_context.vbml_patcher

    @property
    def composer(self) -> Composer:
        """Alias `composer` to get `telegrinder.node.composer.Composer` from the global context."""
        return self.global_context.composer.unwrap()

    @typing.overload
    def handle(
        self,
        *rules: "ABCRule",
        final: bool = True,
    ) -> typing.Callable[[Func[P, R]], FuncHandler[Func[P, R], ErrorHandler]]: ...

    @typing.overload
    def handle(
        self,
        *rules: "ABCRule",
        error_handler: ErrorHandlerT,
        final: bool = True,
    ) -> typing.Callable[[Func[P, R]], FuncHandler[Func[P, R], ErrorHandlerT]]: ...

    def handle(
        self,
        *rules: "ABCRule",
        error_handler: ErrorHandlerT | None = None,
        final: bool = True,
    ) -> typing.Callable[..., typing.Any]:
        def wrapper(func):
            handler = FuncHandler(
                func,
                list(rules),
                final=final,
                error_handler=error_handler or ErrorHandler(),
            )
            self.raw_event.handlers.append(handler)
            return handler

        return wrapper

    async def feed(self, event: Update, api: API) -> bool:
        processed = False
        context = Context().add_update_cute(event, api)
        start_time = self.global_context.loop_wrapper.loop.time()

        if (
            await run_middleware(
                self.global_middleware.pre,
                api,
                event,
                context,
                required_nodes=self.global_middleware.pre_required_nodes,
            )
            is False
        ):
            return processed

        for view in self.get_views().values():
            if await view.check(event):
                logger.debug(
                    "Processing update (id={}, type={!r}) using view {!r} by bot (id={})",
                    event.update_id,
                    event.update_type,
                    view,
                    api.id,
                )

                try:
                    if await view.process(event, api, context):
                        processed = True
                        break
                except BaseException as exception:
                    if not await self.error.process(event, api, context.add_exception_update(exception)):
                        raise exception

        await run_middleware(
            self.global_middleware.post,
            api,
            event,
            context,
            required_nodes=self.global_middleware.post_pre_required_nodes,
        )
        logger.debug(
            "Update (id={}, type={!r}) processed in {} ms by bot (id={})",
            event.update_id,
            event.update_type,
            int((self.global_context.loop_wrapper.loop.time() - start_time) * 1000),
            api.id,
        )
        return processed

    def load(self, external: typing.Self) -> None:
        views_external = external.get_views()

        for name, view in self.get_views().items():
            assert name in views_external, f"View {name!r} is undefined in external dispatch."
            view.load(views_external[name])
            setattr(external, name, view)

        self.global_middleware.filters.difference_update(external.global_middleware.filters)

    def get_view(self, of_type: type[T]) -> Option[T]:
        for view in self.get_views().values():
            if isinstance(view, of_type):
                return Some(view)
        return Nothing()

    def get_views(self) -> dict[str, ABCView]:
        """Get all views."""
        return {
            name: view for name, view in self.__dict__.items() if isinstance(view, ABCView) and name != "error"
        }

    __call__ = handle


__all__ = ("Dispatch",)
