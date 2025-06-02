import typing

from telegrinder.bot.cute_types.message import MessageCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.handler.base import BaseReplyHandler
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.types.objects import InputFile


class StickerReplyHandler(BaseReplyHandler):
    def __init__(
        self,
        sticker: InputFile | str,
        *rules: ABCRule,
        emoji: str | None = None,
        final: bool = True,
        as_reply: bool = False,
        preset_context: Context | None = None,
        **default_params: typing.Any,
    ) -> None:
        self.sticker = sticker
        self.emoji = emoji
        super().__init__(
            *rules,
            final=final,
            as_reply=as_reply,
            preset_context=preset_context,
            **default_params,
        )

    async def handle(self, message: MessageCute) -> None:
        method = message.answer_sticker if not self.as_reply else message.reply_sticker
        await method(sticker=self.sticker, emoji=self.emoji, **self.default_params)


__all__ = ("StickerReplyHandler",)
