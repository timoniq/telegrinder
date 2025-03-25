import base64
import typing
from contextlib import suppress

import msgspec
from fntypes.co import Nothing, Result, Some, Variative, unwrapping

from telegrinder.api import API, APIError
from telegrinder.bot.cute_types.base import BaseCute, compose_method_params
from telegrinder.bot.cute_types.message import MediaType, MessageCute, ReplyMarkup, execute_method_edit
from telegrinder.model import UNSET, From, field, get_params
from telegrinder.msgspec_utils import Option, decoder
from telegrinder.tools.magic import shortcut
from telegrinder.types.objects import *


class CallbackQueryCute(BaseCute[CallbackQuery], CallbackQuery, kw_only=True):
    api: API

    message: Option[Variative[MessageCute, InaccessibleMessage]] = field(
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
            return Nothing()

        if "cached_callback_data" in self.__dict__:
            return self.__dict__["cached_callback_data"]

        data = Nothing()
        with suppress(msgspec.ValidationError, msgspec.DecodeError):
            data = (
                Some(decoder.decode(self.data.unwrap(), type=to))
                if not issubclass(to, str | bytes)
                else self.data
                if issubclass(to, str)
                else Some(base64.urlsafe_b64decode(self.data.unwrap()))
            )

        self.__dict__["cached_callback_data"] = data
        return data  # type: ignore

    @shortcut("answer_callback_query", custom_params={"callback_query_id"})
    async def answer(
        self,
        text: str | None = None,
        *,
        cache_time: int | None = None,
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
        disable_notification: bool | None = None,
        from_chat_id: int | str | None = None,
        message_id: int | None = None,
        message_thread_id: int | None = None,
        parse_mode: str | None = None,
        protect_content: bool | None = None,
        reply_markup: ReplyMarkup | None = None,
        reply_parameters: ReplyParameters | None = None,
        show_caption_above_media: bool | None = None,
        video_start_timestamp: int | None = None,
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
        message_thread_id: int | None = None,
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
        permission in a supergroup or a channel, it can delete any message there.
        Returns True on success."""
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
        message_thread_id: int | None = None,
        parse_mode: str | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
        **other: typing.Any,
    ) -> Result[Variative[MessageCute, bool], APIError]:
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

    @shortcut(
        "edit_message_live_location",
        executor=execute_method_edit,
        custom_params={"message_thread_id"},
    )
    async def edit_live_location(
        self,
        *,
        longitude: float,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        heading: int | None = None,
        horizontal_accuracy: float | None = None,
        inline_message_id: str | None = None,
        live_period: int | None = None,
        message_id: int | None = None,
        message_thread_id: int | None = None,
        proximity_alert_radius: int | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
        **other: typing.Any,
    ) -> Result[Variative[MessageCute, bool], APIError]:
        """Shortcut `API.edit_message_live_location()`, see the [documentation](https://core.telegram.org/bots/api#editmessagelivelocation)

        Use this method to edit live location messages. A location can be edited
        until its live_period expires or editing is explicitly disabled by a call
        to stopMessageLiveLocation. On success, if the edited message is not an
        inline message, the edited Message is returned, otherwise True is returned.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messageto be edited was sent.

        :param chat_id: Required if inline_message_id is not specified. Unique identifier forthe target chat or username of the target channel (in the format @channelusername).
        :param message_id: Required if inline_message_id is not specified. Identifier of the messageto edit.

        :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of theinline message.

        :param latitude: Latitude of new location.

        :param longitude: Longitude of new location.

        :param live_period: New period in seconds during which the location can be updated, startingfrom the message send date. If 0x7FFFFFFF is specified, then the locationcan be updated forever. Otherwise, the new value must not exceed the currentlive_period by more than a day, and the live location expiration date mustremain within the next 90 days. If not specified, then live_period remainsunchanged.

        :param horizontal_accuracy: The radius of uncertainty for the location, measured in meters; 0-1500.
        :param heading: Direction in which the user is moving, in degrees. Must be between 1 and 360if specified.

        :param proximity_alert_radius: The maximum distance for proximity alerts about approaching another chatmember, in meters. Must be between 1 and 100000 if specified.

        :param reply_markup: A JSON-serialized object for a new inline keyboard."""
        ...

    @shortcut(
        "edit_message_caption",
        executor=execute_method_edit,
        custom_params={"message_thread_id"},
    )
    async def edit_caption(
        self,
        caption: str | None = None,
        *,
        business_connection_id: str | None = None,
        caption_entities: list[MessageEntity] | None = None,
        chat_id: int | str | None = None,
        inline_message_id: str | None = None,
        message_id: int | None = None,
        message_thread_id: int | None = None,
        parse_mode: str | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
        show_caption_above_media: bool | None = None,
        **other: typing.Any,
    ) -> Result[Variative[MessageCute, bool], APIError]:
        """Shortcut `API.edit_message_caption()`, see the [documentation](https://core.telegram.org/bots/api#editmessagecaption)

        Use this method to edit captions of messages. On success, if the edited message
        is not an inline message, the edited Message is returned, otherwise True
        is returned. Note that business messages that were not sent by the bot and
        do not contain an inline keyboard can only be edited within 48 hours from
        the time they were sent.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messageto be edited was sent.

        :param chat_id: Required if inline_message_id is not specified. Unique identifier forthe target chat or username of the target channel (in the format @channelusername).
        :param message_id: Required if inline_message_id is not specified. Identifier of the messageto edit.

        :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of theinline message.

        :param caption: New caption of the message, 0-1024 characters after entities parsing.
        :param parse_mode: Mode for parsing entities in the message caption. See formatting optionsfor more details.

        :param caption_entities: A JSON-serialized list of special entities that appear in the caption,which can be specified instead of parse_mode.

        :param show_caption_above_media: Pass True, if the caption must be shown above the message media. Supportedonly for animation, photo and video messages.

        :param reply_markup: A JSON-serialized object for an inline keyboard."""
        ...

    @shortcut(
        "edit_message_media",
        custom_params={
            "media",
            "type",
            "message_thread_id",
            "caption",
            "parse_mode",
            "caption_entities",
        },
    )
    async def edit_media(
        self,
        media: str | InputFile | InputMedia,
        *,
        business_connection_id: str | None = None,
        caption: str | None = None,
        caption_entities: list[MessageEntity] | None = None,
        chat_id: int | str | None = None,
        inline_message_id: str | None = None,
        message_id: int | None = None,
        message_thread_id: int | None = None,
        parse_mode: str | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
        type: MediaType | None = None,
        **other: typing.Any,
    ) -> Result[Variative[MessageCute, bool], APIError]:
        """Shortcut `API.edit_message_media()`, see the [documentation](https://core.telegram.org/bots/api#editmessagemedia)

        Use this method to edit animation, audio, document, photo, or video messages,
        or to add media to text messages. If a message is part of a message album, then
        it can be edited only to an audio for audio albums, only to a document for document
        albums and to a photo or a video otherwise. When an inline message is edited,
        a new file can't be uploaded; use a previously uploaded file via its file_id
        or specify a URL. On success, if the edited message is not an inline message,
        the edited Message is returned, otherwise True is returned. Note that business
        messages that were not sent by the bot and do not contain an inline keyboard
        can only be edited within 48 hours from the time they were sent.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messageto be edited was sent.

        :param chat_id: Required if inline_message_id is not specified. Unique identifier forthe target chat or username of the target channel (in the format @channelusername).
        :param message_id: Required if inline_message_id is not specified. Identifier of the messageto edit.

        :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of theinline message.

        :param media: A JSON-serialized object for a new media content of the message.

        :param reply_markup: A JSON-serialized object for a new inline keyboard."""
        return await MessageCute.edit_media(self, **get_params(locals()))  # type: ignore

    @shortcut(
        "edit_message_reply_markup",
        executor=execute_method_edit,
        custom_params={"message_thread_id"},
    )
    async def edit_reply_markup(
        self,
        *,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        inline_message_id: str | None = None,
        message_id: int | None = None,
        message_thread_id: int | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
        **other: typing.Any,
    ) -> Result[Variative[MessageCute, bool], APIError]:
        """Shortcut `API.edit_message_reply_markup()`, see the [documentation](https://core.telegram.org/bots/api#editmessagereplymarkup)

        Use this method to edit only the reply markup of messages. On success, if
        the edited message is not an inline message, the edited Message is returned,
        otherwise True is returned. Note that business messages that were not sent
        by the bot and do not contain an inline keyboard can only be edited within
        48 hours from the time they were sent.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messageto be edited was sent.

        :param chat_id: Required if inline_message_id is not specified. Unique identifier forthe target chat or username of the target channel (in the format @channelusername).
        :param message_id: Required if inline_message_id is not specified. Identifier of the messageto edit.

        :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of theinline message.

        :param reply_markup: A JSON-serialized object for an inline keyboard."""
        ...


__all__ = ("CallbackQueryCute",)
