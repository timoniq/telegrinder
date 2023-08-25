import typing

from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware
from .abc import ABCStateView
from telegrinder.bot.dispatch.handler import ABCHandler, FuncHandler
from telegrinder.bot.rules import ABCRule
from telegrinder.bot.cute_types import InlineQueryCute
from telegrinder.api.abc import ABCAPI
from telegrinder.bot.dispatch.process import process_inner
from telegrinder.types import Update


class InlineQueryView(ABCStateView[InlineQueryCute]):
    def __init__(self):
        self.auto_rules: list[ABCRule[InlineQueryCute]] = []
        self.handlers: list[ABCHandler[InlineQueryCute]] = []
        self.middlewares: list[ABCMiddleware[InlineQueryCute]] = []

    def __call__(self, *rules: ABCRule, is_blocking: bool = True):
        def wrapper(func: typing.Callable[..., typing.Coroutine]):
            self.handlers.append(
                FuncHandler(
                    func, [*self.auto_rules, *rules], is_blocking, dataclass=None
                )
            )
            return func

        return wrapper

    async def check(self, event: Update) -> bool:
        return bool(event.inline_query)

    def get_state_key(self, event: InlineQueryCute) -> int | None:
        return event.from_.id

    async def process(self, event: Update, api: ABCAPI):
        query = InlineQueryCute(**event.inline_query.to_dict(), api=api)
        return await process_inner(query, event, self.middlewares, self.handlers)

    def load(self, external: typing.Self):
        self.auto_rules.extend(external.auto_rules)
        self.handlers.extend(external.handlers)
        self.middlewares.extend(external.middlewares)
