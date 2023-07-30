from .abc import ABCStateView
from telegrinder.bot.dispatch.handler import ABCHandler, FuncHandler
from telegrinder.bot.dispatch.middleware import ABCMiddleware
from telegrinder.bot.rules import ABCRule
from telegrinder.bot.cute_types import MessageCute
from telegrinder.api.abc import ABCAPI
from telegrinder.bot.dispatch.process import process_inner
from telegrinder.types import Update
import typing


class MessageView(ABCStateView):
    def __init__(self):
        self.auto_rules: list[ABCRule] = []
        self.handlers: list[ABCHandler[MessageCute]] = []
        self.middlewares: list[ABCMiddleware[MessageCute]] = []

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
        return bool(event.message)

    def get_state_key(self, event: MessageCute) -> int | None:
        return event.chat.id

    async def process(self, event: Update, api: ABCAPI):
        msg = MessageCute(**event.message.to_dict(), api=api)
        return await process_inner(msg, event, self.middlewares, self.handlers)
