from telegrinder.api import ABCAPI, APIError
from telegrinder.model import get_params
from telegrinder.option.msgspec_option import Option
from telegrinder.result import Result
from telegrinder.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    Message,
    MessageEntity,
    User,
)

from .base import BaseCute


class CallbackQueryCute(BaseCute[CallbackQuery], CallbackQuery, kw_only=True):
    api: ABCAPI

    @property
    def from_user(self) -> User:
        return self.from_

    async def answer(
        self,
        text: str | Option[str] | None = None,
        show_alert: bool | Option[bool] | None = None,
        url: str | Option[str] | None = None,
        cache_time: int | Option[int] | None = None,
        **other,
    ) -> Result[bool, APIError]:
        params = get_params(locals())
        return await self.ctx_api.answer_callback_query(self.id, **params)

    async def edit_text(
        self,
        text: str | Option[str] | None = None,
        parse_mode: str | Option[str] | None = None,
        entities: list[MessageEntity] | Option[list[MessageEntity]] | None = None,
        disable_web_page_preview: bool | Option[bool] | None = None,
        reply_markup: InlineKeyboardMarkup
        | Option[InlineKeyboardMarkup]
        | None = None,
        **other,
    ) -> Result[Message | bool, APIError]:
        params = get_params(locals())
        if self.message:
            message = self.message.unwrap()
            if message.message_thread_id and "message_thread_id" not in params:
                params["message_thread_id"] = message.message_thread_id
            return await self.ctx_api.edit_message_text(
                chat_id=message.chat.id,
                message_id=message.message_id,
                **params,
            )
        return await self.ctx_api.edit_message_text(
            inline_message_id=self.inline_message_id,
            **params,
        )
