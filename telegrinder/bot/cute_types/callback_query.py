import typing
from contextlib import suppress

import msgspec
from fntypes.co import Ok, Result, Some, Union

from telegrinder.api import ABCAPI, APIError
from telegrinder.model import get_params
from telegrinder.msgspec_utils import Nothing, Option, decoder
from telegrinder.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    Message,
    MessageEntity,
    User,
)

from .base import BaseCute


class CallbackQueryCute(BaseCute[CallbackQuery], CallbackQuery, kw_only=True, dict=True):
    api: ABCAPI

    @property
    def from_user(self) -> User:
        return self.from_
    
    def decode_callback_data(self, *, strict: bool = True) -> Option[dict]:
        if "cached_callback_data" in self.__dict__:
            return self.__dict__["cached_callback_data"]

        data = Nothing
        with suppress(msgspec.ValidationError):
            data = Some(decoder.decode(self.data.unwrap()))
        
        self.__dict__["cached_callback_data"] = data
        return data

    async def answer(
        self,
        text: str | Option[str] = Nothing,
        show_alert: bool | Option[bool] = Nothing,
        url: str | Option[str] = Nothing,
        cache_time: int | Option[int] = Nothing,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        params = get_params(locals())
        return await self.ctx_api.answer_callback_query(self.id, **params)

    async def edit_text(
        self,
        text: str | Option[str] = Nothing,
        parse_mode: str | Option[str] = Nothing,
        entities: list[MessageEntity] | Option[list[MessageEntity]] = Nothing,
        disable_web_page_preview: bool | Option[bool] = Nothing,
        reply_markup: InlineKeyboardMarkup
        | Option[InlineKeyboardMarkup]
        = Nothing,
        **other: typing.Any,
    ) -> Result[Union[Message, bool], APIError]:
        params = get_params(locals())
        if message := self.message.map(lambda message: message.only(Message)).unwrap_or_none():
            if message.unwrap().message_thread_id and "message_thread_id" not in params:
                params["message_thread_id"] = message.unwrap().message_thread_id.unwrap()
            return await self.ctx_api.edit_message_text(
                chat_id=message.unwrap().chat.id,
                message_id=message.unwrap().message_id,
                **params,
            )
        return await self.ctx_api.edit_message_text(
            inline_message_id=self.inline_message_id,
            **params,
        )


__all__ = ("CallbackQueryCute",)
