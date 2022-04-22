from .abc import ABCView
from telegrinder.bot.dispatch.handler import ABCHandler, FuncHandler
from telegrinder.bot.dispatch.waiter import Waiter, wait
from telegrinder.bot.dispatch.middleware import ABCMiddleware
from telegrinder.bot.rules import ABCRule
from telegrinder.bot.cute_types import CallbackQueryCute
from telegrinder.api.abc import ABCAPI
from telegrinder.bot.dispatch.waiter import DefaultWaiterHandler
import typing
import asyncio


class CallbackQueryView(ABCView):
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

        if query.from_.id in self.short_waiters:
            waiter = self.short_waiters[query.from_.id]
            ctx = {}

            for rule in waiter.rules:
                chk_event = query
                if rule.__dataclass__ == dict:
                    chk_event = event
                if not await rule.check(chk_event, ctx):
                    if not waiter.default:
                        return
                    elif isinstance(waiter.default, str):
                        await query.answer(waiter.default)
                    else:
                        await waiter.default(query)
                    return

            self.short_waiters.pop(query.from_.id)
            setattr(waiter.event, "e", (query, ctx))
            waiter.event.set()
            return

        ctx = {}

        for middleware in self.middlewares:
            if not await middleware.pre(query, ctx):
                return False

        found = False
        responses = []
        for handler in self.handlers:
            result = await handler.check(event)
            if result:
                handler.ctx.update(ctx)
                found = True
                response = await handler.run(query)
                responses.append(response)
                if handler.is_blocking:
                    break

        for middleware in self.middlewares:
            await middleware.post(query, responses, ctx)

        return found

    async def wait_for_answer(
        self,
        chat_id: int,
        *rules: ABCRule,
        default: typing.Optional[typing.Union[DefaultWaiterHandler, str]] = None
    ) -> typing.Tuple[CallbackQueryCute, dict]:
        event = asyncio.Event()
        waiter = Waiter(rules, event, default)
        self.short_waiters[chat_id] = waiter
        return await wait(waiter)
