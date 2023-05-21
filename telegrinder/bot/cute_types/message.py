from telegrinder.types import (
    Message,
    MessageEntity,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ForceReply,
)
from telegrinder.model import get_params
from telegrinder.api import API, APIError
from telegrinder.result import Result
import typing


class MessageCute(Message):
    api: API

    @property
    def ctx_api(self) -> API:
        return self.api

    async def answer(
        self,
        text: str | None = None,
        parse_mode: str | None = None,
        entities: list["MessageEntity"] | None = None,
        disable_web_page_preview: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        reply_to_message_id: int | None = None,
        allow_sending_without_reply: bool | None = None,
        reply_markup: typing.Optional[
            typing.Union[
                "InlineKeyboardMarkup",
                "ReplyKeyboardMarkup",
                "ReplyKeyboardRemove",
                "ForceReply",
            ]
        ] = None,
        **other
    ) -> Result["Message", APIError]:
        params = get_params(locals())
        if "message_thread_id" not in params and self.is_topic_message:
            params["message_thread_id"] = self.message_thread_id
        return await self.ctx_api.send_message(chat_id=self.chat.id, **params)

    async def reply(
        self,
        text: str | None = None,
        parse_mode: str | None = None,
        entities: list["MessageEntity"] | None = None,
        disable_web_page_preview: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_sending_without_reply: bool | None = None,
        reply_markup: typing.Optional[
            typing.Union[
                "InlineKeyboardMarkup",
                "ReplyKeyboardMarkup",
                "ReplyKeyboardRemove",
                "ForceReply",
            ]
        ] = None,
        **other
    ) -> Result["Message", APIError]:
        params = get_params(locals())
        if "message_thread_id" not in params and self.is_topic_message:
            params["message_thread_id"] = self.message_thread_id
        return await self.ctx_api.send_message(
            chat_id=self.chat.id, reply_to_message_id=self.message_id, **params
        )

    async def delete(self, **other) -> Result[bool, APIError]:
        params = get_params(locals())
        if "message_thread_id" not in params and self.is_topic_message:
            params["message_thread_id"] = self.message_thread_id
        return await self.ctx_api.delete_message(
            chat_id=self.chat.id, message_id=self.message_id, **params
        )

    async def edit(
        self,
        text: str | None = None,
        parse_mode: str | None = None,
        entities: list[MessageEntity] | None = None,
        disable_web_page_preview: bool | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
        **other
    ) -> Result[Message | bool, APIError]:
        params = get_params(locals())
        if "message_thread_id" not in params and self.is_topic_message:
            params["message_thread_id"] = self.message_thread_id
        return await self.ctx_api.edit_message_text(
            chat_id=self.chat.id, message_id=self.message_id, **params
        )
