import typing

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.cute_types import MessageCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.process import check_rule
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.modules import logger
from telegrinder.msgspec_utils import Nothing
from telegrinder.types.objects import ReplyParameters, Update

from .abc import ABCHandler


class MessageReplyHandler(ABCHandler[MessageCute]):
    def __init__(
        self,
        text: str,
        *rules: ABCRule[MessageCute],
        as_reply: bool = False,
        is_blocking: bool = True,
    ):
        self.text = text
        self.rules = list(rules)
        self.as_reply = as_reply
        self.is_blocking = is_blocking
        self.preset_context = Context()

    async def check(self, api: ABCAPI, event: Update, ctx: Context | None = None) -> bool:
        ctx = ctx or Context()
        temp_ctx = ctx.copy()
        temp_ctx |= self.preset_context

        for rule in self.rules:
            if not await check_rule(api, rule, event, ctx):
                logger.debug("Rule {!r} failed!", rule)
                return False
        ctx.update(temp_ctx)
        return True

    async def run(self, event: MessageCute, _: Context) -> typing.Any:
        await event.answer(
            text=self.text,
            reply_parameters=ReplyParameters(event.message_id if self.as_reply else Nothing),
        )


__all__ = ("MessageReplyHandler",)
