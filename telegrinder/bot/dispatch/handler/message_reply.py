import typing

from telegrinder.bot.cute_types.message import MessageCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.handler.base import BaseReplyHandler
from telegrinder.bot.rules.abc import ABCRule


class MessageReplyHandler(BaseReplyHandler):
    def __init__(
        self,
        text: str,
        *rules: ABCRule,
        parse_mode: str | None = None,
        final: bool = True,
        as_reply: bool = False,
        preset_context: Context | None = None,
        **default_params: typing.Any,
    ) -> None:
        self.text = text
        self.parse_mode = parse_mode
        super().__init__(
            *rules,
            final=final,
            as_reply=as_reply,
            preset_context=preset_context,
            **default_params,
        )

    async def handle(self, message: MessageCute) -> None:
        method = message.answer if not self.as_reply else message.reply
        await method(text=self.text, parse_mode=self.parse_mode, **self.default_params)


__all__ = ("MessageReplyHandler",)
