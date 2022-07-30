from .abc import ABCView
from telegrinder.bot.dispatch.handler import ABCHandler, FuncHandler
from telegrinder.bot.dispatch.waiter import Waiter, wait
from telegrinder.bot.dispatch.middleware import ABCMiddleware
from telegrinder.bot.rules import ABCRule
from telegrinder.bot.cute_types import MessageCute
from telegrinder.api.abc import ABCAPI
from telegrinder.bot.dispatch.waiter import DefaultWaiterHandler
import typing
import asyncio


class MessageView(ABCView):
    def __init__(self):
        self.handlers: typing.List[ABCHandler[MessageCute]] = []
        self.middlewares: typing.List[ABCMiddleware[MessageCute]] = []
        self.short_waiters: typing.Dict[int, Waiter] = {}
        self.loop = asyncio.get_event_loop()

    def __call__(self, *rules: ABCRule, is_blocking: bool = True):
        def wrapper(func: typing.Callable[..., typing.Coroutine]):
            self.handlers.append(
                FuncHandler(func, list(rules), is_blocking, dataclass=None)
            )
            return func
        return wrapper

    def load(self, external: "MessageView"):
        self.handlers.extend(external.handlers)
        self.middlewares.extend(external.middlewares)

    async def check(self, event: dict) -> bool:
        return "message" in event

    async def process(self, event: dict, api: ABCAPI):
        msg = MessageCute(**event["message"], unprep_ctx_api=api)

        if msg.chat.id in self.short_waiters:
            waiter = self.short_waiters[msg.chat.id]
            ctx = {}

            for rule in waiter.rules:
                chk_event = msg
                if rule.__event__ is None:
                    chk_event = event
                if not await rule.check(chk_event, ctx):
                    if not waiter.default:
                        return
                    elif isinstance(waiter.default, str):
                        await msg.answer(waiter.default)
                    else:
                        await waiter.default(msg)
                    return

            self.short_waiters.pop(msg.chat.id)
            setattr(waiter.event, "e", (msg, ctx))
            waiter.event.set()
            return

        ctx = {}

        for middleware in self.middlewares:
            if await middleware.pre(msg, ctx) is False:
                return False

        found = False
        responses = []
        for handler in self.handlers:
            result = await handler.check(event)
            if result:
                handler.ctx.update(ctx)
                found = True
                response = await handler.run(msg)
                responses.append(response)
                if handler.is_blocking:
                    break

        for middleware in self.middlewares:
            await middleware.post(msg, responses, ctx)

        return found

    async def wait_for_message(
        self,
        chat_id: int,
        *rules: ABCRule,
        default: typing.Optional[typing.Union[DefaultWaiterHandler, str]] = None
    ) -> typing.Tuple[MessageCute, dict]:
        event = asyncio.Event()
        waiter = Waiter(rules, event, default)
        self.short_waiters[chat_id] = waiter
        return await wait(waiter)
