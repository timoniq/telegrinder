import base64
import typing
from contextlib import suppress
from datetime import timedelta

import msgspec
from kungfu.library import Nothing, Result, Some, Sum, unwrapping
from kungfu.library.monad.option import NOTHING

from telegrinder.api.api import APIError
from telegrinder.bot.cute_types.base import BaseCute, compose_method_params, shortcut
from telegrinder.bot.cute_types.message import (
    MessageCute,
    MessageEditShortcuts,
    ReplyMarkup,
    execute_method_edit,
)
from telegrinder.model import UNSET, From, field
from telegrinder.msgspec_utils import Option, decoder
from telegrinder.types.methods_utils import get_params
from telegrinder.types.objects import *

CACHED_CALLBACK_DATA_KEY: typing.Final = "cached_callback_data"


class CallbackQueryCute(BaseCute[CallbackQuery], MessageEditShortcuts, CallbackQuery, kw_only=True):
    message: Option[Sum[MessageCute, InaccessibleMessage]] = field(
        default=UNSET,
        converter=From[MessageCute | InaccessibleMessage | None],
    )
    """Optional. Message sent by the bot with the callback button that originated
    the query."""

    @property
    def from_user(self) -> User:
        return self.from_

    @property
    @unwrapping
    def message_cute(self) -> Option[MessageCute]:
        return self.message.unwrap().only().cast(Some, Nothing)

    @property
    def chat_id(self) -> Option[int]:
        """Optional. Message from chat ID. This will be present if the message is sent
        by the bot with the callback button that originated the query.
        """
        return self.message.map(lambda m: m.v.chat.id)

    @property
    def is_topic_message(self) -> Option[bool]:
        """Optional. True, if the message is a topic message with a name,
        color and icon. This will be present if the message is sent
        by the bot with the callback button that originated the query.
        """
        return self.message.map(
            lambda m: m.only().map(lambda m: m.is_topic_message.unwrap_or(False)).unwrap_or(False),
        )

    @property
    @unwrapping
    def message_thread_id(self) -> Option[int]:
        """Optional. Unique identifier of the target message thread (for forum supergroups only).
        This will be present if the message is sent
        by the bot with the callback button that originated the query.
        """
        return self.message.unwrap().only().map(lambda m: m.message_thread_id.unwrap()).cast(Some, Nothing)

    @property
    def message_id(self) -> Option[int]:
        """Optional. Unique message identifier inside this chat. This will be present
        if the message is sent by the bot with the callback button that originated the query.
        """
        return self.message.map(lambda m: m.v.message_id)

    @property
    def chat(self) -> Option[Chat]:
        """Optional. Chat the callback query originated from. This will be present
        if the message is sent by the bot with the callback button that originated the query.
        """
        return self.message.map(lambda m: m.v.chat)

    @typing.overload
    def decode_data(self) -> Option[dict[str, typing.Any]]: ...

    @typing.overload
    def decode_data[T](self, *, to: type[T]) -> Option[T]: ...

    def decode_data[T](self, *, to: type[T] = dict[str, typing.Any]) -> Option[T]:
        if not self.data:
            return NOTHING

        keys = typing.cast(
            "dict[type[typing.Any], typing.Any]",
            self.__dict__.setdefault(CACHED_CALLBACK_DATA_KEY, {}),  # type: ignore
        )
        if to in keys:
            return keys[to]

        data = NOTHING
        orig_to = typing.get_origin(to) or to

        with suppress(msgspec.ValidationError, msgspec.DecodeError):
            data = (
                Some(decoder.decode(self.data.unwrap(), type=to))
                if not issubclass(orig_to, str | bytes)
                else self.data
                if issubclass(orig_to, str)
                else Some(base64.urlsafe_b64decode(self.data.unwrap()))
            )

        keys[to] = data
        return data  # type: ignore

    @shortcut("answer_callback_query", custom_params={"callback_query_id"})
    async def answer(
        self,
        text: str | None = None,
        *,
        cache_time: timedelta | int | None = None,
        callback_query_id: str | None = None,
        show_alert: bool | None = None,
        url: str | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Shortcut `API.answer_callback_query()`, see the [documentation](https://core.telegram.org/bots/api#answercallbackquery)

        Use this method to send answers to callback queries sent from inline keyboards.
        The answer will be displayed to the user as a notification at the top of the
        chat screen or as an alert. On success, True is returned."""
        params = compose_method_params(get_params(locals()), self, default_params={("callback_query_id", "id")})
        return await self.ctx_api.answer_callback_query(**params)

    @shortcut(
        "copy_message",
        custom_params={
            "message_thread_id",
            "chat_id",
            "message_id",
            "from_chat_id",
            "reply_markup",
        },
    )
    async def copy(
        self,
        chat_id: int | str | None = None,
        *,
        allow_paid_broadcast: bool | None = None,
        caption: str | None = None,
        caption_entities: list[MessageEntity] | None = None,
        direct_messages_topic_id: int | None = None,
        disable_notification: bool | None = None,
        from_chat_id: int | str | None = None,
        message_effect_id: str | None = None,
        message_id: int | None = None,
        message_thread_id: str | None = None,
        parse_mode: str | None = None,
        protect_content: bool | None = None,
        reply_markup: ReplyMarkup | None = None,
        reply_parameters: ReplyParameters | None = None,
        show_caption_above_media: bool | None = None,
        suggested_post_parameters: SuggestedPostParameters | None = None,
        video_start_timestamp: timedelta | int | None = None,
        **other: typing.Any,
    ) -> Result[MessageId, APIError]:
        """Shortcut `API.copy_message()`, see the [documentation](https://core.telegram.org/bots/api#copymessage)

        Use this method to copy messages of any kind. Service messages, paid media
        messages, giveaway messages, giveaway winners messages, and invoice
        messages can't be copied. A quiz poll can be copied only if the value of the
        field correct_option_id is known to the bot. The method is analogous to
        the method forwardMessage, but the copied message doesn't have a link to
        the original message. Returns the MessageId of the sent message on success."""
        return await MessageCute.copy(self, **get_params(locals()))  # type: ignore

    @shortcut("delete_message", custom_params={"message_thread_id", "chat_id", "message_id"})
    async def delete(
        self,
        *,
        chat_id: int | None = None,
        message_id: int | None = None,
        message_thread_id: str | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Shortcut `API.delete_message()`, see the [documentation](https://core.telegram.org/bots/api#deletemessage)

        Use this method to delete a message, including service messages, with the
        following limitations: - A message can only be deleted if it was sent less
        than 48 hours ago. - Service messages about a supergroup, channel, or forum
        topic creation can't be deleted. - A dice message in a private chat can only
        be deleted if it was sent more than 24 hours ago. - Bots can delete outgoing
        messages in private chats, groups, and supergroups. - Bots can delete incoming
        messages in private chats. - Bots granted can_post_messages permissions
        can delete outgoing messages in channels. - If the bot is an administrator
        of a group, it can delete any message there. - If the bot has can_delete_messages
        administrator right in a supergroup or a channel, it can delete any message
        there. - If the bot has can_manage_direct_messages administrator right
        in a channel, it can delete any message in the corresponding direct messages
        chat. Returns True on success."""
        return await MessageCute.delete(self, **get_params(locals()))  # type: ignore

    @shortcut(
        "edit_message_text",
        executor=execute_method_edit,
        custom_params={"message_thread_id"},
    )
    async def edit_text(
        self,
        text: str,
        *,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        entities: list[MessageEntity] | None = None,
        inline_message_id: str | None = None,
        link_preview_options: LinkPreviewOptions | None = None,
        message_id: int | None = None,
        message_thread_id: str | None = None,
        parse_mode: str | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
        **other: typing.Any,
    ) -> Result[Sum[MessageCute, bool], APIError]:
        """Shortcut `API.edit_message_text()`, see the [documentation](https://core.telegram.org/bots/api#editmessagetext)

        Use this method to edit text and game messages. On success, if the edited
        message is not an inline message, the edited Message is returned, otherwise
        True is returned. Note that business messages that were not sent by the bot
        and do not contain an inline keyboard can only be edited within 48 hours from
        the time they were sent.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messageto be edited was sent.

        :param chat_id: Required if inline_message_id is not specified. Unique identifier forthe target chat or username of the target channel (in the format @channelusername).
        :param message_id: Required if inline_message_id is not specified. Identifier of the messageto edit.

        :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of theinline message.

        :param text: New text of the message, 1-4096 characters after entities parsing.

        :param parse_mode: Mode for parsing entities in the message text. See formatting options formore details.

        :param entities: A JSON-serialized list of special entities that appear in message text,which can be specified instead of parse_mode.

        :param link_preview_options: Link preview generation options for the message.

        :param reply_markup: A JSON-serialized object for an inline keyboard."""
        ...


__all__ = ("CallbackQueryCute",)
