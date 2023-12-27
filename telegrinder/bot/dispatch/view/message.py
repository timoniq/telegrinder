import typing

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.cute_types import MessageCute
from telegrinder.bot.dispatch.handler import ABCHandler, FuncHandler
from telegrinder.bot.dispatch.handler.func import ErrorHandlerT
from telegrinder.bot.dispatch.middleware import ABCMiddleware
from telegrinder.bot.dispatch.process import process_inner
from telegrinder.bot.dispatch.return_manager import MessageReturnManager
from telegrinder.bot.rules import ABCRule
from telegrinder.types import Update

from .abc import ABCStateView


class MessageView(ABCStateView[MessageCute]):
    def __init__(self):
        self.auto_rules: list[ABCRule[MessageCute]] = []
        self.handlers: list[ABCHandler[MessageCute]] = []
        self.middlewares: list[ABCMiddleware[MessageCute]] = []
        self.return_manager = MessageReturnManager()

    def __call__(
        self,
        *rules: ABCRule[MessageCute],
        is_blocking: bool = True,
        error_handler: ErrorHandlerT | None = None,
    ):
        def wrapper(
            func: typing.Callable[
                typing.Concatenate[MessageCute, ...],
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
        return bool(event.message)

    def get_state_key(self, event: MessageCute) -> int | None:
        return event.chat.id

    async def process(self, event: Update, api: ABCAPI) -> bool:
        msg = MessageCute(**event.message.unwrap().to_dict(), api=api)
        return await process_inner(msg, event, self.middlewares, self.handlers, self.return_manager)

    def load(self, external: typing.Self):
        self.auto_rules.extend(external.auto_rules)
        self.handlers.extend(external.handlers)
        self.middlewares.extend(external.middlewares)
