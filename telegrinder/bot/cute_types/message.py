from __future__ import annotations

import typing

import fntypes.option
from fntypes.co import Result, Some, Variative

from telegrinder.api.api import API, APIError
from telegrinder.bot.cute_types.base import BaseCute, compose_method_params
from telegrinder.bot.cute_types.utils import compose_reactions, input_media
from telegrinder.model import UNSET, From, field, get_params
from telegrinder.msgspec_utils import Option
from telegrinder.tools.magic import shortcut
from telegrinder.types import *

if typing.TYPE_CHECKING:
    from datetime import datetime

    from telegrinder.bot.cute_types.callback_query import CallbackQueryCute

type MediaType = typing.Literal[
    "animation",
    "audio",
    "document",
    "photo",
    "video",
]
type InputMediaType = str | InputMedia | InputFile
type ReplyMarkup = InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply


async def execute_method_answer(
    message: MessageCute,
    method_name: str,
    params: dict[str, typing.Any],
) -> Result[typing.Any, APIError]:
    params = compose_method_params(
        params=params,
        update=message,
        default_params={"chat_id", "message_thread_id"},
        validators={"message_thread_id": lambda x: x.is_topic_message.unwrap_or(False)},
    )
    result = await getattr(message.ctx_api, method_name)(**params)
    return result.map(
        lambda x: (
            x
            if isinstance(x, bool)
            else (
                message.from_update(x, bound_api=message.api)
                if not isinstance(x, list)
                else [message.from_update(m, bound_api=message.api) for m in x]
            )
        )
    )


async def execute_method_reply(
    message: MessageCute,
    method_name: str,
    params: dict[str, typing.Any],
) -> Result[typing.Any, APIError]:
    params.setdefault(
        "reply_parameters",
        ReplyParameters(
            params.get("message_id", message.message_id),
            params.get("chat_id", message.chat_id),
        ),
    )
    return await execute_method_answer(message, method_name, params)


async def execute_method_edit(
    update: MessageCute | CallbackQueryCute,
    method_name: str,
    params: dict[str, typing.Any],
) -> Result[typing.Any, APIError]:
    params = compose_method_params(
        params=params,
        update=update,
        default_params={
            "chat_id",
            "message_id",
            "message_thread_id",
            "inline_message_id",
        },
        validators={
            "inline_message_id": lambda x: not x.message_id,
            "message_thread_id": lambda x: (
                x.is_topic_message.unwrap_or(False)
                if isinstance(x, MessageCute)
                else bool(x.message) and getattr(x.message.unwrap().v, "is_topic_message", False)
            ),
        },
    )

    if "inline_message_id" in params:
        params.pop("message_id", None)
        params.pop("chat_id", None)

    result = await getattr(update.ctx_api, method_name)(**params)
    return result.map(
        lambda v: Variative[MessageCute, bool](
            v.only()
            .map(
                lambda x: MessageCute.from_update(x, bound_api=update.api),
            )
            .unwrap_or(typing.cast(bool, v.v))
        )
    )


def get_entity_value(
    entity_value: typing.Literal["user", "url", "custom_emoji_id", "language"],
    entities: fntypes.option.Option[list[MessageEntity]],
    caption_entities: fntypes.option.Option[list[MessageEntity]],
) -> fntypes.option.Option[typing.Any]:
    ents = entities.unwrap_or(caption_entities.unwrap_or_none())
    if not ents:
        return fntypes.option.Nothing()

    for entity in ents:
        if (obj := getattr(entity, entity_value, fntypes.option.Nothing())) is not fntypes.option.Nothing():
            return obj if isinstance(obj, Some) else Some(obj)

    return fntypes.option.Nothing()


