import typing

from fntypes.co import Option, Result, Some, Variative

from telegrinder.api import ABCAPI, APIError
from telegrinder.model import get_params
from telegrinder.msgspec_utils import Nothing
from telegrinder.types import (
    ForceReply,
    InlineKeyboardMarkup,
    Message,
    MessageEntity,
    ReactionType,
    ReactionTypeEmoji,
    ReactionTypeType,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ReplyParameters,
    User,
)
from telegrinder.types.objects import InputFile

from .base import BaseCute

ReplyMarkup = typing.Union[
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ForceReply,
]


def get_entity_value(
    entities: list[MessageEntity], entity_value: str
) -> Option[typing.Any]:
    for entity in entities:
        if (obj := getattr(entity, entity_value, Nothing)):
            return Some(obj.value if isinstance(obj, Some) else obj)
    return Nothing


class MessageCute(BaseCute[Message], Message, kw_only=True):
    api: ABCAPI

    @property
    def mentioned_user(self) -> Option[User]:
        """Mentioned user without username."""

        if not self.entities:
            return Nothing
        return get_entity_value(self.entities.unwrap(), "user")

    @property
    def url(self) -> Option[str]:
        """Clickable text URL."""

        if not self.entities:
            return Nothing
        return get_entity_value(self.entities.unwrap(), "url")

    @property
    def programming_language(self) -> Option[str]:
        """The programming language of the entity text."""

        if not self.entities:
            return Nothing
        return get_entity_value(self.entities.unwrap(), "language")

    @property
    def custom_emoji_id(self) -> Option[str]:
        """Unique identifier of the custom emoji."""

        if not self.entities:
            return Nothing
        return get_entity_value(self.entities.unwrap(), "custom_emoji_id")

    async def answer(
        self,
        text: str | Option[str],
        parse_mode: str | Option[str] = Nothing,
        entities: list[MessageEntity] | Option[list[MessageEntity]] = Nothing,
        disable_web_page_preview: bool | Option[bool] = Nothing,
        disable_notification: bool | Option[bool] = Nothing,
        protect_content: bool | Option[bool] = Nothing,
        reply_to_message_id: int | Option[int] = Nothing,
        allow_sending_without_reply: bool | Option[bool] = Nothing,
        reply_markup: ReplyMarkup | Option[ReplyMarkup] = Nothing,
        **other: typing.Any,
    ) -> Result["Message", APIError]:
        params = get_params(locals())
        if "message_thread_id" not in params and self.is_topic_message:
            params["message_thread_id"] = self.message_thread_id
        return await self.ctx_api.send_message(chat_id=self.chat.id, **params)
    
    async def answer_file(
        self,
        file: str | InputFile,
        caption: str | Option[str] = Nothing,
        parse_mode: str | Option[str] = Nothing,
        thumbnail: Option[InputFile | str] | InputFile | str = Nothing,
        caption_entities: list[MessageEntity] | Option[list[MessageEntity]] = Nothing,
        disable_content_type_detection: Option[bool] | bool = Nothing,
        disable_notification: Option[bool] | bool = Nothing,
        protect_content: bool | Option[bool] = Nothing,
        reply_parameters: Option[ReplyParameters] | ReplyParameters = Nothing,
        reply_markup: ReplyMarkup | Option[ReplyMarkup] = Nothing,
        **other: typing.Any,
    ) -> Result[Message, APIError]:
        params = get_params(locals())
        if "message_thread_id" not in params and self.is_topic_message:
            params["message_thread_id"] = self.message_thread_id
        return await self.ctx_api.send_document(
            chat_id=self.chat.id,
            document=file,
            **params,
        )

    async def reply(
        self,
        text: str | Option[str],
        parse_mode: str | Option[str] = Nothing,
        entities: list[MessageEntity] | Option[list[MessageEntity]] = Nothing,
        disable_web_page_preview: bool | Option[bool] = Nothing,
        disable_notification: bool | Option[bool] = Nothing,
        protect_content: bool | Option[bool] = Nothing,
        allow_sending_without_reply: bool | Option[bool] = Nothing,
        reply_markup: ReplyMarkup | Option[ReplyMarkup] = Nothing,
        **other: typing.Any,
    ) -> Result["Message", APIError]:
        params = get_params(locals())
        if "message_thread_id" not in params and self.is_topic_message:
            params["message_thread_id"] = self.message_thread_id
        return await self.ctx_api.send_message(
            chat_id=self.chat.id,
            reply_to_message_id=self.message_id,
            **params,
        )

    async def delete(self, **other: typing.Any) -> Result[bool, APIError]:
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
        text: str | Option[str] = Nothing,
        parse_mode: str | Option[str] = Nothing,
        entities: list[MessageEntity] | Option[list[MessageEntity]] = Nothing,
        disable_web_page_preview: bool | Option[bool] = Nothing,
        reply_markup: InlineKeyboardMarkup
        | Option[InlineKeyboardMarkup] = Nothing,
        **other: typing.Any,
    ) -> Result[Variative[Message, bool], APIError]:
        params = get_params(locals())
        if "message_thread_id" not in params and self.is_topic_message:
            params["message_thread_id"] = self.message_thread_id
        return await self.ctx_api.edit_message_text(
            chat_id=self.chat.id,
            message_id=self.message_id,
            **params,
        )
    
    async def react(
        self,
        reaction: str | ReactionType
        | list[str | ReactionType]
        | Option[list[str | ReactionType]] = Nothing,
        is_big: bool | Option[bool] = Nothing,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        if reaction:
            reaction = [
                ReactionTypeEmoji(ReactionTypeType.EMOJI, r)
                if isinstance(r, str)
                else r
                for r in (
                    reaction.unwrap_or([]) if isinstance(reaction, Some | type(Nothing))
                    else [reaction] if not isinstance(reaction, list) else reaction
                )
            ]
        return await self.ctx_api.set_message_reaction(
            chat_id=self.chat.id,
            message_id=self.message_id,
            **get_params(locals())
        )


__all__ = ("MessageCute", "get_entity_value")
