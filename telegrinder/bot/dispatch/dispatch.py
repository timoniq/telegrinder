import asyncio

from .abc import ABCDispatch
from telegrinder.bot.rules import ABCRule
from .handler import ABCHandler, FuncHandler
from telegrinder.types import Update
from telegrinder.api.abc import ABCAPI
from .view import ABCView, MessageView, CallbackQueryView, InlineQueryView
import typing

T = typing.TypeVar("T")

DEFAULT_DATACLASS = Update


class Dispatch(ABCDispatch):
    def __init__(self):
        self.default_handlers: typing.List[ABCHandler] = []
        self.loop = asyncio.get_event_loop()
        self.message = MessageView()
        self.callback_query = CallbackQueryView()
        self.inline_query = InlineQueryView()
        self.views = ["message", "callback_query", "inline_query"]

    def handle(
        self,
        *rules: ABCRule,
        is_blocking: bool = True,
        dataclass: typing.Any = DEFAULT_DATACLASS,
    ):
        def wrapper(func: typing.Callable):
            self.default_handlers.append(
                FuncHandler(func, list(rules), is_blocking, dataclass)
            )
            return func

        return wrapper

    def get_views(self) -> typing.Iterator[ABCView]:
        for view_name in self.views:
            view = getattr(self, view_name)
            assert view, f"View {view_name} is undefined in dispatch"
            yield view

    def get_view(self, view_t: typing.Type[T], name: str) -> typing.Optional[T]:
        if name not in self.views:
            return None
        view = getattr(self, name)
        assert isinstance(view, view_t)
        return view  # type: ignore

    def load(self, external: "Dispatch"):
        for view_name in self.views:
            view = getattr(self, view_name)
            assert view, f"View {view_name} is undefined in dispatch"
            view_external = getattr(external, view_name)
            assert view_external, f"View {view_name} is undefined in external dispatch"
            view.load(view_external)

    async def feed(self, event: Update, api: ABCAPI) -> bool:

        for view in self.get_views():
            if await view.check(event):
                await view.process(event, api)
                return True

        found = False
        for handler in self.default_handlers:
            result = await handler.check(event)
            if result:
                found = True
                self.loop.create_task(handler.run(event))
                if handler.is_blocking:
                    return True
        return found

    def mount(self, view_t: typing.Type["ABCView"], name: str):
        self.views.append(name)
        setattr(self, name, view_t)
