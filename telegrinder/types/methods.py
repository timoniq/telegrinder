import typing
from .objects import *
from telegrinder.tools import Result
from telegrinder.api.error import APIError

if typing.TYPE_CHECKING:
    from telegrinder.api.abc import ABCAPI

X = typing.TypeVar("X")


class APIMethods:
    def __init__(self, api: "ABCAPI"):
        self.api = api

    @staticmethod
    def get_params(loc: dict) -> dict:
        n = {
            k: v for k, v in loc.items() if k not in ("self", "other") and v is not None
        }
        n.update(loc["other"])
        return n

    @staticmethod
    def get_response(r: dict) -> dict:
        if "json" in r:
            r["json_"] = r["json"]
        return r

    async def get_updates(
        self,
        offset: typing.Optional[int] = None,
        limit: typing.Optional[int] = None,
        timeout: typing.Optional[int] = None,
        allowed_updates: typing.Optional[typing.List[str]] = None,
        **other
    ) -> Result[typing.List["Update"], APIError]:
        result = await self.api.request("getUpdates", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def set_webhook(
        self,
        url: typing.Optional[str] = None,
        certificate: typing.Optional["InputFile"] = None,
        ip_address: typing.Optional[str] = None,
        max_connections: typing.Optional[int] = None,
        allowed_updates: typing.Optional[typing.List[str]] = None,
        drop_pending_updates: typing.Optional[bool] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("setWebhook", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def delete_webhook(
        self, drop_pending_updates: typing.Optional[bool] = None, **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("deleteWebhook", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_webhook_info(self, **other) -> Result["WebhookInfo", APIError]:
        result = await self.api.request("getWebhookInfo", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=WebhookInfo(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_me(self, **other) -> Result["User", APIError]:
        result = await self.api.request("getMe", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=User(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def log_out(self, **other) -> Result[bool, APIError]:
        result = await self.api.request("logOut", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def close(self, **other) -> Result[bool, APIError]:
        result = await self.api.request("close", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def send_message(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
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
        result = await self.api.request("sendMessage", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Message(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def forward_message(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        from_chat_id: typing.Optional[typing.Union[int, str]] = None,
        disable_notification: typing.Optional[bool] = None,
        protect_content: typing.Optional[bool] = None,
        message_id: typing.Optional[int] = None,
        **other
    ) -> Result["Message", APIError]:
        result = await self.api.request("forwardMessage", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Message(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def copy_message(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        from_chat_id: typing.Optional[typing.Union[int, str]] = None,
        message_id: typing.Optional[int] = None,
        caption: typing.Optional[str] = None,
        parse_mode: typing.Optional[str] = None,
        caption_entities: typing.Optional[typing.List["MessageEntity"]] = None,
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
    ) -> Result["MessageId", APIError]:
        result = await self.api.request("copyMessage", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=MessageId(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def send_photo(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        photo: typing.Optional[typing.Union["InputFile", str]] = None,
        caption: typing.Optional[str] = None,
        parse_mode: typing.Optional[str] = None,
        caption_entities: typing.Optional[typing.List["MessageEntity"]] = None,
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
        result = await self.api.request("sendPhoto", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Message(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def send_audio(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        audio: typing.Optional[typing.Union["InputFile", str]] = None,
        caption: typing.Optional[str] = None,
        parse_mode: typing.Optional[str] = None,
        caption_entities: typing.Optional[typing.List["MessageEntity"]] = None,
        duration: typing.Optional[int] = None,
        performer: typing.Optional[str] = None,
        title: typing.Optional[str] = None,
        thumb: typing.Optional[typing.Union["InputFile", str]] = None,
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
        result = await self.api.request("sendAudio", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Message(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def send_document(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        document: typing.Optional[typing.Union["InputFile", str]] = None,
        thumb: typing.Optional[typing.Union["InputFile", str]] = None,
        caption: typing.Optional[str] = None,
        parse_mode: typing.Optional[str] = None,
        caption_entities: typing.Optional[typing.List["MessageEntity"]] = None,
        disable_content_type_detection: typing.Optional[bool] = None,
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
        result = await self.api.request("sendDocument", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Message(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def send_video(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        video: typing.Optional[typing.Union["InputFile", str]] = None,
        duration: typing.Optional[int] = None,
        width: typing.Optional[int] = None,
        height: typing.Optional[int] = None,
        thumb: typing.Optional[typing.Union["InputFile", str]] = None,
        caption: typing.Optional[str] = None,
        parse_mode: typing.Optional[str] = None,
        caption_entities: typing.Optional[typing.List["MessageEntity"]] = None,
        supports_streaming: typing.Optional[bool] = None,
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
        result = await self.api.request("sendVideo", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Message(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def send_animation(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        animation: typing.Optional[typing.Union["InputFile", str]] = None,
        duration: typing.Optional[int] = None,
        width: typing.Optional[int] = None,
        height: typing.Optional[int] = None,
        thumb: typing.Optional[typing.Union["InputFile", str]] = None,
        caption: typing.Optional[str] = None,
        parse_mode: typing.Optional[str] = None,
        caption_entities: typing.Optional[typing.List["MessageEntity"]] = None,
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
        result = await self.api.request("sendAnimation", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Message(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def send_voice(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        voice: typing.Optional[typing.Union["InputFile", str]] = None,
        caption: typing.Optional[str] = None,
        parse_mode: typing.Optional[str] = None,
        caption_entities: typing.Optional[typing.List["MessageEntity"]] = None,
        duration: typing.Optional[int] = None,
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
        result = await self.api.request("sendVoice", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Message(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def send_video_note(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        video_note: typing.Optional[typing.Union["InputFile", str]] = None,
        duration: typing.Optional[int] = None,
        length: typing.Optional[int] = None,
        thumb: typing.Optional[typing.Union["InputFile", str]] = None,
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
        result = await self.api.request("sendVideoNote", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Message(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def send_media_group(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        media: typing.Optional[
            typing.List[
                typing.Union[
                    "InputMediaAudio",
                    "InputMediaDocument",
                    "InputMediaPhoto",
                    "InputMediaVideo",
                ]
            ]
        ] = None,
        disable_notification: typing.Optional[bool] = None,
        protect_content: typing.Optional[bool] = None,
        reply_to_message_id: typing.Optional[int] = None,
        allow_sending_without_reply: typing.Optional[bool] = None,
        **other
    ) -> Result[typing.List["Message"], APIError]:
        result = await self.api.request("sendMediaGroup", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def send_location(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        latitude: typing.Optional[float] = None,
        longitude: typing.Optional[float] = None,
        horizontal_accuracy: typing.Optional[float] = None,
        live_period: typing.Optional[int] = None,
        heading: typing.Optional[int] = None,
        proximity_alert_radius: typing.Optional[int] = None,
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
        result = await self.api.request("sendLocation", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Message(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def edit_message_live_location(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        message_id: typing.Optional[int] = None,
        inline_message_id: typing.Optional[str] = None,
        latitude: typing.Optional[float] = None,
        longitude: typing.Optional[float] = None,
        horizontal_accuracy: typing.Optional[float] = None,
        heading: typing.Optional[int] = None,
        proximity_alert_radius: typing.Optional[int] = None,
        reply_markup: typing.Optional["InlineKeyboardMarkup"] = None,
        **other
    ) -> Result[typing.Union["Message", bool], APIError]:
        result = await self.api.request(
            "editMessageLiveLocation", self.get_params(locals())
        )
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def stop_message_live_location(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        message_id: typing.Optional[int] = None,
        inline_message_id: typing.Optional[str] = None,
        reply_markup: typing.Optional["InlineKeyboardMarkup"] = None,
        **other
    ) -> Result[typing.Union["Message", bool], APIError]:
        result = await self.api.request(
            "stopMessageLiveLocation", self.get_params(locals())
        )
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def send_venue(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        latitude: typing.Optional[float] = None,
        longitude: typing.Optional[float] = None,
        title: typing.Optional[str] = None,
        address: typing.Optional[str] = None,
        foursquare_id: typing.Optional[str] = None,
        foursquare_type: typing.Optional[str] = None,
        google_place_id: typing.Optional[str] = None,
        google_place_type: typing.Optional[str] = None,
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
        result = await self.api.request("sendVenue", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Message(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def send_contact(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        phone_number: typing.Optional[str] = None,
        first_name: typing.Optional[str] = None,
        last_name: typing.Optional[str] = None,
        vcard: typing.Optional[str] = None,
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
        result = await self.api.request("sendContact", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Message(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def send_poll(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        question: typing.Optional[str] = None,
        options: typing.Optional[typing.List[str]] = None,
        is_anonymous: typing.Optional[bool] = None,
        type: typing.Optional[str] = None,
        allows_multiple_answers: typing.Optional[bool] = None,
        correct_option_id: typing.Optional[int] = None,
        explanation: typing.Optional[str] = None,
        explanation_parse_mode: typing.Optional[str] = None,
        explanation_entities: typing.Optional[typing.List["MessageEntity"]] = None,
        open_period: typing.Optional[int] = None,
        close_date: typing.Optional[int] = None,
        is_closed: typing.Optional[bool] = None,
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
        result = await self.api.request("sendPoll", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Message(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def send_dice(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        emoji: typing.Optional[str] = None,
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
        result = await self.api.request("sendDice", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Message(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def send_chat_action(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        action: typing.Optional[str] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("sendChatAction", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_user_profile_photos(
        self,
        user_id: typing.Optional[int] = None,
        offset: typing.Optional[int] = None,
        limit: typing.Optional[int] = None,
        **other
    ) -> Result["UserProfilePhotos", APIError]:
        result = await self.api.request(
            "getUserProfilePhotos", self.get_params(locals())
        )
        if result.is_ok:
            return Result(
                True, value=UserProfilePhotos(**self.get_response(result.unwrap()))
            )
        return Result(False, error=result.error)

    async def get_file(
        self, file_id: typing.Optional[str] = None, **other
    ) -> Result["File", APIError]:
        result = await self.api.request("getFile", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=File(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def ban_chat_member(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        user_id: typing.Optional[int] = None,
        until_date: typing.Optional[int] = None,
        revoke_messages: typing.Optional[bool] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("banChatMember", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def unban_chat_member(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        user_id: typing.Optional[int] = None,
        only_if_banned: typing.Optional[bool] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("unbanChatMember", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def restrict_chat_member(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        user_id: typing.Optional[int] = None,
        permissions: typing.Optional["ChatPermissions"] = None,
        until_date: typing.Optional[int] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("restrictChatMember", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def promote_chat_member(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        user_id: typing.Optional[int] = None,
        is_anonymous: typing.Optional[bool] = None,
        can_manage_chat: typing.Optional[bool] = None,
        can_post_messages: typing.Optional[bool] = None,
        can_edit_messages: typing.Optional[bool] = None,
        can_delete_messages: typing.Optional[bool] = None,
        can_manage_video_chats: typing.Optional[bool] = None,
        can_restrict_members: typing.Optional[bool] = None,
        can_promote_members: typing.Optional[bool] = None,
        can_change_info: typing.Optional[bool] = None,
        can_invite_users: typing.Optional[bool] = None,
        can_pin_messages: typing.Optional[bool] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("promoteChatMember", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def set_chat_administrator_custom_title(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        user_id: typing.Optional[int] = None,
        custom_title: typing.Optional[str] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request(
            "setChatAdministratorCustomTitle", self.get_params(locals())
        )
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def ban_chat_sender_chat(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        sender_chat_id: typing.Optional[int] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("banChatSenderChat", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def unban_chat_sender_chat(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        sender_chat_id: typing.Optional[int] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request(
            "unbanChatSenderChat", self.get_params(locals())
        )
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def set_chat_permissions(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        permissions: typing.Optional["ChatPermissions"] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("setChatPermissions", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def export_chat_invite_link(
        self, chat_id: typing.Optional[typing.Union[int, str]] = None, **other
    ) -> Result[str, APIError]:
        result = await self.api.request(
            "exportChatInviteLink", self.get_params(locals())
        )
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def create_chat_invite_link(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        name: typing.Optional[str] = None,
        expire_date: typing.Optional[int] = None,
        member_limit: typing.Optional[int] = None,
        creates_join_request: typing.Optional[bool] = None,
        **other
    ) -> Result["ChatInviteLink", APIError]:
        result = await self.api.request(
            "createChatInviteLink", self.get_params(locals())
        )
        if result.is_ok:
            return Result(
                True, value=ChatInviteLink(**self.get_response(result.unwrap()))
            )
        return Result(False, error=result.error)

    async def edit_chat_invite_link(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        invite_link: typing.Optional[str] = None,
        name: typing.Optional[str] = None,
        expire_date: typing.Optional[int] = None,
        member_limit: typing.Optional[int] = None,
        creates_join_request: typing.Optional[bool] = None,
        **other
    ) -> Result["ChatInviteLink", APIError]:
        result = await self.api.request("editChatInviteLink", self.get_params(locals()))
        if result.is_ok:
            return Result(
                True, value=ChatInviteLink(**self.get_response(result.unwrap()))
            )
        return Result(False, error=result.error)

    async def revoke_chat_invite_link(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        invite_link: typing.Optional[str] = None,
        **other
    ) -> Result["ChatInviteLink", APIError]:
        result = await self.api.request(
            "revokeChatInviteLink", self.get_params(locals())
        )
        if result.is_ok:
            return Result(
                True, value=ChatInviteLink(**self.get_response(result.unwrap()))
            )
        return Result(False, error=result.error)

    async def approve_chat_join_request(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        user_id: typing.Optional[int] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request(
            "approveChatJoinRequest", self.get_params(locals())
        )
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def decline_chat_join_request(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        user_id: typing.Optional[int] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request(
            "declineChatJoinRequest", self.get_params(locals())
        )
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def set_chat_photo(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        photo: typing.Optional["InputFile"] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("setChatPhoto", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def delete_chat_photo(
        self, chat_id: typing.Optional[typing.Union[int, str]] = None, **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("deleteChatPhoto", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def set_chat_title(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        title: typing.Optional[str] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("setChatTitle", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def set_chat_description(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        description: typing.Optional[str] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("setChatDescription", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def pin_chat_message(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        message_id: typing.Optional[int] = None,
        disable_notification: typing.Optional[bool] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("pinChatMessage", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def unpin_chat_message(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        message_id: typing.Optional[int] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("unpinChatMessage", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def unpin_all_chat_messages(
        self, chat_id: typing.Optional[typing.Union[int, str]] = None, **other
    ) -> Result[bool, APIError]:
        result = await self.api.request(
            "unpinAllChatMessages", self.get_params(locals())
        )
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def leave_chat(
        self, chat_id: typing.Optional[typing.Union[int, str]] = None, **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("leaveChat", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_chat(
        self, chat_id: typing.Optional[typing.Union[int, str]] = None, **other
    ) -> Result["Chat", APIError]:
        result = await self.api.request("getChat", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Chat(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_chat_administrators(
        self, chat_id: typing.Optional[typing.Union[int, str]] = None, **other
    ) -> Result[typing.List["ChatMember"], APIError]:
        result = await self.api.request(
            "getChatAdministrators", self.get_params(locals())
        )
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_chat_member_count(
        self, chat_id: typing.Optional[typing.Union[int, str]] = None, **other
    ) -> Result[int, APIError]:
        result = await self.api.request("getChatMemberCount", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_chat_member(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        user_id: typing.Optional[int] = None,
        **other
    ) -> Result["ChatMember", APIError]:
        result = await self.api.request("getChatMember", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=ChatMember(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def set_chat_sticker_set(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        sticker_set_name: typing.Optional[str] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("setChatStickerSet", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def delete_chat_sticker_set(
        self, chat_id: typing.Optional[typing.Union[int, str]] = None, **other
    ) -> Result[bool, APIError]:
        result = await self.api.request(
            "deleteChatStickerSet", self.get_params(locals())
        )
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def answer_callback_query(
        self,
        callback_query_id: typing.Optional[str] = None,
        text: typing.Optional[str] = None,
        show_alert: typing.Optional[bool] = None,
        url: typing.Optional[str] = None,
        cache_time: typing.Optional[int] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request(
            "answerCallbackQuery", self.get_params(locals())
        )
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def set_my_commands(
        self,
        commands: typing.Optional[typing.List["BotCommand"]] = None,
        scope: typing.Optional["BotCommandScope"] = None,
        language_code: typing.Optional[str] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("setMyCommands", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def delete_my_commands(
        self,
        scope: typing.Optional["BotCommandScope"] = None,
        language_code: typing.Optional[str] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("deleteMyCommands", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_my_commands(
        self,
        scope: typing.Optional["BotCommandScope"] = None,
        language_code: typing.Optional[str] = None,
        **other
    ) -> Result[typing.List["BotCommand"], APIError]:
        result = await self.api.request("getMyCommands", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def set_chat_menu_button(
        self,
        chat_id: typing.Optional[int] = None,
        menu_button: typing.Optional["MenuButton"] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("setChatMenuButton", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_chat_menu_button(
        self, chat_id: typing.Optional[int] = None, **other
    ) -> Result["MenuButton", APIError]:
        result = await self.api.request("getChatMenuButton", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=MenuButton(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def set_my_default_administrator_rights(
        self,
        rights: typing.Optional["ChatAdministratorRights"] = None,
        for_channels: typing.Optional[bool] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request(
            "setMyDefaultAdministratorRights", self.get_params(locals())
        )
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_my_default_administrator_rights(
        self, for_channels: typing.Optional[bool] = None, **other
    ) -> Result["ChatAdministratorRights", APIError]:
        result = await self.api.request(
            "getMyDefaultAdministratorRights", self.get_params(locals())
        )
        if result.is_ok:
            return Result(
                True,
                value=ChatAdministratorRights(**self.get_response(result.unwrap())),
            )
        return Result(False, error=result.error)

    async def edit_message_text(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        message_id: typing.Optional[int] = None,
        inline_message_id: typing.Optional[str] = None,
        text: typing.Optional[str] = None,
        parse_mode: typing.Optional[str] = None,
        entities: typing.Optional[typing.List["MessageEntity"]] = None,
        disable_web_page_preview: typing.Optional[bool] = None,
        reply_markup: typing.Optional["InlineKeyboardMarkup"] = None,
        **other
    ) -> Result[typing.Union["Message", bool], APIError]:
        result = await self.api.request("editMessageText", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def edit_message_caption(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        message_id: typing.Optional[int] = None,
        inline_message_id: typing.Optional[str] = None,
        caption: typing.Optional[str] = None,
        parse_mode: typing.Optional[str] = None,
        caption_entities: typing.Optional[typing.List["MessageEntity"]] = None,
        reply_markup: typing.Optional["InlineKeyboardMarkup"] = None,
        **other
    ) -> Result[typing.Union["Message", bool], APIError]:
        result = await self.api.request("editMessageCaption", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def edit_message_media(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        message_id: typing.Optional[int] = None,
        inline_message_id: typing.Optional[str] = None,
        media: typing.Optional["InputMedia"] = None,
        reply_markup: typing.Optional["InlineKeyboardMarkup"] = None,
        **other
    ) -> Result[typing.Union["Message", bool], APIError]:
        result = await self.api.request("editMessageMedia", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def edit_message_reply_markup(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        message_id: typing.Optional[int] = None,
        inline_message_id: typing.Optional[str] = None,
        reply_markup: typing.Optional["InlineKeyboardMarkup"] = None,
        **other
    ) -> Result[typing.Union["Message", bool], APIError]:
        result = await self.api.request(
            "editMessageReplyMarkup", self.get_params(locals())
        )
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def stop_poll(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        message_id: typing.Optional[int] = None,
        reply_markup: typing.Optional["InlineKeyboardMarkup"] = None,
        **other
    ) -> Result["Poll", APIError]:
        result = await self.api.request("stopPoll", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Poll(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def delete_message(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        message_id: typing.Optional[int] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("deleteMessage", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def send_sticker(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        sticker: typing.Optional[typing.Union["InputFile", str]] = None,
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
        result = await self.api.request("sendSticker", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Message(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_sticker_set(
        self, name: typing.Optional[str] = None, **other
    ) -> Result["StickerSet", APIError]:
        result = await self.api.request("getStickerSet", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=StickerSet(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def upload_sticker_file(
        self,
        user_id: typing.Optional[int] = None,
        png_sticker: typing.Optional["InputFile"] = None,
        **other
    ) -> Result["File", APIError]:
        result = await self.api.request("uploadStickerFile", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=File(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def create_new_sticker_set(
        self,
        user_id: typing.Optional[int] = None,
        name: typing.Optional[str] = None,
        title: typing.Optional[str] = None,
        png_sticker: typing.Optional[typing.Union["InputFile", str]] = None,
        tgs_sticker: typing.Optional["InputFile"] = None,
        webm_sticker: typing.Optional["InputFile"] = None,
        emojis: typing.Optional[str] = None,
        contains_masks: typing.Optional[bool] = None,
        mask_position: typing.Optional["MaskPosition"] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request(
            "createNewStickerSet", self.get_params(locals())
        )
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def add_sticker_to_set(
        self,
        user_id: typing.Optional[int] = None,
        name: typing.Optional[str] = None,
        png_sticker: typing.Optional[typing.Union["InputFile", str]] = None,
        tgs_sticker: typing.Optional["InputFile"] = None,
        webm_sticker: typing.Optional["InputFile"] = None,
        emojis: typing.Optional[str] = None,
        mask_position: typing.Optional["MaskPosition"] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("addStickerToSet", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def set_sticker_position_in_set(
        self,
        sticker: typing.Optional[str] = None,
        position: typing.Optional[int] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request(
            "setStickerPositionInSet", self.get_params(locals())
        )
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def delete_sticker_from_set(
        self, sticker: typing.Optional[str] = None, **other
    ) -> Result[bool, APIError]:
        result = await self.api.request(
            "deleteStickerFromSet", self.get_params(locals())
        )
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def set_sticker_set_thumb(
        self,
        name: typing.Optional[str] = None,
        user_id: typing.Optional[int] = None,
        thumb: typing.Optional[typing.Union["InputFile", str]] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("setStickerSetThumb", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def answer_inline_query(
        self,
        inline_query_id: typing.Optional[str] = None,
        results: typing.Optional[typing.List["InlineQueryResult"]] = None,
        cache_time: typing.Optional[int] = None,
        is_personal: typing.Optional[bool] = None,
        next_offset: typing.Optional[str] = None,
        switch_pm_text: typing.Optional[str] = None,
        switch_pm_parameter: typing.Optional[str] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("answerInlineQuery", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def answer_web_app_query(
        self,
        web_app_query_id: typing.Optional[str] = None,
        result: typing.Optional["InlineQueryResult"] = None,
        **other
    ) -> Result["SentWebAppMessage", APIError]:
        result = await self.api.request("answerWebAppQuery", self.get_params(locals()))
        if result.is_ok:
            return Result(
                True, value=SentWebAppMessage(**self.get_response(result.unwrap()))
            )
        return Result(False, error=result.error)

    async def send_invoice(
        self,
        chat_id: typing.Optional[typing.Union[int, str]] = None,
        title: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
        payload: typing.Optional[str] = None,
        provider_token: typing.Optional[str] = None,
        currency: typing.Optional[str] = None,
        prices: typing.Optional[typing.List["LabeledPrice"]] = None,
        max_tip_amount: typing.Optional[int] = None,
        suggested_tip_amounts: typing.Optional[typing.List[int]] = None,
        start_parameter: typing.Optional[str] = None,
        provider_data: typing.Optional[str] = None,
        photo_url: typing.Optional[str] = None,
        photo_size: typing.Optional[int] = None,
        photo_width: typing.Optional[int] = None,
        photo_height: typing.Optional[int] = None,
        need_name: typing.Optional[bool] = None,
        need_phone_number: typing.Optional[bool] = None,
        need_email: typing.Optional[bool] = None,
        need_shipping_address: typing.Optional[bool] = None,
        send_phone_number_to_provider: typing.Optional[bool] = None,
        send_email_to_provider: typing.Optional[bool] = None,
        is_flexible: typing.Optional[bool] = None,
        disable_notification: typing.Optional[bool] = None,
        protect_content: typing.Optional[bool] = None,
        reply_to_message_id: typing.Optional[int] = None,
        allow_sending_without_reply: typing.Optional[bool] = None,
        reply_markup: typing.Optional["InlineKeyboardMarkup"] = None,
        **other
    ) -> Result["Message", APIError]:
        result = await self.api.request("sendInvoice", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Message(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def answer_shipping_query(
        self,
        shipping_query_id: typing.Optional[str] = None,
        ok: typing.Optional[bool] = None,
        shipping_options: typing.Optional[typing.List["ShippingOption"]] = None,
        error_message: typing.Optional[str] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request(
            "answerShippingQuery", self.get_params(locals())
        )
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def answer_pre_checkout_query(
        self,
        pre_checkout_query_id: typing.Optional[str] = None,
        ok: typing.Optional[bool] = None,
        error_message: typing.Optional[str] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request(
            "answerPreCheckoutQuery", self.get_params(locals())
        )
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def set_passport_data_errors(
        self,
        user_id: typing.Optional[int] = None,
        errors: typing.Optional[typing.List["PassportElementError"]] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request(
            "setPassportDataErrors", self.get_params(locals())
        )
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def send_game(
        self,
        chat_id: typing.Optional[int] = None,
        game_short_name: typing.Optional[str] = None,
        disable_notification: typing.Optional[bool] = None,
        protect_content: typing.Optional[bool] = None,
        reply_to_message_id: typing.Optional[int] = None,
        allow_sending_without_reply: typing.Optional[bool] = None,
        reply_markup: typing.Optional["InlineKeyboardMarkup"] = None,
        **other
    ) -> Result["Message", APIError]:
        result = await self.api.request("sendGame", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Message(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def set_game_score(
        self,
        user_id: typing.Optional[int] = None,
        score: typing.Optional[int] = None,
        force: typing.Optional[bool] = None,
        disable_edit_message: typing.Optional[bool] = None,
        chat_id: typing.Optional[int] = None,
        message_id: typing.Optional[int] = None,
        inline_message_id: typing.Optional[str] = None,
        **other
    ) -> Result[typing.Union["Message", bool], APIError]:
        result = await self.api.request("setGameScore", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_game_high_scores(
        self,
        user_id: typing.Optional[int] = None,
        chat_id: typing.Optional[int] = None,
        message_id: typing.Optional[int] = None,
        inline_message_id: typing.Optional[str] = None,
        **other
    ) -> Result[typing.List["GameHighScore"], APIError]:
        result = await self.api.request("getGameHighScores", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)
