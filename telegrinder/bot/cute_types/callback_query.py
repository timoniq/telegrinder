from telegrinder.api import ABCAPI, APIError
from telegrinder.model import get_params
from telegrinder.result import Result
from telegrinder.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    Message,
    MessageEntity,
    User,
)

from .base import BaseCute


class CallbackQueryCute(BaseCute, CallbackQuery, kw_only=True):
    api: ABCAPI

    @property
    def from_user(self) -> User:
        return self.from_

    async def answer(
        self,
        text: str | None = None,
        show_alert: bool | None = None,
        url: str | None = None,
        cache_time: int | None = None,
        **other,
    ) -> Result[bool, APIError]:
        params = get_params(locals())
        return await self.ctx_api.answer_callback_query(self.id, **params)

    async def edit_text(
        self,
        inline_message_id: str | None = None,
        text: str | None = None,
        parse_mode: str | None = None,
        entities: list[MessageEntity] | None = None,
        disable_web_page_preview: bool | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
        **other,
    ) -> Result[Message | bool, APIError]:
        params = get_params(locals())
        return await self.ctx_api.edit_message_text(
            chat_id=self.message.chat.id,
            message_id=self.message.message_id,
            **params,
        )
