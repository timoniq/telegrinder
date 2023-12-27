import typing

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.cute_types import CallbackQueryCute
from telegrinder.bot.dispatch.handler import ABCHandler, FuncHandler
from telegrinder.bot.dispatch.handler.func import ErrorHandlerT
from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware
from telegrinder.bot.dispatch.process import process_inner
from telegrinder.bot.dispatch.return_manager import CallbackQueryReturnManager
from telegrinder.bot.rules import ABCRule
from telegrinder.types import Update

from .abc import ABCStateView


class CallbackQueryView(ABCStateView[CallbackQueryCute]):
    def __init__(self):
        self.auto_rules: list[ABCRule[CallbackQueryCute]] = []
        self.handlers: list[ABCHandler[CallbackQueryCute]] = []
        self.middlewares: list[ABCMiddleware[CallbackQueryCute]] = []
        self.return_manager = CallbackQueryReturnManager()

    def __call__(
        self,
        *rules: ABCRule[CallbackQueryCute],
        is_blocking: bool = True,
        error_handler: ErrorHandlerT | None = None,
    ):
        def wrapper(
            func: typing.Callable[
                typing.Concatenate[CallbackQueryCute, ...],
                typing.Coroutine,
            ]
        ):
            func_handler = FuncHandler(
                func,
                [*self.auto_rules, *rules],
                is_blocking,
                dataclass=None,
                error_handler=error_handler,
            )
            self.handlers.append(func_handler)
            return func_handler

        return wrapper

    async def check(self, event: Update) -> bool:
        return bool(event.callback_query)

    def get_state_key(self, event: CallbackQueryCute) -> int | None:
        return event.message.message_id  # type: ignore

    async def process(self, event: Update, api: ABCAPI) -> bool:
        query = CallbackQueryCute(**event.callback_query.unwrap().to_dict(), api=api)
        return await process_inner(query, event, self.middlewares, self.handlers, self.return_manager)

    def load(self, external: typing.Self):
        self.auto_rules.extend(external.auto_rules)
        self.handlers.extend(external.handlers)
        self.middlewares.extend(external.middlewares)
