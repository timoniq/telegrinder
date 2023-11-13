import asyncio
import typing

from vbml.patcher import Patcher

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.rules import ABCRule
from telegrinder.modules import logger
from telegrinder.tools.global_context import TelegrinderCtx
from telegrinder.types import Update

from .abc import ABCDispatch
from .handler import ABCHandler, FuncHandler
from .view import ABCView, CallbackQueryView, InlineQueryView, MessageView

T = typing.TypeVar("T")
DEFAULT_DATACLASS = Update


class Dispatch(ABCDispatch):
    def __init__(self):
        self.message = MessageView()
        self.callback_query = CallbackQueryView()
        self.inline_query = InlineQueryView()
        self.views = {"message", "callback_query", "inline_query"}
        self.global_context: TelegrinderCtx = TelegrinderCtx()
        self.default_handlers: list[ABCHandler] = []

    @property
    def patcher(self) -> Patcher:
        """Alias `patcher` to get `vbml.Patcher` from the global context"""
        return self.global_context.vbml_patcher

    def handle(
        self,
        *rules: ABCRule,
        is_blocking: bool = True,
        dataclass: type[typing.Any] = DEFAULT_DATACLASS,
    ):
        def wrapper(func: typing.Callable):
            self.default_handlers.append(
                FuncHandler(func, list(rules), is_blocking, dataclass)
            )
            return func

        return wrapper

    def get_views(self) -> typing.Iterator[ABCView]:
        for view_name in self.views:
            view = getattr(self, view_name, None)
            assert view, f"View {view_name!r} is undefined in dispatch"
            yield view

    def get_view(self, view_t: typing.Type[T], name: str) -> T | None:
        if name not in self.views:
            return None
        view = getattr(self, name)
        assert isinstance(view, view_t)
        return view

    def load(self, external: typing.Self):
        for view_name in self.views:
            view = getattr(self, view_name, None)
            assert view, f"View {view_name!r} is undefined in dispatch"
            view_external = getattr(external, view_name, None)
            assert (
                view_external
            ), f"View {view_name!r} is undefined in external dispatch"
            view.load(view_external)
            setattr(external, view_name, view)

    async def feed(self, event: Update, api: ABCAPI) -> bool:
        logger.debug("Processing update (update_id={})", event.update_id)
        for view in self.get_views():
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

    def mount(self, view: ABCView, name: str):
        self.views.add(name)
        setattr(self, name, view)
