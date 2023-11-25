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
from telegrinder.types.methods import OptionType

from .base import BaseCute


class CallbackQueryCute(BaseCute[CallbackQuery], CallbackQuery, kw_only=True):
    api: ABCAPI

    @property
    def from_user(self) -> User:
        return self.from_

    async def answer(
        self,
        text: str | OptionType[str] | None = None,
        show_alert: bool | OptionType[bool] | None = None,
        url: str | OptionType[str] | None = None,
        cache_time: int | OptionType[int] | None = None,
        **other,
    ) -> Result[bool, APIError]:
        params = get_params(locals())
        return await self.ctx_api.answer_callback_query(self.id, **params)

    async def edit_text(
        self,
        text: str | OptionType[str] | None = None,
        parse_mode: str | OptionType[str] | None = None,
        entities: list[MessageEntity] | OptionType[list[MessageEntity]] | None = None,
        disable_web_page_preview: bool | OptionType[bool] | None = None,
        reply_markup: InlineKeyboardMarkup
        | OptionType[InlineKeyboardMarkup]
        | None = None,
        **other,
    ) -> Result[Message | bool, APIError]:
        params = get_params(locals())
        if self.message:
            message = self.message.unwrap()
            return await self.ctx_api.edit_message_text(
                chat_id=message.chat.id,
                message_id=message.message_id,
                **params,
            )
        return await self.ctx_api.edit_message_text(
            inline_message_id=self.inline_message_id,
            **params,
        )
