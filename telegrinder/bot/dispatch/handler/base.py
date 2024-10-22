import abc
import typing

from fntypes.result import Result

from telegrinder.api.api import API
from telegrinder.api.error import APIError
from telegrinder.bot.cute_types.message import MessageCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.handler.abc import ABCHandler
from telegrinder.bot.dispatch.process import check_rule
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.modules import logger
from telegrinder.types.objects import Update

type APIMethod = typing.Callable[
    typing.Concatenate[MessageCute, ...], typing.Awaitable[Result[typing.Any, APIError]]
]


class BaseReplyHandler(ABCHandler[MessageCute], abc.ABC):
    def __init__(
        self,
        *rules: ABCRule,
        is_blocking: bool = True,
        as_reply: bool = False,
        preset_context: Context | None = None,
        **default_params: typing.Any,
    ) -> None:
        self.rules = list(rules)
        self.as_reply = as_reply
        self.is_blocking = is_blocking
        self.default_params = default_params
        self.preset_context = preset_context or Context()

    def __repr__(self) -> str:
        return f"<{self.__class__.__qualname__}>"

    async def check(self, api: API, event: Update, ctx: Context | None = None) -> bool:
        ctx = Context(raw_update=event) if ctx is None else ctx
        temp_ctx = ctx.copy()
        temp_ctx |= self.preset_context

        for rule in self.rules:
            if not await check_rule(api, rule, event, ctx):
                logger.debug("Rule {!r} failed!", rule)
                return False

        ctx |= temp_ctx
        return True

    @abc.abstractmethod
    async def run(self, api: API, event: MessageCute, ctx: Context) -> typing.Any:
        pass


__all__ = ("BaseReplyHandler",)
