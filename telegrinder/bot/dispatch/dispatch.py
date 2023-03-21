import asyncio

from .abc import ABCDispatch
from telegrinder.bot.rules import ABCRule
from .handler import ABCHandler, FuncHandler
from telegrinder.types import Update
from telegrinder.api.abc import ABCAPI
from telegrinder.modules import logger
from .view import ABCView, MessageView, CallbackQueryView, InlineQueryView
from vbml.patcher.abc import ABCPatcher
import typing
import vbml

T = typing.TypeVar("T")

DEFAULT_DATACLASS = Update


class Dispatch(ABCDispatch):
    def __init__(
        self,
        patcher: typing.Optional[ABCPatcher] = None,
        **rule_dependencies: typing.Any,
    ):
        self.auto_rules: typing.List[ABCRule] = []
        self.patcher = patcher or vbml.Patcher()
        rule_dependencies["patcher"] = self.patcher
        self.rule_dependencies = rule_dependencies
        self.default_handlers: typing.List[ABCHandler] = []
        self.message = MessageView(**self.rule_dependencies)
        self.callback_query = CallbackQueryView(**self.rule_dependencies)
        self.inline_query = InlineQueryView(**self.rule_dependencies)
        self.views = ["message", "callback_query", "inline_query"]

    def handle(
        self,
        *rules: ABCRule,
        is_blocking: bool = True,
        dataclass: typing.Any = DEFAULT_DATACLASS,
    ):
        def wrapper(func: typing.Callable):
            self.default_handlers.append(
                FuncHandler(
                    func, [*self.auto_rules, *rules], is_blocking, dataclass,
                    **self.rule_dependencies
                )
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
        logger.debug("processing update (update_id={})", event.update_id)
        for view in self.get_views():
            if await view.check(event):
                logger.debug(
                    "update {} matched view {}",
                    event.update_id,
                    view.__class__.__name__,
                )
                await view.process(event, api)
                return True

        loop = asyncio.get_running_loop()
        assert loop, "No running loop"

        found = False
        for handler in self.default_handlers:
            result = await handler.check(api, event)
            if result:
                found = True
                loop.create_task(handler.run(event))
                if handler.is_blocking:
                    return True
        return found

    def mount(self, view_t: typing.Type["ABCView"], name: str):
        self.views.append(name)
        setattr(self, name, view_t)
