import typing

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.cute_types import MessageCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.process import check_rule
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.modules import logger
from telegrinder.types.objects import ReplyParameters, Update

from .abc import ABCHandler


class MessageReplyHandler(ABCHandler[MessageCute]):
    def __init__(
        self,
        text: str,
        *rules: ABCRule,
        is_blocking: bool = True,
        as_reply: bool = False,
        preset_context: Context | None = None,
        **default_params: typing.Any,
    ) -> None:
        self.text = text
        self.rules = list(rules)
        self.as_reply = as_reply
        self.is_blocking = is_blocking
        self.default_params = default_params
        self.preset_context = preset_context or Context()

    def __repr__(self) -> str:
        return "<{}: with rules={!r}, {}: {!r}>".format(
            ("blocking " if self.is_blocking else "") + self.__class__.__name__,
            self.rules,
            "answer text as reply" if self.as_reply else "answer text",
            self.text,
        )

    async def check(self, api: ABCAPI, event: Update, ctx: Context | None = None) -> bool:
        ctx = ctx or Context()
        temp_ctx = ctx.copy()
        temp_ctx |= self.preset_context

        for rule in self.rules:
            if not await check_rule(api, rule, event, ctx):
                logger.debug("Rule {!r} failed!", rule)
                return False

        ctx |= temp_ctx
        return True

    async def run(self, event: MessageCute, _: Context) -> typing.Any:
        await event.answer(
            text=self.text,
            reply_parameters=ReplyParameters(event.message_id) if self.as_reply else None,
            **self.default_params,
        )


__all__ = ("MessageReplyHandler",)
