import typing

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.cute_types import InlineQueryCute
from telegrinder.bot.dispatch.handler import ABCHandler, FuncHandler
from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware
from telegrinder.bot.dispatch.process import process_inner
from telegrinder.bot.rules import ABCRule
from telegrinder.types import Update

from .abc import ABCStateView


class InlineQueryView(ABCStateView[InlineQueryCute]):
    def __init__(self):
        self.auto_rules: list[ABCRule[InlineQueryCute]] = []
        self.handlers: list[ABCHandler[InlineQueryCute]] = []
        self.middlewares: list[ABCMiddleware[InlineQueryCute]] = []

    def __call__(self, *rules: ABCRule[InlineQueryCute], is_blocking: bool = True):
        def wrapper(
            func: typing.Callable[
                typing.Concatenate[InlineQueryCute, ...],
                typing.Coroutine,
            ]
        ):
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
        query = InlineQueryCute(**event.inline_query.to_dict(), api=api)  # type: ignore
        return await process_inner(query, event, self.middlewares, self.handlers)

    def load(self, external: typing.Self):
        self.auto_rules.extend(external.auto_rules)
        self.handlers.extend(external.handlers)
        self.middlewares.extend(external.middlewares)
