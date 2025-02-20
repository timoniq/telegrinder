import typing

from telegrinder.api.api import API
from telegrinder.bot.cute_types.message import MessageCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.handler.base import BaseReplyHandler
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.types.objects import InputFile


class VideoReplyHandler(BaseReplyHandler):
    def __init__(
        self,
        video: InputFile | str,
        *rules: ABCRule,
        caption: str | None = None,
        parse_mode: str | None = None,
        final: bool = True,
        as_reply: bool = False,
        preset_context: Context | None = None,
        **default_params: typing.Any,
    ) -> None:
        self.video = video
        self.parse_mode = parse_mode
        self.caption = caption
        super().__init__(
            *rules,
            final=final,
            as_reply=as_reply,
            preset_context=preset_context,
            **default_params,
        )

    async def run(self, _: API, event: MessageCute, __: Context) -> typing.Any:
        method = event.answer_video if not self.as_reply else event.reply_video
        await method(
            video=self.video,
            parse_mode=self.parse_mode,
            caption=self.caption,
            **self.default_params,
        )


__all__ = ("VideoReplyHandler",)
