from .abc import ABCView
from telegrinder.bot.dispatch.handler import ABCHandler, FuncHandler
from telegrinder.bot.dispatch.waiter import Waiter
from telegrinder.bot.dispatch.middleware import ABCMiddleware
from telegrinder.bot.rules import ABCRule
from telegrinder.bot.cute_types import CallbackQueryCute
from telegrinder.api.abc import ABCAPI
from telegrinder.bot.dispatch.waiter import WithWaiter
from telegrinder.bot.dispatch.process import process_waiters, process_inner
import typing
import asyncio


class CallbackQueryView(ABCView, WithWaiter[int, CallbackQueryCute]):
    def __init__(self):
        self.handlers: typing.List[ABCHandler[CallbackQueryCute]] = []
        self.middlewares: typing.List[ABCMiddleware[CallbackQueryCute]] = []
        self.short_waiters: typing.Dict[int, Waiter] = {}
        self.loop = asyncio.get_event_loop()

    def __call__(self, *rules: ABCRule, is_blocking: bool = True):
        def wrapper(func: typing.Callable[..., typing.Coroutine]):
            self.handlers.append(
                FuncHandler(func, list(rules), is_blocking, dataclass=None)
            )
            return func

        return wrapper

    async def check(self, event: dict) -> bool:
        return "callback_query" in event

    async def process(self, event: dict, api: ABCAPI):
        query = CallbackQueryCute(**event["callback_query"], unprep_ctx_api=api)

        if await process_waiters(
            self.short_waiters, query.from_.id, query, event, query.answer
        ):
            return

        return await process_inner(query, event, self.middlewares, self.handlers)

    def load(self, external: "CallbackQueryView"):
        self.handlers.extend(external.handlers)
        self.middlewares.extend(external.middlewares)
        external.short_waiters = self.short_waiters
