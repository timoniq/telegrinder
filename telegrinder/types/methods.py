import typing

from telegrinder.api.error import APIError
from telegrinder.option import Nothing, Some
from telegrinder.option.msgspec_option import Option
from telegrinder.result import Result

from .objects import *

if typing.TYPE_CHECKING:
    from telegrinder.api.abc import ABCAPI

X = typing.TypeVar("X")
Value = typing.TypeVar("Value")
OptionType = Option[Value] | Some[Value] | type(Nothing)


class APIMethods:
    def __init__(self, api: "ABCAPI"):
        self.api = api

    async def get_updates(
        self,
        offset: int | OptionType[int] | None = None,
        limit: int | OptionType[int] | None = None,
        timeout: int | OptionType[int] | None = None,
        allowed_updates: list[str] | OptionType[list[str]] | None = None,
        **other
    ) -> Result[list[Update], APIError]:
        result = await self.api.request_raw("getUpdates", get_params(locals()))
        return full_result(result, list[Update])

    async def set_webhook(
        self,
        url: str | OptionType[str] | None = None,
        certificate: InputFile | OptionType[InputFile] | None = None,
        ip_address: str | OptionType[str] | None = None,
        max_connections: int | OptionType[int] | None = None,
        allowed_updates: list[str] | OptionType[list[str]] | None = None,
        drop_pending_updates: bool | OptionType[bool] | None = None,
        secret_token: str | OptionType[str] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("setWebhook", get_params(locals()))
        return full_result(result, bool)

    async def delete_webhook(
        self, drop_pending_updates: bool | OptionType[bool] | None = None, **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("deleteWebhook", get_params(locals()))
        return full_result(result, bool)

    async def get_webhook_info(self, **other) -> Result[WebhookInfo, APIError]:
        result = await self.api.request_raw("getWebhookInfo", get_params(locals()))
        return full_result(result, WebhookInfo)

    async def get_me(self, **other) -> Result[User, APIError]:
        result = await self.api.request_raw("getMe", get_params(locals()))
        return full_result(result, User)

    async def log_out(self, **other) -> Result[bool, APIError]:
        result = await self.api.request_raw("logOut", get_params(locals()))
        return full_result(result, bool)

    async def close(self, **other) -> Result[bool, APIError]:
        result = await self.api.request_raw("close", get_params(locals()))
        return full_result(result, bool)

    async def send_message(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_thread_id: int | OptionType[int] | None = None,
        text: str | OptionType[str] | None = None,
        parse_mode: str | OptionType[str] | None = None,
        entities: list[MessageEntity] | OptionType[list[MessageEntity]] | None = None,
        disable_web_page_preview: bool | OptionType[bool] | None = None,
        disable_notification: bool | OptionType[bool] | None = None,
        protect_content: bool | OptionType[bool] | None = None,
        reply_to_message_id: int | OptionType[int] | None = None,
        allow_sending_without_reply: bool | OptionType[bool] | None = None,
        reply_markup: typing.Union[
            InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply
        ]
        | OptionType[
            typing.Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ]
        | None = None,
        **other
    ) -> Result[Message, APIError]:
        result = await self.api.request_raw("sendMessage", get_params(locals()))
        return full_result(result, Message)

    async def forward_message(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_thread_id: int | OptionType[int] | None = None,
        from_chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        disable_notification: bool | OptionType[bool] | None = None,
        protect_content: bool | OptionType[bool] | None = None,
        message_id: int | OptionType[int] | None = None,
        **other
    ) -> Result[Message, APIError]:
        result = await self.api.request_raw("forwardMessage", get_params(locals()))
        return full_result(result, Message)

    async def copy_message(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_thread_id: int | OptionType[int] | None = None,
        from_chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_id: int | OptionType[int] | None = None,
        caption: str | OptionType[str] | None = None,
        parse_mode: str | OptionType[str] | None = None,
        caption_entities: list[MessageEntity]
        | OptionType[list[MessageEntity]]
        | None = None,
        disable_notification: bool | OptionType[bool] | None = None,
        protect_content: bool | OptionType[bool] | None = None,
        reply_to_message_id: int | OptionType[int] | None = None,
        allow_sending_without_reply: bool | OptionType[bool] | None = None,
        reply_markup: typing.Union[
            InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply
        ]
        | OptionType[
            typing.Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ]
        | None = None,
        **other
    ) -> Result[MessageId, APIError]:
        result = await self.api.request_raw("copyMessage", get_params(locals()))
        return full_result(result, MessageId)

    async def send_photo(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_thread_id: int | OptionType[int] | None = None,
        photo: typing.Union[InputFile, str]
        | OptionType[typing.Union[InputFile, str]]
        | None = None,
        caption: str | OptionType[str] | None = None,
        parse_mode: str | OptionType[str] | None = None,
        caption_entities: list[MessageEntity]
        | OptionType[list[MessageEntity]]
        | None = None,
        has_spoiler: bool | OptionType[bool] | None = None,
        disable_notification: bool | OptionType[bool] | None = None,
        protect_content: bool | OptionType[bool] | None = None,
        reply_to_message_id: int | OptionType[int] | None = None,
        allow_sending_without_reply: bool | OptionType[bool] | None = None,
        reply_markup: typing.Union[
            InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply
        ]
        | OptionType[
            typing.Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ]
        | None = None,
        **other
    ) -> Result[Message, APIError]:
        result = await self.api.request_raw("sendPhoto", get_params(locals()))
        return full_result(result, Message)

    async def send_audio(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_thread_id: int | OptionType[int] | None = None,
        audio: typing.Union[InputFile, str]
        | OptionType[typing.Union[InputFile, str]]
        | None = None,
        caption: str | OptionType[str] | None = None,
        parse_mode: str | OptionType[str] | None = None,
        caption_entities: list[MessageEntity]
        | OptionType[list[MessageEntity]]
        | None = None,
        duration: int | OptionType[int] | None = None,
        performer: str | OptionType[str] | None = None,
        title: str | OptionType[str] | None = None,
        thumbnail: typing.Union[InputFile, str]
        | OptionType[typing.Union[InputFile, str]]
        | None = None,
        disable_notification: bool | OptionType[bool] | None = None,
        protect_content: bool | OptionType[bool] | None = None,
        reply_to_message_id: int | OptionType[int] | None = None,
        allow_sending_without_reply: bool | OptionType[bool] | None = None,
        reply_markup: typing.Union[
            InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply
        ]
        | OptionType[
            typing.Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ]
        | None = None,
        **other
    ) -> Result[Message, APIError]:
        result = await self.api.request_raw("sendAudio", get_params(locals()))
        return full_result(result, Message)

    async def send_document(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_thread_id: int | OptionType[int] | None = None,
        document: typing.Union[InputFile, str]
        | OptionType[typing.Union[InputFile, str]]
        | None = None,
        thumbnail: typing.Union[InputFile, str]
        | OptionType[typing.Union[InputFile, str]]
        | None = None,
        caption: str | OptionType[str] | None = None,
        parse_mode: str | OptionType[str] | None = None,
        caption_entities: list[MessageEntity]
        | OptionType[list[MessageEntity]]
        | None = None,
        disable_content_type_detection: bool | OptionType[bool] | None = None,
        disable_notification: bool | OptionType[bool] | None = None,
        protect_content: bool | OptionType[bool] | None = None,
        reply_to_message_id: int | OptionType[int] | None = None,
        allow_sending_without_reply: bool | OptionType[bool] | None = None,
        reply_markup: typing.Union[
            InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply
        ]
        | OptionType[
            typing.Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ]
        | None = None,
        **other
    ) -> Result[Message, APIError]:
        result = await self.api.request_raw("sendDocument", get_params(locals()))
        return full_result(result, Message)

    async def send_video(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_thread_id: int | OptionType[int] | None = None,
        video: typing.Union[InputFile, str]
        | OptionType[typing.Union[InputFile, str]]
        | None = None,
        duration: int | OptionType[int] | None = None,
        width: int | OptionType[int] | None = None,
        height: int | OptionType[int] | None = None,
        thumbnail: typing.Union[InputFile, str]
        | OptionType[typing.Union[InputFile, str]]
        | None = None,
        caption: str | OptionType[str] | None = None,
        parse_mode: str | OptionType[str] | None = None,
        caption_entities: list[MessageEntity]
        | OptionType[list[MessageEntity]]
        | None = None,
        has_spoiler: bool | OptionType[bool] | None = None,
        supports_streaming: bool | OptionType[bool] | None = None,
        disable_notification: bool | OptionType[bool] | None = None,
        protect_content: bool | OptionType[bool] | None = None,
        reply_to_message_id: int | OptionType[int] | None = None,
        allow_sending_without_reply: bool | OptionType[bool] | None = None,
        reply_markup: typing.Union[
            InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply
        ]
        | OptionType[
            typing.Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ]
        | None = None,
        **other
    ) -> Result[Message, APIError]:
        result = await self.api.request_raw("sendVideo", get_params(locals()))
        return full_result(result, Message)

    async def send_animation(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_thread_id: int | OptionType[int] | None = None,
        animation: typing.Union[InputFile, str]
        | OptionType[typing.Union[InputFile, str]]
        | None = None,
        duration: int | OptionType[int] | None = None,
        width: int | OptionType[int] | None = None,
        height: int | OptionType[int] | None = None,
        thumbnail: typing.Union[InputFile, str]
        | OptionType[typing.Union[InputFile, str]]
        | None = None,
        caption: str | OptionType[str] | None = None,
        parse_mode: str | OptionType[str] | None = None,
        caption_entities: list[MessageEntity]
        | OptionType[list[MessageEntity]]
        | None = None,
        has_spoiler: bool | OptionType[bool] | None = None,
        disable_notification: bool | OptionType[bool] | None = None,
        protect_content: bool | OptionType[bool] | None = None,
        reply_to_message_id: int | OptionType[int] | None = None,
        allow_sending_without_reply: bool | OptionType[bool] | None = None,
        reply_markup: typing.Union[
            InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply
        ]
        | OptionType[
            typing.Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ]
        | None = None,
        **other
    ) -> Result[Message, APIError]:
        result = await self.api.request_raw("sendAnimation", get_params(locals()))
        return full_result(result, Message)

    async def send_voice(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_thread_id: int | OptionType[int] | None = None,
        voice: typing.Union[InputFile, str]
        | OptionType[typing.Union[InputFile, str]]
        | None = None,
        caption: str | OptionType[str] | None = None,
        parse_mode: str | OptionType[str] | None = None,
        caption_entities: list[MessageEntity]
        | OptionType[list[MessageEntity]]
        | None = None,
        duration: int | OptionType[int] | None = None,
        disable_notification: bool | OptionType[bool] | None = None,
        protect_content: bool | OptionType[bool] | None = None,
        reply_to_message_id: int | OptionType[int] | None = None,
        allow_sending_without_reply: bool | OptionType[bool] | None = None,
        reply_markup: typing.Union[
            InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply
        ]
        | OptionType[
            typing.Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ]
        | None = None,
        **other
    ) -> Result[Message, APIError]:
        result = await self.api.request_raw("sendVoice", get_params(locals()))
        return full_result(result, Message)

    async def send_video_note(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_thread_id: int | OptionType[int] | None = None,
        video_note: typing.Union[InputFile, str]
        | OptionType[typing.Union[InputFile, str]]
        | None = None,
        duration: int | OptionType[int] | None = None,
        length: int | OptionType[int] | None = None,
        thumbnail: typing.Union[InputFile, str]
        | OptionType[typing.Union[InputFile, str]]
        | None = None,
        disable_notification: bool | OptionType[bool] | None = None,
        protect_content: bool | OptionType[bool] | None = None,
        reply_to_message_id: int | OptionType[int] | None = None,
        allow_sending_without_reply: bool | OptionType[bool] | None = None,
        reply_markup: typing.Union[
            InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply
        ]
        | OptionType[
            typing.Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ]
        | None = None,
        **other
    ) -> Result[Message, APIError]:
        result = await self.api.request_raw("sendVideoNote", get_params(locals()))
        return full_result(result, Message)

    async def send_media_group(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_thread_id: int | OptionType[int] | None = None,
        media: list[
            typing.Union[
                InputMediaAudio, InputMediaDocument, InputMediaPhoto, InputMediaVideo
            ]
        ]
        | OptionType[
            list[
                typing.Union[
                    InputMediaAudio,
                    InputMediaDocument,
                    InputMediaPhoto,
                    InputMediaVideo,
                ]
            ]
        ]
        | None = None,
        disable_notification: bool | OptionType[bool] | None = None,
        protect_content: bool | OptionType[bool] | None = None,
        reply_to_message_id: int | OptionType[int] | None = None,
        allow_sending_without_reply: bool | OptionType[bool] | None = None,
        **other
    ) -> Result[list[Message], APIError]:
        result = await self.api.request_raw("sendMediaGroup", get_params(locals()))
        return full_result(result, list[Message])

    async def send_location(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_thread_id: int | OptionType[int] | None = None,
        latitude: float | OptionType[float] | None = None,
        longitude: float | OptionType[float] | None = None,
        horizontal_accuracy: float | OptionType[float] | None = None,
        live_period: int | OptionType[int] | None = None,
        heading: int | OptionType[int] | None = None,
        proximity_alert_radius: int | OptionType[int] | None = None,
        disable_notification: bool | OptionType[bool] | None = None,
        protect_content: bool | OptionType[bool] | None = None,
        reply_to_message_id: int | OptionType[int] | None = None,
        allow_sending_without_reply: bool | OptionType[bool] | None = None,
        reply_markup: typing.Union[
            InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply
        ]
        | OptionType[
            typing.Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ]
        | None = None,
        **other
    ) -> Result[Message, APIError]:
        result = await self.api.request_raw("sendLocation", get_params(locals()))
        return full_result(result, Message)

    async def send_venue(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_thread_id: int | OptionType[int] | None = None,
        latitude: float | OptionType[float] | None = None,
        longitude: float | OptionType[float] | None = None,
        title: str | OptionType[str] | None = None,
        address: str | OptionType[str] | None = None,
        foursquare_id: str | OptionType[str] | None = None,
        foursquare_type: str | OptionType[str] | None = None,
        google_place_id: str | OptionType[str] | None = None,
        google_place_type: str | OptionType[str] | None = None,
        disable_notification: bool | OptionType[bool] | None = None,
        protect_content: bool | OptionType[bool] | None = None,
        reply_to_message_id: int | OptionType[int] | None = None,
        allow_sending_without_reply: bool | OptionType[bool] | None = None,
        reply_markup: typing.Union[
            InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply
        ]
        | OptionType[
            typing.Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ]
        | None = None,
        **other
    ) -> Result[Message, APIError]:
        result = await self.api.request_raw("sendVenue", get_params(locals()))
        return full_result(result, Message)

    async def send_contact(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_thread_id: int | OptionType[int] | None = None,
        phone_number: str | OptionType[str] | None = None,
        first_name: str | OptionType[str] | None = None,
        last_name: str | OptionType[str] | None = None,
        vcard: str | OptionType[str] | None = None,
        disable_notification: bool | OptionType[bool] | None = None,
        protect_content: bool | OptionType[bool] | None = None,
        reply_to_message_id: int | OptionType[int] | None = None,
        allow_sending_without_reply: bool | OptionType[bool] | None = None,
        reply_markup: typing.Union[
            InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply
        ]
        | OptionType[
            typing.Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ]
        | None = None,
        **other
    ) -> Result[Message, APIError]:
        result = await self.api.request_raw("sendContact", get_params(locals()))
        return full_result(result, Message)

    async def send_poll(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_thread_id: int | OptionType[int] | None = None,
        question: str | OptionType[str] | None = None,
        options: list[str] | OptionType[list[str]] | None = None,
        is_anonymous: bool | OptionType[bool] | None = None,
        type: str | OptionType[str] | None = None,
        allows_multiple_answers: bool | OptionType[bool] | None = None,
        correct_option_id: int | OptionType[int] | None = None,
        explanation: str | OptionType[str] | None = None,
        explanation_parse_mode: str | OptionType[str] | None = None,
        explanation_entities: list[MessageEntity]
        | OptionType[list[MessageEntity]]
        | None = None,
        open_period: int | OptionType[int] | None = None,
        close_date: int | OptionType[int] | None = None,
        is_closed: bool | OptionType[bool] | None = None,
        disable_notification: bool | OptionType[bool] | None = None,
        protect_content: bool | OptionType[bool] | None = None,
        reply_to_message_id: int | OptionType[int] | None = None,
        allow_sending_without_reply: bool | OptionType[bool] | None = None,
        reply_markup: typing.Union[
            InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply
        ]
        | OptionType[
            typing.Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ]
        | None = None,
        **other
    ) -> Result[Message, APIError]:
        result = await self.api.request_raw("sendPoll", get_params(locals()))
        return full_result(result, Message)

    async def send_dice(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_thread_id: int | OptionType[int] | None = None,
        emoji: str | OptionType[str] | None = None,
        disable_notification: bool | OptionType[bool] | None = None,
        protect_content: bool | OptionType[bool] | None = None,
        reply_to_message_id: int | OptionType[int] | None = None,
        allow_sending_without_reply: bool | OptionType[bool] | None = None,
        reply_markup: typing.Union[
            InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply
        ]
        | OptionType[
            typing.Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ]
        | None = None,
        **other
    ) -> Result[Message, APIError]:
        result = await self.api.request_raw("sendDice", get_params(locals()))
        return full_result(result, Message)

    async def send_chat_action(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_thread_id: int | OptionType[int] | None = None,
        action: str | OptionType[str] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("sendChatAction", get_params(locals()))
        return full_result(result, bool)

    async def get_user_profile_photos(
        self,
        user_id: int | OptionType[int] | None = None,
        offset: int | OptionType[int] | None = None,
        limit: int | OptionType[int] | None = None,
        **other
    ) -> Result[UserProfilePhotos, APIError]:
        result = await self.api.request_raw(
            "getUserProfilePhotos", get_params(locals())
        )
        return full_result(result, UserProfilePhotos)

    async def get_file(
        self, file_id: str | OptionType[str] | None = None, **other
    ) -> Result[File, APIError]:
        result = await self.api.request_raw("getFile", get_params(locals()))
        return full_result(result, File)

    async def ban_chat_member(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        user_id: int | OptionType[int] | None = None,
        until_date: int | OptionType[int] | None = None,
        revoke_messages: bool | OptionType[bool] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("banChatMember", get_params(locals()))
        return full_result(result, bool)

    async def unban_chat_member(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        user_id: int | OptionType[int] | None = None,
        only_if_banned: bool | OptionType[bool] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("unbanChatMember", get_params(locals()))
        return full_result(result, bool)

    async def restrict_chat_member(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        user_id: int | OptionType[int] | None = None,
        permissions: ChatPermissions | OptionType[ChatPermissions] | None = None,
        use_independent_chat_permissions: bool | OptionType[bool] | None = None,
        until_date: int | OptionType[int] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("restrictChatMember", get_params(locals()))
        return full_result(result, bool)

    async def promote_chat_member(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        user_id: int | OptionType[int] | None = None,
        is_anonymous: bool | OptionType[bool] | None = None,
        can_manage_chat: bool | OptionType[bool] | None = None,
        can_delete_messages: bool | OptionType[bool] | None = None,
        can_manage_video_chats: bool | OptionType[bool] | None = None,
        can_restrict_members: bool | OptionType[bool] | None = None,
        can_promote_members: bool | OptionType[bool] | None = None,
        can_change_info: bool | OptionType[bool] | None = None,
        can_invite_users: bool | OptionType[bool] | None = None,
        can_post_messages: bool | OptionType[bool] | None = None,
        can_edit_messages: bool | OptionType[bool] | None = None,
        can_pin_messages: bool | OptionType[bool] | None = None,
        can_post_stories: bool | OptionType[bool] | None = None,
        can_edit_stories: bool | OptionType[bool] | None = None,
        can_delete_stories: bool | OptionType[bool] | None = None,
        can_manage_topics: bool | OptionType[bool] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("promoteChatMember", get_params(locals()))
        return full_result(result, bool)

    async def set_chat_administrator_custom_title(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        user_id: int | OptionType[int] | None = None,
        custom_title: str | OptionType[str] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw(
            "setChatAdministratorCustomTitle", get_params(locals())
        )
        return full_result(result, bool)

    async def ban_chat_sender_chat(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        sender_chat_id: int | OptionType[int] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("banChatSenderChat", get_params(locals()))
        return full_result(result, bool)

    async def unban_chat_sender_chat(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        sender_chat_id: int | OptionType[int] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("unbanChatSenderChat", get_params(locals()))
        return full_result(result, bool)

    async def set_chat_permissions(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        permissions: ChatPermissions | OptionType[ChatPermissions] | None = None,
        use_independent_chat_permissions: bool | OptionType[bool] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("setChatPermissions", get_params(locals()))
        return full_result(result, bool)

    async def export_chat_invite_link(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        **other
    ) -> Result[str, APIError]:
        result = await self.api.request_raw(
            "exportChatInviteLink", get_params(locals())
        )
        return full_result(result, str)

    async def create_chat_invite_link(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        name: str | OptionType[str] | None = None,
        expire_date: int | OptionType[int] | None = None,
        member_limit: int | OptionType[int] | None = None,
        creates_join_request: bool | OptionType[bool] | None = None,
        **other
    ) -> Result[ChatInviteLink, APIError]:
        result = await self.api.request_raw(
            "createChatInviteLink", get_params(locals())
        )
        return full_result(result, ChatInviteLink)

    async def edit_chat_invite_link(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        invite_link: str | OptionType[str] | None = None,
        name: str | OptionType[str] | None = None,
        expire_date: int | OptionType[int] | None = None,
        member_limit: int | OptionType[int] | None = None,
        creates_join_request: bool | OptionType[bool] | None = None,
        **other
    ) -> Result[ChatInviteLink, APIError]:
        result = await self.api.request_raw("editChatInviteLink", get_params(locals()))
        return full_result(result, ChatInviteLink)

    async def revoke_chat_invite_link(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        invite_link: str | OptionType[str] | None = None,
        **other
    ) -> Result[ChatInviteLink, APIError]:
        result = await self.api.request_raw(
            "revokeChatInviteLink", get_params(locals())
        )
        return full_result(result, ChatInviteLink)

    async def approve_chat_join_request(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        user_id: int | OptionType[int] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw(
            "approveChatJoinRequest", get_params(locals())
        )
        return full_result(result, bool)

    async def decline_chat_join_request(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        user_id: int | OptionType[int] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw(
            "declineChatJoinRequest", get_params(locals())
        )
        return full_result(result, bool)

    async def set_chat_photo(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        photo: InputFile | OptionType[InputFile] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("setChatPhoto", get_params(locals()))
        return full_result(result, bool)

    async def delete_chat_photo(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("deleteChatPhoto", get_params(locals()))
        return full_result(result, bool)

    async def set_chat_title(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        title: str | OptionType[str] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("setChatTitle", get_params(locals()))
        return full_result(result, bool)

    async def set_chat_description(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        description: str | OptionType[str] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("setChatDescription", get_params(locals()))
        return full_result(result, bool)

    async def pin_chat_message(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_id: int | OptionType[int] | None = None,
        disable_notification: bool | OptionType[bool] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("pinChatMessage", get_params(locals()))
        return full_result(result, bool)

    async def unpin_chat_message(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_id: int | OptionType[int] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("unpinChatMessage", get_params(locals()))
        return full_result(result, bool)

    async def unpin_all_chat_messages(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw(
            "unpinAllChatMessages", get_params(locals())
        )
        return full_result(result, bool)

    async def leave_chat(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("leaveChat", get_params(locals()))
        return full_result(result, bool)

    async def get_chat(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        **other
    ) -> Result[Chat, APIError]:
        result = await self.api.request_raw("getChat", get_params(locals()))
        return full_result(result, Chat)

    async def get_chat_administrators(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        **other
    ) -> Result[list[ChatMember], APIError]:
        result = await self.api.request_raw(
            "getChatAdministrators", get_params(locals())
        )
        return full_result(result, list[ChatMember])

    async def get_chat_member_count(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        **other
    ) -> Result[int, APIError]:
        result = await self.api.request_raw("getChatMemberCount", get_params(locals()))
        return full_result(result, int)

    async def get_chat_member(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        user_id: int | OptionType[int] | None = None,
        **other
    ) -> Result[ChatMember, APIError]:
        result = await self.api.request_raw("getChatMember", get_params(locals()))
        return full_result(result, ChatMember)

    async def set_chat_sticker_set(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        sticker_set_name: str | OptionType[str] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("setChatStickerSet", get_params(locals()))
        return full_result(result, bool)

    async def delete_chat_sticker_set(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw(
            "deleteChatStickerSet", get_params(locals())
        )
        return full_result(result, bool)

    async def get_forum_topic_icon_stickers(
        self, **other
    ) -> Result[list[Sticker], APIError]:
        result = await self.api.request_raw(
            "getForumTopicIconStickers", get_params(locals())
        )
        return full_result(result, list[Sticker])

    async def create_forum_topic(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        name: str | OptionType[str] | None = None,
        icon_color: int | OptionType[int] | None = None,
        icon_custom_emoji_id: str | OptionType[str] | None = None,
        **other
    ) -> Result[ForumTopic, APIError]:
        result = await self.api.request_raw("createForumTopic", get_params(locals()))
        return full_result(result, ForumTopic)

    async def edit_forum_topic(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_thread_id: int | OptionType[int] | None = None,
        name: str | OptionType[str] | None = None,
        icon_custom_emoji_id: str | OptionType[str] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("editForumTopic", get_params(locals()))
        return full_result(result, bool)

    async def close_forum_topic(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_thread_id: int | OptionType[int] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("closeForumTopic", get_params(locals()))
        return full_result(result, bool)

    async def reopen_forum_topic(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_thread_id: int | OptionType[int] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("reopenForumTopic", get_params(locals()))
        return full_result(result, bool)

    async def delete_forum_topic(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_thread_id: int | OptionType[int] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("deleteForumTopic", get_params(locals()))
        return full_result(result, bool)

    async def unpin_all_forum_topic_messages(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_thread_id: int | OptionType[int] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw(
            "unpinAllForumTopicMessages", get_params(locals())
        )
        return full_result(result, bool)

    async def edit_general_forum_topic(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        name: str | OptionType[str] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw(
            "editGeneralForumTopic", get_params(locals())
        )
        return full_result(result, bool)

    async def close_general_forum_topic(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw(
            "closeGeneralForumTopic", get_params(locals())
        )
        return full_result(result, bool)

    async def reopen_general_forum_topic(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw(
            "reopenGeneralForumTopic", get_params(locals())
        )
        return full_result(result, bool)

    async def hide_general_forum_topic(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw(
            "hideGeneralForumTopic", get_params(locals())
        )
        return full_result(result, bool)

    async def unhide_general_forum_topic(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw(
            "unhideGeneralForumTopic", get_params(locals())
        )
        return full_result(result, bool)

    async def unpin_all_general_forum_topic_messages(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw(
            "unpinAllGeneralForumTopicMessages", get_params(locals())
        )
        return full_result(result, bool)

    async def answer_callback_query(
        self,
        callback_query_id: str | OptionType[str] | None = None,
        text: str | OptionType[str] | None = None,
        show_alert: bool | OptionType[bool] | None = None,
        url: str | OptionType[str] | None = None,
        cache_time: int | OptionType[int] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("answerCallbackQuery", get_params(locals()))
        return full_result(result, bool)

    async def set_my_commands(
        self,
        commands: list[BotCommand] | OptionType[list[BotCommand]] | None = None,
        scope: BotCommandScope | OptionType[BotCommandScope] | None = None,
        language_code: str | OptionType[str] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("setMyCommands", get_params(locals()))
        return full_result(result, bool)

    async def delete_my_commands(
        self,
        scope: BotCommandScope | OptionType[BotCommandScope] | None = None,
        language_code: str | OptionType[str] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("deleteMyCommands", get_params(locals()))
        return full_result(result, bool)

    async def get_my_commands(
        self,
        scope: BotCommandScope | OptionType[BotCommandScope] | None = None,
        language_code: str | OptionType[str] | None = None,
        **other
    ) -> Result[list[BotCommand], APIError]:
        result = await self.api.request_raw("getMyCommands", get_params(locals()))
        return full_result(result, list[BotCommand])

    async def set_my_name(
        self,
        name: str | OptionType[str] | None = None,
        language_code: str | OptionType[str] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("setMyName", get_params(locals()))
        return full_result(result, bool)

    async def get_my_name(
        self, language_code: str | OptionType[str] | None = None, **other
    ) -> Result[BotName, APIError]:
        result = await self.api.request_raw("getMyName", get_params(locals()))
        return full_result(result, BotName)

    async def set_my_description(
        self,
        description: str | OptionType[str] | None = None,
        language_code: str | OptionType[str] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("setMyDescription", get_params(locals()))
        return full_result(result, bool)

    async def get_my_description(
        self, language_code: str | OptionType[str] | None = None, **other
    ) -> Result[BotDescription, APIError]:
        result = await self.api.request_raw("getMyDescription", get_params(locals()))
        return full_result(result, BotDescription)

    async def set_my_short_description(
        self,
        short_description: str | OptionType[str] | None = None,
        language_code: str | OptionType[str] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw(
            "setMyShortDescription", get_params(locals())
        )
        return full_result(result, bool)

    async def get_my_short_description(
        self, language_code: str | OptionType[str] | None = None, **other
    ) -> Result[BotShortDescription, APIError]:
        result = await self.api.request_raw(
            "getMyShortDescription", get_params(locals())
        )
        return full_result(result, BotShortDescription)

    async def set_chat_menu_button(
        self,
        chat_id: int | OptionType[int] | None = None,
        menu_button: MenuButton | OptionType[MenuButton] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("setChatMenuButton", get_params(locals()))
        return full_result(result, bool)

    async def get_chat_menu_button(
        self, chat_id: int | OptionType[int] | None = None, **other
    ) -> Result[MenuButton, APIError]:
        result = await self.api.request_raw("getChatMenuButton", get_params(locals()))
        return full_result(result, MenuButton)

    async def set_my_default_administrator_rights(
        self,
        rights: ChatAdministratorRights
        | OptionType[ChatAdministratorRights]
        | None = None,
        for_channels: bool | OptionType[bool] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw(
            "setMyDefaultAdministratorRights", get_params(locals())
        )
        return full_result(result, bool)

    async def get_my_default_administrator_rights(
        self, for_channels: bool | OptionType[bool] | None = None, **other
    ) -> Result[ChatAdministratorRights, APIError]:
        result = await self.api.request_raw(
            "getMyDefaultAdministratorRights", get_params(locals())
        )
        return full_result(result, ChatAdministratorRights)

    async def edit_message_text(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_id: int | OptionType[int] | None = None,
        inline_message_id: str | OptionType[str] | None = None,
        text: str | OptionType[str] | None = None,
        parse_mode: str | OptionType[str] | None = None,
        entities: list[MessageEntity] | OptionType[list[MessageEntity]] | None = None,
        disable_web_page_preview: bool | OptionType[bool] | None = None,
        reply_markup: InlineKeyboardMarkup
        | OptionType[InlineKeyboardMarkup]
        | None = None,
        **other
    ) -> Result[typing.Union[Message, bool], APIError]:
        result = await self.api.request_raw("editMessageText", get_params(locals()))
        return full_result(result, typing.Union[Message, bool])

    async def edit_message_caption(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_id: int | OptionType[int] | None = None,
        inline_message_id: str | OptionType[str] | None = None,
        caption: str | OptionType[str] | None = None,
        parse_mode: str | OptionType[str] | None = None,
        caption_entities: list[MessageEntity]
        | OptionType[list[MessageEntity]]
        | None = None,
        reply_markup: InlineKeyboardMarkup
        | OptionType[InlineKeyboardMarkup]
        | None = None,
        **other
    ) -> Result[typing.Union[Message, bool], APIError]:
        result = await self.api.request_raw("editMessageCaption", get_params(locals()))
        return full_result(result, typing.Union[Message, bool])

    async def edit_message_media(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_id: int | OptionType[int] | None = None,
        inline_message_id: str | OptionType[str] | None = None,
        media: InputMedia | OptionType[InputMedia] | None = None,
        reply_markup: InlineKeyboardMarkup
        | OptionType[InlineKeyboardMarkup]
        | None = None,
        **other
    ) -> Result[typing.Union[Message, bool], APIError]:
        result = await self.api.request_raw("editMessageMedia", get_params(locals()))
        return full_result(result, typing.Union[Message, bool])

    async def edit_message_live_location(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_id: int | OptionType[int] | None = None,
        inline_message_id: str | OptionType[str] | None = None,
        latitude: float | OptionType[float] | None = None,
        longitude: float | OptionType[float] | None = None,
        horizontal_accuracy: float | OptionType[float] | None = None,
        heading: int | OptionType[int] | None = None,
        proximity_alert_radius: int | OptionType[int] | None = None,
        reply_markup: InlineKeyboardMarkup
        | OptionType[InlineKeyboardMarkup]
        | None = None,
        **other
    ) -> Result[typing.Union[Message, bool], APIError]:
        result = await self.api.request_raw(
            "editMessageLiveLocation", get_params(locals())
        )
        return full_result(result, typing.Union[Message, bool])

    async def stop_message_live_location(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_id: int | OptionType[int] | None = None,
        inline_message_id: str | OptionType[str] | None = None,
        reply_markup: InlineKeyboardMarkup
        | OptionType[InlineKeyboardMarkup]
        | None = None,
        **other
    ) -> Result[typing.Union[Message, bool], APIError]:
        result = await self.api.request_raw(
            "stopMessageLiveLocation", get_params(locals())
        )
        return full_result(result, typing.Union[Message, bool])

    async def edit_message_reply_markup(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_id: int | OptionType[int] | None = None,
        inline_message_id: str | OptionType[str] | None = None,
        reply_markup: InlineKeyboardMarkup
        | OptionType[InlineKeyboardMarkup]
        | None = None,
        **other
    ) -> Result[typing.Union[Message, bool], APIError]:
        result = await self.api.request_raw(
            "editMessageReplyMarkup", get_params(locals())
        )
        return full_result(result, typing.Union[Message, bool])

    async def stop_poll(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_id: int | OptionType[int] | None = None,
        reply_markup: InlineKeyboardMarkup
        | OptionType[InlineKeyboardMarkup]
        | None = None,
        **other
    ) -> Result[Poll, APIError]:
        result = await self.api.request_raw("stopPoll", get_params(locals()))
        return full_result(result, Poll)

    async def delete_message(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_id: int | OptionType[int] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("deleteMessage", get_params(locals()))
        return full_result(result, bool)

    async def send_sticker(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_thread_id: int | OptionType[int] | None = None,
        sticker: typing.Union[InputFile, str]
        | OptionType[typing.Union[InputFile, str]]
        | None = None,
        emoji: str | OptionType[str] | None = None,
        disable_notification: bool | OptionType[bool] | None = None,
        protect_content: bool | OptionType[bool] | None = None,
        reply_to_message_id: int | OptionType[int] | None = None,
        allow_sending_without_reply: bool | OptionType[bool] | None = None,
        reply_markup: typing.Union[
            InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply
        ]
        | OptionType[
            typing.Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ]
        | None = None,
        **other
    ) -> Result[Message, APIError]:
        result = await self.api.request_raw("sendSticker", get_params(locals()))
        return full_result(result, Message)

    async def get_sticker_set(
        self, name: str | OptionType[str] | None = None, **other
    ) -> Result[StickerSet, APIError]:
        result = await self.api.request_raw("getStickerSet", get_params(locals()))
        return full_result(result, StickerSet)

    async def get_custom_emoji_stickers(
        self, custom_emoji_ids: list[str] | OptionType[list[str]] | None = None, **other
    ) -> Result[list[Sticker], APIError]:
        result = await self.api.request_raw(
            "getCustomEmojiStickers", get_params(locals())
        )
        return full_result(result, list[Sticker])

    async def upload_sticker_file(
        self,
        user_id: int | OptionType[int] | None = None,
        sticker: InputFile | OptionType[InputFile] | None = None,
        sticker_format: str | OptionType[str] | None = None,
        **other
    ) -> Result[File, APIError]:
        result = await self.api.request_raw("uploadStickerFile", get_params(locals()))
        return full_result(result, File)

    async def create_new_sticker_set(
        self,
        user_id: int | OptionType[int] | None = None,
        name: str | OptionType[str] | None = None,
        title: str | OptionType[str] | None = None,
        stickers: list[InputSticker] | OptionType[list[InputSticker]] | None = None,
        sticker_format: str | OptionType[str] | None = None,
        sticker_type: str | OptionType[str] | None = None,
        needs_repainting: bool | OptionType[bool] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("createNewStickerSet", get_params(locals()))
        return full_result(result, bool)

    async def add_sticker_to_set(
        self,
        user_id: int | OptionType[int] | None = None,
        name: str | OptionType[str] | None = None,
        sticker: InputSticker | OptionType[InputSticker] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("addStickerToSet", get_params(locals()))
        return full_result(result, bool)

    async def set_sticker_position_in_set(
        self,
        sticker: str | OptionType[str] | None = None,
        position: int | OptionType[int] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw(
            "setStickerPositionInSet", get_params(locals())
        )
        return full_result(result, bool)

    async def delete_sticker_from_set(
        self, sticker: str | OptionType[str] | None = None, **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw(
            "deleteStickerFromSet", get_params(locals())
        )
        return full_result(result, bool)

    async def set_sticker_emoji_list(
        self,
        sticker: str | OptionType[str] | None = None,
        emoji_list: list[str] | OptionType[list[str]] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("setStickerEmojiList", get_params(locals()))
        return full_result(result, bool)

    async def set_sticker_keywords(
        self,
        sticker: str | OptionType[str] | None = None,
        keywords: list[str] | OptionType[list[str]] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("setStickerKeywords", get_params(locals()))
        return full_result(result, bool)

    async def set_sticker_mask_position(
        self,
        sticker: str | OptionType[str] | None = None,
        mask_position: MaskPosition | OptionType[MaskPosition] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw(
            "setStickerMaskPosition", get_params(locals())
        )
        return full_result(result, bool)

    async def set_sticker_set_title(
        self,
        name: str | OptionType[str] | None = None,
        title: str | OptionType[str] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("setStickerSetTitle", get_params(locals()))
        return full_result(result, bool)

    async def set_sticker_set_thumbnail(
        self,
        name: str | OptionType[str] | None = None,
        user_id: int | OptionType[int] | None = None,
        thumbnail: typing.Union[InputFile, str]
        | OptionType[typing.Union[InputFile, str]]
        | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw(
            "setStickerSetThumbnail", get_params(locals())
        )
        return full_result(result, bool)

    async def set_custom_emoji_sticker_set_thumbnail(
        self,
        name: str | OptionType[str] | None = None,
        custom_emoji_id: str | OptionType[str] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw(
            "setCustomEmojiStickerSetThumbnail", get_params(locals())
        )
        return full_result(result, bool)

    async def delete_sticker_set(
        self, name: str | OptionType[str] | None = None, **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("deleteStickerSet", get_params(locals()))
        return full_result(result, bool)

    async def answer_inline_query(
        self,
        inline_query_id: str | OptionType[str] | None = None,
        results: list[InlineQueryResult]
        | OptionType[list[InlineQueryResult]]
        | None = None,
        cache_time: int | OptionType[int] | None = None,
        is_personal: bool | OptionType[bool] | None = None,
        next_offset: str | OptionType[str] | None = None,
        button: InlineQueryResultsButton
        | OptionType[InlineQueryResultsButton]
        | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("answerInlineQuery", get_params(locals()))
        return full_result(result, bool)

    async def answer_web_app_query(
        self,
        web_app_query_id: str | OptionType[str] | None = None,
        result: InlineQueryResult | OptionType[InlineQueryResult] | None = None,
        **other
    ) -> Result[SentWebAppMessage, APIError]:
        _result = await self.api.request_raw("answerWebAppQuery", get_params(locals()))
        return full_result(_result, SentWebAppMessage)

    async def send_invoice(
        self,
        chat_id: typing.Union[int, str]
        | OptionType[typing.Union[int, str]]
        | None = None,
        message_thread_id: int | OptionType[int] | None = None,
        title: str | OptionType[str] | None = None,
        description: str | OptionType[str] | None = None,
        payload: str | OptionType[str] | None = None,
        provider_token: str | OptionType[str] | None = None,
        currency: str | OptionType[str] | None = None,
        prices: list[LabeledPrice] | OptionType[list[LabeledPrice]] | None = None,
        max_tip_amount: int | OptionType[int] | None = None,
        suggested_tip_amounts: list[int] | OptionType[list[int]] | None = None,
        start_parameter: str | OptionType[str] | None = None,
        provider_data: str | OptionType[str] | None = None,
        photo_url: str | OptionType[str] | None = None,
        photo_size: int | OptionType[int] | None = None,
        photo_width: int | OptionType[int] | None = None,
        photo_height: int | OptionType[int] | None = None,
        need_name: bool | OptionType[bool] | None = None,
        need_phone_number: bool | OptionType[bool] | None = None,
        need_email: bool | OptionType[bool] | None = None,
        need_shipping_address: bool | OptionType[bool] | None = None,
        send_phone_number_to_provider: bool | OptionType[bool] | None = None,
        send_email_to_provider: bool | OptionType[bool] | None = None,
        is_flexible: bool | OptionType[bool] | None = None,
        disable_notification: bool | OptionType[bool] | None = None,
        protect_content: bool | OptionType[bool] | None = None,
        reply_to_message_id: int | OptionType[int] | None = None,
        allow_sending_without_reply: bool | OptionType[bool] | None = None,
        reply_markup: InlineKeyboardMarkup
        | OptionType[InlineKeyboardMarkup]
        | None = None,
        **other
    ) -> Result[Message, APIError]:
        result = await self.api.request_raw("sendInvoice", get_params(locals()))
        return full_result(result, Message)

    async def create_invoice_link(
        self,
        title: str | OptionType[str] | None = None,
        description: str | OptionType[str] | None = None,
        payload: str | OptionType[str] | None = None,
        provider_token: str | OptionType[str] | None = None,
        currency: str | OptionType[str] | None = None,
        prices: list[LabeledPrice] | OptionType[list[LabeledPrice]] | None = None,
        max_tip_amount: int | OptionType[int] | None = None,
        suggested_tip_amounts: list[int] | OptionType[list[int]] | None = None,
        provider_data: str | OptionType[str] | None = None,
        photo_url: str | OptionType[str] | None = None,
        photo_size: int | OptionType[int] | None = None,
        photo_width: int | OptionType[int] | None = None,
        photo_height: int | OptionType[int] | None = None,
        need_name: bool | OptionType[bool] | None = None,
        need_phone_number: bool | OptionType[bool] | None = None,
        need_email: bool | OptionType[bool] | None = None,
        need_shipping_address: bool | OptionType[bool] | None = None,
        send_phone_number_to_provider: bool | OptionType[bool] | None = None,
        send_email_to_provider: bool | OptionType[bool] | None = None,
        is_flexible: bool | OptionType[bool] | None = None,
        **other
    ) -> Result[str, APIError]:
        result = await self.api.request_raw("createInvoiceLink", get_params(locals()))
        return full_result(result, str)

    async def answer_shipping_query(
        self,
        shipping_query_id: str | OptionType[str] | None = None,
        ok: bool | OptionType[bool] | None = None,
        shipping_options: list[ShippingOption]
        | OptionType[list[ShippingOption]]
        | None = None,
        error_message: str | OptionType[str] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw("answerShippingQuery", get_params(locals()))
        return full_result(result, bool)

    async def answer_pre_checkout_query(
        self,
        pre_checkout_query_id: str | OptionType[str] | None = None,
        ok: bool | OptionType[bool] | None = None,
        error_message: str | OptionType[str] | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw(
            "answerPreCheckoutQuery", get_params(locals())
        )
        return full_result(result, bool)

    async def set_passport_data_errors(
        self,
        user_id: int | OptionType[int] | None = None,
        errors: list[PassportElementError]
        | OptionType[list[PassportElementError]]
        | None = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request_raw(
            "setPassportDataErrors", get_params(locals())
        )
        return full_result(result, bool)

    async def send_game(
        self,
        chat_id: int | OptionType[int] | None = None,
        message_thread_id: int | OptionType[int] | None = None,
        game_short_name: str | OptionType[str] | None = None,
        disable_notification: bool | OptionType[bool] | None = None,
        protect_content: bool | OptionType[bool] | None = None,
        reply_to_message_id: int | OptionType[int] | None = None,
        allow_sending_without_reply: bool | OptionType[bool] | None = None,
        reply_markup: InlineKeyboardMarkup
        | OptionType[InlineKeyboardMarkup]
        | None = None,
        **other
    ) -> Result[Message, APIError]:
        result = await self.api.request_raw("sendGame", get_params(locals()))
        return full_result(result, Message)

    async def set_game_score(
        self,
        user_id: int | OptionType[int] | None = None,
        score: int | OptionType[int] | None = None,
        force: bool | OptionType[bool] | None = None,
        disable_edit_message: bool | OptionType[bool] | None = None,
        chat_id: int | OptionType[int] | None = None,
        message_id: int | OptionType[int] | None = None,
        inline_message_id: str | OptionType[str] | None = None,
        **other
    ) -> Result[typing.Union[Message, bool], APIError]:
        result = await self.api.request_raw("setGameScore", get_params(locals()))
        return full_result(result, typing.Union[Message, bool])

    async def get_game_high_scores(
        self,
        user_id: int | OptionType[int] | None = None,
        chat_id: int | OptionType[int] | None = None,
        message_id: int | OptionType[int] | None = None,
        inline_message_id: str | OptionType[str] | None = None,
        **other
    ) -> Result[list[GameHighScore], APIError]:
        result = await self.api.request_raw("getGameHighScores", get_params(locals()))
        return full_result(result, list[GameHighScore])
