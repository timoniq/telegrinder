from .abc import ABCView
from telegrinder.bot.dispatch.handler import ABCHandler, FuncHandler
from telegrinder.bot.dispatch.waiter import Waiter
from telegrinder.bot.dispatch.middleware import ABCMiddleware
from telegrinder.bot.rules import ABCRule
from telegrinder.bot.cute_types import InlineQueryCute
from telegrinder.api.abc import ABCAPI
from telegrinder.bot.dispatch.waiter import WithWaiter
from telegrinder.bot.dispatch.process import process_waiters, process_inner
from telegrinder.types import Update
import typing


class InlineQueryView(ABCView, WithWaiter[str, InlineQueryCute]):
    def __init__(self):
        self.handlers: typing.List[ABCHandler[InlineQueryCute]] = []
        self.middlewares: typing.List[ABCMiddleware[InlineQueryCute]] = []
        self.short_waiters: typing.Dict[str, Waiter] = {}

    def __call__(self, *rules: ABCRule, is_blocking: bool = True):
        def wrapper(func: typing.Callable[..., typing.Coroutine]):
            self.handlers.append(
                FuncHandler(func, list(rules), is_blocking, dataclass=None)
            )
            return func

        return wrapper

    def load(self, external: "InlineQueryView"):
        self.handlers.extend(external.handlers)
        self.middlewares.extend(external.middlewares)
        external.short_waiters = self.short_waiters

    async def check(self, event: Update) -> bool:
        return bool(event.inline_query)

    async def process(self, event: Update, api: ABCAPI):
        query = InlineQueryCute(**event.inline_query.to_dict(), api=api)

        if await process_waiters(
            self.short_waiters, query.id, query, event, query.answer
        ):
            return

        return await process_inner(query, event, self.middlewares, self.handlers)
