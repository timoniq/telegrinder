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
        text: typing.Optional[str] = None,
        parse_mode: typing.Optional[str] = None,
        entities: typing.Optional[typing.List["MessageEntity"]] = None,
        disable_web_page_preview: typing.Optional[bool] = None,
        disable_notification: typing.Optional[bool] = None,
        protect_content: typing.Optional[bool] = None,
        reply_to_message_id: typing.Optional[int] = None,
        allow_sending_without_reply: typing.Optional[bool] = None,
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
        text: typing.Optional[str] = None,
        parse_mode: typing.Optional[str] = None,
        entities: typing.Optional[typing.List["MessageEntity"]] = None,
        disable_web_page_preview: typing.Optional[bool] = None,
        disable_notification: typing.Optional[bool] = None,
        protect_content: typing.Optional[bool] = None,
        allow_sending_without_reply: typing.Optional[bool] = None,
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
        text: typing.Optional[str] = None,
        parse_mode: typing.Optional[str] = None,
        entities: typing.Optional[typing.List[MessageEntity]] = None,
        disable_web_page_preview: typing.Optional[bool] = None,
        reply_markup: typing.Optional[InlineKeyboardMarkup] = None,
        **other
    ) -> Result[Message | bool, APIError]:
        params = get_params(locals())
        if "message_thread_id" not in params and self.is_topic_message:
            params["message_thread_id"] = self.message_thread_id
        return await self.ctx_api.edit_message_text(
            chat_id=self.chat.id, message_id=self.message_id, **params
        )