class MessageCute(BaseCute[Message], Message, kw_only=True):
    api: API

    reply_to_message: Option[MessageCute] = field(
        default=UNSET,
        converter=From["MessageCute | None"],
    )
    """Optional. For replies in the same chat and message thread, the original
    message. Note that the Message object in this field will not contain further
    reply_to_message fields even if it itself is a reply."""

    pinned_message: Option[Variative[MessageCute, InaccessibleMessage]] = field(
        default=UNSET,
        converter=From["MessageCute | InaccessibleMessage | None"],
    )
    """Optional. Specified message was pinned. Note that the Message object in
    this field will not contain further reply_to_message fields even if it
    itself is a reply."""

    @property
    def mentioned_user(self) -> fntypes.option.Option[User]:
        """Mentioned user without username."""
        return get_entity_value("user", self.entities, self.caption_entities)

    @property
    def url(self) -> fntypes.option.Option[str]:
        """Clickable text URL."""
        return get_entity_value("url", self.entities, self.caption_entities)

    @property
    def programming_language(self) -> fntypes.option.Option[str]:
        """The programming language of the entity text."""
        return get_entity_value("language", self.entities, self.caption_entities)

    @property
    def custom_emoji_id(self) -> fntypes.option.Option[str]:
        """Unique identifier of the custom emoji."""
        return get_entity_value("custom_emoji_id", self.entities, self.caption_entities)

    @shortcut(
        "send_message",
        executor=execute_method_answer,
        custom_params={"link_preview_options", "message_thread_id", "chat_id", "text"},
    )
    async def answer(
        self,
        text: str | None = None,
        *,
        allow_paid_broadcast: bool | None = None,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        disable_notification: bool | None = None,
        entities: list[MessageEntity] | None = None,
        link_preview_options: LinkPreviewOptions | None = None,
        message_effect_id: str | None = None,
        message_thread_id: int | None = None,
        parse_mode: str | None = None,
        protect_content: bool | None = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
        reply_parameters: ReplyParameters | None = None,
        **other: typing.Any,
    ) -> Result[MessageCute, APIError]:
        """Shortcut `API.send_message()`, see the [documentation](https://core.telegram.org/bots/api#sendmessage)

        Use this method to send text messages. On success, the sent Message is returned.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messagewill be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel(in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; forforum supergroups only.

        :param text: Text of the message to be sent, 1-4096 characters after entities parsing.
        :param parse_mode: Mode for parsing entities in the message text. See formatting options formore details.

        :param entities: A JSON-serialized list of special entities that appear in message text,which can be specified instead of parse_mode.

        :param link_preview_options: Link preview generation options for the message.

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcastinglimits for a fee of 0.1 Telegram Stars per message. The relevant Stars willbe withdrawn from the bot's balance.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for privatechats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inlinekeyboard, custom reply keyboard, instructions to remove a reply keyboardor to force a reply from the user."""
        ...

    @shortcut(
        "send_message",
        executor=execute_method_reply,
        custom_params={"message_thread_id", "chat_id", "message_id"},
    )
    async def reply(
        self,
        text: str,
        *,
        allow_paid_broadcast: bool | None = None,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        disable_notification: bool | None = None,
        entities: list[MessageEntity] | None = None,
        link_preview_options: LinkPreviewOptions | None = None,
        message_effect_id: str | None = None,
        message_id: int | None = None,
        message_thread_id: int | None = None,
        parse_mode: str | None = None,
        protect_content: bool | None = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
        reply_parameters: ReplyParameters | None = None,
        **other: typing.Any,
    ) -> Result[MessageCute, APIError]:
        """Shortcut `API.send_message()`, see the [documentation](https://core.telegram.org/bots/api#sendmessage)

        Use this method to send text messages. On success, the sent Message is returned.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messagewill be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel(in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; forforum supergroups only.

        :param text: Text of the message to be sent, 1-4096 characters after entities parsing.
        :param parse_mode: Mode for parsing entities in the message text. See formatting options formore details.

        :param entities: A JSON-serialized list of special entities that appear in message text,which can be specified instead of parse_mode.

        :param link_preview_options: Link preview generation options for the message.

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcastinglimits for a fee of 0.1 Telegram Stars per message. The relevant Stars willbe withdrawn from the bot's balance.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for privatechats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inlinekeyboard, custom reply keyboard, instructions to remove a reply keyboardor to force a reply from the user."""
        ...

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
        params = compose_method_params(
            params=get_params(locals()),
            update=self,
            default_params={"chat_id", "message_id", "message_thread_id"},
            validators={"message_thread_id": lambda x: x.is_topic_message.unwrap_or(False)},
        )
        return await self.ctx_api.delete_message(**params)

    @shortcut(
        "edit_message_text",
        executor=execute_method_edit,
        custom_params={"link_preview_options", "message_thread_id", "message_id"},
    )
    async def edit(
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
        "copy_message",
        custom_params={"message_thread_id", "chat_id", "message_id", "from_chat_id"},
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
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
        reply_parameters: ReplyParameters | None = None,
        show_caption_above_media: bool | None = None,
        **other: typing.Any,
    ) -> Result[MessageId, APIError]:
        """Shortcut `API.copy_message()`, see the [documentation](https://core.telegram.org/bots/api#copymessage)

        Use this method to copy messages of any kind. Service messages, paid media
        messages, giveaway messages, giveaway winners messages, and invoice
        messages can't be copied. A quiz poll can be copied only if the value of the
        field correct_option_id is known to the bot. The method is analogous to
        the method forwardMessage, but the copied message doesn't have a link to
        the original message. Returns the MessageId of the sent message on success."""
        params = compose_method_params(
            params=get_params(locals()),
            update=self,
            default_params={
                "chat_id",
                "message_id",
                ("from_chat_id", "chat_id"),
                "message_thread_id",
            },
            validators={"message_thread_id": lambda x: x.is_topic_message.unwrap_or(False)},
        )
        if isinstance(reply_parameters, dict):
            reply_parameters.setdefault("message_id", params.get("message_id"))
            reply_parameters.setdefault("chat_id", params.get("chat_id"))
            params["reply_parameters"] = ReplyParameters(**reply_parameters)
        return await self.ctx_api.copy_message(**params)

    @shortcut(
        "set_message_reaction",
        custom_params={"message_thread_id", "reaction", "chat_id", "message_id"},
    )
    async def react(
        self,
        reaction: (str | ReactionEmoji | ReactionType | list[str | ReactionEmoji | ReactionType] | None) = None,
        *,
        chat_id: int | str | None = None,
        is_big: bool | None = None,
        message_id: int | None = None,
        message_thread_id: int | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Shortcut `API.set_message_reaction()`, see the [documentation](https://core.telegram.org/bots/api#setmessagereaction)

        Use this method to change the chosen reactions on a message. Service messages
        can't be reacted to. Automatically forwarded messages from a channel to
        its discussion group have the same available reactions as messages in the
        channel. Bots can't use paid reactions. Returns True on success."""
        params = compose_method_params(
            params=get_params(locals()),
            update=self,
            default_params={"chat_id", "message_id", "message_thread_id"},
            validators={"message_thread_id": lambda x: x.is_topic_message.unwrap_or(False)},
        )
        if reaction:
            params["reaction"] = compose_reactions(
                reaction.unwrap() if isinstance(reaction, Some) else reaction,
            )
        return await self.ctx_api.set_message_reaction(**params)

    @shortcut("forward_message", custom_params={"message_thread_id", "from_chat_id", "message_id"})
    async def forward(
        self,
        chat_id: int | str,
        *,
        disable_notification: bool | None = None,
        from_chat_id: int | str | None = None,
        message_id: int | None = None,
        message_thread_id: int | None = None,
        protect_content: bool | None = None,
        **other: typing.Any,
    ) -> Result[MessageCute, APIError]:
        """Shortcut `API.forward_message()`, see the [documentation](https://core.telegram.org/bots/api#forwardmessage)

        Use this method to forward messages of any kind. Service messages and messages
        with protected content can't be forwarded. On success, the sent Message
        is returned.
        :param chat_id: Unique identifier for the target chat or username of the target channel(in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; forforum supergroups only.

        :param from_chat_id: Unique identifier for the chat where the original message was sent (or channelusername in the format @channelusername).

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the forwarded message from forwarding and saving.
        :param message_id: Message identifier in the chat specified in from_chat_id."""
        params = compose_method_params(
            params=get_params(locals()),
            update=self,
            default_params={
                ("from_chat_id", "chat_id"),
                "message_id",
                "message_thread_id",
            },
            validators={"message_thread_id": lambda x: x.is_topic_message.unwrap_or(False)},
        )
        return (await self.ctx_api.forward_message(**params)).map(
            lambda message: MessageCute.from_update(message, bound_api=self.api),
        )

    @shortcut("pin_chat_message", custom_params={"message_thread_id", "chat_id", "message_id"})
    async def pin(
        self,
        *,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        disable_notification: bool | None = None,
        message_id: int | None = None,
        message_thread_id: int | None = None,
        **other: typing.Any,
    ) -> Result[bool, "APIError"]:
        """Shortcut `API.pin_chat_message()`, see the [documentation](https://core.telegram.org/bots/api#pinchatmessage)

        Use this method to add a message to the list of pinned messages in a chat. If
        the chat is not a private chat, the bot must be an administrator in the chat
        for this to work and must have the 'can_pin_messages' administrator right
        in a supergroup or 'can_edit_messages' administrator right in a channel.
        Returns True on success.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messagewill be pinned.

        :param chat_id: Unique identifier for the target chat or username of the target channel(in the format @channelusername).

        :param message_id: Identifier of a message to pin.

        :param disable_notification: Pass True if it is not necessary to send a notification to all chat membersabout the new pinned message. Notifications are always disabled in channelsand private chats."""
        params = compose_method_params(
            params=get_params(locals()),
            update=self,
            default_params={"chat_id", "message_id", "message_thread_id"},
            validators={"message_thread_id": lambda x: x.is_topic_message.unwrap_or(False)},
        )
        return await self.ctx_api.pin_chat_message(**params)

    @shortcut("unpin_chat_message", custom_params={"message_thread_id", "chat_id", "message_id"})
    async def unpin(
        self,
        *,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        message_id: int | None = None,
        message_thread_id: int | None = None,
        **other: typing.Any,
    ) -> Result[bool, "APIError"]:
        """Shortcut `API.unpin_chat_message()`, see the [documentation](https://core.telegram.org/bots/api#unpinchatmessage)

        Use this method to remove a message from the list of pinned messages in a chat.
        If the chat is not a private chat, the bot must be an administrator in the chat
        for this to work and must have the 'can_pin_messages' administrator right
        in a supergroup or 'can_edit_messages' administrator right in a channel.
        Returns True on success.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messagewill be unpinned.

        :param chat_id: Unique identifier for the target chat or username of the target channel(in the format @channelusername).

        :param message_id: Identifier of the message to unpin. Required if business_connection_idis specified. If not specified, the most recent pinned message (by sendingdate) will be unpinned."""
        params = compose_method_params(
            params=get_params(locals()),
            update=self,
            default_params={"chat_id", "message_id", "message_thread_id"},
            validators={"message_thread_id": lambda x: x.is_topic_message.unwrap_or(False)},
        )
        return await self.ctx_api.pin_chat_message(**params)

    @shortcut(
        "send_audio",
        executor=execute_method_answer,
        custom_params={"message_thread_id", "chat_id"},
    )
    async def answer_audio(
        self,
        audio: InputFile | str,
        *,
        allow_paid_broadcast: bool | None = None,
        business_connection_id: str | None = None,
        caption: str | None = None,
        caption_entities: list[MessageEntity] | None = None,
        chat_id: int | str | None = None,
        disable_notification: bool | None = None,
        duration: int | None = None,
        message_effect_id: str | None = None,
        message_thread_id: int | None = None,
        parse_mode: str | None = None,
        performer: str | None = None,
        protect_content: bool | None = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
        reply_parameters: ReplyParameters | None = None,
        thumbnail: InputFile | str | None = None,
        title: str | None = None,
        **other: typing.Any,
    ) -> Result[MessageCute, APIError]:
        """Shortcut `API.send_audio()`, see the [documentation](https://core.telegram.org/bots/api#sendaudio)

        Use this method to send audio files, if you want Telegram clients to display
        them in the music player. Your audio must be in the .MP3 or .M4A format. On
        success, the sent Message is returned. Bots can currently send audio files
        of up to 50 MB in size, this limit may be changed in the future. For sending
        voice messages, use the sendVoice method instead.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messagewill be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel(in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; forforum supergroups only.

        :param audio: Audio file to send. Pass a file_id as String to send an audio file that existson the Telegram servers (recommended), pass an HTTP URL as a String for Telegramto get an audio file from the Internet, or upload a new one using multipart/form-data.More information on Sending Files: https://core.telegram.org/bots/api#sending-files.
        :param caption: Audio caption, 0-1024 characters after entities parsing.

        :param parse_mode: Mode for parsing entities in the audio caption. See formatting optionsfor more details.

        :param caption_entities: A JSON-serialized list of special entities that appear in the caption,which can be specified instead of parse_mode.

        :param duration: Duration of the audio in seconds.

        :param performer: Performer.

        :param title: Track name.

        :param thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for thefile is supported server-side. The thumbnail should be in JPEG format andless than 200 kB in size. A thumbnail's width and height should not exceed320. Ignored if the file is not uploaded using multipart/form-data. Thumbnailscan't be reused and can be only uploaded as a new file, so you can pass `attach://<file_attach_name>`if the thumbnail was uploaded using multipart/form-data under <file_attach_name>.More information on Sending Files: https://core.telegram.org/bots/api#sending-files.
        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcastinglimits for a fee of 0.1 Telegram Stars per message. The relevant Stars willbe withdrawn from the bot's balance.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for privatechats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inlinekeyboard, custom reply keyboard, instructions to remove a reply keyboardor to force a reply from the user."""
        ...

    @shortcut(
        "send_animation",
        executor=execute_method_answer,
        custom_params={"message_thread_id", "chat_id"},
    )
    async def answer_animation(
        self,
        animation: InputFile | str,
        *,
        allow_paid_broadcast: bool | None = None,
        business_connection_id: str | None = None,
        caption: str | None = None,
        caption_entities: list[MessageEntity] | None = None,
        chat_id: int | str | None = None,
        disable_notification: bool | None = None,
        duration: int | None = None,
        has_spoiler: bool | None = None,
        height: int | None = None,
        message_effect_id: str | None = None,
        message_thread_id: int | None = None,
        parse_mode: str | None = None,
        protect_content: bool | None = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
        reply_parameters: ReplyParameters | None = None,
        show_caption_above_media: bool | None = None,
        thumbnail: InputFile | str | None = None,
        width: int | None = None,
        **other: typing.Any,
    ) -> Result[MessageCute, APIError]:
        """Shortcut `API.send_animation()`, see the [documentation](https://core.telegram.org/bots/api#sendanimation)

        Use this method to send animation files (GIF or H.264/MPEG-4 AVC video without
        sound). On success, the sent Message is returned. Bots can currently send
        animation files of up to 50 MB in size, this limit may be changed in the future.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messagewill be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel(in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; forforum supergroups only.

        :param animation: Animation to send. Pass a file_id as String to send an animation that existson the Telegram servers (recommended), pass an HTTP URL as a String for Telegramto get an animation from the Internet, or upload a new animation using multipart/form-data.More information on Sending Files: https://core.telegram.org/bots/api#sending-files.
        :param duration: Duration of sent animation in seconds.

        :param width: Animation width.

        :param height: Animation height.

        :param thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for thefile is supported server-side. The thumbnail should be in JPEG format andless than 200 kB in size. A thumbnail's width and height should not exceed320. Ignored if the file is not uploaded using multipart/form-data. Thumbnailscan't be reused and can be only uploaded as a new file, so you can pass `attach://<file_attach_name>`if the thumbnail was uploaded using multipart/form-data under <file_attach_name>.More information on Sending Files: https://core.telegram.org/bots/api#sending-files.
        :param caption: Animation caption (may also be used when resending animation by file_id),0-1024 characters after entities parsing.

        :param parse_mode: Mode for parsing entities in the animation caption. See formatting optionsfor more details.

        :param caption_entities: A JSON-serialized list of special entities that appear in the caption,which can be specified instead of parse_mode.

        :param show_caption_above_media: Pass True, if the caption must be shown above the message media.

        :param has_spoiler: Pass True if the animation needs to be covered with a spoiler animation.
        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcastinglimits for a fee of 0.1 Telegram Stars per message. The relevant Stars willbe withdrawn from the bot's balance.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for privatechats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inlinekeyboard, custom reply keyboard, instructions to remove a reply keyboardor to force a reply from the user."""
        ...

    @shortcut(
        "send_document",
        executor=execute_method_answer,
        custom_params={"message_thread_id", "chat_id"},
    )
    async def answer_document(
        self,
        document: InputFile | str,
        *,
        allow_paid_broadcast: bool | None = None,
        business_connection_id: str | None = None,
        caption: str | None = None,
        caption_entities: list[MessageEntity] | None = None,
        chat_id: int | str | None = None,
        disable_content_type_detection: bool | None = None,
        disable_notification: bool | None = None,
        message_effect_id: str | None = None,
        message_thread_id: int | None = None,
        parse_mode: str | None = None,
        protect_content: bool | None = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
        reply_parameters: ReplyParameters | None = None,
        show_caption_above_media: bool | None = None,
        thumbnail: InputFile | str | None = None,
        **other: typing.Any,
    ) -> Result[MessageCute, APIError]:
        """Shortcut `API.send_document()`, see the [documentation](https://core.telegram.org/bots/api#senddocument)

        Use this method to send general files. On success, the sent Message is returned.
        Bots can currently send files of any type of up to 50 MB in size, this limit
        may be changed in the future.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messagewill be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel(in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; forforum supergroups only.

        :param document: File to send. Pass a file_id as String to send a file that exists on the Telegramservers (recommended), pass an HTTP URL as a String for Telegram to get afile from the Internet, or upload a new one using multipart/form-data.More information on Sending Files: https://core.telegram.org/bots/api#sending-files.
        :param thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for thefile is supported server-side. The thumbnail should be in JPEG format andless than 200 kB in size. A thumbnail's width and height should not exceed320. Ignored if the file is not uploaded using multipart/form-data. Thumbnailscan't be reused and can be only uploaded as a new file, so you can pass `attach://<file_attach_name>`if the thumbnail was uploaded using multipart/form-data under <file_attach_name>.More information on Sending Files: https://core.telegram.org/bots/api#sending-files.
        :param caption: Document caption (may also be used when resending documents by file_id),0-1024 characters after entities parsing.

        :param parse_mode: Mode for parsing entities in the document caption. See formatting optionsfor more details.

        :param caption_entities: A JSON-serialized list of special entities that appear in the caption,which can be specified instead of parse_mode.

        :param disable_content_type_detection: Disables automatic server-side content type detection for files uploadedusing multipart/form-data.

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcastinglimits for a fee of 0.1 Telegram Stars per message. The relevant Stars willbe withdrawn from the bot's balance.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for privatechats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inlinekeyboard, custom reply keyboard, instructions to remove a reply keyboardor to force a reply from the user."""
        ...

    @shortcut(
        "send_photo",
        executor=execute_method_answer,
        custom_params={"message_thread_id", "chat_id"},
    )
    async def answer_photo(
        self,
        photo: InputFile | str,
        *,
        allow_paid_broadcast: bool | None = None,
        business_connection_id: str | None = None,
        caption: str | None = None,
        caption_entities: list[MessageEntity] | None = None,
        chat_id: int | str | None = None,
        disable_notification: bool | None = None,
        has_spoiler: bool | None = None,
        message_effect_id: str | None = None,
        message_thread_id: int | None = None,
        parse_mode: str | None = None,
        protect_content: bool | None = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
        reply_parameters: ReplyParameters | None = None,
        show_caption_above_media: bool | None = None,
        **other: typing.Any,
    ) -> Result[MessageCute, APIError]:
        """Shortcut `API.send_photo()`, see the [documentation](https://core.telegram.org/bots/api#sendphoto)

        Use this method to send photos. On success, the sent Message is returned.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messagewill be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel(in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; forforum supergroups only.

        :param photo: Photo to send. Pass a file_id as String to send a photo that exists on the Telegramservers (recommended), pass an HTTP URL as a String for Telegram to get aphoto from the Internet, or upload a new photo using multipart/form-data.The photo must be at most 10 MB in size. The photo's width and height must notexceed 10000 in total. Width and height ratio must be at most 20. More informationon Sending Files: https://core.telegram.org/bots/api#sending-files.
        :param caption: Photo caption (may also be used when resending photos by file_id), 0-1024characters after entities parsing.

        :param parse_mode: Mode for parsing entities in the photo caption. See formatting optionsfor more details.

        :param caption_entities: A JSON-serialized list of special entities that appear in the caption,which can be specified instead of parse_mode.

        :param show_caption_above_media: Pass True, if the caption must be shown above the message media.

        :param has_spoiler: Pass True if the photo needs to be covered with a spoiler animation.

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcastinglimits for a fee of 0.1 Telegram Stars per message. The relevant Stars willbe withdrawn from the bot's balance.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for privatechats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inlinekeyboard, custom reply keyboard, instructions to remove a reply keyboardor to force a reply from the user."""
        ...

    @shortcut(
        "send_sticker",
        executor=execute_method_answer,
        custom_params={"message_thread_id", "chat_id"},
    )
    async def answer_sticker(
        self,
        sticker: InputFile | str,
        *,
        allow_paid_broadcast: bool | None = None,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        disable_notification: bool | None = None,
        emoji: str | None = None,
        message_effect_id: str | None = None,
        message_thread_id: int | None = None,
        protect_content: bool | None = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
        reply_parameters: ReplyParameters | None = None,
        **other: typing.Any,
    ) -> Result[MessageCute, APIError]:
        """Shortcut `API.send_sticker()`, see the [documentation](https://core.telegram.org/bots/api#sendsticker)

        Use this method to send static .WEBP, animated .TGS, or video .WEBM stickers.
        On success, the sent Message is returned.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messagewill be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel(in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; forforum supergroups only.

        :param sticker: Sticker to send. Pass a file_id as String to send a file that exists on theTelegram servers (recommended), pass an HTTP URL as a String for Telegramto get a .WEBP sticker from the Internet, or upload a new .WEBP, .TGS, or .WEBMsticker using multipart/form-data. More information on Sending Files:https://core.telegram.org/bots/api#sending-files. Video and animatedstickers can't be sent via an HTTP URL.

        :param emoji: Emoji associated with the sticker; only for just uploaded stickers.

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcastinglimits for a fee of 0.1 Telegram Stars per message. The relevant Stars willbe withdrawn from the bot's balance.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for privatechats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inlinekeyboard, custom reply keyboard, instructions to remove a reply keyboardor to force a reply from the user."""
        ...

    @shortcut(
        "send_video",
        executor=execute_method_answer,
        custom_params={"message_thread_id", "chat_id"},
    )
    async def answer_video(
        self,
        video: InputFile | str,
        *,
        allow_paid_broadcast: bool | None = None,
        business_connection_id: str | None = None,
        caption: str | None = None,
        caption_entities: list[MessageEntity] | None = None,
        chat_id: int | str | None = None,
        disable_notification: bool | None = None,
        duration: int | None = None,
        emoji: str | None = None,
        has_spoiler: bool | None = None,
        height: int | None = None,
        message_effect_id: str | None = None,
        message_thread_id: int | None = None,
        protect_content: bool | None = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
        reply_parameters: ReplyParameters | None = None,
        show_caption_above_media: bool | None = None,
        supports_streaming: bool | None = None,
        thumbnail: InputFile | str | None = None,
        width: int | None = None,
        **other: typing.Any,
    ) -> Result[MessageCute, APIError]:
        """Shortcut `API.send_video()`, see the [documentation](https://core.telegram.org/bots/api#sendvideo)

        Use this method to send video files, Telegram clients support MPEG4 videos
        (other formats may be sent as Document). On success, the sent Message is
        returned. Bots can currently send video files of up to 50 MB in size, this
        limit may be changed in the future.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messagewill be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel(in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; forforum supergroups only.

        :param video: Video to send. Pass a file_id as String to send a video that exists on the Telegramservers (recommended), pass an HTTP URL as a String for Telegram to get avideo from the Internet, or upload a new video using multipart/form-data.More information on Sending Files: https://core.telegram.org/bots/api#sending-files.
        :param duration: Duration of sent video in seconds.

        :param width: Video width.

        :param height: Video height.

        :param thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for thefile is supported server-side. The thumbnail should be in JPEG format andless than 200 kB in size. A thumbnail's width and height should not exceed320. Ignored if the file is not uploaded using multipart/form-data. Thumbnailscan't be reused and can be only uploaded as a new file, so you can pass `attach://<file_attach_name>`if the thumbnail was uploaded using multipart/form-data under <file_attach_name>.More information on Sending Files: https://core.telegram.org/bots/api#sending-files.
        :param caption: Video caption (may also be used when resending videos by file_id), 0-1024characters after entities parsing.

        :param parse_mode: Mode for parsing entities in the video caption. See formatting optionsfor more details.

        :param caption_entities: A JSON-serialized list of special entities that appear in the caption,which can be specified instead of parse_mode.

        :param show_caption_above_media: Pass True, if the caption must be shown above the message media.

        :param has_spoiler: Pass True if the video needs to be covered with a spoiler animation.

        :param supports_streaming: Pass True if the uploaded video is suitable for streaming.

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcastinglimits for a fee of 0.1 Telegram Stars per message. The relevant Stars willbe withdrawn from the bot's balance.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for privatechats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inlinekeyboard, custom reply keyboard, instructions to remove a reply keyboardor to force a reply from the user."""
        ...

    @shortcut(
        "send_video_note",
        executor=execute_method_answer,
        custom_params={"message_thread_id", "chat_id"},
    )
    async def answer_video_note(
        self,
        video_note: InputFile | str,
        *,
        allow_paid_broadcast: bool | None = None,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        disable_notification: bool | None = None,
        duration: int | None = None,
        length: int | None = None,
        message_effect_id: str | None = None,
        message_thread_id: int | None = None,
        protect_content: bool | None = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
        reply_parameters: ReplyParameters | None = None,
        thumbnail: InputFile | str | None = None,
        **other: typing.Any,
    ) -> Result[MessageCute, APIError]:
        """Shortcut `API.send_video_note()`, see the [documentation](https://core.telegram.org/bots/api#sendvideonote)

        As of v.4.0, Telegram clients support rounded square MPEG4 videos of up
        to 1 minute long. Use this method to send video messages. On success, the
        sent Message is returned.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messagewill be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel(in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; forforum supergroups only.

        :param video_note: Video note to send. Pass a file_id as String to send a video note that existson the Telegram servers (recommended) or upload a new video using multipart/form-data.More information on Sending Files: https://core.telegram.org/bots/api#sending-files.Sending video notes by a URL is currently unsupported.

        :param duration: Duration of sent video in seconds.

        :param length: Video width and height, i.e. diameter of the video message.

        :param thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for thefile is supported server-side. The thumbnail should be in JPEG format andless than 200 kB in size. A thumbnail's width and height should not exceed320. Ignored if the file is not uploaded using multipart/form-data. Thumbnailscan't be reused and can be only uploaded as a new file, so you can pass `attach://<file_attach_name>`if the thumbnail was uploaded using multipart/form-data under <file_attach_name>.More information on Sending Files: https://core.telegram.org/bots/api#sending-files.
        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcastinglimits for a fee of 0.1 Telegram Stars per message. The relevant Stars willbe withdrawn from the bot's balance.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for privatechats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inlinekeyboard, custom reply keyboard, instructions to remove a reply keyboardor to force a reply from the user."""
        ...

    @shortcut(
        "send_voice",
        executor=execute_method_answer,
        custom_params={"message_thread_id", "chat_id"},
    )
    async def answer_voice(
        self,
        voice: InputFile | str,
        *,
        allow_paid_broadcast: bool | None = None,
        business_connection_id: str | None = None,
        caption: str | None = None,
        caption_entities: list[MessageEntity] | None = None,
        chat_id: int | str | None = None,
        disable_notification: bool | None = None,
        duration: int | None = None,
        message_effect_id: str | None = None,
        message_thread_id: int | None = None,
        parse_mode: str | None = None,
        protect_content: bool | None = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
        reply_parameters: ReplyParameters | None = None,
        **other: typing.Any,
    ) -> Result[MessageCute, APIError]:
        """Shortcut `API.send_voice()`, see the [documentation](https://core.telegram.org/bots/api#sendvoice)

        Use this method to send audio files, if you want Telegram clients to display
        the file as a playable voice message. For this to work, your audio must be
        in an .OGG file encoded with OPUS, or in .MP3 format, or in .M4A format (other
        formats may be sent as Audio or Document). On success, the sent Message is
        returned. Bots can currently send voice messages of up to 50 MB in size, this
        limit may be changed in the future.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messagewill be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel(in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; forforum supergroups only.

        :param voice: Audio file to send. Pass a file_id as String to send a file that exists on theTelegram servers (recommended), pass an HTTP URL as a String for Telegramto get a file from the Internet, or upload a new one using multipart/form-data.More information on Sending Files: https://core.telegram.org/bots/api#sending-files.
        :param caption: Voice message caption, 0-1024 characters after entities parsing.

        :param parse_mode: Mode for parsing entities in the voice message caption. See formattingoptions for more details.

        :param caption_entities: A JSON-serialized list of special entities that appear in the caption,which can be specified instead of parse_mode.

        :param duration: Duration of the voice message in seconds.

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcastinglimits for a fee of 0.1 Telegram Stars per message. The relevant Stars willbe withdrawn from the bot's balance.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for privatechats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inlinekeyboard, custom reply keyboard, instructions to remove a reply keyboardor to force a reply from the user."""
        ...

    @shortcut(
        "send_poll",
        executor=execute_method_answer,
        custom_params={"message_thread_id", "chat_id"},
    )
    async def answer_poll(
        self,
        question: str,
        *,
        options: list[InputPollOption],
        allow_paid_broadcast: bool | None = None,
        allows_multiple_answers: bool | None = None,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        close_date: datetime | int | None = None,
        correct_option_id: int | None = None,
        disable_notification: bool | None = None,
        explanation: str | None = None,
        explanation_entities: list[MessageEntity] | None = None,
        explanation_parse_mode: str | None = None,
        is_anonymous: bool | None = None,
        is_closed: bool | None = None,
        message_effect_id: str | None = None,
        message_thread_id: int | None = None,
        open_period: int | None = None,
        protect_content: bool | None = None,
        question_entities: list[MessageEntity] | None = None,
        question_parse_mode: str | None = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
        reply_parameters: ReplyParameters | None = None,
        show_caption_above_media: bool | None = None,
        type: typing.Literal["quiz", "regular"] | None = None,
        **other: typing.Any,
    ) -> Result[MessageCute, APIError]:
        """Shortcut `API.send_poll()`, see the [documentation](https://core.telegram.org/bots/api#sendpoll)

        Use this method to send a native poll. On success, the sent Message is returned.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messagewill be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel(in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; forforum supergroups only.

        :param question: Poll question, 1-300 characters.

        :param question_parse_mode: Mode for parsing entities in the question. See formatting options for moredetails. Currently, only custom emoji entities are allowed.

        :param question_entities: A JSON-serialized list of special entities that appear in the poll question.It can be specified instead of question_parse_mode.

        :param options: A JSON-serialized list of 2-10 answer options.

        :param is_anonymous: True, if the poll needs to be anonymous, defaults to True.

        :param type: Poll type, `quiz` or `regular`, defaults to `regular`.

        :param allows_multiple_answers: True, if the poll allows multiple answers, ignored for polls in quiz mode,defaults to False.

        :param correct_option_id: 0-based identifier of the correct answer option, required for polls inquiz mode.

        :param explanation: Text that is shown when a user chooses an incorrect answer or taps on the lampicon in a quiz-style poll, 0-200 characters with at most 2 line feeds afterentities parsing.

        :param explanation_parse_mode: Mode for parsing entities in the explanation. See formatting options formore details.

        :param explanation_entities: A JSON-serialized list of special entities that appear in the poll explanation.It can be specified instead of explanation_parse_mode.

        :param open_period: Amount of time in seconds the poll will be active after creation, 5-600.Can't be used together with close_date.

        :param close_date: Point in time (Unix timestamp) when the poll will be automatically closed.Must be at least 5 and no more than 600 seconds in the future. Can't be usedtogether with open_period.

        :param is_closed: Pass True if the poll needs to be immediately closed. This can be useful forpoll preview.

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcastinglimits for a fee of 0.1 Telegram Stars per message. The relevant Stars willbe withdrawn from the bot's balance.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for privatechats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inlinekeyboard, custom reply keyboard, instructions to remove a reply keyboardor to force a reply from the user."""
        ...

    @shortcut(
        "send_venue",
        executor=execute_method_answer,
        custom_params={"message_thread_id", "chat_id"},
    )
    async def answer_venue(
        self,
        *,
        address: str,
        latitude: float,
        longitude: float,
        title: str,
        allow_paid_broadcast: bool | None = None,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        disable_notification: bool | None = None,
        foursquare_id: str | None = None,
        foursquare_type: str | None = None,
        google_place_id: str | None = None,
        google_place_type: str | None = None,
        message_effect_id: str | None = None,
        message_thread_id: int | None = None,
        protect_content: bool | None = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
        reply_parameters: ReplyParameters | None = None,
        **other: typing.Any,
    ) -> Result[MessageCute, APIError]:
        """Shortcut `API.send_venue()`, see the [documentation](https://core.telegram.org/bots/api#sendvenue)

        Use this method to send information about a venue. On success, the sent Message
        is returned.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messagewill be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel(in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; forforum supergroups only.

        :param latitude: Latitude of the venue.

        :param longitude: Longitude of the venue.

        :param title: Name of the venue.

        :param address: Address of the venue.

        :param foursquare_id: Foursquare identifier of the venue.

        :param foursquare_type: Foursquare type of the venue, if known. (For example, `arts_entertainment/default`,`arts_entertainment/aquarium` or `food/icecream`.).

        :param google_place_id: Google Places identifier of the venue.

        :param google_place_type: Google Places type of the venue. (See supported types.).

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcastinglimits for a fee of 0.1 Telegram Stars per message. The relevant Stars willbe withdrawn from the bot's balance.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for privatechats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inlinekeyboard, custom reply keyboard, instructions to remove a reply keyboardor to force a reply from the user."""
        ...

    @shortcut(
        "send_dice",
        executor=execute_method_answer,
        custom_params={"message_thread_id", "chat_id"},
    )
    async def answer_dice(
        self,
        emoji: DiceEmoji | None = None,
        *,
        allow_paid_broadcast: bool | None = None,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        disable_notification: bool | None = None,
        message_effect_id: str | None = None,
        message_thread_id: int | None = None,
        protect_content: bool | None = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
        reply_parameters: ReplyParameters | None = None,
        **other: typing.Any,
    ) -> Result[MessageCute, APIError]:
        """Shortcut `API.send_dice()`, see the [documentation](https://core.telegram.org/bots/api#senddice)

        Use this method to send an animated emoji that will display a random value.
        On success, the sent Message is returned.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messagewill be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel(in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; forforum supergroups only.

        :param emoji: Emoji on which the dice throw animation is based. Currently, must be oneof `🎲`, `🎯`, `🏀`, `⚽`, `🎳`, or `🎰`. Dice can have values 1-6 for `🎲`, `🎯` and`🎳`, values 1-5 for `🏀` and `⚽`, and values 1-64 for `🎰`. Defaults to `🎲`.
        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding.

        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcastinglimits for a fee of 0.1 Telegram Stars per message. The relevant Stars willbe withdrawn from the bot's balance.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for privatechats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inlinekeyboard, custom reply keyboard, instructions to remove a reply keyboardor to force a reply from the user."""
        ...

    @shortcut(
        "send_game",
        executor=execute_method_answer,
        custom_params={"message_thread_id", "chat_id"},
    )
    async def answer_game(
        self,
        game_short_name: str,
        *,
        allow_paid_broadcast: bool | None = None,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        disable_notification: bool | None = None,
        message_effect_id: str | None = None,
        message_thread_id: int | None = None,
        protect_content: bool | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
        reply_parameters: ReplyParameters | None = None,
        **other: typing.Any,
    ) -> Result[MessageCute, APIError]:
        """Shortcut `API.send_game()`, see the [documentation](https://core.telegram.org/bots/api#sendgame)

        Use this method to send a game. On success, the sent Message is returned.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messagewill be sent.

        :param chat_id: Unique identifier for the target chat.

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; forforum supergroups only.

        :param game_short_name: Short name of the game, serves as the unique identifier for the game. Setup your games via @BotFather.

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcastinglimits for a fee of 0.1 Telegram Stars per message. The relevant Stars willbe withdrawn from the bot's balance.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for privatechats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: A JSON-serialized object for an inline keyboard. If empty, one 'Play game_title'button will be shown. If not empty, the first button must launch the game."""
        ...

    @shortcut(
        "send_invoice",
        executor=execute_method_answer,
        custom_params={"message_thread_id", "chat_id"},
    )
    async def answer_invoice(
        self,
        *,
        currency: Currency,
        description: str,
        payload: str,
        prices: list[LabeledPrice],
        title: str,
        allow_paid_broadcast: bool | None = None,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        disable_notification: bool | None = None,
        is_flexible: bool | None = None,
        max_tip_amount: int | None = None,
        message_effect_id: str | None = None,
        message_thread_id: int | None = None,
        need_email: bool | None = None,
        need_name: bool | None = None,
        need_phone_number: bool | None = None,
        need_shipping_address: bool | None = None,
        photo_height: int | None = None,
        photo_size: int | None = None,
        photo_url: str | None = None,
        photo_width: int | None = None,
        protect_content: bool | None = None,
        provider_data: str | None = None,
        provider_token: str | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
        reply_parameters: ReplyParameters | None = None,
        send_email_to_provider: bool | None = None,
        send_phone_number_to_provider: bool | None = None,
        start_parameter: str | None = None,
        suggested_tip_amounts: list[int] | None = None,
        **other: typing.Any,
    ) -> Result[MessageCute, APIError]:
        """Shortcut `API.send_invoice()`, see the [documentation](https://core.telegram.org/bots/api#sendinvoice)

        Use this method to send invoices. On success, the sent Message is returned."""
        ...

    @shortcut(
        "send_chat_action",
        executor=execute_method_answer,
        custom_params={"message_thread_id", "chat_id"},
    )
    async def answer_chat_action(
        self,
        action: ChatAction,
        *,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        message_thread_id: int | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Shortcut `API.send_chat_action()`, see the [documentation](https://core.telegram.org/bots/api#sendchataction)

        Use this method when you need to tell the user that something is happening
        on the bot's side. The status is set for 5 seconds or less (when a message arrives
        from your bot, Telegram clients clear its typing status). Returns True
        on success. We only recommend using this method when a response from the
        bot will take a noticeable amount of time to arrive.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the actionwill be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel(in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread; for supergroups only.
        :param action: Type of action to broadcast. Choose one, depending on what the user is aboutto receive: typing for text messages, upload_photo for photos, record_videoor upload_video for videos, record_voice or upload_voice for voice notes,upload_document for general files, choose_sticker for stickers, find_locationfor location data, record_video_note or upload_video_note for videonotes."""
        ...

    @shortcut(
        "send_media_group",
        custom_params={"media", "chat_id", "message_thread_id"},
    )
    async def answer_media_group(
        self,
        media: InputMedia | list[InputMedia],
        *,
        allow_paid_broadcast: bool | None = None,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        disable_notification: bool | None = None,
        media_type: MediaType | None = None,
        message_effect_id: str | None = None,
        message_thread_id: int | None = None,
        protect_content: bool | None = None,
        reply_parameters: ReplyParameters | None = None,
        **other: typing.Any,
    ) -> Result[list[MessageCute], APIError]:
        """Shortcut `API.send_media_group()`, see the [documentation](https://core.telegram.org/bots/api#sendmediagroup)

        Use this method to send a group of photos, videos, documents or audios as
        an album. Documents and audio files can be only grouped in an album with messages
        of the same type. On success, an array of Messages that were sent is returned.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messagewill be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel(in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; forforum supergroups only.

        :param media: A JSON-serialized array describing messages to be sent, must include 2-10items.

        :param disable_notification: Sends messages silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent messages from forwarding and saving.
        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcastinglimits for a fee of 0.1 Telegram Stars per message. The relevant Stars willbe withdrawn from the bot's balance.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for privatechats only.

        :param reply_parameters: Description of the message to reply to."""
        media = [media] if not isinstance(media, list) else media
        params = get_params(locals())
        return await execute_method_answer(self, "send_media_group", params)

    @shortcut(
        "send_location",
        executor=execute_method_answer,
        custom_params={"message_thread_id", "chat_id"},
    )
    async def answer_location(
        self,
        *,
        latitude: float,
        longitude: float,
        allow_paid_broadcast: bool | None = None,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        disable_notification: bool | None = None,
        heading: int | None = None,
        horizontal_accuracy: float | None = None,
        live_period: int | None = None,
        message_effect_id: str | None = None,
        message_thread_id: int | None = None,
        protect_content: bool | None = None,
        proximity_alert_radius: int | None = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
        reply_parameters: ReplyParameters | None = None,
        **other: typing.Any,
    ) -> Result[MessageCute, APIError]:
        """Shortcut `API.send_location()`, see the [documentation](https://core.telegram.org/bots/api#sendlocation)

        Use this method to send point on the map. On success, the sent Message is returned.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messagewill be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel(in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; forforum supergroups only.

        :param latitude: Latitude of the location.

        :param longitude: Longitude of the location.

        :param horizontal_accuracy: The radius of uncertainty for the location, measured in meters; 0-1500.
        :param live_period: Period in seconds during which the location will be updated (see Live Locations,should be between 60 and 86400, or 0x7FFFFFFF for live locations that canbe edited indefinitely.

        :param heading: For live locations, a direction in which the user is moving, in degrees.Must be between 1 and 360 if specified.

        :param proximity_alert_radius: For live locations, a maximum distance for proximity alerts about approachinganother chat member, in meters. Must be between 1 and 100000 if specified.
        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcastinglimits for a fee of 0.1 Telegram Stars per message. The relevant Stars willbe withdrawn from the bot's balance.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for privatechats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inlinekeyboard, custom reply keyboard, instructions to remove a reply keyboardor to force a reply from the user."""
        ...

    @shortcut(
        "send_contact",
        executor=execute_method_answer,
        custom_params={"message_thread_id", "chat_id"},
    )
    async def answer_contact(
        self,
        *,
        first_name: str,
        phone_number: str,
        allow_paid_broadcast: bool | None = None,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        disable_notification: bool | None = None,
        last_name: str | None = None,
        message_effect_id: str | None = None,
        message_thread_id: int | None = None,
        protect_content: bool | None = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
        reply_parameters: ReplyParameters | None = None,
        vcard: str | None = None,
        **other: typing.Any,
    ) -> Result[MessageCute, APIError]:
        """Shortcut `API.send_contact()`, see the [documentation](https://core.telegram.org/bots/api#sendcontact)

        Use this method to send phone contacts. On success, the sent Message is returned.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messagewill be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel(in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; forforum supergroups only.

        :param phone_number: Contact's phone number.

        :param first_name: Contact's first name.

        :param last_name: Contact's last name.

        :param vcard: Additional data about the contact in the form of a vCard, 0-2048 bytes.

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcastinglimits for a fee of 0.1 Telegram Stars per message. The relevant Stars willbe withdrawn from the bot's balance.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for privatechats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inlinekeyboard, custom reply keyboard, instructions to remove a reply keyboardor to force a reply from the user."""
        ...

    @shortcut(
        "send_audio",
        executor=execute_method_reply,
        custom_params={"message_thread_id", "chat_id"},
    )
    async def reply_audio(
        self,
        audio: InputFile | str,
        *,
        allow_paid_broadcast: bool | None = None,
        business_connection_id: str | None = None,
        caption: str | None = None,
        caption_entities: list[MessageEntity] | None = None,
        chat_id: int | str | None = None,
        disable_notification: bool | None = None,
        duration: int | None = None,
        message_effect_id: str | None = None,
        message_thread_id: int | None = None,
        parse_mode: str | None = None,
        performer: str | None = None,
        protect_content: bool | None = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
        reply_parameters: ReplyParameters | None = None,
        thumbnail: InputFile | str | None = None,
        title: str | None = None,
        **other: typing.Any,
    ) -> Result[MessageCute, APIError]:
        """Shortcut `API.send_audio()`, see the [documentation](https://core.telegram.org/bots/api#sendaudio)

        Use this method to send audio files, if you want Telegram clients to display
        them in the music player. Your audio must be in the .MP3 or .M4A format. On
        success, the sent Message is returned. Bots can currently send audio files
        of up to 50 MB in size, this limit may be changed in the future. For sending
        voice messages, use the sendVoice method instead.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messagewill be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel(in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; forforum supergroups only.

        :param audio: Audio file to send. Pass a file_id as String to send an audio file that existson the Telegram servers (recommended), pass an HTTP URL as a String for Telegramto get an audio file from the Internet, or upload a new one using multipart/form-data.More information on Sending Files: https://core.telegram.org/bots/api#sending-files.
        :param caption: Audio caption, 0-1024 characters after entities parsing.

        :param parse_mode: Mode for parsing entities in the audio caption. See formatting optionsfor more details.

        :param caption_entities: A JSON-serialized list of special entities that appear in the caption,which can be specified instead of parse_mode.

        :param duration: Duration of the audio in seconds.

        :param performer: Performer.

        :param title: Track name.

        :param thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for thefile is supported server-side. The thumbnail should be in JPEG format andless than 200 kB in size. A thumbnail's width and height should not exceed320. Ignored if the file is not uploaded using multipart/form-data. Thumbnailscan't be reused and can be only uploaded as a new file, so you can pass `attach://<file_attach_name>`if the thumbnail was uploaded using multipart/form-data under <file_attach_name>.More information on Sending Files: https://core.telegram.org/bots/api#sending-files.
        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcastinglimits for a fee of 0.1 Telegram Stars per message. The relevant Stars willbe withdrawn from the bot's balance.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for privatechats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inlinekeyboard, custom reply keyboard, instructions to remove a reply keyboardor to force a reply from the user."""
        ...

    @shortcut(
        "send_animation",
        executor=execute_method_reply,
        custom_params={"message_thread_id", "chat_id"},
    )
    async def reply_animation(
        self,
        animation: InputFile | str,
        *,
        allow_paid_broadcast: bool | None = None,
        business_connection_id: str | None = None,
        caption: str | None = None,
        caption_entities: list[MessageEntity] | None = None,
        chat_id: int | str | None = None,
        disable_notification: bool | None = None,
        duration: int | None = None,
        has_spoiler: bool | None = None,
        height: int | None = None,
        message_effect_id: str | None = None,
        message_thread_id: int | None = None,
        parse_mode: str | None = None,
        protect_content: bool | None = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
        reply_parameters: ReplyParameters | None = None,
        show_caption_above_media: bool | None = None,
        thumbnail: InputFile | str | None = None,
        width: int | None = None,
        **other: typing.Any,
    ) -> Result[MessageCute, APIError]:
        """Shortcut `API.send_animation()`, see the [documentation](https://core.telegram.org/bots/api#sendanimation)

        Use this method to send animation files (GIF or H.264/MPEG-4 AVC video without
        sound). On success, the sent Message is returned. Bots can currently send
        animation files of up to 50 MB in size, this limit may be changed in the future.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messagewill be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel(in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; forforum supergroups only.

        :param animation: Animation to send. Pass a file_id as String to send an animation that existson the Telegram servers (recommended), pass an HTTP URL as a String for Telegramto get an animation from the Internet, or upload a new animation using multipart/form-data.More information on Sending Files: https://core.telegram.org/bots/api#sending-files.
        :param duration: Duration of sent animation in seconds.

        :param width: Animation width.

        :param height: Animation height.

        :param thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for thefile is supported server-side. The thumbnail should be in JPEG format andless than 200 kB in size. A thumbnail's width and height should not exceed320. Ignored if the file is not uploaded using multipart/form-data. Thumbnailscan't be reused and can be only uploaded as a new file, so you can pass `attach://<file_attach_name>`if the thumbnail was uploaded using multipart/form-data under <file_attach_name>.More information on Sending Files: https://core.telegram.org/bots/api#sending-files.
        :param caption: Animation caption (may also be used when resending animation by file_id),0-1024 characters after entities parsing.

        :param parse_mode: Mode for parsing entities in the animation caption. See formatting optionsfor more details.

        :param caption_entities: A JSON-serialized list of special entities that appear in the caption,which can be specified instead of parse_mode.

        :param show_caption_above_media: Pass True, if the caption must be shown above the message media.

        :param has_spoiler: Pass True if the animation needs to be covered with a spoiler animation.
        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcastinglimits for a fee of 0.1 Telegram Stars per message. The relevant Stars willbe withdrawn from the bot's balance.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for privatechats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inlinekeyboard, custom reply keyboard, instructions to remove a reply keyboardor to force a reply from the user."""
        ...

    @shortcut(
        "send_document",
        executor=execute_method_reply,
        custom_params={"message_thread_id", "chat_id"},
    )
    async def reply_document(
        self,
        document: InputFile | str,
        *,
        allow_paid_broadcast: bool | None = None,
        business_connection_id: str | None = None,
        caption: str | None = None,
        caption_entities: list[MessageEntity] | None = None,
        chat_id: int | str | None = None,
        disable_content_type_detection: bool | None = None,
        disable_notification: bool | None = None,
        message_effect_id: str | None = None,
        message_thread_id: int | None = None,
        parse_mode: str | None = None,
        protect_content: bool | None = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
        reply_parameters: ReplyParameters | None = None,
        show_caption_above_media: bool | None = None,
        thumbnail: InputFile | str | None = None,
        **other: typing.Any,
    ) -> Result[MessageCute, APIError]:
        """Shortcut `API.send_document()`, see the [documentation](https://core.telegram.org/bots/api#senddocument)

        Use this method to send general files. On success, the sent Message is returned.
        Bots can currently send files of any type of up to 50 MB in size, this limit
        may be changed in the future.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messagewill be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel(in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; forforum supergroups only.

        :param document: File to send. Pass a file_id as String to send a file that exists on the Telegramservers (recommended), pass an HTTP URL as a String for Telegram to get afile from the Internet, or upload a new one using multipart/form-data.More information on Sending Files: https://core.telegram.org/bots/api#sending-files.
        :param thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for thefile is supported server-side. The thumbnail should be in JPEG format andless than 200 kB in size. A thumbnail's width and height should not exceed320. Ignored if the file is not uploaded using multipart/form-data. Thumbnailscan't be reused and can be only uploaded as a new file, so you can pass `attach://<file_attach_name>`if the thumbnail was uploaded using multipart/form-data under <file_attach_name>.More information on Sending Files: https://core.telegram.org/bots/api#sending-files.
        :param caption: Document caption (may also be used when resending documents by file_id),0-1024 characters after entities parsing.

        :param parse_mode: Mode for parsing entities in the document caption. See formatting optionsfor more details.

        :param caption_entities: A JSON-serialized list of special entities that appear in the caption,which can be specified instead of parse_mode.

        :param disable_content_type_detection: Disables automatic server-side content type detection for files uploadedusing multipart/form-data.

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcastinglimits for a fee of 0.1 Telegram Stars per message. The relevant Stars willbe withdrawn from the bot's balance.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for privatechats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inlinekeyboard, custom reply keyboard, instructions to remove a reply keyboardor to force a reply from the user."""
        ...

    @shortcut(
        "send_photo",
        executor=execute_method_reply,
        custom_params={"message_thread_id", "chat_id"},
    )
    async def reply_photo(
        self,
        photo: InputFile | str,
        *,
        allow_paid_broadcast: bool | None = None,
        business_connection_id: str | None = None,
        caption: str | None = None,
        caption_entities: list[MessageEntity] | None = None,
        chat_id: int | str | None = None,
        disable_notification: bool | None = None,
        has_spoiler: bool | None = None,
        message_effect_id: str | None = None,
        message_thread_id: int | None = None,
        parse_mode: str | None = None,
        protect_content: bool | None = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
        reply_parameters: ReplyParameters | None = None,
        show_caption_above_media: bool | None = None,
        **other: typing.Any,
    ) -> Result[MessageCute, APIError]:
        """Shortcut `API.send_photo()`, see the [documentation](https://core.telegram.org/bots/api#sendphoto)

        Use this method to send photos. On success, the sent Message is returned.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messagewill be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel(in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; forforum supergroups only.

        :param photo: Photo to send. Pass a file_id as String to send a photo that exists on the Telegramservers (recommended), pass an HTTP URL as a String for Telegram to get aphoto from the Internet, or upload a new photo using multipart/form-data.The photo must be at most 10 MB in size. The photo's width and height must notexceed 10000 in total. Width and height ratio must be at most 20. More informationon Sending Files: https://core.telegram.org/bots/api#sending-files.
        :param caption: Photo caption (may also be used when resending photos by file_id), 0-1024characters after entities parsing.

        :param parse_mode: Mode for parsing entities in the photo caption. See formatting optionsfor more details.

        :param caption_entities: A JSON-serialized list of special entities that appear in the caption,which can be specified instead of parse_mode.

        :param show_caption_above_media: Pass True, if the caption must be shown above the message media.

        :param has_spoiler: Pass True if the photo needs to be covered with a spoiler animation.

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcastinglimits for a fee of 0.1 Telegram Stars per message. The relevant Stars willbe withdrawn from the bot's balance.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for privatechats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inlinekeyboard, custom reply keyboard, instructions to remove a reply keyboardor to force a reply from the user."""
        ...

    @shortcut(
        "send_sticker",
        executor=execute_method_reply,
        custom_params={"message_thread_id", "chat_id"},
    )
    async def reply_sticker(
        self,
        sticker: InputFile | str,
        *,
        allow_paid_broadcast: bool | None = None,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        disable_notification: bool | None = None,
        emoji: str | None = None,
        message_effect_id: str | None = None,
        message_thread_id: int | None = None,
        protect_content: bool | None = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
        reply_parameters: ReplyParameters | None = None,
        **other: typing.Any,
    ) -> Result[MessageCute, APIError]:
        """Shortcut `API.send_sticker()`, see the [documentation](https://core.telegram.org/bots/api#sendsticker)

        Use this method to send static .WEBP, animated .TGS, or video .WEBM stickers.
        On success, the sent Message is returned.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messagewill be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel(in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; forforum supergroups only.

        :param sticker: Sticker to send. Pass a file_id as String to send a file that exists on theTelegram servers (recommended), pass an HTTP URL as a String for Telegramto get a .WEBP sticker from the Internet, or upload a new .WEBP, .TGS, or .WEBMsticker using multipart/form-data. More information on Sending Files:https://core.telegram.org/bots/api#sending-files. Video and animatedstickers can't be sent via an HTTP URL.

        :param emoji: Emoji associated with the sticker; only for just uploaded stickers.

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcastinglimits for a fee of 0.1 Telegram Stars per message. The relevant Stars willbe withdrawn from the bot's balance.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for privatechats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inlinekeyboard, custom reply keyboard, instructions to remove a reply keyboardor to force a reply from the user."""
        ...

    @shortcut(
        "send_video",
        executor=execute_method_reply,
        custom_params={"message_thread_id", "chat_id"},
    )
    async def reply_video(
        self,
        video: InputFile | str,
        *,
        allow_paid_broadcast: bool | None = None,
        business_connection_id: str | None = None,
        caption: str | None = None,
        caption_entities: list[MessageEntity] | None = None,
        chat_id: int | str | None = None,
        disable_notification: bool | None = None,
        duration: int | None = None,
        emoji: str | None = None,
        has_spoiler: bool | None = None,
        height: int | None = None,
        message_effect_id: str | None = None,
        message_thread_id: int | None = None,
        protect_content: bool | None = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
        reply_parameters: ReplyParameters | None = None,
        show_caption_above_media: bool | None = None,
        supports_streaming: bool | None = None,
        thumbnail: InputFile | str | None = None,
        width: int | None = None,
        **other: typing.Any,
    ) -> Result[MessageCute, APIError]:
        """Shortcut `API.send_video()`, see the [documentation](https://core.telegram.org/bots/api#sendvideo)

        Use this method to send video files, Telegram clients support MPEG4 videos
        (other formats may be sent as Document). On success, the sent Message is
        returned. Bots can currently send video files of up to 50 MB in size, this
        limit may be changed in the future.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messagewill be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel(in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; forforum supergroups only.

        :param video: Video to send. Pass a file_id as String to send a video that exists on the Telegramservers (recommended), pass an HTTP URL as a String for Telegram to get avideo from the Internet, or upload a new video using multipart/form-data.More information on Sending Files: https://core.telegram.org/bots/api#sending-files.
        :param duration: Duration of sent video in seconds.

        :param width: Video width.

        :param height: Video height.

        :param thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for thefile is supported server-side. The thumbnail should be in JPEG format andless than 200 kB in size. A thumbnail's width and height should not exceed320. Ignored if the file is not uploaded using multipart/form-data. Thumbnailscan't be reused and can be only uploaded as a new file, so you can pass `attach://<file_attach_name>`if the thumbnail was uploaded using multipart/form-data under <file_attach_name>.More information on Sending Files: https://core.telegram.org/bots/api#sending-files.
        :param caption: Video caption (may also be used when resending videos by file_id), 0-1024characters after entities parsing.

        :param parse_mode: Mode for parsing entities in the video caption. See formatting optionsfor more details.

        :param caption_entities: A JSON-serialized list of special entities that appear in the caption,which can be specified instead of parse_mode.

        :param show_caption_above_media: Pass True, if the caption must be shown above the message media.

        :param has_spoiler: Pass True if the video needs to be covered with a spoiler animation.

        :param supports_streaming: Pass True if the uploaded video is suitable for streaming.

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcastinglimits for a fee of 0.1 Telegram Stars per message. The relevant Stars willbe withdrawn from the bot's balance.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for privatechats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inlinekeyboard, custom reply keyboard, instructions to remove a reply keyboardor to force a reply from the user."""
        ...

    @shortcut(
        "send_video_note",
        executor=execute_method_reply,
        custom_params={"message_thread_id", "chat_id"},
    )
    async def reply_video_note(
        self,
        video_note: InputFile | str,
        *,
        allow_paid_broadcast: bool | None = None,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        disable_notification: bool | None = None,
        duration: int | None = None,
        length: int | None = None,
        message_effect_id: str | None = None,
        message_thread_id: int | None = None,
        protect_content: bool | None = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
        reply_parameters: ReplyParameters | None = None,
        thumbnail: InputFile | str | None = None,
        **other: typing.Any,
    ) -> Result[MessageCute, APIError]:
        """Shortcut `API.send_video_note()`, see the [documentation](https://core.telegram.org/bots/api#sendvideonote)

        As of v.4.0, Telegram clients support rounded square MPEG4 videos of up
        to 1 minute long. Use this method to send video messages. On success, the
        sent Message is returned.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messagewill be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel(in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; forforum supergroups only.

        :param video_note: Video note to send. Pass a file_id as String to send a video note that existson the Telegram servers (recommended) or upload a new video using multipart/form-data.More information on Sending Files: https://core.telegram.org/bots/api#sending-files.Sending video notes by a URL is currently unsupported.

        :param duration: Duration of sent video in seconds.

        :param length: Video width and height, i.e. diameter of the video message.

        :param thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for thefile is supported server-side. The thumbnail should be in JPEG format andless than 200 kB in size. A thumbnail's width and height should not exceed320. Ignored if the file is not uploaded using multipart/form-data. Thumbnailscan't be reused and can be only uploaded as a new file, so you can pass `attach://<file_attach_name>`if the thumbnail was uploaded using multipart/form-data under <file_attach_name>.More information on Sending Files: https://core.telegram.org/bots/api#sending-files.
        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcastinglimits for a fee of 0.1 Telegram Stars per message. The relevant Stars willbe withdrawn from the bot's balance.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for privatechats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inlinekeyboard, custom reply keyboard, instructions to remove a reply keyboardor to force a reply from the user."""
        ...

    @shortcut(
        "send_voice",
        executor=execute_method_reply,
        custom_params={"message_thread_id", "chat_id"},
    )
    async def reply_voice(
        self,
        voice: InputFile | str,
        *,
        allow_paid_broadcast: bool | None = None,
        business_connection_id: str | None = None,
        caption: str | None = None,
        caption_entities: list[MessageEntity] | None = None,
        chat_id: int | str | None = None,
        disable_notification: bool | None = None,
        duration: int | None = None,
        message_effect_id: str | None = None,
        message_thread_id: int | None = None,
        parse_mode: str | None = None,
        protect_content: bool | None = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
        reply_parameters: ReplyParameters | None = None,
        **other: typing.Any,
    ) -> Result[MessageCute, APIError]:
        """Shortcut `API.send_voice()`, see the [documentation](https://core.telegram.org/bots/api#sendvoice)

        Use this method to send audio files, if you want Telegram clients to display
        the file as a playable voice message. For this to work, your audio must be
        in an .OGG file encoded with OPUS, or in .MP3 format, or in .M4A format (other
        formats may be sent as Audio or Document). On success, the sent Message is
        returned. Bots can currently send voice messages of up to 50 MB in size, this
        limit may be changed in the future.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messagewill be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel(in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; forforum supergroups only.

        :param voice: Audio file to send. Pass a file_id as String to send a file that exists on theTelegram servers (recommended), pass an HTTP URL as a String for Telegramto get a file from the Internet, or upload a new one using multipart/form-data.More information on Sending Files: https://core.telegram.org/bots/api#sending-files.
        :param caption: Voice message caption, 0-1024 characters after entities parsing.

        :param parse_mode: Mode for parsing entities in the voice message caption. See formattingoptions for more details.

        :param caption_entities: A JSON-serialized list of special entities that appear in the caption,which can be specified instead of parse_mode.

        :param duration: Duration of the voice message in seconds.

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcastinglimits for a fee of 0.1 Telegram Stars per message. The relevant Stars willbe withdrawn from the bot's balance.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for privatechats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inlinekeyboard, custom reply keyboard, instructions to remove a reply keyboardor to force a reply from the user."""
        ...

    @shortcut(
        "send_poll",
        executor=execute_method_reply,
        custom_params={"message_thread_id", "chat_id"},
    )
    async def reply_poll(
        self,
        question: str,
        *,
        options: list[InputPollOption],
        allow_paid_broadcast: bool | None = None,
        allows_multiple_answers: bool | None = None,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        close_date: datetime | int | None = None,
        correct_option_id: int | None = None,
        disable_notification: bool | None = None,
        explanation: str | None = None,
        explanation_entities: list[MessageEntity] | None = None,
        explanation_parse_mode: str | None = None,
        is_anonymous: bool | None = None,
        is_closed: bool | None = None,
        message_effect_id: str | None = None,
        message_thread_id: int | None = None,
        open_period: int | None = None,
        protect_content: bool | None = None,
        question_entities: list[MessageEntity] | None = None,
        question_parse_mode: str | None = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
        reply_parameters: ReplyParameters | None = None,
        show_caption_above_media: bool | None = None,
        type: typing.Literal["quiz", "regular"] | None = None,
        **other: typing.Any,
    ) -> Result[MessageCute, APIError]:
        """Shortcut `API.send_poll()`, see the [documentation](https://core.telegram.org/bots/api#sendpoll)

        Use this method to send a native poll. On success, the sent Message is returned.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messagewill be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel(in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; forforum supergroups only.

        :param question: Poll question, 1-300 characters.

        :param question_parse_mode: Mode for parsing entities in the question. See formatting options for moredetails. Currently, only custom emoji entities are allowed.

        :param question_entities: A JSON-serialized list of special entities that appear in the poll question.It can be specified instead of question_parse_mode.

        :param options: A JSON-serialized list of 2-10 answer options.

        :param is_anonymous: True, if the poll needs to be anonymous, defaults to True.

        :param type: Poll type, `quiz` or `regular`, defaults to `regular`.

        :param allows_multiple_answers: True, if the poll allows multiple answers, ignored for polls in quiz mode,defaults to False.

        :param correct_option_id: 0-based identifier of the correct answer option, required for polls inquiz mode.

        :param explanation: Text that is shown when a user chooses an incorrect answer or taps on the lampicon in a quiz-style poll, 0-200 characters with at most 2 line feeds afterentities parsing.

        :param explanation_parse_mode: Mode for parsing entities in the explanation. See formatting options formore details.

        :param explanation_entities: A JSON-serialized list of special entities that appear in the poll explanation.It can be specified instead of explanation_parse_mode.

        :param open_period: Amount of time in seconds the poll will be active after creation, 5-600.Can't be used together with close_date.

        :param close_date: Point in time (Unix timestamp) when the poll will be automatically closed.Must be at least 5 and no more than 600 seconds in the future. Can't be usedtogether with open_period.

        :param is_closed: Pass True if the poll needs to be immediately closed. This can be useful forpoll preview.

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcastinglimits for a fee of 0.1 Telegram Stars per message. The relevant Stars willbe withdrawn from the bot's balance.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for privatechats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inlinekeyboard, custom reply keyboard, instructions to remove a reply keyboardor to force a reply from the user."""
        ...

    @shortcut(
        "send_venue",
        executor=execute_method_reply,
        custom_params={"message_thread_id", "chat_id"},
    )
    async def reply_venue(
        self,
        *,
        address: str,
        latitude: float,
        longitude: float,
        title: str,
        allow_paid_broadcast: bool | None = None,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        disable_notification: bool | None = None,
        foursquare_id: str | None = None,
        foursquare_type: str | None = None,
        google_place_id: str | None = None,
        google_place_type: str | None = None,
        message_effect_id: str | None = None,
        message_thread_id: int | None = None,
        protect_content: bool | None = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
        reply_parameters: ReplyParameters | None = None,
        **other: typing.Any,
    ) -> Result[MessageCute, APIError]:
        """Shortcut `API.send_venue()`, see the [documentation](https://core.telegram.org/bots/api#sendvenue)

        Use this method to send information about a venue. On success, the sent Message
        is returned.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messagewill be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel(in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; forforum supergroups only.

        :param latitude: Latitude of the venue.

        :param longitude: Longitude of the venue.

        :param title: Name of the venue.

        :param address: Address of the venue.

        :param foursquare_id: Foursquare identifier of the venue.

        :param foursquare_type: Foursquare type of the venue, if known. (For example, `arts_entertainment/default`,`arts_entertainment/aquarium` or `food/icecream`.).

        :param google_place_id: Google Places identifier of the venue.

        :param google_place_type: Google Places type of the venue. (See supported types.).

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcastinglimits for a fee of 0.1 Telegram Stars per message. The relevant Stars willbe withdrawn from the bot's balance.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for privatechats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inlinekeyboard, custom reply keyboard, instructions to remove a reply keyboardor to force a reply from the user."""
        ...

    @shortcut(
        "send_dice",
        executor=execute_method_reply,
        custom_params={"message_thread_id", "chat_id"},
    )
    async def reply_dice(
        self,
        emoji: DiceEmoji | None = None,
        *,
        allow_paid_broadcast: bool | None = None,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        disable_notification: bool | None = None,
        message_effect_id: str | None = None,
        message_thread_id: int | None = None,
        protect_content: bool | None = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
        reply_parameters: ReplyParameters | None = None,
        **other: typing.Any,
    ) -> Result[MessageCute, APIError]:
        """Shortcut `API.send_dice()`, see the [documentation](https://core.telegram.org/bots/api#senddice)

        Use this method to send an animated emoji that will display a random value.
        On success, the sent Message is returned.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messagewill be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel(in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; forforum supergroups only.

        :param emoji: Emoji on which the dice throw animation is based. Currently, must be oneof `🎲`, `🎯`, `🏀`, `⚽`, `🎳`, or `🎰`. Dice can have values 1-6 for `🎲`, `🎯` and`🎳`, values 1-5 for `🏀` and `⚽`, and values 1-64 for `🎰`. Defaults to `🎲`.
        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding.

        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcastinglimits for a fee of 0.1 Telegram Stars per message. The relevant Stars willbe withdrawn from the bot's balance.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for privatechats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inlinekeyboard, custom reply keyboard, instructions to remove a reply keyboardor to force a reply from the user."""
        ...

    @shortcut(
        "send_game",
        executor=execute_method_reply,
        custom_params={"message_thread_id", "chat_id"},
    )
    async def reply_game(
        self,
        game_short_name: str,
        *,
        allow_paid_broadcast: bool | None = None,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        disable_notification: bool | None = None,
        message_effect_id: str | None = None,
        message_thread_id: int | None = None,
        protect_content: bool | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
        reply_parameters: ReplyParameters | None = None,
        **other: typing.Any,
    ) -> Result[MessageCute, APIError]:
        """Shortcut `API.send_game()`, see the [documentation](https://core.telegram.org/bots/api#sendgame)

        Use this method to send a game. On success, the sent Message is returned.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messagewill be sent.

        :param chat_id: Unique identifier for the target chat.

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; forforum supergroups only.

        :param game_short_name: Short name of the game, serves as the unique identifier for the game. Setup your games via @BotFather.

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcastinglimits for a fee of 0.1 Telegram Stars per message. The relevant Stars willbe withdrawn from the bot's balance.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for privatechats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: A JSON-serialized object for an inline keyboard. If empty, one 'Play game_title'button will be shown. If not empty, the first button must launch the game."""
        ...

    @shortcut(
        "send_invoice",
        executor=execute_method_reply,
        custom_params={"message_thread_id", "chat_id"},
    )
    async def reply_invoice(
        self,
        *,
        currency: Currency,
        description: str,
        payload: str,
        prices: list[LabeledPrice],
        title: str,
        allow_paid_broadcast: bool | None = None,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        disable_notification: bool | None = None,
        is_flexible: bool | None = None,
        max_tip_amount: int | None = None,
        message_effect_id: str | None = None,
        message_thread_id: int | None = None,
        need_email: bool | None = None,
        need_name: bool | None = None,
        need_phone_number: bool | None = None,
        need_shipping_address: bool | None = None,
        photo_height: int | None = None,
        photo_size: int | None = None,
        photo_url: str | None = None,
        photo_width: int | None = None,
        protect_content: bool | None = None,
        provider_data: str | None = None,
        provider_token: str | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
        reply_parameters: ReplyParameters | None = None,
        send_email_to_provider: bool | None = None,
        send_phone_number_to_provider: bool | None = None,
        start_parameter: str | None = None,
        suggested_tip_amounts: list[int] | None = None,
        **other: typing.Any,
    ) -> Result[MessageCute, APIError]:
        """Shortcut `API.send_invoice()`, see the [documentation](https://core.telegram.org/bots/api#sendinvoice)

        Use this method to send invoices. On success, the sent Message is returned."""
        ...

    @shortcut(
        "send_media_group",
        custom_params={
            "media",
            "chat_id",
            "message_thread_id",
        },
    )
    async def reply_media_group(
        self,
        media: InputMedia | list[InputMedia],
        *,
        allow_paid_broadcast: bool | None = None,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        disable_notification: bool | None = None,
        message_effect_id: str | None = None,
        message_thread_id: int | None = None,
        protect_content: bool | None = None,
        reply_parameters: ReplyParameters | None = None,
        **other: typing.Any,
    ) -> Result[list[MessageCute], APIError]:
        """Shortcut `API.send_media_group()`, see the [documentation](https://core.telegram.org/bots/api#sendmediagroup)

        Use this method to send a group of photos, videos, documents or audios as
        an album. Documents and audio files can be only grouped in an album with messages
        of the same type. On success, an array of Messages that were sent is returned.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messagewill be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel(in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; forforum supergroups only.

        :param media: A JSON-serialized array describing messages to be sent, must include 2-10items.

        :param disable_notification: Sends messages silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent messages from forwarding and saving.
        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcastinglimits for a fee of 0.1 Telegram Stars per message. The relevant Stars willbe withdrawn from the bot's balance.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for privatechats only.

        :param reply_parameters: Description of the message to reply to."""
        params = get_params(locals())
        params.setdefault("reply_parameters", ReplyParameters(self.message_id))
        return await self.answer_media_group(**params)

    @shortcut(
        "send_location",
        executor=execute_method_reply,
        custom_params={"message_thread_id", "chat_id"},
    )
    async def reply_location(
        self,
        *,
        latitude: float,
        longitude: float,
        allow_paid_broadcast: bool | None = None,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        disable_notification: bool | None = None,
        heading: int | None = None,
        horizontal_accuracy: float | None = None,
        live_period: int | None = None,
        message_effect_id: str | None = None,
        message_thread_id: int | None = None,
        protect_content: bool | None = None,
        proximity_alert_radius: int | None = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
        reply_parameters: ReplyParameters | None = None,
        **other: typing.Any,
    ) -> Result[MessageCute, APIError]:
        """Shortcut `API.send_location()`, see the [documentation](https://core.telegram.org/bots/api#sendlocation)

        Use this method to send point on the map. On success, the sent Message is returned.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messagewill be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel(in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; forforum supergroups only.

        :param latitude: Latitude of the location.

        :param longitude: Longitude of the location.

        :param horizontal_accuracy: The radius of uncertainty for the location, measured in meters; 0-1500.
        :param live_period: Period in seconds during which the location will be updated (see Live Locations,should be between 60 and 86400, or 0x7FFFFFFF for live locations that canbe edited indefinitely.

        :param heading: For live locations, a direction in which the user is moving, in degrees.Must be between 1 and 360 if specified.

        :param proximity_alert_radius: For live locations, a maximum distance for proximity alerts about approachinganother chat member, in meters. Must be between 1 and 100000 if specified.
        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcastinglimits for a fee of 0.1 Telegram Stars per message. The relevant Stars willbe withdrawn from the bot's balance.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for privatechats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inlinekeyboard, custom reply keyboard, instructions to remove a reply keyboardor to force a reply from the user."""
        ...

    @shortcut(
        "send_contact",
        executor=execute_method_reply,
        custom_params={"message_thread_id", "chat_id"},
    )
    async def reply_contact(
        self,
        *,
        first_name: str,
        phone_number: str,
        allow_paid_broadcast: bool | None = None,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        disable_notification: bool | None = None,
        last_name: str | None = None,
        message_effect_id: str | None = None,
        message_thread_id: int | None = None,
        protect_content: bool | None = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
        reply_parameters: ReplyParameters | None = None,
        vcard: str | None = None,
        **other: typing.Any,
    ) -> Result[MessageCute, APIError]:
        """Shortcut `API.send_contact()`, see the [documentation](https://core.telegram.org/bots/api#sendcontact)

        Use this method to send phone contacts. On success, the sent Message is returned.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messagewill be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel(in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; forforum supergroups only.

        :param phone_number: Contact's phone number.

        :param first_name: Contact's first name.

        :param last_name: Contact's last name.

        :param vcard: Additional data about the contact in the form of a vCard, 0-2048 bytes.

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcastinglimits for a fee of 0.1 Telegram Stars per message. The relevant Stars willbe withdrawn from the bot's balance.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for privatechats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inlinekeyboard, custom reply keyboard, instructions to remove a reply keyboardor to force a reply from the user."""
        ...

    @shortcut(
        "edit_message_live_location",
        executor=execute_method_edit,
        custom_params={"message_thread_id", "chat_id", "message_id"},
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
        custom_params={"message_thread_id", "chat_id", "message_id"},
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
            "chat_id",
            "message_id",
            "parse_mode",
            "caption_entities",
        },
    )
    async def edit_media(
        self,
        media: InputFile | InputMedia | str,
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
        params = get_params(locals())
        if not isinstance(media, InputMedia):
            assert type, "Parameter 'type' is required, because 'media' is a file id or an 'InputFile' object."
            params["media"] = input_media(
                params.pop("type"),
                media,
                caption=caption,
                caption_entities=caption_entities,
                parse_mode=parse_mode,
            )

        return await execute_method_edit(self, "edit_message_media", params)

    @shortcut(
        "edit_message_reply_markup",
        executor=execute_method_edit,
        custom_params={"message_thread_id", "chat_id", "message_id"},
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


__all__ = ("MessageCute",)
