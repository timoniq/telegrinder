import typing
from telegrinder.bot.cute_types import MessageCute
from telegrinder.types.objects import Update
from telegrinder.api.abc import ABCAPI
from telegrinder.bot.dispatch.process import check_rule
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.modules import logger
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
        self.dataclass = MessageCute
        self.ctx = {}

    async def check(self, api: ABCAPI, event: Update, ctx: dict) -> bool:
        ctx = ctx or {}
        preset_ctx = self.ctx.copy()
        self.ctx |= ctx
        for rule in self.rules:
            if not await check_rule(api, rule, event, self.ctx):
                logger.debug("Rule {} failed", rule)
                return False
        return True

    async def run(self, event: MessageCute) -> typing.Any:
        await event.answer(
            text=self.text,
            reply_to_message_id=(event.message_id if self.as_reply else None),
        )
