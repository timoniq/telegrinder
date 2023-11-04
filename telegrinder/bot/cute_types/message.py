import typing

from telegrinder.api import ABCAPI, API, APIError
from telegrinder.model import get_params
from telegrinder.result import Result
from telegrinder.types import (
    ForceReply,
    InlineKeyboardMarkup,
    Message,
    MessageEntity,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    User,
)


def get_enitity_value(
    entities: list[MessageEntity], name_value: str
) -> typing.Any | None:
    for entity in entities:
        if (enitity_value := getattr(entity, name_value)) is not None:
            return enitity_value


class MessageCute(Message):
    api: ABCAPI

    @property
    def ctx_api(self) -> API:
        return self.api  # type: ignore

    @property
    def mentioned_user(self) -> User | None:
        """Mentioned user without username"""
        if not self.entities:
            return
        return get_enitity_value(self.entities, "user")

    @property
    def url(self) -> str | None:
        """Clickable text URL"""
        if not self.entities:
            return
        return get_enitity_value(self.entities, "url")

    @property
    def programming_language(self) -> str | None:
        """The programming language of the entity text"""
        if not self.entities:
            return
        return get_enitity_value(self.entities, "language")

    @property
    def custom_emoji_id(self) -> str | None:
        """Unique identifier of the custom emoji"""
        if not self.entities:
            return
        return get_enitity_value(self.entities, "custom_emoji_id")

    @classmethod
    def from_update(cls, update: Message, bound_api: ABCAPI) -> typing.Self:
        return cls(**update.to_dict(), api=bound_api)

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
        **other,
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
        **other,
    ) -> Result["Message", APIError]:
        params = get_params(locals())
        if "message_thread_id" not in params and self.is_topic_message:
            params["message_thread_id"] = self.message_thread_id
        return await self.ctx_api.send_message(
            chat_id=self.chat.id,
            reply_to_message_id=self.message_id,
            **params,
        )

    async def delete(self, **other) -> Result[bool, APIError]:
        params = get_params(locals())
        if "message_thread_id" not in params and self.is_topic_message:
            params["message_thread_id"] = self.message_thread_id
        return await self.ctx_api.delete_message(
            chat_id=self.chat.id,
            message_id=self.message_id,
            **params,
        )

    async def edit(
        self,
        text: str | None = None,
        parse_mode: str | None = None,
        entities: list[MessageEntity] | None = None,
        disable_web_page_preview: bool | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
        **other,
    ) -> Result[Message | bool, APIError]:
        params = get_params(locals())
        if "message_thread_id" not in params and self.is_topic_message:
            params["message_thread_id"] = self.message_thread_id
        return await self.ctx_api.edit_message_text(
            chat_id=self.chat.id,
            message_id=self.message_id,
            **params,
        )

    def to_dict(self) -> dict[str, typing.Any]:
        return super().to_dict(exclude_fields={"api"})
