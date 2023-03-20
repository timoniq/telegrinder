from .abc import ABCView
from telegrinder.bot.dispatch.handler import ABCHandler, FuncHandler
from telegrinder.bot.dispatch.waiter import Waiter
from telegrinder.bot.dispatch.middleware import ABCMiddleware
from telegrinder.bot.rules import ABCRule
from telegrinder.bot.cute_types import MessageCute
from telegrinder.api.abc import ABCAPI
from telegrinder.bot.dispatch.waiter import WithWaiter, DefaultWaiterHandler
from telegrinder.bot.dispatch.process import process_waiters, process_inner
from telegrinder.types import Update
import typing


class MessageView(ABCView, WithWaiter[int, MessageCute]):
    def __init__(self, **rule_dependencies: typing.Any):
        self.auto_rules: typing.List[ABCRule] = []
        self.handlers: typing.List[ABCHandler[MessageCute]] = []
        self.middlewares: typing.List[ABCMiddleware[MessageCute]] = []
        self.short_waiters: typing.Dict[int, Waiter] = {}
        self.rule_dependencies = rule_dependencies

    def __call__(self, *rules: ABCRule, is_blocking: bool = True):
        def wrapper(func: typing.Callable[..., typing.Coroutine]):
            self.handlers.append(
                FuncHandler(
                    func, [*self.auto_rules, *rules], is_blocking, dataclass=None,
                    **self.rule_dependencies
                )
            )
            return func

        return wrapper

    def load(self, external: "MessageView"):
        self.handlers.extend(external.handlers)
        self.middlewares.extend(external.middlewares)
        external.short_waiters = self.short_waiters

    async def check(self, event: Update) -> bool:
        return bool(event.message)

    async def process(self, event: Update, api: ABCAPI):
        msg = MessageCute(**event.message.to_dict(), api=api)

        if await process_waiters(
            self.short_waiters, msg.chat.id, msg, event, msg.answer,
            **self.rule_dependencies
        ):
            return

        return await process_inner(msg, event, self.middlewares, self.handlers)

    async def wait_for_message(
        self,
        chat_id: int,
        *rules: ABCRule,
        default: typing.Optional[typing.Union[DefaultWaiterHandler, str]] = None
    ) -> typing.Tuple["MessageCute", dict]:
        return await self.wait_for_answer(chat_id, [*self.auto_rules, *rules], default=default)
