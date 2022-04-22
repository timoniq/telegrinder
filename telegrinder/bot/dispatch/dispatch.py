import asyncio

from .abc import ABCDispatch
from abc import ABC, abstractmethod
from telegrinder.bot.rules import ABCRule
from .handler import ABCHandler, FuncHandler
from telegrinder.types import Update
from telegrinder.api.abc import ABCAPI
from .view import ABCView, MessageView, CallbackQueryView
import typing

T = typing.TypeVar("T")

DEFAULT_DATACLASS = Update


class Dispatch(ABCDispatch):
    def __init__(self):
        self.default_handlers: typing.List[ABCHandler] = []
        self.loop = asyncio.get_event_loop()
        self.message = MessageView()
        self.callback_query = CallbackQueryView()
        self.views = ["message"]

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

    async def feed(self, event: dict, api: ABCAPI) -> bool:

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
