import typing
from datetime import datetime

from fntypes.co import Result, Variative

from telegrinder.api.error import APIError
from telegrinder.model import full_result, get_params
from telegrinder.types.enums import *  # noqa: F403
from telegrinder.types.objects import *  # noqa: F403

if typing.TYPE_CHECKING:
    from telegrinder.api.abc import ABCAPI


class APIMethods:
    """Telegram Bot API 7.5 methods, released `June 18, 2024`."""

    def __init__(self, api: "ABCAPI") -> None:
        self.api = api

    async def get_updates(
        self,
        offset: int | None = None,
        limit: int | None = None,
        timeout: int | None = None,
        allowed_updates: list[str] | None = None,
        **other: typing.Any,
    ) -> Result[list[Update], APIError]:
        """Method `getUpdates`, see the [documentation](https://core.telegram.org/bots/api#getupdates)

        Use this method to receive incoming updates using long polling (wiki). 
        Returns an Array of Update objects.

        :param offset: Identifier of the first update to be returned. Must be greater by one than \
        the highest among the identifiers of previously received updates. By default, \
        updates starting with the earliest unconfirmed update are returned. An \
        update is considered confirmed as soon as getUpdates is called with an offset \
        higher than its update_id. The negative offset can be specified to retrieve \
        updates starting from -offset update from the end of the updates queue. \
        All previous updates will be forgotten.

        :param limit: Limits the number of updates to be retrieved. Values between 1-100 are accepted. \
        Defaults to 100.

        :param timeout: Timeout in seconds for long polling. Defaults to 0, i.e. usual short polling. \
        Should be positive, short polling should be used for testing purposes only. \

        :param allowed_updates: A JSON-serialized list of the update types you want your bot to receive. \
        For example, specify [`message`, `edited_channel_post`, `callback_query`] \
        to only receive updates of these types. See Update for a complete list of \
        available update types. Specify an empty list to receive all update types \
        except chat_member, message_reaction, and message_reaction_count \
        (default). If not specified, the previous setting will be used. Please \
        note that this parameter doesn't affect updates created before the call \
        to the getUpdates, so unwanted updates may be received for a short period \
        of time.
        """

        method_response = await self.api.request_raw(
            "getUpdates",
            get_params(locals()),
        )
        return full_result(method_response, list[Update])

    async def set_webhook(
        self,
        url: str,
        certificate: InputFile | None = None,
        ip_address: str | None = None,
        max_connections: int | None = None,
        allowed_updates: list[str] | None = None,
        drop_pending_updates: bool | None = None,
        secret_token: str | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `setWebhook`, see the [documentation](https://core.telegram.org/bots/api#setwebhook)

        Use this method to specify a URL and receive incoming updates via an outgoing 
        webhook. Whenever there is an update for the bot, we will send an HTTPS POST 
        request to the specified URL, containing a JSON-serialized Update. In 
        case of an unsuccessful request, we will give up after a reasonable amount 
        of attempts. Returns True on success. If you'd like to make sure that the 
        webhook was set by you, you can specify secret data in the parameter secret_token. 
        If specified, the request will contain a header "X-Telegram-Bot-Api-Secret-Token" 
        with the secret token as content.

        :param url: HTTPS URL to send updates to. Use an empty string to remove webhook integration. \

        :param certificate: Upload your public key certificate so that the root certificate in use can \
        be checked. See our self-signed guide for details.

        :param ip_address: The fixed IP address which will be used to send webhook requests instead \
        of the IP address resolved through DNS.

        :param max_connections: The maximum allowed number of simultaneous HTTPS connections to the webhook \
        for update delivery, 1-100. Defaults to 40. Use lower values to limit the \
        load on your bot's server, and higher values to increase your bot's throughput. \

        :param allowed_updates: A JSON-serialized list of the update types you want your bot to receive. \
        For example, specify [`message`, `edited_channel_post`, `callback_query`] \
        to only receive updates of these types. See Update for a complete list of \
        available update types. Specify an empty list to receive all update types \
        except chat_member, message_reaction, and message_reaction_count \
        (default). If not specified, the previous setting will be used. Please \
        note that this parameter doesn't affect updates created before the call \
        to the setWebhook, so unwanted updates may be received for a short period \
        of time.

        :param drop_pending_updates: Pass True to drop all pending updates.

        :param secret_token: A secret token to be sent in a header `X-Telegram-Bot-Api-Secret-Token` \
        in every webhook request, 1-256 characters. Only characters A-Z, a-z, \
        0-9, _ and - are allowed. The header is useful to ensure that the request comes \
        from a webhook set by you.
        """

        method_response = await self.api.request_raw(
            "setWebhook",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def delete_webhook(
        self,
        drop_pending_updates: bool | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `deleteWebhook`, see the [documentation](https://core.telegram.org/bots/api#deletewebhook)

        Use this method to remove webhook integration if you decide to switch back
        to getUpdates. Returns True on success.

        :param drop_pending_updates: Pass True to drop all pending updates.
        """

        method_response = await self.api.request_raw(
            "deleteWebhook",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def get_webhook_info(self, **other: typing.Any) -> Result[WebhookInfo, APIError]:
        """Method `getWebhookInfo`, see the [documentation](https://core.telegram.org/bots/api#getwebhookinfo)

        Use this method to get current webhook status. Requires no parameters.
        On success, returns a WebhookInfo object. If the bot is using getUpdates,
        will return an object with the url field empty.
        """

        method_response = await self.api.request_raw(
            "getWebhookInfo",
            get_params(locals()),
        )
        return full_result(method_response, WebhookInfo)

    async def get_me(self, **other: typing.Any) -> Result[User, APIError]:
        """Method `getMe`, see the [documentation](https://core.telegram.org/bots/api#getme)

        A simple method for testing your bot's authentication token. Requires
        no parameters. Returns basic information about the bot in form of a User
        object.
        """

        method_response = await self.api.request_raw(
            "getMe",
            get_params(locals()),
        )
        return full_result(method_response, User)

    async def log_out(self, **other: typing.Any) -> Result[bool, APIError]:
        """Method `logOut`, see the [documentation](https://core.telegram.org/bots/api#logout)

        Use this method to log out from the cloud Bot API server before launching
        the bot locally. You must log out the bot before running it locally, otherwise
        there is no guarantee that the bot will receive updates. After a successful
        call, you can immediately log in on a local server, but will not be able to
        log in back to the cloud Bot API server for 10 minutes. Returns True on success.
        Requires no parameters.
        """

        method_response = await self.api.request_raw(
            "logOut",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def close(self, **other: typing.Any) -> Result[bool, APIError]:
        """Method `close`, see the [documentation](https://core.telegram.org/bots/api#close)

        Use this method to close the bot instance before moving it from one local
        server to another. You need to delete the webhook before calling this method
        to ensure that the bot isn't launched again after server restart. The method
        will return error 429 in the first 10 minutes after the bot is launched. Returns
        True on success. Requires no parameters.
        """

        method_response = await self.api.request_raw(
            "close",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def send_message(
        self,
        chat_id: int | str,
        text: str,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        parse_mode: str | None = None,
        entities: list[MessageEntity] | None = None,
        link_preview_options: LinkPreviewOptions | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
        **other: typing.Any,
    ) -> Result[Message, APIError]:
        """Method `sendMessage`, see the [documentation](https://core.telegram.org/bots/api#sendmessage)

        Use this method to send text messages. On success, the sent Message is returned.

        :param business_connection_id: Unique identifier of the business connection on behalf of which the message \
        will be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for \
        forum supergroups only.

        :param text: Text of the message to be sent, 1-4096 characters after entities parsing. \

        :param parse_mode: Mode for parsing entities in the message text. See formatting options for \
        more details.

        :param entities: A JSON-serialized list of special entities that appear in message text, \
        which can be specified instead of parse_mode.

        :param link_preview_options: Link preview generation options for the message.

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound. \

        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for private \
        chats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inline \
        keyboard, custom reply keyboard, instructions to remove a reply keyboard \
        or to force a reply from the user.
        """

        method_response = await self.api.request_raw(
            "sendMessage",
            get_params(locals()),
        )
        return full_result(method_response, Message)

    async def forward_message(
        self,
        chat_id: int | str,
        from_chat_id: int | str,
        message_id: int,
        message_thread_id: int | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        **other: typing.Any,
    ) -> Result[Message, APIError]:
        """Method `forwardMessage`, see the [documentation](https://core.telegram.org/bots/api#forwardmessage)

        Use this method to forward messages of any kind. Service messages and messages 
        with protected content can't be forwarded. On success, the sent Message 
        is returned.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for \
        forum supergroups only.

        :param from_chat_id: Unique identifier for the chat where the original message was sent (or channel \
        username in the format @channelusername).

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound. \

        :param protect_content: Protects the contents of the forwarded message from forwarding and saving. \

        :param message_id: Message identifier in the chat specified in from_chat_id.
        """

        method_response = await self.api.request_raw(
            "forwardMessage",
            get_params(locals()),
        )
        return full_result(method_response, Message)

    async def forward_messages(
        self,
        chat_id: int | str,
        from_chat_id: int | str,
        message_ids: list[int],
        message_thread_id: int | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        **other: typing.Any,
    ) -> Result[list[MessageId], APIError]:
        """Method `forwardMessages`, see the [documentation](https://core.telegram.org/bots/api#forwardmessages)

        Use this method to forward multiple messages of any kind. If some of the specified 
        messages can't be found or forwarded, they are skipped. Service messages 
        and messages with protected content can't be forwarded. Album grouping 
        is kept for forwarded messages. On success, an array of MessageId of the 
        sent messages is returned.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for \
        forum supergroups only.

        :param from_chat_id: Unique identifier for the chat where the original messages were sent (or \
        channel username in the format @channelusername).

        :param message_ids: A JSON-serialized list of 1-100 identifiers of messages in the chat from_chat_id \
        to forward. The identifiers must be specified in a strictly increasing \
        order.

        :param disable_notification: Sends the messages silently. Users will receive a notification with no \
        sound.

        :param protect_content: Protects the contents of the forwarded messages from forwarding and saving. \
        """

        method_response = await self.api.request_raw(
            "forwardMessages",
            get_params(locals()),
        )
        return full_result(method_response, list[MessageId])

    async def copy_message(
        self,
        chat_id: int | str,
        from_chat_id: int | str,
        message_id: int,
        message_thread_id: int | None = None,
        caption: str | None = None,
        parse_mode: str | None = None,
        caption_entities: list[MessageEntity] | None = None,
        show_caption_above_media: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
        **other: typing.Any,
    ) -> Result[MessageId, APIError]:
        """Method `copyMessage`, see the [documentation](https://core.telegram.org/bots/api#copymessage)

        Use this method to copy messages of any kind. Service messages, giveaway 
        messages, giveaway winners messages, and invoice messages can't be copied. 
        A quiz poll can be copied only if the value of the field correct_option_id 
        is known to the bot. The method is analogous to the method forwardMessage, 
        but the copied message doesn't have a link to the original message. Returns 
        the MessageId of the sent message on success.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for \
        forum supergroups only.

        :param from_chat_id: Unique identifier for the chat where the original message was sent (or channel \
        username in the format @channelusername).

        :param message_id: Message identifier in the chat specified in from_chat_id.

        :param caption: New caption for media, 0-1024 characters after entities parsing. If not \
        specified, the original caption is kept.

        :param parse_mode: Mode for parsing entities in the new caption. See formatting options for \
        more details.

        :param caption_entities: A JSON-serialized list of special entities that appear in the new caption, \
        which can be specified instead of parse_mode.

        :param show_caption_above_media: Pass True, if the caption must be shown above the message media. Ignored \
        if a new caption isn't specified.

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound. \

        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inline \
        keyboard, custom reply keyboard, instructions to remove a reply keyboard \
        or to force a reply from the user.
        """

        method_response = await self.api.request_raw(
            "copyMessage",
            get_params(locals()),
        )
        return full_result(method_response, MessageId)

    async def copy_messages(
        self,
        chat_id: int | str,
        from_chat_id: int | str,
        message_ids: list[int],
        message_thread_id: int | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        remove_caption: bool | None = None,
        **other: typing.Any,
    ) -> Result[list[MessageId], APIError]:
        """Method `copyMessages`, see the [documentation](https://core.telegram.org/bots/api#copymessages)

        Use this method to copy messages of any kind. If some of the specified messages 
        can't be found or copied, they are skipped. Service messages, giveaway 
        messages, giveaway winners messages, and invoice messages can't be copied. 
        A quiz poll can be copied only if the value of the field correct_option_id 
        is known to the bot. The method is analogous to the method forwardMessages, 
        but the copied messages don't have a link to the original message. Album 
        grouping is kept for copied messages. On success, an array of MessageId 
        of the sent messages is returned.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for \
        forum supergroups only.

        :param from_chat_id: Unique identifier for the chat where the original messages were sent (or \
        channel username in the format @channelusername).

        :param message_ids: A JSON-serialized list of 1-100 identifiers of messages in the chat from_chat_id \
        to copy. The identifiers must be specified in a strictly increasing order. \

        :param disable_notification: Sends the messages silently. Users will receive a notification with no \
        sound.

        :param protect_content: Protects the contents of the sent messages from forwarding and saving. \

        :param remove_caption: Pass True to copy the messages without their captions.
        """

        method_response = await self.api.request_raw(
            "copyMessages",
            get_params(locals()),
        )
        return full_result(method_response, list[MessageId])

    async def send_photo(
        self,
        chat_id: int | str,
        photo: InputFile | str,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        caption: str | None = None,
        parse_mode: str | None = None,
        caption_entities: list[MessageEntity] | None = None,
        show_caption_above_media: bool | None = None,
        has_spoiler: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
        **other: typing.Any,
    ) -> Result[Message, APIError]:
        """Method `sendPhoto`, see the [documentation](https://core.telegram.org/bots/api#sendphoto)

        Use this method to send photos. On success, the sent Message is returned.

        :param business_connection_id: Unique identifier of the business connection on behalf of which the message \
        will be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for \
        forum supergroups only.

        :param photo: Photo to send. Pass a file_id as String to send a photo that exists on the Telegram \
        servers (recommended), pass an HTTP URL as a String for Telegram to get a \
        photo from the Internet, or upload a new photo using multipart/form-data. \
        The photo must be at most 10 MB in size. The photo's width and height must not \
        exceed 10000 in total. Width and height ratio must be at most 20. More information \
        on Sending Files: https://core.telegram.org/bots/api#sending-files. \

        :param caption: Photo caption (may also be used when resending photos by file_id), 0-1024 \
        characters after entities parsing.

        :param parse_mode: Mode for parsing entities in the photo caption. See formatting options \
        for more details.

        :param caption_entities: A JSON-serialized list of special entities that appear in the caption, \
        which can be specified instead of parse_mode.

        :param show_caption_above_media: Pass True, if the caption must be shown above the message media.

        :param has_spoiler: Pass True if the photo needs to be covered with a spoiler animation.

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound. \

        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for private \
        chats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inline \
        keyboard, custom reply keyboard, instructions to remove a reply keyboard \
        or to force a reply from the user.
        """

        method_response = await self.api.request_raw(
            "sendPhoto",
            get_params(locals()),
        )
        return full_result(method_response, Message)

    async def send_audio(
        self,
        chat_id: int | str,
        audio: InputFile | str,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        caption: str | None = None,
        parse_mode: str | None = None,
        caption_entities: list[MessageEntity] | None = None,
        duration: int | None = None,
        performer: str | None = None,
        title: str | None = None,
        thumbnail: InputFile | str | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
        **other: typing.Any,
    ) -> Result[Message, APIError]:
        """Method `sendAudio`, see the [documentation](https://core.telegram.org/bots/api#sendaudio)

        Use this method to send audio files, if you want Telegram clients to display 
        them in the music player. Your audio must be in the .MP3 or .M4A format. On 
        success, the sent Message is returned. Bots can currently send audio files 
        of up to 50 MB in size, this limit may be changed in the future. For sending 
        voice messages, use the sendVoice method instead.

        :param business_connection_id: Unique identifier of the business connection on behalf of which the message \
        will be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for \
        forum supergroups only.

        :param audio: Audio file to send. Pass a file_id as String to send an audio file that exists \
        on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram \
        to get an audio file from the Internet, or upload a new one using multipart/form-data. \
        More information on Sending Files: https://core.telegram.org/bots/api#sending-files. \

        :param caption: Audio caption, 0-1024 characters after entities parsing.

        :param parse_mode: Mode for parsing entities in the audio caption. See formatting options \
        for more details.

        :param caption_entities: A JSON-serialized list of special entities that appear in the caption, \
        which can be specified instead of parse_mode.

        :param duration: Duration of the audio in seconds.

        :param performer: Performer.

        :param title: Track name.

        :param thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for the \
        file is supported server-side. The thumbnail should be in JPEG format and \
        less than 200 kB in size. A thumbnail's width and height should not exceed \
        320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails \
        can't be reused and can be only uploaded as a new file, so you can pass `attach://<file_attach_name>` \
        if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. \
        More information on Sending Files: https://core.telegram.org/bots/api#sending-files. \

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound. \

        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for private \
        chats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inline \
        keyboard, custom reply keyboard, instructions to remove a reply keyboard \
        or to force a reply from the user.
        """

        method_response = await self.api.request_raw(
            "sendAudio",
            get_params(locals()),
        )
        return full_result(method_response, Message)

    async def send_document(
        self,
        chat_id: int | str,
        document: InputFile | str,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        thumbnail: InputFile | str | None = None,
        caption: str | None = None,
        parse_mode: str | None = None,
        caption_entities: list[MessageEntity] | None = None,
        disable_content_type_detection: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
        **other: typing.Any,
    ) -> Result[Message, APIError]:
        """Method `sendDocument`, see the [documentation](https://core.telegram.org/bots/api#senddocument)

        Use this method to send general files. On success, the sent Message is returned. 
        Bots can currently send files of any type of up to 50 MB in size, this limit 
        may be changed in the future.

        :param business_connection_id: Unique identifier of the business connection on behalf of which the message \
        will be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for \
        forum supergroups only.

        :param document: File to send. Pass a file_id as String to send a file that exists on the Telegram \
        servers (recommended), pass an HTTP URL as a String for Telegram to get a \
        file from the Internet, or upload a new one using multipart/form-data. \
        More information on Sending Files: https://core.telegram.org/bots/api#sending-files. \

        :param thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for the \
        file is supported server-side. The thumbnail should be in JPEG format and \
        less than 200 kB in size. A thumbnail's width and height should not exceed \
        320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails \
        can't be reused and can be only uploaded as a new file, so you can pass `attach://<file_attach_name>` \
        if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. \
        More information on Sending Files: https://core.telegram.org/bots/api#sending-files. \

        :param caption: Document caption (may also be used when resending documents by file_id), \
        0-1024 characters after entities parsing.

        :param parse_mode: Mode for parsing entities in the document caption. See formatting options \
        for more details.

        :param caption_entities: A JSON-serialized list of special entities that appear in the caption, \
        which can be specified instead of parse_mode.

        :param disable_content_type_detection: Disables automatic server-side content type detection for files uploaded \
        using multipart/form-data.

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound. \

        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for private \
        chats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inline \
        keyboard, custom reply keyboard, instructions to remove a reply keyboard \
        or to force a reply from the user.
        """

        method_response = await self.api.request_raw(
            "sendDocument",
            get_params(locals()),
        )
        return full_result(method_response, Message)

    async def send_video(
        self,
        chat_id: int | str,
        video: InputFile | str,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        duration: int | None = None,
        width: int | None = None,
        height: int | None = None,
        thumbnail: InputFile | str | None = None,
        caption: str | None = None,
        parse_mode: str | None = None,
        caption_entities: list[MessageEntity] | None = None,
        show_caption_above_media: bool | None = None,
        has_spoiler: bool | None = None,
        supports_streaming: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
        **other: typing.Any,
    ) -> Result[Message, APIError]:
        """Method `sendVideo`, see the [documentation](https://core.telegram.org/bots/api#sendvideo)

        Use this method to send video files, Telegram clients support MPEG4 videos 
        (other formats may be sent as Document). On success, the sent Message is 
        returned. Bots can currently send video files of up to 50 MB in size, this 
        limit may be changed in the future.

        :param business_connection_id: Unique identifier of the business connection on behalf of which the message \
        will be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for \
        forum supergroups only.

        :param video: Video to send. Pass a file_id as String to send a video that exists on the Telegram \
        servers (recommended), pass an HTTP URL as a String for Telegram to get a \
        video from the Internet, or upload a new video using multipart/form-data. \
        More information on Sending Files: https://core.telegram.org/bots/api#sending-files. \

        :param duration: Duration of sent video in seconds.

        :param width: Video width.

        :param height: Video height.

        :param thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for the \
        file is supported server-side. The thumbnail should be in JPEG format and \
        less than 200 kB in size. A thumbnail's width and height should not exceed \
        320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails \
        can't be reused and can be only uploaded as a new file, so you can pass `attach://<file_attach_name>` \
        if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. \
        More information on Sending Files: https://core.telegram.org/bots/api#sending-files. \

        :param caption: Video caption (may also be used when resending videos by file_id), 0-1024 \
        characters after entities parsing.

        :param parse_mode: Mode for parsing entities in the video caption. See formatting options \
        for more details.

        :param caption_entities: A JSON-serialized list of special entities that appear in the caption, \
        which can be specified instead of parse_mode.

        :param show_caption_above_media: Pass True, if the caption must be shown above the message media.

        :param has_spoiler: Pass True if the video needs to be covered with a spoiler animation.

        :param supports_streaming: Pass True if the uploaded video is suitable for streaming.

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound. \

        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for private \
        chats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inline \
        keyboard, custom reply keyboard, instructions to remove a reply keyboard \
        or to force a reply from the user.
        """

        method_response = await self.api.request_raw(
            "sendVideo",
            get_params(locals()),
        )
        return full_result(method_response, Message)

    async def send_animation(
        self,
        chat_id: int | str,
        animation: InputFile | str,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        duration: int | None = None,
        width: int | None = None,
        height: int | None = None,
        thumbnail: InputFile | str | None = None,
        caption: str | None = None,
        parse_mode: str | None = None,
        caption_entities: list[MessageEntity] | None = None,
        show_caption_above_media: bool | None = None,
        has_spoiler: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
        **other: typing.Any,
    ) -> Result[Message, APIError]:
        """Method `sendAnimation`, see the [documentation](https://core.telegram.org/bots/api#sendanimation)

        Use this method to send animation files (GIF or H.264/MPEG-4 AVC video without 
        sound). On success, the sent Message is returned. Bots can currently send 
        animation files of up to 50 MB in size, this limit may be changed in the future.

        :param business_connection_id: Unique identifier of the business connection on behalf of which the message \
        will be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for \
        forum supergroups only.

        :param animation: Animation to send. Pass a file_id as String to send an animation that exists \
        on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram \
        to get an animation from the Internet, or upload a new animation using multipart/form-data. \
        More information on Sending Files: https://core.telegram.org/bots/api#sending-files. \

        :param duration: Duration of sent animation in seconds.

        :param width: Animation width.

        :param height: Animation height.

        :param thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for the \
        file is supported server-side. The thumbnail should be in JPEG format and \
        less than 200 kB in size. A thumbnail's width and height should not exceed \
        320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails \
        can't be reused and can be only uploaded as a new file, so you can pass `attach://<file_attach_name>` \
        if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. \
        More information on Sending Files: https://core.telegram.org/bots/api#sending-files. \

        :param caption: Animation caption (may also be used when resending animation by file_id), \
        0-1024 characters after entities parsing.

        :param parse_mode: Mode for parsing entities in the animation caption. See formatting options \
        for more details.

        :param caption_entities: A JSON-serialized list of special entities that appear in the caption, \
        which can be specified instead of parse_mode.

        :param show_caption_above_media: Pass True, if the caption must be shown above the message media.

        :param has_spoiler: Pass True if the animation needs to be covered with a spoiler animation. \

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound. \

        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for private \
        chats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inline \
        keyboard, custom reply keyboard, instructions to remove a reply keyboard \
        or to force a reply from the user.
        """

        method_response = await self.api.request_raw(
            "sendAnimation",
            get_params(locals()),
        )
        return full_result(method_response, Message)

    async def send_voice(
        self,
        chat_id: int | str,
        voice: InputFile | str,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        caption: str | None = None,
        parse_mode: str | None = None,
        caption_entities: list[MessageEntity] | None = None,
        duration: int | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
        **other: typing.Any,
    ) -> Result[Message, APIError]:
        """Method `sendVoice`, see the [documentation](https://core.telegram.org/bots/api#sendvoice)

        Use this method to send audio files, if you want Telegram clients to display 
        the file as a playable voice message. For this to work, your audio must be 
        in an .OGG file encoded with OPUS, or in .MP3 format, or in .M4A format (other 
        formats may be sent as Audio or Document). On success, the sent Message is 
        returned. Bots can currently send voice messages of up to 50 MB in size, this 
        limit may be changed in the future.

        :param business_connection_id: Unique identifier of the business connection on behalf of which the message \
        will be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for \
        forum supergroups only.

        :param voice: Audio file to send. Pass a file_id as String to send a file that exists on the \
        Telegram servers (recommended), pass an HTTP URL as a String for Telegram \
        to get a file from the Internet, or upload a new one using multipart/form-data. \
        More information on Sending Files: https://core.telegram.org/bots/api#sending-files. \

        :param caption: Voice message caption, 0-1024 characters after entities parsing.

        :param parse_mode: Mode for parsing entities in the voice message caption. See formatting \
        options for more details.

        :param caption_entities: A JSON-serialized list of special entities that appear in the caption, \
        which can be specified instead of parse_mode.

        :param duration: Duration of the voice message in seconds.

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound. \

        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for private \
        chats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inline \
        keyboard, custom reply keyboard, instructions to remove a reply keyboard \
        or to force a reply from the user.
        """

        method_response = await self.api.request_raw(
            "sendVoice",
            get_params(locals()),
        )
        return full_result(method_response, Message)

    async def send_video_note(
        self,
        chat_id: int | str,
        video_note: InputFile | str,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        duration: int | None = None,
        length: int | None = None,
        thumbnail: InputFile | str | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
        **other: typing.Any,
    ) -> Result[Message, APIError]:
        """Method `sendVideoNote`, see the [documentation](https://core.telegram.org/bots/api#sendvideonote)

        As of v.4.0, Telegram clients support rounded square MPEG4 videos of up 
        to 1 minute long. Use this method to send video messages. On success, the 
        sent Message is returned.

        :param business_connection_id: Unique identifier of the business connection on behalf of which the message \
        will be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for \
        forum supergroups only.

        :param video_note: Video note to send. Pass a file_id as String to send a video note that exists \
        on the Telegram servers (recommended) or upload a new video using multipart/form-data. \
        More information on Sending Files: https://core.telegram.org/bots/api#sending-files. \
        Sending video notes by a URL is currently unsupported.

        :param duration: Duration of sent video in seconds.

        :param length: Video width and height, i.e. diameter of the video message.

        :param thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for the \
        file is supported server-side. The thumbnail should be in JPEG format and \
        less than 200 kB in size. A thumbnail's width and height should not exceed \
        320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails \
        can't be reused and can be only uploaded as a new file, so you can pass `attach://<file_attach_name>` \
        if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. \
        More information on Sending Files: https://core.telegram.org/bots/api#sending-files. \

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound. \

        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for private \
        chats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inline \
        keyboard, custom reply keyboard, instructions to remove a reply keyboard \
        or to force a reply from the user.
        """

        method_response = await self.api.request_raw(
            "sendVideoNote",
            get_params(locals()),
        )
        return full_result(method_response, Message)

    async def send_media_group(
        self,
        chat_id: int | str,
        media: list[InputMediaAudio | InputMediaDocument | InputMediaPhoto | InputMediaVideo],
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        **other: typing.Any,
    ) -> Result[list[Message], APIError]:
        """Method `sendMediaGroup`, see the [documentation](https://core.telegram.org/bots/api#sendmediagroup)

        Use this method to send a group of photos, videos, documents or audios as 
        an album. Documents and audio files can be only grouped in an album with messages 
        of the same type. On success, an array of Messages that were sent is returned.

        :param business_connection_id: Unique identifier of the business connection on behalf of which the message \
        will be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for \
        forum supergroups only.

        :param media: A JSON-serialized array describing messages to be sent, must include 2-10 \
        items.

        :param disable_notification: Sends messages silently. Users will receive a notification with no sound. \

        :param protect_content: Protects the contents of the sent messages from forwarding and saving. \

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for private \
        chats only.

        :param reply_parameters: Description of the message to reply to.
        """

        method_response = await self.api.request_raw(
            "sendMediaGroup",
            get_params(locals()),
        )
        return full_result(method_response, list[Message])

    async def send_location(
        self,
        chat_id: int | str,
        latitude: float,
        longitude: float,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        horizontal_accuracy: float | None = None,
        live_period: int | None = None,
        heading: int | None = None,
        proximity_alert_radius: int | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
        **other: typing.Any,
    ) -> Result[Message, APIError]:
        """Method `sendLocation`, see the [documentation](https://core.telegram.org/bots/api#sendlocation)

        Use this method to send point on the map. On success, the sent Message is returned.

        :param business_connection_id: Unique identifier of the business connection on behalf of which the message \
        will be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for \
        forum supergroups only.

        :param latitude: Latitude of the location.

        :param longitude: Longitude of the location.

        :param horizontal_accuracy: The radius of uncertainty for the location, measured in meters; 0-1500. \

        :param live_period: Period in seconds during which the location will be updated (see Live Locations, \
        should be between 60 and 86400, or 0x7FFFFFFF for live locations that can \
        be edited indefinitely.

        :param heading: For live locations, a direction in which the user is moving, in degrees. \
        Must be between 1 and 360 if specified.

        :param proximity_alert_radius: For live locations, a maximum distance for proximity alerts about approaching \
        another chat member, in meters. Must be between 1 and 100000 if specified. \

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound. \

        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for private \
        chats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inline \
        keyboard, custom reply keyboard, instructions to remove a reply keyboard \
        or to force a reply from the user.
        """

        method_response = await self.api.request_raw(
            "sendLocation",
            get_params(locals()),
        )
        return full_result(method_response, Message)

    async def send_venue(
        self,
        chat_id: int | str,
        latitude: float,
        longitude: float,
        title: str,
        address: str,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        foursquare_id: str | None = None,
        foursquare_type: str | None = None,
        google_place_id: str | None = None,
        google_place_type: str | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
        **other: typing.Any,
    ) -> Result[Message, APIError]:
        """Method `sendVenue`, see the [documentation](https://core.telegram.org/bots/api#sendvenue)

        Use this method to send information about a venue. On success, the sent Message 
        is returned.

        :param business_connection_id: Unique identifier of the business connection on behalf of which the message \
        will be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for \
        forum supergroups only.

        :param latitude: Latitude of the venue.

        :param longitude: Longitude of the venue.

        :param title: Name of the venue.

        :param address: Address of the venue.

        :param foursquare_id: Foursquare identifier of the venue.

        :param foursquare_type: Foursquare type of the venue, if known. (For example, `arts_entertainment/default`, \
        `arts_entertainment/aquarium` or `food/icecream`.).

        :param google_place_id: Google Places identifier of the venue.

        :param google_place_type: Google Places type of the venue. (See supported types.).

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound. \

        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for private \
        chats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inline \
        keyboard, custom reply keyboard, instructions to remove a reply keyboard \
        or to force a reply from the user.
        """

        method_response = await self.api.request_raw(
            "sendVenue",
            get_params(locals()),
        )
        return full_result(method_response, Message)

    async def send_contact(
        self,
        chat_id: int | str,
        phone_number: str,
        first_name: str,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        last_name: str | None = None,
        vcard: str | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
        **other: typing.Any,
    ) -> Result[Message, APIError]:
        """Method `sendContact`, see the [documentation](https://core.telegram.org/bots/api#sendcontact)

        Use this method to send phone contacts. On success, the sent Message is returned.

        :param business_connection_id: Unique identifier of the business connection on behalf of which the message \
        will be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for \
        forum supergroups only.

        :param phone_number: Contact's phone number.

        :param first_name: Contact's first name.

        :param last_name: Contact's last name.

        :param vcard: Additional data about the contact in the form of a vCard, 0-2048 bytes.

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound. \

        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for private \
        chats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inline \
        keyboard, custom reply keyboard, instructions to remove a reply keyboard \
        or to force a reply from the user.
        """

        method_response = await self.api.request_raw(
            "sendContact",
            get_params(locals()),
        )
        return full_result(method_response, Message)

    async def send_poll(
        self,
        chat_id: int | str,
        question: str,
        options: list[InputPollOption],
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        question_parse_mode: str | None = None,
        question_entities: list[MessageEntity] | None = None,
        is_anonymous: bool | None = None,
        type: typing.Literal["quiz", "regular"] | None = None,
        allows_multiple_answers: bool | None = None,
        correct_option_id: int | None = None,
        explanation: str | None = None,
        explanation_parse_mode: str | None = None,
        explanation_entities: list[MessageEntity] | None = None,
        open_period: int | None = None,
        close_date: datetime | int | None = None,
        is_closed: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
        **other: typing.Any,
    ) -> Result[Message, APIError]:
        """Method `sendPoll`, see the [documentation](https://core.telegram.org/bots/api#sendpoll)

        Use this method to send a native poll. On success, the sent Message is returned.

        :param business_connection_id: Unique identifier of the business connection on behalf of which the message \
        will be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for \
        forum supergroups only.

        :param question: Poll question, 1-300 characters.

        :param question_parse_mode: Mode for parsing entities in the question. See formatting options for more \
        details. Currently, only custom emoji entities are allowed.

        :param question_entities: A JSON-serialized list of special entities that appear in the poll question. \
        It can be specified instead of question_parse_mode.

        :param options: A JSON-serialized list of 2-10 answer options.

        :param is_anonymous: True, if the poll needs to be anonymous, defaults to True.

        :param type: Poll type, `quiz` or `regular`, defaults to `regular`.

        :param allows_multiple_answers: True, if the poll allows multiple answers, ignored for polls in quiz mode, \
        defaults to False.

        :param correct_option_id: 0-based identifier of the correct answer option, required for polls in \
        quiz mode.

        :param explanation: Text that is shown when a user chooses an incorrect answer or taps on the lamp \
        icon in a quiz-style poll, 0-200 characters with at most 2 line feeds after \
        entities parsing.

        :param explanation_parse_mode: Mode for parsing entities in the explanation. See formatting options for \
        more details.

        :param explanation_entities: A JSON-serialized list of special entities that appear in the poll explanation. \
        It can be specified instead of explanation_parse_mode.

        :param open_period: Amount of time in seconds the poll will be active after creation, 5-600. \
        Can't be used together with close_date.

        :param close_date: Point in time (Unix timestamp) when the poll will be automatically closed. \
        Must be at least 5 and no more than 600 seconds in the future. Can't be used \
        together with open_period.

        :param is_closed: Pass True if the poll needs to be immediately closed. This can be useful for \
        poll preview.

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound. \

        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for private \
        chats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inline \
        keyboard, custom reply keyboard, instructions to remove a reply keyboard \
        or to force a reply from the user.
        """

        method_response = await self.api.request_raw(
            "sendPoll",
            get_params(locals()),
        )
        return full_result(method_response, Message)

    async def send_dice(
        self,
        chat_id: int | str,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        emoji: DiceEmoji | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
        **other: typing.Any,
    ) -> Result[Message, APIError]:
        """Method `sendDice`, see the [documentation](https://core.telegram.org/bots/api#senddice)

        Use this method to send an animated emoji that will display a random value. 
        On success, the sent Message is returned.

        :param business_connection_id: Unique identifier of the business connection on behalf of which the message \
        will be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for \
        forum supergroups only.

        :param emoji: Emoji on which the dice throw animation is based. Currently, must be one \
        of `🎲`, `🎯`, `🏀`, `⚽`, `🎳`, or `🎰`. Dice can have values 1-6 for `🎲`, `🎯` and \
        `🎳`, values 1-5 for `🏀` and `⚽`, and values 1-64 for `🎰`. Defaults to `🎲`. \

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound. \

        :param protect_content: Protects the contents of the sent message from forwarding.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for private \
        chats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inline \
        keyboard, custom reply keyboard, instructions to remove a reply keyboard \
        or to force a reply from the user.
        """

        method_response = await self.api.request_raw(
            "sendDice",
            get_params(locals()),
        )
        return full_result(method_response, Message)

    async def send_chat_action(
        self,
        chat_id: int | str,
        action: ChatAction,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `sendChatAction`, see the [documentation](https://core.telegram.org/bots/api#sendchataction)

        Use this method when you need to tell the user that something is happening 
        on the bot's side. The status is set for 5 seconds or less (when a message arrives 
        from your bot, Telegram clients clear its typing status). Returns True 
        on success. We only recommend using this method when a response from the 
        bot will take a noticeable amount of time to arrive.

        :param business_connection_id: Unique identifier of the business connection on behalf of which the action \
        will be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread; for supergroups only. \

        :param action: Type of action to broadcast. Choose one, depending on what the user is about \
        to receive: typing for text messages, upload_photo for photos, record_video \
        or upload_video for videos, record_voice or upload_voice for voice notes, \
        upload_document for general files, choose_sticker for stickers, find_location \
        for location data, record_video_note or upload_video_note for video \
        notes.
        """

        method_response = await self.api.request_raw(
            "sendChatAction",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def set_message_reaction(
        self,
        chat_id: int | str,
        message_id: int,
        reaction: list[ReactionType] | None = None,
        is_big: bool | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `setMessageReaction`, see the [documentation](https://core.telegram.org/bots/api#setmessagereaction)

        Use this method to change the chosen reactions on a message. Service messages 
        can't be reacted to. Automatically forwarded messages from a channel to 
        its discussion group have the same available reactions as messages in the 
        channel. Returns True on success.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param message_id: Identifier of the target message. If the message belongs to a media group, \
        the reaction is set to the first non-deleted message in the group instead. \

        :param reaction: A JSON-serialized list of reaction types to set on the message. Currently, \
        as non-premium users, bots can set up to one reaction per message. A custom \
        emoji reaction can be used if it is either already present on the message \
        or explicitly allowed by chat administrators.

        :param is_big: Pass True to set the reaction with a big animation.
        """

        method_response = await self.api.request_raw(
            "setMessageReaction",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def get_user_profile_photos(
        self,
        user_id: int,
        offset: int | None = None,
        limit: int | None = None,
        **other: typing.Any,
    ) -> Result[UserProfilePhotos, APIError]:
        """Method `getUserProfilePhotos`, see the [documentation](https://core.telegram.org/bots/api#getuserprofilephotos)

        Use this method to get a list of profile pictures for a user. Returns a UserProfilePhotos 
        object.

        :param user_id: Unique identifier of the target user.

        :param offset: Sequential number of the first photo to be returned. By default, all photos \
        are returned.

        :param limit: Limits the number of photos to be retrieved. Values between 1-100 are accepted. \
        Defaults to 100.
        """

        method_response = await self.api.request_raw(
            "getUserProfilePhotos",
            get_params(locals()),
        )
        return full_result(method_response, UserProfilePhotos)

    async def get_file(
        self,
        file_id: str,
        **other: typing.Any,
    ) -> Result[File, APIError]:
        """Method `getFile`, see the [documentation](https://core.telegram.org/bots/api#getfile)

        Use this method to get basic information about a file and prepare it for downloading.
        For the moment, bots can download files of up to 20MB in size. On success,
        a File object is returned. The file can then be downloaded via the link https://api.telegram.org/file/bot<token>/<file_path>,
        where <file_path> is taken from the response. It is guaranteed that the
        link will be valid for at least 1 hour. When the link expires, a new one can
        be requested by calling getFile again. Note: This function may not preserve
        the original file name and MIME type. You should save the file's MIME type
        and name (if available) when the File object is received.

        :param file_id: File identifier to get information about.
        """

        method_response = await self.api.request_raw(
            "getFile",
            get_params(locals()),
        )
        return full_result(method_response, File)

    async def ban_chat_member(
        self,
        chat_id: int | str,
        user_id: int,
        until_date: datetime | int | None = None,
        revoke_messages: bool | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `banChatMember`, see the [documentation](https://core.telegram.org/bots/api#banchatmember)

        Use this method to ban a user in a group, a supergroup or a channel. In the case 
        of supergroups and channels, the user will not be able to return to the chat 
        on their own using invite links, etc., unless unbanned first. The bot must 
        be an administrator in the chat for this to work and must have the appropriate 
        administrator rights. Returns True on success.

        :param chat_id: Unique identifier for the target group or username of the target supergroup \
        or channel (in the format @channelusername).

        :param user_id: Unique identifier of the target user.

        :param until_date: Date when the user will be unbanned; Unix time. If user is banned for more \
        than 366 days or less than 30 seconds from the current time they are considered \
        to be banned forever. Applied for supergroups and channels only.

        :param revoke_messages: Pass True to delete all messages from the chat for the user that is being removed. \
        If False, the user will be able to see messages in the group that were sent \
        before the user was removed. Always True for supergroups and channels. \
        """

        method_response = await self.api.request_raw(
            "banChatMember",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def unban_chat_member(
        self,
        chat_id: int | str,
        user_id: int,
        only_if_banned: bool | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `unbanChatMember`, see the [documentation](https://core.telegram.org/bots/api#unbanchatmember)

        Use this method to unban a previously banned user in a supergroup or channel. 
        The user will not return to the group or channel automatically, but will 
        be able to join via link, etc. The bot must be an administrator for this to 
        work. By default, this method guarantees that after the call the user is 
        not a member of the chat, but will be able to join it. So if the user is a member 
        of the chat they will also be removed from the chat. If you don't want this, 
        use the parameter only_if_banned. Returns True on success.

        :param chat_id: Unique identifier for the target group or username of the target supergroup \
        or channel (in the format @channelusername).

        :param user_id: Unique identifier of the target user.

        :param only_if_banned: Do nothing if the user is not banned.
        """

        method_response = await self.api.request_raw(
            "unbanChatMember",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def restrict_chat_member(
        self,
        chat_id: int | str,
        user_id: int,
        permissions: ChatPermissions,
        use_independent_chat_permissions: bool | None = None,
        until_date: datetime | int | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `restrictChatMember`, see the [documentation](https://core.telegram.org/bots/api#restrictchatmember)

        Use this method to restrict a user in a supergroup. The bot must be an administrator 
        in the supergroup for this to work and must have the appropriate administrator 
        rights. Pass True for all permissions to lift restrictions from a user. 
        Returns True on success.

        :param chat_id: Unique identifier for the target chat or username of the target supergroup \
        (in the format @supergroupusername).

        :param user_id: Unique identifier of the target user.

        :param permissions: A JSON-serialized object for new user permissions.

        :param use_independent_chat_permissions: Pass True if chat permissions are set independently. Otherwise, the can_send_other_messages \
        and can_add_web_page_previews permissions will imply the can_send_messages, \
        can_send_audios, can_send_documents, can_send_photos, can_send_videos, \
        can_send_video_notes, and can_send_voice_notes permissions; the can_send_polls \
        permission will imply the can_send_messages permission.

        :param until_date: Date when restrictions will be lifted for the user; Unix time. If user is \
        restricted for more than 366 days or less than 30 seconds from the current \
        time, they are considered to be restricted forever.
        """

        method_response = await self.api.request_raw(
            "restrictChatMember",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def promote_chat_member(
        self,
        chat_id: int | str,
        user_id: int,
        is_anonymous: bool | None = None,
        can_manage_chat: bool | None = None,
        can_delete_messages: bool | None = None,
        can_manage_video_chats: bool | None = None,
        can_restrict_members: bool | None = None,
        can_promote_members: bool | None = None,
        can_change_info: bool | None = None,
        can_invite_users: bool | None = None,
        can_post_stories: bool | None = None,
        can_edit_stories: bool | None = None,
        can_delete_stories: bool | None = None,
        can_post_messages: bool | None = None,
        can_edit_messages: bool | None = None,
        can_pin_messages: bool | None = None,
        can_manage_topics: bool | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `promoteChatMember`, see the [documentation](https://core.telegram.org/bots/api#promotechatmember)

        Use this method to promote or demote a user in a supergroup or a channel. The 
        bot must be an administrator in the chat for this to work and must have the 
        appropriate administrator rights. Pass False for all boolean parameters 
        to demote a user. Returns True on success.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param user_id: Unique identifier of the target user.

        :param is_anonymous: Pass True if the administrator's presence in the chat is hidden.

        :param can_manage_chat: Pass True if the administrator can access the chat event log, get boost list, \
        see hidden supergroup and channel members, report spam messages and ignore \
        slow mode. Implied by any other administrator privilege.

        :param can_delete_messages: Pass True if the administrator can delete messages of other users.

        :param can_manage_video_chats: Pass True if the administrator can manage video chats.

        :param can_restrict_members: Pass True if the administrator can restrict, ban or unban chat members, \
        or access supergroup statistics.

        :param can_promote_members: Pass True if the administrator can add new administrators with a subset \
        of their own privileges or demote administrators that they have promoted, \
        directly or indirectly (promoted by administrators that were appointed \
        by him).

        :param can_change_info: Pass True if the administrator can change chat title, photo and other settings. \

        :param can_invite_users: Pass True if the administrator can invite new users to the chat.

        :param can_post_stories: Pass True if the administrator can post stories to the chat.

        :param can_edit_stories: Pass True if the administrator can edit stories posted by other users, post \
        stories to the chat page, pin chat stories, and access the chat's story archive. \

        :param can_delete_stories: Pass True if the administrator can delete stories posted by other users. \

        :param can_post_messages: Pass True if the administrator can post messages in the channel, or access \
        channel statistics; for channels only.

        :param can_edit_messages: Pass True if the administrator can edit messages of other users and can pin \
        messages; for channels only.

        :param can_pin_messages: Pass True if the administrator can pin messages; for supergroups only. \

        :param can_manage_topics: Pass True if the user is allowed to create, rename, close, and reopen forum \
        topics; for supergroups only.
        """

        method_response = await self.api.request_raw(
            "promoteChatMember",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def set_chat_administrator_custom_title(
        self,
        chat_id: int | str,
        user_id: int,
        custom_title: str,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `setChatAdministratorCustomTitle`, see the [documentation](https://core.telegram.org/bots/api#setchatadministratorcustomtitle)

        Use this method to set a custom title for an administrator in a supergroup 
        promoted by the bot. Returns True on success.

        :param chat_id: Unique identifier for the target chat or username of the target supergroup \
        (in the format @supergroupusername).

        :param user_id: Unique identifier of the target user.

        :param custom_title: New custom title for the administrator; 0-16 characters, emoji are not \
        allowed.
        """

        method_response = await self.api.request_raw(
            "setChatAdministratorCustomTitle",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def ban_chat_sender_chat(
        self,
        chat_id: int | str,
        sender_chat_id: int,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `banChatSenderChat`, see the [documentation](https://core.telegram.org/bots/api#banchatsenderchat)

        Use this method to ban a channel chat in a supergroup or a channel. Until the 
        chat is unbanned, the owner of the banned chat won't be able to send messages 
        on behalf of any of their channels. The bot must be an administrator in the 
        supergroup or channel for this to work and must have the appropriate administrator 
        rights. Returns True on success.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param sender_chat_id: Unique identifier of the target sender chat.
        """

        method_response = await self.api.request_raw(
            "banChatSenderChat",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def unban_chat_sender_chat(
        self,
        chat_id: int | str,
        sender_chat_id: int,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `unbanChatSenderChat`, see the [documentation](https://core.telegram.org/bots/api#unbanchatsenderchat)

        Use this method to unban a previously banned channel chat in a supergroup 
        or channel. The bot must be an administrator for this to work and must have 
        the appropriate administrator rights. Returns True on success.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param sender_chat_id: Unique identifier of the target sender chat.
        """

        method_response = await self.api.request_raw(
            "unbanChatSenderChat",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def set_chat_permissions(
        self,
        chat_id: int | str,
        permissions: ChatPermissions,
        use_independent_chat_permissions: bool | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `setChatPermissions`, see the [documentation](https://core.telegram.org/bots/api#setchatpermissions)

        Use this method to set default chat permissions for all members. The bot 
        must be an administrator in the group or a supergroup for this to work and 
        must have the can_restrict_members administrator rights. Returns True 
        on success.

        :param chat_id: Unique identifier for the target chat or username of the target supergroup \
        (in the format @supergroupusername).

        :param permissions: A JSON-serialized object for new default chat permissions.

        :param use_independent_chat_permissions: Pass True if chat permissions are set independently. Otherwise, the can_send_other_messages \
        and can_add_web_page_previews permissions will imply the can_send_messages, \
        can_send_audios, can_send_documents, can_send_photos, can_send_videos, \
        can_send_video_notes, and can_send_voice_notes permissions; the can_send_polls \
        permission will imply the can_send_messages permission.
        """

        method_response = await self.api.request_raw(
            "setChatPermissions",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def export_chat_invite_link(
        self,
        chat_id: int | str,
        **other: typing.Any,
    ) -> Result[str, APIError]:
        """Method `exportChatInviteLink`, see the [documentation](https://core.telegram.org/bots/api#exportchatinvitelink)

        Use this method to generate a new primary invite link for a chat; any previously 
        generated primary link is revoked. The bot must be an administrator in the 
        chat for this to work and must have the appropriate administrator rights. 
        Returns the new invite link as String on success.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).
        """

        method_response = await self.api.request_raw(
            "exportChatInviteLink",
            get_params(locals()),
        )
        return full_result(method_response, str)

    async def create_chat_invite_link(
        self,
        chat_id: int | str,
        name: str | None = None,
        expire_date: datetime | int | None = None,
        member_limit: int | None = None,
        creates_join_request: bool | None = None,
        **other: typing.Any,
    ) -> Result[ChatInviteLink, APIError]:
        """Method `createChatInviteLink`, see the [documentation](https://core.telegram.org/bots/api#createchatinvitelink)

        Use this method to create an additional invite link for a chat. The bot must 
        be an administrator in the chat for this to work and must have the appropriate 
        administrator rights. The link can be revoked using the method revokeChatInviteLink. 
        Returns the new invite link as ChatInviteLink object.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param name: Invite link name; 0-32 characters.

        :param expire_date: Point in time (Unix timestamp) when the link will expire.

        :param member_limit: The maximum number of users that can be members of the chat simultaneously \
        after joining the chat via this invite link; 1-99999.

        :param creates_join_request: True, if users joining the chat via the link need to be approved by chat administrators. \
        If True, member_limit can't be specified.
        """

        method_response = await self.api.request_raw(
            "createChatInviteLink",
            get_params(locals()),
        )
        return full_result(method_response, ChatInviteLink)

    async def edit_chat_invite_link(
        self,
        chat_id: int | str,
        invite_link: str,
        name: str | None = None,
        expire_date: datetime | int | None = None,
        member_limit: int | None = None,
        creates_join_request: bool | None = None,
        **other: typing.Any,
    ) -> Result[ChatInviteLink, APIError]:
        """Method `editChatInviteLink`, see the [documentation](https://core.telegram.org/bots/api#editchatinvitelink)

        Use this method to edit a non-primary invite link created by the bot. The 
        bot must be an administrator in the chat for this to work and must have the 
        appropriate administrator rights. Returns the edited invite link as a 
        ChatInviteLink object.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param invite_link: The invite link to edit.

        :param name: Invite link name; 0-32 characters.

        :param expire_date: Point in time (Unix timestamp) when the link will expire.

        :param member_limit: The maximum number of users that can be members of the chat simultaneously \
        after joining the chat via this invite link; 1-99999.

        :param creates_join_request: True, if users joining the chat via the link need to be approved by chat administrators. \
        If True, member_limit can't be specified.
        """

        method_response = await self.api.request_raw(
            "editChatInviteLink",
            get_params(locals()),
        )
        return full_result(method_response, ChatInviteLink)

    async def revoke_chat_invite_link(
        self,
        chat_id: int | str,
        invite_link: str,
        **other: typing.Any,
    ) -> Result[ChatInviteLink, APIError]:
        """Method `revokeChatInviteLink`, see the [documentation](https://core.telegram.org/bots/api#revokechatinvitelink)

        Use this method to revoke an invite link created by the bot. If the primary 
        link is revoked, a new link is automatically generated. The bot must be an 
        administrator in the chat for this to work and must have the appropriate 
        administrator rights. Returns the revoked invite link as ChatInviteLink 
        object.

        :param chat_id: Unique identifier of the target chat or username of the target channel (in \
        the format @channelusername).

        :param invite_link: The invite link to revoke.
        """

        method_response = await self.api.request_raw(
            "revokeChatInviteLink",
            get_params(locals()),
        )
        return full_result(method_response, ChatInviteLink)

    async def approve_chat_join_request(
        self,
        chat_id: int | str,
        user_id: int,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `approveChatJoinRequest`, see the [documentation](https://core.telegram.org/bots/api#approvechatjoinrequest)

        Use this method to approve a chat join request. The bot must be an administrator 
        in the chat for this to work and must have the can_invite_users administrator 
        right. Returns True on success.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param user_id: Unique identifier of the target user.
        """

        method_response = await self.api.request_raw(
            "approveChatJoinRequest",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def decline_chat_join_request(
        self,
        chat_id: int | str,
        user_id: int,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `declineChatJoinRequest`, see the [documentation](https://core.telegram.org/bots/api#declinechatjoinrequest)

        Use this method to decline a chat join request. The bot must be an administrator 
        in the chat for this to work and must have the can_invite_users administrator 
        right. Returns True on success.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param user_id: Unique identifier of the target user.
        """

        method_response = await self.api.request_raw(
            "declineChatJoinRequest",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def set_chat_photo(
        self,
        chat_id: int | str,
        photo: InputFile,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `setChatPhoto`, see the [documentation](https://core.telegram.org/bots/api#setchatphoto)

        Use this method to set a new profile photo for the chat. Photos can't be changed 
        for private chats. The bot must be an administrator in the chat for this to 
        work and must have the appropriate administrator rights. Returns True 
        on success.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param photo: New chat photo, uploaded using multipart/form-data.
        """

        method_response = await self.api.request_raw(
            "setChatPhoto",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def delete_chat_photo(
        self,
        chat_id: int | str,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `deleteChatPhoto`, see the [documentation](https://core.telegram.org/bots/api#deletechatphoto)

        Use this method to delete a chat photo. Photos can't be changed for private 
        chats. The bot must be an administrator in the chat for this to work and must 
        have the appropriate administrator rights. Returns True on success.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).
        """

        method_response = await self.api.request_raw(
            "deleteChatPhoto",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def set_chat_title(
        self,
        chat_id: int | str,
        title: str,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `setChatTitle`, see the [documentation](https://core.telegram.org/bots/api#setchattitle)

        Use this method to change the title of a chat. Titles can't be changed for 
        private chats. The bot must be an administrator in the chat for this to work 
        and must have the appropriate administrator rights. Returns True on success.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param title: New chat title, 1-128 characters.
        """

        method_response = await self.api.request_raw(
            "setChatTitle",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def set_chat_description(
        self,
        chat_id: int | str,
        description: str | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `setChatDescription`, see the [documentation](https://core.telegram.org/bots/api#setchatdescription)

        Use this method to change the description of a group, a supergroup or a channel. 
        The bot must be an administrator in the chat for this to work and must have 
        the appropriate administrator rights. Returns True on success.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param description: New chat description, 0-255 characters.
        """

        method_response = await self.api.request_raw(
            "setChatDescription",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def pin_chat_message(
        self,
        chat_id: int | str,
        message_id: int,
        disable_notification: bool | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `pinChatMessage`, see the [documentation](https://core.telegram.org/bots/api#pinchatmessage)

        Use this method to add a message to the list of pinned messages in a chat. If 
        the chat is not a private chat, the bot must be an administrator in the chat 
        for this to work and must have the 'can_pin_messages' administrator right 
        in a supergroup or 'can_edit_messages' administrator right in a channel. 
        Returns True on success.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param message_id: Identifier of a message to pin.

        :param disable_notification: Pass True if it is not necessary to send a notification to all chat members \
        about the new pinned message. Notifications are always disabled in channels \
        and private chats.
        """

        method_response = await self.api.request_raw(
            "pinChatMessage",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def unpin_chat_message(
        self,
        chat_id: int | str,
        message_id: int | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `unpinChatMessage`, see the [documentation](https://core.telegram.org/bots/api#unpinchatmessage)

        Use this method to remove a message from the list of pinned messages in a chat. 
        If the chat is not a private chat, the bot must be an administrator in the chat 
        for this to work and must have the 'can_pin_messages' administrator right 
        in a supergroup or 'can_edit_messages' administrator right in a channel. 
        Returns True on success.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param message_id: Identifier of a message to unpin. If not specified, the most recent pinned \
        message (by sending date) will be unpinned.
        """

        method_response = await self.api.request_raw(
            "unpinChatMessage",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def unpin_all_chat_messages(
        self,
        chat_id: int | str,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `unpinAllChatMessages`, see the [documentation](https://core.telegram.org/bots/api#unpinallchatmessages)

        Use this method to clear the list of pinned messages in a chat. If the chat 
        is not a private chat, the bot must be an administrator in the chat for this 
        to work and must have the 'can_pin_messages' administrator right in a supergroup 
        or 'can_edit_messages' administrator right in a channel. Returns True 
        on success.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).
        """

        method_response = await self.api.request_raw(
            "unpinAllChatMessages",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def leave_chat(
        self,
        chat_id: int | str,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `leaveChat`, see the [documentation](https://core.telegram.org/bots/api#leavechat)

        Use this method for your bot to leave a group, supergroup or channel. Returns 
        True on success.

        :param chat_id: Unique identifier for the target chat or username of the target supergroup \
        or channel (in the format @channelusername).
        """

        method_response = await self.api.request_raw(
            "leaveChat",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def get_chat(
        self,
        chat_id: int | str,
        **other: typing.Any,
    ) -> Result[ChatFullInfo, APIError]:
        """Method `getChat`, see the [documentation](https://core.telegram.org/bots/api#getchat)

        Use this method to get up-to-date information about the chat. Returns a 
        ChatFullInfo object on success.

        :param chat_id: Unique identifier for the target chat or username of the target supergroup \
        or channel (in the format @channelusername).
        """

        method_response = await self.api.request_raw(
            "getChat",
            get_params(locals()),
        )
        return full_result(method_response, ChatFullInfo)

    async def get_chat_administrators(
        self,
        chat_id: int | str,
        **other: typing.Any,
    ) -> Result[
        list[
            Variative[
                ChatMemberOwner,
                ChatMemberAdministrator,
                ChatMemberMember,
                ChatMemberRestricted,
                ChatMemberLeft,
                ChatMemberBanned,
            ]
        ],
        APIError,
    ]:
        """Method `getChatAdministrators`, see the [documentation](https://core.telegram.org/bots/api#getchatadministrators)

        Use this method to get a list of administrators in a chat, which aren't bots. 
        Returns an Array of ChatMember objects.

        :param chat_id: Unique identifier for the target chat or username of the target supergroup \
        or channel (in the format @channelusername).
        """

        method_response = await self.api.request_raw(
            "getChatAdministrators",
            get_params(locals()),
        )
        return full_result(
            method_response,
            list[
                Variative[
                    ChatMemberOwner,
                    ChatMemberAdministrator,
                    ChatMemberMember,
                    ChatMemberRestricted,
                    ChatMemberLeft,
                    ChatMemberBanned,
                ]
            ],
        )

    async def get_chat_member_count(
        self,
        chat_id: int | str,
        **other: typing.Any,
    ) -> Result[int, APIError]:
        """Method `getChatMemberCount`, see the [documentation](https://core.telegram.org/bots/api#getchatmembercount)

        Use this method to get the number of members in a chat. Returns Int on success.

        :param chat_id: Unique identifier for the target chat or username of the target supergroup \
        or channel (in the format @channelusername).
        """

        method_response = await self.api.request_raw(
            "getChatMemberCount",
            get_params(locals()),
        )
        return full_result(method_response, int)

    async def get_chat_member(
        self,
        chat_id: int | str,
        user_id: int,
        **other: typing.Any,
    ) -> Result[
        Variative[
            ChatMemberOwner,
            ChatMemberAdministrator,
            ChatMemberMember,
            ChatMemberRestricted,
            ChatMemberLeft,
            ChatMemberBanned,
        ],
        APIError,
    ]:
        """Method `getChatMember`, see the [documentation](https://core.telegram.org/bots/api#getchatmember)

        Use this method to get information about a member of a chat. The method is 
        only guaranteed to work for other users if the bot is an administrator in 
        the chat. Returns a ChatMember object on success.

        :param chat_id: Unique identifier for the target chat or username of the target supergroup \
        or channel (in the format @channelusername).

        :param user_id: Unique identifier of the target user.
        """

        method_response = await self.api.request_raw(
            "getChatMember",
            get_params(locals()),
        )
        return full_result(
            method_response,
            Variative[
                ChatMemberOwner,
                ChatMemberAdministrator,
                ChatMemberMember,
                ChatMemberRestricted,
                ChatMemberLeft,
                ChatMemberBanned,
            ],
        )

    async def set_chat_sticker_set(
        self,
        chat_id: int | str,
        sticker_set_name: str,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `setChatStickerSet`, see the [documentation](https://core.telegram.org/bots/api#setchatstickerset)

        Use this method to set a new group sticker set for a supergroup. The bot must 
        be an administrator in the chat for this to work and must have the appropriate 
        administrator rights. Use the field can_set_sticker_set optionally 
        returned in getChat requests to check if the bot can use this method. Returns 
        True on success.

        :param chat_id: Unique identifier for the target chat or username of the target supergroup \
        (in the format @supergroupusername).

        :param sticker_set_name: Name of the sticker set to be set as the group sticker set.
        """

        method_response = await self.api.request_raw(
            "setChatStickerSet",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def delete_chat_sticker_set(
        self,
        chat_id: int | str,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `deleteChatStickerSet`, see the [documentation](https://core.telegram.org/bots/api#deletechatstickerset)

        Use this method to delete a group sticker set from a supergroup. The bot must 
        be an administrator in the chat for this to work and must have the appropriate 
        administrator rights. Use the field can_set_sticker_set optionally 
        returned in getChat requests to check if the bot can use this method. Returns 
        True on success.

        :param chat_id: Unique identifier for the target chat or username of the target supergroup \
        (in the format @supergroupusername).
        """

        method_response = await self.api.request_raw(
            "deleteChatStickerSet",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def get_forum_topic_icon_stickers(self, **other: typing.Any) -> Result[list[Sticker], APIError]:
        """Method `getForumTopicIconStickers`, see the [documentation](https://core.telegram.org/bots/api#getforumtopiciconstickers)

        Use this method to get custom emoji stickers, which can be used as a forum
        topic icon by any user. Requires no parameters. Returns an Array of Sticker
        objects.
        """

        method_response = await self.api.request_raw(
            "getForumTopicIconStickers",
            get_params(locals()),
        )
        return full_result(method_response, list[Sticker])

    async def create_forum_topic(
        self,
        chat_id: int | str,
        name: str,
        icon_color: TopicIconColor | None = None,
        icon_custom_emoji_id: str | None = None,
        **other: typing.Any,
    ) -> Result[ForumTopic, APIError]:
        """Method `createForumTopic`, see the [documentation](https://core.telegram.org/bots/api#createforumtopic)

        Use this method to create a topic in a forum supergroup chat. The bot must 
        be an administrator in the chat for this to work and must have the can_manage_topics 
        administrator rights. Returns information about the created topic as 
        a ForumTopic object.

        :param chat_id: Unique identifier for the target chat or username of the target supergroup \
        (in the format @supergroupusername).

        :param name: Topic name, 1-128 characters.

        :param icon_color: Color of the topic icon in RGB format. Currently, must be one of 7322096 (0x6FB9F0), \
        16766590 (0xFFD67E), 13338331 (0xCB86DB), 9367192 (0x8EEE98), 16749490 \
        (0xFF93B2), or 16478047 (0xFB6F5F).

        :param icon_custom_emoji_id: Unique identifier of the custom emoji shown as the topic icon. Use getForumTopicIconStickers \
        to get all allowed custom emoji identifiers.
        """

        method_response = await self.api.request_raw(
            "createForumTopic",
            get_params(locals()),
        )
        return full_result(method_response, ForumTopic)

    async def edit_forum_topic(
        self,
        chat_id: int | str,
        message_thread_id: int,
        name: str | None = None,
        icon_custom_emoji_id: str | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `editForumTopic`, see the [documentation](https://core.telegram.org/bots/api#editforumtopic)

        Use this method to edit name and icon of a topic in a forum supergroup chat. 
        The bot must be an administrator in the chat for this to work and must have 
        can_manage_topics administrator rights, unless it is the creator of the 
        topic. Returns True on success.

        :param chat_id: Unique identifier for the target chat or username of the target supergroup \
        (in the format @supergroupusername).

        :param message_thread_id: Unique identifier for the target message thread of the forum topic.

        :param name: New topic name, 0-128 characters. If not specified or empty, the current \
        name of the topic will be kept.

        :param icon_custom_emoji_id: New unique identifier of the custom emoji shown as the topic icon. Use getForumTopicIconStickers \
        to get all allowed custom emoji identifiers. Pass an empty string to remove \
        the icon. If not specified, the current icon will be kept.
        """

        method_response = await self.api.request_raw(
            "editForumTopic",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def close_forum_topic(
        self,
        chat_id: int | str,
        message_thread_id: int,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `closeForumTopic`, see the [documentation](https://core.telegram.org/bots/api#closeforumtopic)

        Use this method to close an open topic in a forum supergroup chat. The bot 
        must be an administrator in the chat for this to work and must have the can_manage_topics 
        administrator rights, unless it is the creator of the topic. Returns True 
        on success.

        :param chat_id: Unique identifier for the target chat or username of the target supergroup \
        (in the format @supergroupusername).

        :param message_thread_id: Unique identifier for the target message thread of the forum topic.
        """

        method_response = await self.api.request_raw(
            "closeForumTopic",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def reopen_forum_topic(
        self,
        chat_id: int | str,
        message_thread_id: int,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `reopenForumTopic`, see the [documentation](https://core.telegram.org/bots/api#reopenforumtopic)

        Use this method to reopen a closed topic in a forum supergroup chat. The bot 
        must be an administrator in the chat for this to work and must have the can_manage_topics 
        administrator rights, unless it is the creator of the topic. Returns True 
        on success.

        :param chat_id: Unique identifier for the target chat or username of the target supergroup \
        (in the format @supergroupusername).

        :param message_thread_id: Unique identifier for the target message thread of the forum topic.
        """

        method_response = await self.api.request_raw(
            "reopenForumTopic",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def delete_forum_topic(
        self,
        chat_id: int | str,
        message_thread_id: int,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `deleteForumTopic`, see the [documentation](https://core.telegram.org/bots/api#deleteforumtopic)

        Use this method to delete a forum topic along with all its messages in a forum 
        supergroup chat. The bot must be an administrator in the chat for this to 
        work and must have the can_delete_messages administrator rights. Returns 
        True on success.

        :param chat_id: Unique identifier for the target chat or username of the target supergroup \
        (in the format @supergroupusername).

        :param message_thread_id: Unique identifier for the target message thread of the forum topic.
        """

        method_response = await self.api.request_raw(
            "deleteForumTopic",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def unpin_all_forum_topic_messages(
        self,
        chat_id: int | str,
        message_thread_id: int,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `unpinAllForumTopicMessages`, see the [documentation](https://core.telegram.org/bots/api#unpinallforumtopicmessages)

        Use this method to clear the list of pinned messages in a forum topic. The 
        bot must be an administrator in the chat for this to work and must have the 
        can_pin_messages administrator right in the supergroup. Returns True 
        on success.

        :param chat_id: Unique identifier for the target chat or username of the target supergroup \
        (in the format @supergroupusername).

        :param message_thread_id: Unique identifier for the target message thread of the forum topic.
        """

        method_response = await self.api.request_raw(
            "unpinAllForumTopicMessages",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def edit_general_forum_topic(
        self,
        chat_id: int | str,
        name: str,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `editGeneralForumTopic`, see the [documentation](https://core.telegram.org/bots/api#editgeneralforumtopic)

        Use this method to edit the name of the 'General' topic in a forum supergroup 
        chat. The bot must be an administrator in the chat for this to work and must 
        have can_manage_topics administrator rights. Returns True on success.

        :param chat_id: Unique identifier for the target chat or username of the target supergroup \
        (in the format @supergroupusername).

        :param name: New topic name, 1-128 characters.
        """

        method_response = await self.api.request_raw(
            "editGeneralForumTopic",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def close_general_forum_topic(
        self,
        chat_id: int | str,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `closeGeneralForumTopic`, see the [documentation](https://core.telegram.org/bots/api#closegeneralforumtopic)

        Use this method to close an open 'General' topic in a forum supergroup chat. 
        The bot must be an administrator in the chat for this to work and must have 
        the can_manage_topics administrator rights. Returns True on success.

        :param chat_id: Unique identifier for the target chat or username of the target supergroup \
        (in the format @supergroupusername).
        """

        method_response = await self.api.request_raw(
            "closeGeneralForumTopic",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def reopen_general_forum_topic(
        self,
        chat_id: int | str,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `reopenGeneralForumTopic`, see the [documentation](https://core.telegram.org/bots/api#reopengeneralforumtopic)

        Use this method to reopen a closed 'General' topic in a forum supergroup 
        chat. The bot must be an administrator in the chat for this to work and must 
        have the can_manage_topics administrator rights. The topic will be automatically 
        unhidden if it was hidden. Returns True on success.

        :param chat_id: Unique identifier for the target chat or username of the target supergroup \
        (in the format @supergroupusername).
        """

        method_response = await self.api.request_raw(
            "reopenGeneralForumTopic",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def hide_general_forum_topic(
        self,
        chat_id: int | str,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `hideGeneralForumTopic`, see the [documentation](https://core.telegram.org/bots/api#hidegeneralforumtopic)

        Use this method to hide the 'General' topic in a forum supergroup chat. The 
        bot must be an administrator in the chat for this to work and must have the 
        can_manage_topics administrator rights. The topic will be automatically 
        closed if it was open. Returns True on success.

        :param chat_id: Unique identifier for the target chat or username of the target supergroup \
        (in the format @supergroupusername).
        """

        method_response = await self.api.request_raw(
            "hideGeneralForumTopic",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def unhide_general_forum_topic(
        self,
        chat_id: int | str,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `unhideGeneralForumTopic`, see the [documentation](https://core.telegram.org/bots/api#unhidegeneralforumtopic)

        Use this method to unhide the 'General' topic in a forum supergroup chat. 
        The bot must be an administrator in the chat for this to work and must have 
        the can_manage_topics administrator rights. Returns True on success.

        :param chat_id: Unique identifier for the target chat or username of the target supergroup \
        (in the format @supergroupusername).
        """

        method_response = await self.api.request_raw(
            "unhideGeneralForumTopic",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def unpin_all_general_forum_topic_messages(
        self,
        chat_id: int | str,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `unpinAllGeneralForumTopicMessages`, see the [documentation](https://core.telegram.org/bots/api#unpinallgeneralforumtopicmessages)

        Use this method to clear the list of pinned messages in a General forum topic. 
        The bot must be an administrator in the chat for this to work and must have 
        the can_pin_messages administrator right in the supergroup. Returns 
        True on success.

        :param chat_id: Unique identifier for the target chat or username of the target supergroup \
        (in the format @supergroupusername).
        """

        method_response = await self.api.request_raw(
            "unpinAllGeneralForumTopicMessages",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def answer_callback_query(
        self,
        callback_query_id: str,
        text: str | None = None,
        show_alert: bool | None = None,
        url: str | None = None,
        cache_time: int | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `answerCallbackQuery`, see the [documentation](https://core.telegram.org/bots/api#answercallbackquery)

        Use this method to send answers to callback queries sent from inline keyboards. 
        The answer will be displayed to the user as a notification at the top of the 
        chat screen or as an alert. On success, True is returned.

        :param callback_query_id: Unique identifier for the query to be answered.

        :param text: Text of the notification. If not specified, nothing will be shown to the \
        user, 0-200 characters.

        :param show_alert: If True, an alert will be shown by the client instead of a notification at \
        the top of the chat screen. Defaults to false.

        :param url: URL that will be opened by the user's client. If you have created a Game and \
        accepted the conditions via @BotFather, specify the URL that opens your \
        game - note that this will only work if the query comes from a callback_game \
        button. Otherwise, you may use links like t.me/your_bot?start=XXXX that \
        open your bot with a parameter.

        :param cache_time: The maximum amount of time in seconds that the result of the callback query \
        may be cached client-side. Telegram apps will support caching starting \
        in version 3.14. Defaults to 0.
        """

        method_response = await self.api.request_raw(
            "answerCallbackQuery",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def get_user_chat_boosts(
        self,
        chat_id: int | str,
        user_id: int,
        **other: typing.Any,
    ) -> Result[UserChatBoosts, APIError]:
        """Method `getUserChatBoosts`, see the [documentation](https://core.telegram.org/bots/api#getuserchatboosts)

        Use this method to get the list of boosts added to a chat by a user. Requires 
        administrator rights in the chat. Returns a UserChatBoosts object.

        :param chat_id: Unique identifier for the chat or username of the channel (in the format \
        @channelusername).

        :param user_id: Unique identifier of the target user.
        """

        method_response = await self.api.request_raw(
            "getUserChatBoosts",
            get_params(locals()),
        )
        return full_result(method_response, UserChatBoosts)

    async def get_business_connection(
        self,
        business_connection_id: str,
        **other: typing.Any,
    ) -> Result[BusinessConnection, APIError]:
        """Method `getBusinessConnection`, see the [documentation](https://core.telegram.org/bots/api#getbusinessconnection)

        Use this method to get information about the connection of the bot with a
        business account. Returns a BusinessConnection object on success.

        :param business_connection_id: Unique identifier of the business connection.
        """

        method_response = await self.api.request_raw(
            "getBusinessConnection",
            get_params(locals()),
        )
        return full_result(method_response, BusinessConnection)

    async def set_my_commands(
        self,
        commands: list[BotCommand],
        scope: BotCommandScope | None = None,
        language_code: str | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `setMyCommands`, see the [documentation](https://core.telegram.org/bots/api#setmycommands)

        Use this method to change the list of the bot's commands. See this manual 
        for more details about bot commands. Returns True on success.

        :param commands: A JSON-serialized list of bot commands to be set as the list of the bot's commands. \
        At most 100 commands can be specified.

        :param scope: A JSON-serialized object, describing scope of users for which the commands \
        are relevant. Defaults to BotCommandScopeDefault.

        :param language_code: A two-letter ISO 639-1 language code. If empty, commands will be applied \
        to all users from the given scope, for whose language there are no dedicated \
        commands.
        """

        method_response = await self.api.request_raw(
            "setMyCommands",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def delete_my_commands(
        self,
        scope: BotCommandScope | None = None,
        language_code: str | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `deleteMyCommands`, see the [documentation](https://core.telegram.org/bots/api#deletemycommands)

        Use this method to delete the list of the bot's commands for the given scope 
        and user language. After deletion, higher level commands will be shown 
        to affected users. Returns True on success.

        :param scope: A JSON-serialized object, describing scope of users for which the commands \
        are relevant. Defaults to BotCommandScopeDefault.

        :param language_code: A two-letter ISO 639-1 language code. If empty, commands will be applied \
        to all users from the given scope, for whose language there are no dedicated \
        commands.
        """

        method_response = await self.api.request_raw(
            "deleteMyCommands",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def get_my_commands(
        self,
        scope: BotCommandScope | None = None,
        language_code: str | None = None,
        **other: typing.Any,
    ) -> Result[list[BotCommand], APIError]:
        """Method `getMyCommands`, see the [documentation](https://core.telegram.org/bots/api#getmycommands)

        Use this method to get the current list of the bot's commands for the given 
        scope and user language. Returns an Array of BotCommand objects. If commands 
        aren't set, an empty list is returned.

        :param scope: A JSON-serialized object, describing scope of users. Defaults to BotCommandScopeDefault. \

        :param language_code: A two-letter ISO 639-1 language code or an empty string.
        """

        method_response = await self.api.request_raw(
            "getMyCommands",
            get_params(locals()),
        )
        return full_result(method_response, list[BotCommand])

    async def set_my_name(
        self,
        name: str | None = None,
        language_code: str | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `setMyName`, see the [documentation](https://core.telegram.org/bots/api#setmyname)

        Use this method to change the bot's name. Returns True on success.

        :param name: New bot name; 0-64 characters. Pass an empty string to remove the dedicated \
        name for the given language.

        :param language_code: A two-letter ISO 639-1 language code. If empty, the name will be shown to \
        all users for whose language there is no dedicated name.
        """

        method_response = await self.api.request_raw(
            "setMyName",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def get_my_name(
        self,
        language_code: str | None = None,
        **other: typing.Any,
    ) -> Result[BotName, APIError]:
        """Method `getMyName`, see the [documentation](https://core.telegram.org/bots/api#getmyname)

        Use this method to get the current bot name for the given user language. Returns
        BotName on success.

        :param language_code: A two-letter ISO 639-1 language code or an empty string.
        """

        method_response = await self.api.request_raw(
            "getMyName",
            get_params(locals()),
        )
        return full_result(method_response, BotName)

    async def set_my_description(
        self,
        description: str | None = None,
        language_code: str | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `setMyDescription`, see the [documentation](https://core.telegram.org/bots/api#setmydescription)

        Use this method to change the bot's description, which is shown in the chat 
        with the bot if the chat is empty. Returns True on success.

        :param description: New bot description; 0-512 characters. Pass an empty string to remove the \
        dedicated description for the given language.

        :param language_code: A two-letter ISO 639-1 language code. If empty, the description will be \
        applied to all users for whose language there is no dedicated description. \
        """

        method_response = await self.api.request_raw(
            "setMyDescription",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def get_my_description(
        self,
        language_code: str | None = None,
        **other: typing.Any,
    ) -> Result[BotDescription, APIError]:
        """Method `getMyDescription`, see the [documentation](https://core.telegram.org/bots/api#getmydescription)

        Use this method to get the current bot description for the given user language.
        Returns BotDescription on success.

        :param language_code: A two-letter ISO 639-1 language code or an empty string.
        """

        method_response = await self.api.request_raw(
            "getMyDescription",
            get_params(locals()),
        )
        return full_result(method_response, BotDescription)

    async def set_my_short_description(
        self,
        short_description: str | None = None,
        language_code: str | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `setMyShortDescription`, see the [documentation](https://core.telegram.org/bots/api#setmyshortdescription)

        Use this method to change the bot's short description, which is shown on 
        the bot's profile page and is sent together with the link when users share 
        the bot. Returns True on success.

        :param short_description: New short description for the bot; 0-120 characters. Pass an empty string \
        to remove the dedicated short description for the given language.

        :param language_code: A two-letter ISO 639-1 language code. If empty, the short description will \
        be applied to all users for whose language there is no dedicated short description. \
        """

        method_response = await self.api.request_raw(
            "setMyShortDescription",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def get_my_short_description(
        self,
        language_code: str | None = None,
        **other: typing.Any,
    ) -> Result[BotShortDescription, APIError]:
        """Method `getMyShortDescription`, see the [documentation](https://core.telegram.org/bots/api#getmyshortdescription)

        Use this method to get the current bot short description for the given user
        language. Returns BotShortDescription on success.

        :param language_code: A two-letter ISO 639-1 language code or an empty string.
        """

        method_response = await self.api.request_raw(
            "getMyShortDescription",
            get_params(locals()),
        )
        return full_result(method_response, BotShortDescription)

    async def set_chat_menu_button(
        self,
        chat_id: int | None = None,
        menu_button: MenuButton | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `setChatMenuButton`, see the [documentation](https://core.telegram.org/bots/api#setchatmenubutton)

        Use this method to change the bot's menu button in a private chat, or the default 
        menu button. Returns True on success.

        :param chat_id: Unique identifier for the target private chat. If not specified, default \
        bot's menu button will be changed.

        :param menu_button: A JSON-serialized object for the bot's new menu button. Defaults to MenuButtonDefault. \
        """

        method_response = await self.api.request_raw(
            "setChatMenuButton",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def get_chat_menu_button(
        self,
        chat_id: int | None = None,
        **other: typing.Any,
    ) -> Result[Variative[MenuButtonCommands, MenuButtonWebApp, MenuButtonDefault], APIError]:
        """Method `getChatMenuButton`, see the [documentation](https://core.telegram.org/bots/api#getchatmenubutton)

        Use this method to get the current value of the bot's menu button in a private 
        chat, or the default menu button. Returns MenuButton on success.

        :param chat_id: Unique identifier for the target private chat. If not specified, default \
        bot's menu button will be returned.
        """

        method_response = await self.api.request_raw(
            "getChatMenuButton",
            get_params(locals()),
        )
        return full_result(
            method_response, Variative[MenuButtonCommands, MenuButtonWebApp, MenuButtonDefault]
        )

    async def set_my_default_administrator_rights(
        self,
        rights: ChatAdministratorRights | None = None,
        for_channels: bool | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `setMyDefaultAdministratorRights`, see the [documentation](https://core.telegram.org/bots/api#setmydefaultadministratorrights)

        Use this method to change the default administrator rights requested by 
        the bot when it's added as an administrator to groups or channels. These 
        rights will be suggested to users, but they are free to modify the list before 
        adding the bot. Returns True on success.

        :param rights: A JSON-serialized object describing new default administrator rights. \
        If not specified, the default administrator rights will be cleared.

        :param for_channels: Pass True to change the default administrator rights of the bot in channels. \
        Otherwise, the default administrator rights of the bot for groups and supergroups \
        will be changed.
        """

        method_response = await self.api.request_raw(
            "setMyDefaultAdministratorRights",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def get_my_default_administrator_rights(
        self,
        for_channels: bool | None = None,
        **other: typing.Any,
    ) -> Result[ChatAdministratorRights, APIError]:
        """Method `getMyDefaultAdministratorRights`, see the [documentation](https://core.telegram.org/bots/api#getmydefaultadministratorrights)

        Use this method to get the current default administrator rights of the bot. 
        Returns ChatAdministratorRights on success.

        :param for_channels: Pass True to get default administrator rights of the bot in channels. Otherwise, \
        default administrator rights of the bot for groups and supergroups will \
        be returned.
        """

        method_response = await self.api.request_raw(
            "getMyDefaultAdministratorRights",
            get_params(locals()),
        )
        return full_result(method_response, ChatAdministratorRights)

    async def edit_message_text(
        self,
        text: str,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
        parse_mode: str | None = None,
        entities: list[MessageEntity] | None = None,
        link_preview_options: LinkPreviewOptions | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
        **other: typing.Any,
    ) -> Result[Variative[Message, bool], APIError]:
        """Method `editMessageText`, see the [documentation](https://core.telegram.org/bots/api#editmessagetext)

        Use this method to edit text and game messages. On success, if the edited 
        message is not an inline message, the edited Message is returned, otherwise 
        True is returned. Note that business messages that were not sent by the bot 
        and do not contain an inline keyboard can only be edited within 48 hours from 
        the time they were sent.

        :param business_connection_id: Unique identifier of the business connection on behalf of which the message \
        to be edited was sent.

        :param chat_id: Required if inline_message_id is not specified. Unique identifier for \
        the target chat or username of the target channel (in the format @channelusername). \

        :param message_id: Required if inline_message_id is not specified. Identifier of the message \
        to edit.

        :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the \
        inline message.

        :param text: New text of the message, 1-4096 characters after entities parsing.

        :param parse_mode: Mode for parsing entities in the message text. See formatting options for \
        more details.

        :param entities: A JSON-serialized list of special entities that appear in message text, \
        which can be specified instead of parse_mode.

        :param link_preview_options: Link preview generation options for the message.

        :param reply_markup: A JSON-serialized object for an inline keyboard.
        """

        method_response = await self.api.request_raw(
            "editMessageText",
            get_params(locals()),
        )
        return full_result(method_response, Variative[Message, bool])

    async def edit_message_caption(
        self,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
        caption: str | None = None,
        parse_mode: str | None = None,
        caption_entities: list[MessageEntity] | None = None,
        show_caption_above_media: bool | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
        **other: typing.Any,
    ) -> Result[Variative[Message, bool], APIError]:
        """Method `editMessageCaption`, see the [documentation](https://core.telegram.org/bots/api#editmessagecaption)

        Use this method to edit captions of messages. On success, if the edited message 
        is not an inline message, the edited Message is returned, otherwise True 
        is returned. Note that business messages that were not sent by the bot and 
        do not contain an inline keyboard can only be edited within 48 hours from 
        the time they were sent.

        :param business_connection_id: Unique identifier of the business connection on behalf of which the message \
        to be edited was sent.

        :param chat_id: Required if inline_message_id is not specified. Unique identifier for \
        the target chat or username of the target channel (in the format @channelusername). \

        :param message_id: Required if inline_message_id is not specified. Identifier of the message \
        to edit.

        :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the \
        inline message.

        :param caption: New caption of the message, 0-1024 characters after entities parsing. \

        :param parse_mode: Mode for parsing entities in the message caption. See formatting options \
        for more details.

        :param caption_entities: A JSON-serialized list of special entities that appear in the caption, \
        which can be specified instead of parse_mode.

        :param show_caption_above_media: Pass True, if the caption must be shown above the message media. Supported \
        only for animation, photo and video messages.

        :param reply_markup: A JSON-serialized object for an inline keyboard.
        """

        method_response = await self.api.request_raw(
            "editMessageCaption",
            get_params(locals()),
        )
        return full_result(method_response, Variative[Message, bool])

    async def edit_message_media(
        self,
        media: InputMedia,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
        **other: typing.Any,
    ) -> Result[Variative[Message, bool], APIError]:
        """Method `editMessageMedia`, see the [documentation](https://core.telegram.org/bots/api#editmessagemedia)

        Use this method to edit animation, audio, document, photo, or video messages. 
        If a message is part of a message album, then it can be edited only to an audio 
        for audio albums, only to a document for document albums and to a photo or 
        a video otherwise. When an inline message is edited, a new file can't be uploaded; 
        use a previously uploaded file via its file_id or specify a URL. On success, 
        if the edited message is not an inline message, the edited Message is returned, 
        otherwise True is returned. Note that business messages that were not sent 
        by the bot and do not contain an inline keyboard can only be edited within 
        48 hours from the time they were sent.

        :param business_connection_id: Unique identifier of the business connection on behalf of which the message \
        to be edited was sent.

        :param chat_id: Required if inline_message_id is not specified. Unique identifier for \
        the target chat or username of the target channel (in the format @channelusername). \

        :param message_id: Required if inline_message_id is not specified. Identifier of the message \
        to edit.

        :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the \
        inline message.

        :param media: A JSON-serialized object for a new media content of the message.

        :param reply_markup: A JSON-serialized object for a new inline keyboard.
        """

        method_response = await self.api.request_raw(
            "editMessageMedia",
            get_params(locals()),
        )
        return full_result(method_response, Variative[Message, bool])

    async def edit_message_live_location(
        self,
        latitude: float,
        longitude: float,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
        live_period: int | None = None,
        horizontal_accuracy: float | None = None,
        heading: int | None = None,
        proximity_alert_radius: int | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
        **other: typing.Any,
    ) -> Result[Variative[Message, bool], APIError]:
        """Method `editMessageLiveLocation`, see the [documentation](https://core.telegram.org/bots/api#editmessagelivelocation)

        Use this method to edit live location messages. A location can be edited 
        until its live_period expires or editing is explicitly disabled by a call 
        to stopMessageLiveLocation. On success, if the edited message is not an 
        inline message, the edited Message is returned, otherwise True is returned.

        :param business_connection_id: Unique identifier of the business connection on behalf of which the message \
        to be edited was sent.

        :param chat_id: Required if inline_message_id is not specified. Unique identifier for \
        the target chat or username of the target channel (in the format @channelusername). \

        :param message_id: Required if inline_message_id is not specified. Identifier of the message \
        to edit.

        :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the \
        inline message.

        :param latitude: Latitude of new location.

        :param longitude: Longitude of new location.

        :param live_period: New period in seconds during which the location can be updated, starting \
        from the message send date. If 0x7FFFFFFF is specified, then the location \
        can be updated forever. Otherwise, the new value must not exceed the current \
        live_period by more than a day, and the live location expiration date must \
        remain within the next 90 days. If not specified, then live_period remains \
        unchanged.

        :param horizontal_accuracy: The radius of uncertainty for the location, measured in meters; 0-1500. \

        :param heading: Direction in which the user is moving, in degrees. Must be between 1 and 360 \
        if specified.

        :param proximity_alert_radius: The maximum distance for proximity alerts about approaching another chat \
        member, in meters. Must be between 1 and 100000 if specified.

        :param reply_markup: A JSON-serialized object for a new inline keyboard.
        """

        method_response = await self.api.request_raw(
            "editMessageLiveLocation",
            get_params(locals()),
        )
        return full_result(method_response, Variative[Message, bool])

    async def stop_message_live_location(
        self,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
        **other: typing.Any,
    ) -> Result[Variative[Message, bool], APIError]:
        """Method `stopMessageLiveLocation`, see the [documentation](https://core.telegram.org/bots/api#stopmessagelivelocation)

        Use this method to stop updating a live location message before live_period 
        expires. On success, if the message is not an inline message, the edited 
        Message is returned, otherwise True is returned.

        :param business_connection_id: Unique identifier of the business connection on behalf of which the message \
        to be edited was sent.

        :param chat_id: Required if inline_message_id is not specified. Unique identifier for \
        the target chat or username of the target channel (in the format @channelusername). \

        :param message_id: Required if inline_message_id is not specified. Identifier of the message \
        with live location to stop.

        :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the \
        inline message.

        :param reply_markup: A JSON-serialized object for a new inline keyboard.
        """

        method_response = await self.api.request_raw(
            "stopMessageLiveLocation",
            get_params(locals()),
        )
        return full_result(method_response, Variative[Message, bool])

    async def edit_message_reply_markup(
        self,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
        **other: typing.Any,
    ) -> Result[Variative[Message, bool], APIError]:
        """Method `editMessageReplyMarkup`, see the [documentation](https://core.telegram.org/bots/api#editmessagereplymarkup)

        Use this method to edit only the reply markup of messages. On success, if 
        the edited message is not an inline message, the edited Message is returned, 
        otherwise True is returned. Note that business messages that were not sent 
        by the bot and do not contain an inline keyboard can only be edited within 
        48 hours from the time they were sent.

        :param business_connection_id: Unique identifier of the business connection on behalf of which the message \
        to be edited was sent.

        :param chat_id: Required if inline_message_id is not specified. Unique identifier for \
        the target chat or username of the target channel (in the format @channelusername). \

        :param message_id: Required if inline_message_id is not specified. Identifier of the message \
        to edit.

        :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the \
        inline message.

        :param reply_markup: A JSON-serialized object for an inline keyboard.
        """

        method_response = await self.api.request_raw(
            "editMessageReplyMarkup",
            get_params(locals()),
        )
        return full_result(method_response, Variative[Message, bool])

    async def stop_poll(
        self,
        chat_id: int | str,
        message_id: int,
        business_connection_id: str | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
        **other: typing.Any,
    ) -> Result[Poll, APIError]:
        """Method `stopPoll`, see the [documentation](https://core.telegram.org/bots/api#stoppoll)

        Use this method to stop a poll which was sent by the bot. On success, the stopped 
        Poll is returned.

        :param business_connection_id: Unique identifier of the business connection on behalf of which the message \
        to be edited was sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param message_id: Identifier of the original message with the poll.

        :param reply_markup: A JSON-serialized object for a new message inline keyboard.
        """

        method_response = await self.api.request_raw(
            "stopPoll",
            get_params(locals()),
        )
        return full_result(method_response, Poll)

    async def delete_message(
        self,
        chat_id: int | str,
        message_id: int,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `deleteMessage`, see the [documentation](https://core.telegram.org/bots/api#deletemessage)

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
        Returns True on success.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param message_id: Identifier of the message to delete.
        """

        method_response = await self.api.request_raw(
            "deleteMessage",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def delete_messages(
        self,
        chat_id: int | str,
        message_ids: list[int],
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `deleteMessages`, see the [documentation](https://core.telegram.org/bots/api#deletemessages)

        Use this method to delete multiple messages simultaneously. If some of 
        the specified messages can't be found, they are skipped. Returns True on 
        success.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param message_ids: A JSON-serialized list of 1-100 identifiers of messages to delete. See \
        deleteMessage for limitations on which messages can be deleted.
        """

        method_response = await self.api.request_raw(
            "deleteMessages",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def send_sticker(
        self,
        chat_id: int | str,
        sticker: InputFile | str,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        emoji: str | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
        **other: typing.Any,
    ) -> Result[Message, APIError]:
        """Method `sendSticker`, see the [documentation](https://core.telegram.org/bots/api#sendsticker)

        Use this method to send static .WEBP, animated .TGS, or video .WEBM stickers. 
        On success, the sent Message is returned.

        :param business_connection_id: Unique identifier of the business connection on behalf of which the message \
        will be sent.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for \
        forum supergroups only.

        :param sticker: Sticker to send. Pass a file_id as String to send a file that exists on the \
        Telegram servers (recommended), pass an HTTP URL as a String for Telegram \
        to get a .WEBP sticker from the Internet, or upload a new .WEBP, .TGS, or .WEBM \
        sticker using multipart/form-data. More information on Sending Files: \
        https://core.telegram.org/bots/api#sending-files. Video and animated \
        stickers can't be sent via an HTTP URL.

        :param emoji: Emoji associated with the sticker; only for just uploaded stickers.

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound. \

        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for private \
        chats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: Additional interface options. A JSON-serialized object for an inline \
        keyboard, custom reply keyboard, instructions to remove a reply keyboard \
        or to force a reply from the user.
        """

        method_response = await self.api.request_raw(
            "sendSticker",
            get_params(locals()),
        )
        return full_result(method_response, Message)

    async def get_sticker_set(
        self,
        name: str,
        **other: typing.Any,
    ) -> Result[StickerSet, APIError]:
        """Method `getStickerSet`, see the [documentation](https://core.telegram.org/bots/api#getstickerset)

        Use this method to get a sticker set. On success, a StickerSet object is returned.

        :param name: Name of the sticker set.
        """

        method_response = await self.api.request_raw(
            "getStickerSet",
            get_params(locals()),
        )
        return full_result(method_response, StickerSet)

    async def get_custom_emoji_stickers(
        self,
        custom_emoji_ids: list[str],
        **other: typing.Any,
    ) -> Result[list[Sticker], APIError]:
        """Method `getCustomEmojiStickers`, see the [documentation](https://core.telegram.org/bots/api#getcustomemojistickers)

        Use this method to get information about custom emoji stickers by their 
        identifiers. Returns an Array of Sticker objects.

        :param custom_emoji_ids: A JSON-serialized list of custom emoji identifiers. At most 200 custom \
        emoji identifiers can be specified.
        """

        method_response = await self.api.request_raw(
            "getCustomEmojiStickers",
            get_params(locals()),
        )
        return full_result(method_response, list[Sticker])

    async def upload_sticker_file(
        self,
        user_id: int,
        sticker: InputFile,
        sticker_format: typing.Literal["static", "animated", "video"],
        **other: typing.Any,
    ) -> Result[File, APIError]:
        """Method `uploadStickerFile`, see the [documentation](https://core.telegram.org/bots/api#uploadstickerfile)

        Use this method to upload a file with a sticker for later use in the createNewStickerSet, 
        addStickerToSet, or replaceStickerInSet methods (the file can be used 
        multiple times). Returns the uploaded File on success.

        :param user_id: User identifier of sticker file owner.

        :param sticker: A file with the sticker in .WEBP, .PNG, .TGS, or .WEBM format. See https://core.telegram.org/stickers \
        for technical requirements. More information on Sending Files: https://core.telegram.org/bots/api#sending-files. \

        :param sticker_format: Format of the sticker, must be one of `static`, `animated`, `video`.
        """

        method_response = await self.api.request_raw(
            "uploadStickerFile",
            get_params(locals()),
        )
        return full_result(method_response, File)

    async def create_new_sticker_set(
        self,
        user_id: int,
        name: str,
        title: str,
        stickers: list[InputSticker],
        sticker_type: typing.Literal["regular", "mask", "custom_emoji"] | None = None,
        needs_repainting: bool | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `createNewStickerSet`, see the [documentation](https://core.telegram.org/bots/api#createnewstickerset)

        Use this method to create a new sticker set owned by a user. The bot will be 
        able to edit the sticker set thus created. Returns True on success.

        :param user_id: User identifier of created sticker set owner.

        :param name: Short name of sticker set, to be used in t.me/addstickers/ URLs (e.g., animals). \
        Can contain only English letters, digits and underscores. Must begin with \
        a letter, can't contain consecutive underscores and must end in `_by_<bot_username>`. \
        <bot_username> is case insensitive. 1-64 characters.

        :param title: Sticker set title, 1-64 characters.

        :param stickers: A JSON-serialized list of 1-50 initial stickers to be added to the sticker \
        set.

        :param sticker_type: Type of stickers in the set, pass `regular`, `mask`, or `custom_emoji`. \
        By default, a regular sticker set is created.

        :param needs_repainting: Pass True if stickers in the sticker set must be repainted to the color of \
        text when used in messages, the accent color if used as emoji status, white \
        on chat photos, or another appropriate color based on context; for custom \
        emoji sticker sets only.
        """

        method_response = await self.api.request_raw(
            "createNewStickerSet",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def add_sticker_to_set(
        self,
        user_id: int,
        name: str,
        sticker: InputSticker,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `addStickerToSet`, see the [documentation](https://core.telegram.org/bots/api#addstickertoset)

        Use this method to add a new sticker to a set created by the bot. Emoji sticker 
        sets can have up to 200 stickers. Other sticker sets can have up to 120 stickers. 
        Returns True on success.

        :param user_id: User identifier of sticker set owner.

        :param name: Sticker set name.

        :param sticker: A JSON-serialized object with information about the added sticker. If \
        exactly the same sticker had already been added to the set, then the set isn't \
        changed.
        """

        method_response = await self.api.request_raw(
            "addStickerToSet",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def set_sticker_position_in_set(
        self,
        sticker: str,
        position: int,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `setStickerPositionInSet`, see the [documentation](https://core.telegram.org/bots/api#setstickerpositioninset)

        Use this method to move a sticker in a set created by the bot to a specific position.
        Returns True on success.

        :param sticker: File identifier of the sticker.

        :param position: New sticker position in the set, zero-based.
        """

        method_response = await self.api.request_raw(
            "setStickerPositionInSet",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def delete_sticker_from_set(
        self,
        sticker: str,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `deleteStickerFromSet`, see the [documentation](https://core.telegram.org/bots/api#deletestickerfromset)

        Use this method to delete a sticker from a set created by the bot. Returns
        True on success.

        :param sticker: File identifier of the sticker.
        """

        method_response = await self.api.request_raw(
            "deleteStickerFromSet",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def replace_sticker_in_set(
        self,
        user_id: int,
        name: str,
        old_sticker: str,
        sticker: InputSticker,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `replaceStickerInSet`, see the [documentation](https://core.telegram.org/bots/api#replacestickerinset)

        Use this method to replace an existing sticker in a sticker set with a new 
        one. The method is equivalent to calling deleteStickerFromSet, then addStickerToSet, 
        then setStickerPositionInSet. Returns True on success.

        :param user_id: User identifier of the sticker set owner.

        :param name: Sticker set name.

        :param old_sticker: File identifier of the replaced sticker.

        :param sticker: A JSON-serialized object with information about the added sticker. If \
        exactly the same sticker had already been added to the set, then the set remains \
        unchanged.
        """

        method_response = await self.api.request_raw(
            "replaceStickerInSet",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def set_sticker_emoji_list(
        self,
        sticker: str,
        emoji_list: list[str],
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `setStickerEmojiList`, see the [documentation](https://core.telegram.org/bots/api#setstickeremojilist)

        Use this method to change the list of emoji assigned to a regular or custom
        emoji sticker. The sticker must belong to a sticker set created by the bot.
        Returns True on success.

        :param sticker: File identifier of the sticker.

        :param emoji_list: A JSON-serialized list of 1-20 emoji associated with the sticker.
        """

        method_response = await self.api.request_raw(
            "setStickerEmojiList",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def set_sticker_keywords(
        self,
        sticker: str,
        keywords: list[str] | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `setStickerKeywords`, see the [documentation](https://core.telegram.org/bots/api#setstickerkeywords)

        Use this method to change search keywords assigned to a regular or custom 
        emoji sticker. The sticker must belong to a sticker set created by the bot. 
        Returns True on success.

        :param sticker: File identifier of the sticker.

        :param keywords: A JSON-serialized list of 0-20 search keywords for the sticker with total \
        length of up to 64 characters.
        """

        method_response = await self.api.request_raw(
            "setStickerKeywords",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def set_sticker_mask_position(
        self,
        sticker: str,
        mask_position: MaskPosition | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `setStickerMaskPosition`, see the [documentation](https://core.telegram.org/bots/api#setstickermaskposition)

        Use this method to change the mask position of a mask sticker. The sticker 
        must belong to a sticker set that was created by the bot. Returns True on success.

        :param sticker: File identifier of the sticker.

        :param mask_position: A JSON-serialized object with the position where the mask should be placed \
        on faces. Omit the parameter to remove the mask position.
        """

        method_response = await self.api.request_raw(
            "setStickerMaskPosition",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def set_sticker_set_title(
        self,
        name: str,
        title: str,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `setStickerSetTitle`, see the [documentation](https://core.telegram.org/bots/api#setstickersettitle)

        Use this method to set the title of a created sticker set. Returns True on
        success.

        :param name: Sticker set name.

        :param title: Sticker set title, 1-64 characters.
        """

        method_response = await self.api.request_raw(
            "setStickerSetTitle",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def set_sticker_set_thumbnail(
        self,
        name: str,
        user_id: int,
        format: str,
        thumbnail: InputFile | str | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `setStickerSetThumbnail`, see the [documentation](https://core.telegram.org/bots/api#setstickersetthumbnail)

        Use this method to set the thumbnail of a regular or mask sticker set. The 
        format of the thumbnail file must match the format of the stickers in the 
        set. Returns True on success.

        :param name: Sticker set name.

        :param user_id: User identifier of the sticker set owner.

        :param thumbnail: A .WEBP or .PNG image with the thumbnail, must be up to 128 kilobytes in size \
        and have a width and height of exactly 100px, or a .TGS animation with a thumbnail \
        up to 32 kilobytes in size (see https://core.telegram.org/stickers#animated-sticker-requirements \
        for animated sticker technical requirements), or a WEBM video with the \
        thumbnail up to 32 kilobytes in size; see https://core.telegram.org/stickers#video-sticker-requirements \
        for video sticker technical requirements. Pass a file_id as a String to \
        send a file that already exists on the Telegram servers, pass an HTTP URL \
        as a String for Telegram to get a file from the Internet, or upload a new one \
        using multipart/form-data. More information on Sending Files: https://core.telegram.org/bots/api#sending-files. \
        Animated and video sticker set thumbnails can't be uploaded via HTTP URL. \
        If omitted, then the thumbnail is dropped and the first sticker is used as \
        the thumbnail.

        :param format: Format of the thumbnail, must be one of `static` for a .WEBP or .PNG image, \
        `animated` for a .TGS animation, or `video` for a WEBM video.
        """

        method_response = await self.api.request_raw(
            "setStickerSetThumbnail",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def set_custom_emoji_sticker_set_thumbnail(
        self,
        name: str,
        custom_emoji_id: str | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `setCustomEmojiStickerSetThumbnail`, see the [documentation](https://core.telegram.org/bots/api#setcustomemojistickersetthumbnail)

        Use this method to set the thumbnail of a custom emoji sticker set. Returns 
        True on success.

        :param name: Sticker set name.

        :param custom_emoji_id: Custom emoji identifier of a sticker from the sticker set; pass an empty \
        string to drop the thumbnail and use the first sticker as the thumbnail. \
        """

        method_response = await self.api.request_raw(
            "setCustomEmojiStickerSetThumbnail",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def delete_sticker_set(
        self,
        name: str,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `deleteStickerSet`, see the [documentation](https://core.telegram.org/bots/api#deletestickerset)

        Use this method to delete a sticker set that was created by the bot. Returns
        True on success.

        :param name: Sticker set name.
        """

        method_response = await self.api.request_raw(
            "deleteStickerSet",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def answer_inline_query(
        self,
        inline_query_id: str,
        results: list[InlineQueryResult],
        cache_time: int | None = None,
        is_personal: bool | None = None,
        next_offset: str | None = None,
        button: InlineQueryResultsButton | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `answerInlineQuery`, see the [documentation](https://core.telegram.org/bots/api#answerinlinequery)

        Use this method to send answers to an inline query. On success, True is returned. 
        No more than 50 results per query are allowed.

        :param inline_query_id: Unique identifier for the answered query.

        :param results: A JSON-serialized array of results for the inline query.

        :param cache_time: The maximum amount of time in seconds that the result of the inline query \
        may be cached on the server. Defaults to 300.

        :param is_personal: Pass True if results may be cached on the server side only for the user that \
        sent the query. By default, results may be returned to any user who sends \
        the same query.

        :param next_offset: Pass the offset that a client should send in the next query with the same text \
        to receive more results. Pass an empty string if there are no more results \
        or if you don't support pagination. Offset length can't exceed 64 bytes. \

        :param button: A JSON-serialized object describing a button to be shown above inline query \
        results.
        """

        method_response = await self.api.request_raw(
            "answerInlineQuery",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def answer_web_app_query(
        self,
        web_app_query_id: str,
        result: InlineQueryResult,
        **other: typing.Any,
    ) -> Result[SentWebAppMessage, APIError]:
        """Method `answerWebAppQuery`, see the [documentation](https://core.telegram.org/bots/api#answerwebappquery)

        Use this method to set the result of an interaction with a Web App and send
        a corresponding message on behalf of the user to the chat from which the query
        originated. On success, a SentWebAppMessage object is returned.

        :param web_app_query_id: Unique identifier for the query to be answered.

        :param result: A JSON-serialized object describing the message to be sent.
        """

        method_response = await self.api.request_raw(
            "answerWebAppQuery",
            get_params(locals()),
        )
        return full_result(method_response, SentWebAppMessage)

    async def send_invoice(
        self,
        chat_id: int | str,
        title: str,
        description: str,
        payload: str,
        currency: str,
        prices: list[LabeledPrice],
        message_thread_id: int | None = None,
        provider_token: str | None = None,
        max_tip_amount: int | None = None,
        suggested_tip_amounts: list[int] | None = None,
        start_parameter: str | None = None,
        provider_data: str | None = None,
        photo_url: str | None = None,
        photo_size: int | None = None,
        photo_width: int | None = None,
        photo_height: int | None = None,
        need_name: bool | None = None,
        need_phone_number: bool | None = None,
        need_email: bool | None = None,
        need_shipping_address: bool | None = None,
        send_phone_number_to_provider: bool | None = None,
        send_email_to_provider: bool | None = None,
        is_flexible: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
        **other: typing.Any,
    ) -> Result[Message, APIError]:
        """Method `sendInvoice`, see the [documentation](https://core.telegram.org/bots/api#sendinvoice)

        Use this method to send invoices. On success, the sent Message is returned.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for \
        forum supergroups only.

        :param title: Product name, 1-32 characters.

        :param description: Product description, 1-255 characters.

        :param payload: Bot-defined invoice payload, 1-128 bytes. This will not be displayed to \
        the user, use for your internal processes.

        :param provider_token: Payment provider token, obtained via @BotFather. Pass an empty string \
        for payments in Telegram Stars.

        :param currency: Three-letter ISO 4217 currency code, see more on currencies. Pass `XTR` \
        for payments in Telegram Stars.

        :param prices: Price breakdown, a JSON-serialized list of components (e.g. product price, \
        tax, discount, delivery cost, delivery tax, bonus, etc.). Must contain \
        exactly one item for payments in Telegram Stars.

        :param max_tip_amount: The maximum accepted amount for tips in the smallest units of the currency \
        (integer, not float/double). For example, for a maximum tip of US$ 1.45 \
        pass max_tip_amount = 145. See the exp parameter in currencies.json, it \
        shows the number of digits past the decimal point for each currency (2 for \
        the majority of currencies). Defaults to 0. Not supported for payments \
        in Telegram Stars.

        :param suggested_tip_amounts: A JSON-serialized array of suggested amounts of tips in the smallest units \
        of the currency (integer, not float/double). At most 4 suggested tip amounts \
        can be specified. The suggested tip amounts must be positive, passed in \
        a strictly increased order and must not exceed max_tip_amount.

        :param start_parameter: Unique deep-linking parameter. If left empty, forwarded copies of the \
        sent message will have a Pay button, allowing multiple users to pay directly \
        from the forwarded message, using the same invoice. If non-empty, forwarded \
        copies of the sent message will have a URL button with a deep link to the bot \
        (instead of a Pay button), with the value used as the start parameter.

        :param provider_data: JSON-serialized data about the invoice, which will be shared with the payment \
        provider. A detailed description of required fields should be provided \
        by the payment provider.

        :param photo_url: URL of the product photo for the invoice. Can be a photo of the goods or a marketing \
        image for a service. People like it better when they see what they are paying \
        for.

        :param photo_size: Photo size in bytes.

        :param photo_width: Photo width.

        :param photo_height: Photo height.

        :param need_name: Pass True if you require the user's full name to complete the order. Ignored \
        for payments in Telegram Stars.

        :param need_phone_number: Pass True if you require the user's phone number to complete the order. Ignored \
        for payments in Telegram Stars.

        :param need_email: Pass True if you require the user's email address to complete the order. \
        Ignored for payments in Telegram Stars.

        :param need_shipping_address: Pass True if you require the user's shipping address to complete the order. \
        Ignored for payments in Telegram Stars.

        :param send_phone_number_to_provider: Pass True if the user's phone number should be sent to the provider. Ignored \
        for payments in Telegram Stars.

        :param send_email_to_provider: Pass True if the user's email address should be sent to the provider. Ignored \
        for payments in Telegram Stars.

        :param is_flexible: Pass True if the final price depends on the shipping method. Ignored for \
        payments in Telegram Stars.

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound. \

        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for private \
        chats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: A JSON-serialized object for an inline keyboard. If empty, one 'Pay total \
        price' button will be shown. If not empty, the first button must be a Pay button. \
        """

        method_response = await self.api.request_raw(
            "sendInvoice",
            get_params(locals()),
        )
        return full_result(method_response, Message)

    async def create_invoice_link(
        self,
        title: str,
        description: str,
        payload: str,
        currency: str,
        prices: list[LabeledPrice],
        provider_token: str | None = None,
        max_tip_amount: int | None = None,
        suggested_tip_amounts: list[int] | None = None,
        provider_data: str | None = None,
        photo_url: str | None = None,
        photo_size: int | None = None,
        photo_width: int | None = None,
        photo_height: int | None = None,
        need_name: bool | None = None,
        need_phone_number: bool | None = None,
        need_email: bool | None = None,
        need_shipping_address: bool | None = None,
        send_phone_number_to_provider: bool | None = None,
        send_email_to_provider: bool | None = None,
        is_flexible: bool | None = None,
        **other: typing.Any,
    ) -> Result[str, APIError]:
        """Method `createInvoiceLink`, see the [documentation](https://core.telegram.org/bots/api#createinvoicelink)

        Use this method to create a link for an invoice. Returns the created invoice 
        link as String on success.

        :param title: Product name, 1-32 characters.

        :param description: Product description, 1-255 characters.

        :param payload: Bot-defined invoice payload, 1-128 bytes. This will not be displayed to \
        the user, use for your internal processes.

        :param provider_token: Payment provider token, obtained via @BotFather. Pass an empty string \
        for payments in Telegram Stars.

        :param currency: Three-letter ISO 4217 currency code, see more on currencies. Pass `XTR` \
        for payments in Telegram Stars.

        :param prices: Price breakdown, a JSON-serialized list of components (e.g. product price, \
        tax, discount, delivery cost, delivery tax, bonus, etc.). Must contain \
        exactly one item for payments in Telegram Stars.

        :param max_tip_amount: The maximum accepted amount for tips in the smallest units of the currency \
        (integer, not float/double). For example, for a maximum tip of US$ 1.45 \
        pass max_tip_amount = 145. See the exp parameter in currencies.json, it \
        shows the number of digits past the decimal point for each currency (2 for \
        the majority of currencies). Defaults to 0. Not supported for payments \
        in Telegram Stars.

        :param suggested_tip_amounts: A JSON-serialized array of suggested amounts of tips in the smallest units \
        of the currency (integer, not float/double). At most 4 suggested tip amounts \
        can be specified. The suggested tip amounts must be positive, passed in \
        a strictly increased order and must not exceed max_tip_amount.

        :param provider_data: JSON-serialized data about the invoice, which will be shared with the payment \
        provider. A detailed description of required fields should be provided \
        by the payment provider.

        :param photo_url: URL of the product photo for the invoice. Can be a photo of the goods or a marketing \
        image for a service.

        :param photo_size: Photo size in bytes.

        :param photo_width: Photo width.

        :param photo_height: Photo height.

        :param need_name: Pass True if you require the user's full name to complete the order. Ignored \
        for payments in Telegram Stars.

        :param need_phone_number: Pass True if you require the user's phone number to complete the order. Ignored \
        for payments in Telegram Stars.

        :param need_email: Pass True if you require the user's email address to complete the order. \
        Ignored for payments in Telegram Stars.

        :param need_shipping_address: Pass True if you require the user's shipping address to complete the order. \
        Ignored for payments in Telegram Stars.

        :param send_phone_number_to_provider: Pass True if the user's phone number should be sent to the provider. Ignored \
        for payments in Telegram Stars.

        :param send_email_to_provider: Pass True if the user's email address should be sent to the provider. Ignored \
        for payments in Telegram Stars.

        :param is_flexible: Pass True if the final price depends on the shipping method. Ignored for \
        payments in Telegram Stars.
        """

        method_response = await self.api.request_raw(
            "createInvoiceLink",
            get_params(locals()),
        )
        return full_result(method_response, str)

    async def answer_shipping_query(
        self,
        shipping_query_id: str,
        ok: bool,
        shipping_options: list[ShippingOption] | None = None,
        error_message: str | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `answerShippingQuery`, see the [documentation](https://core.telegram.org/bots/api#answershippingquery)

        If you sent an invoice requesting a shipping address and the parameter is_flexible 
        was specified, the Bot API will send an Update with a shipping_query field 
        to the bot. Use this method to reply to shipping queries. On success, True 
        is returned.

        :param shipping_query_id: Unique identifier for the query to be answered.

        :param ok: Pass True if delivery to the specified address is possible and False if there \
        are any problems (for example, if delivery to the specified address is not \
        possible).

        :param shipping_options: Required if ok is True. A JSON-serialized array of available shipping options. \

        :param error_message: Required if ok is False. Error message in human readable form that explains \
        why it is impossible to complete the order (e.g. `Sorry, delivery to your \
        desired address is unavailable'). Telegram will display this message \
        to the user.
        """

        method_response = await self.api.request_raw(
            "answerShippingQuery",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def answer_pre_checkout_query(
        self,
        pre_checkout_query_id: str,
        ok: bool,
        error_message: str | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `answerPreCheckoutQuery`, see the [documentation](https://core.telegram.org/bots/api#answerprecheckoutquery)

        Once the user has confirmed their payment and shipping details, the Bot 
        API sends the final confirmation in the form of an Update with the field pre_checkout_query. 
        Use this method to respond to such pre-checkout queries. On success, True 
        is returned. Note: The Bot API must receive an answer within 10 seconds after 
        the pre-checkout query was sent.

        :param pre_checkout_query_id: Unique identifier for the query to be answered.

        :param ok: Specify True if everything is alright (goods are available, etc.) and the \
        bot is ready to proceed with the order. Use False if there are any problems. \

        :param error_message: Required if ok is False. Error message in human readable form that explains \
        the reason for failure to proceed with the checkout (e.g. `Sorry, somebody \
        just bought the last of our amazing black T-shirts while you were busy filling \
        out your payment details. Please choose a different color or garment!`). \
        Telegram will display this message to the user.
        """

        method_response = await self.api.request_raw(
            "answerPreCheckoutQuery",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def get_star_transactions(
        self,
        offset: int | None = None,
        limit: int | None = None,
        **other: typing.Any,
    ) -> Result[StarTransactions, APIError]:
        """Method `getStarTransactions`, see the [documentation](https://core.telegram.org/bots/api#getstartransactions)

        Returns the bot's Telegram Star transactions in chronological order. 
        On success, returns a StarTransactions object.

        :param offset: Number of transactions to skip in the response.

        :param limit: The maximum number of transactions to be retrieved. Values between 1-100 \
        are accepted. Defaults to 100.
        """

        method_response = await self.api.request_raw(
            "getStarTransactions",
            get_params(locals()),
        )
        return full_result(method_response, StarTransactions)

    async def refund_star_payment(
        self,
        user_id: int,
        telegram_payment_charge_id: str,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `refundStarPayment`, see the [documentation](https://core.telegram.org/bots/api#refundstarpayment)

        Refunds a successful payment in Telegram Stars. Returns True on success.

        :param user_id: Identifier of the user whose payment will be refunded.

        :param telegram_payment_charge_id: Telegram payment identifier.
        """

        method_response = await self.api.request_raw(
            "refundStarPayment",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def set_passport_data_errors(
        self,
        user_id: int,
        errors: list[PassportElementError],
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Method `setPassportDataErrors`, see the [documentation](https://core.telegram.org/bots/api#setpassportdataerrors)

        Informs a user that some of the Telegram Passport elements they provided
        contains errors. The user will not be able to re-submit their Passport to
        you until the errors are fixed (the contents of the field for which you returned
        the error must change). Returns True on success. Use this if the data submitted
        by the user doesn't satisfy the standards your service requires for any
        reason. For example, if a birthday date seems invalid, a submitted document
        is blurry, a scan shows evidence of tampering, etc. Supply some details
        in the error message to make sure the user knows how to correct the issues.

        :param user_id: User identifier.

        :param errors: A JSON-serialized array describing the errors.
        """

        method_response = await self.api.request_raw(
            "setPassportDataErrors",
            get_params(locals()),
        )
        return full_result(method_response, bool)

    async def send_game(
        self,
        chat_id: int,
        game_short_name: str,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
        **other: typing.Any,
    ) -> Result[Message, APIError]:
        """Method `sendGame`, see the [documentation](https://core.telegram.org/bots/api#sendgame)

        Use this method to send a game. On success, the sent Message is returned.

        :param business_connection_id: Unique identifier of the business connection on behalf of which the message \
        will be sent.

        :param chat_id: Unique identifier for the target chat.

        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for \
        forum supergroups only.

        :param game_short_name: Short name of the game, serves as the unique identifier for the game. Set \
        up your games via @BotFather.

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound. \

        :param protect_content: Protects the contents of the sent message from forwarding and saving.

        :param message_effect_id: Unique identifier of the message effect to be added to the message; for private \
        chats only.

        :param reply_parameters: Description of the message to reply to.

        :param reply_markup: A JSON-serialized object for an inline keyboard. If empty, one 'Play game_title' \
        button will be shown. If not empty, the first button must launch the game. \
        """

        method_response = await self.api.request_raw(
            "sendGame",
            get_params(locals()),
        )
        return full_result(method_response, Message)

    async def set_game_score(
        self,
        user_id: int,
        score: int,
        force: bool | None = None,
        disable_edit_message: bool | None = None,
        chat_id: int | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
        **other: typing.Any,
    ) -> Result[Variative[Message, bool], APIError]:
        """Method `setGameScore`, see the [documentation](https://core.telegram.org/bots/api#setgamescore)

        Use this method to set the score of the specified user in a game message. On 
        success, if the message is not an inline message, the Message is returned, 
        otherwise True is returned. Returns an error, if the new score is not greater 
        than the user's current score in the chat and force is False.

        :param user_id: User identifier.

        :param score: New score, must be non-negative.

        :param force: Pass True if the high score is allowed to decrease. This can be useful when \
        fixing mistakes or banning cheaters.

        :param disable_edit_message: Pass True if the game message should not be automatically edited to include \
        the current scoreboard.

        :param chat_id: Required if inline_message_id is not specified. Unique identifier for \
        the target chat.

        :param message_id: Required if inline_message_id is not specified. Identifier of the sent \
        message.

        :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the \
        inline message.
        """

        method_response = await self.api.request_raw(
            "setGameScore",
            get_params(locals()),
        )
        return full_result(method_response, Variative[Message, bool])

    async def get_game_high_scores(
        self,
        user_id: int,
        chat_id: int | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
        **other: typing.Any,
    ) -> Result[list[GameHighScore], APIError]:
        """Method `getGameHighScores`, see the [documentation](https://core.telegram.org/bots/api#getgamehighscores)

        Use this method to get data for high score tables. Will return the score of 
        the specified user and several of their neighbors in a game. Returns an Array 
        of GameHighScore objects.

        :param user_id: Target user id.

        :param chat_id: Required if inline_message_id is not specified. Unique identifier for \
        the target chat.

        :param message_id: Required if inline_message_id is not specified. Identifier of the sent \
        message.

        :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the \
        inline message.
        """

        method_response = await self.api.request_raw(
            "getGameHighScores",
            get_params(locals()),
        )
        return full_result(method_response, list[GameHighScore])
