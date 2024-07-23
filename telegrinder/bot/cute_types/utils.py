import typing

from telegrinder.model import get_params
from telegrinder.types import (
    ChatPermissions,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InlineQueryResultAudio,
    InlineQueryResultCachedAudio,
    InlineQueryResultCachedDocument,
    InlineQueryResultCachedGif,
    InlineQueryResultCachedMpeg4Gif,
    InlineQueryResultCachedPhoto,
    InlineQueryResultCachedSticker,
    InlineQueryResultCachedVideo,
    InlineQueryResultCachedVoice,
    InlineQueryResultContact,
    InlineQueryResultDocument,
    InlineQueryResultGame,
    InlineQueryResultGif,
    InlineQueryResultLocation,
    InlineQueryResultMpeg4Gif,
    InlineQueryResultPhoto,
    InlineQueryResultVenue,
    InlineQueryResultVideo,
    InlineQueryResultVoice,
    InputContactMessageContent,
    InputFile,
    InputInvoiceMessageContent,
    InputLocationMessageContent,
    InputMediaAnimation,
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
    InputTextMessageContent,
    InputVenueMessageContent,
    LabeledPrice,
    LinkPreviewOptions,
    MessageEntity,
    ReactionEmoji,
    ReactionType,
    ReactionTypeEmoji,
    ReplyParameters,
)

InputMedia: typing.TypeAlias = typing.Union[
    InputMediaAnimation,
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
]
InputMessageContent: typing.TypeAlias = typing.Union[
    InputTextMessageContent,
    InputLocationMessageContent,
    InputVenueMessageContent,
    InputContactMessageContent,
    InputInvoiceMessageContent,
]

INPUT_MEDIA_TYPES: typing.Final[dict[str, type[InputMedia]]] = {
    "animation": InputMediaAnimation,
    "audio": InputMediaAudio,
    "document": InputMediaDocument,
    "photo": InputMediaPhoto,
    "video": InputMediaVideo,
}


def compose_reactions(
    reactions: (str | ReactionEmoji | ReactionType | list[str | ReactionEmoji | ReactionType]),
    /,
) -> list[ReactionType]:
    if not isinstance(reactions, list):
        reactions = [reactions]
    return [
        (
            ReactionTypeEmoji("emoji", emoji)
            if isinstance(emoji, ReactionEmoji)
            else (ReactionTypeEmoji("emoji", ReactionEmoji(emoji)) if isinstance(emoji, str) else emoji)
        )
        for emoji in ([reactions] if isinstance(reactions, str) else reactions)
    ]


def compose_reply_params(
    message_id: int | None,
    chat_id: int | str | None,
    *,
    allow_sending_without_reply: bool | None = None,
    quote: str | None = None,
    quote_parse_mode: str | None = None,
    quote_entities: list[MessageEntity] | None = None,
    quote_position: int | None = None,
    **other: typing.Any,
) -> ReplyParameters:
    return ReplyParameters(**get_params(locals()))


def compose_link_preview_options(
    *,
    is_disabled: bool | None = None,
    url: str | None = None,
    prefer_small_media: bool | None = None,
    prefer_large_media: bool | None = None,
    show_above_text: bool | None = None,
    **other: typing.Any,
) -> LinkPreviewOptions:
    return LinkPreviewOptions(**get_params(locals()))


def compose_chat_permissions(
    *,
    can_send_messages: bool | None = None,
    can_send_audios: bool | None = None,
    can_send_documents: bool | None = None,
    can_send_photos: bool | None = None,
    can_send_videos: bool | None = None,
    can_send_video_notes: bool | None = None,
    can_send_voice_notes: bool | None = None,
    can_send_polls: bool | None = None,
    can_send_other_messages: bool | None = None,
    can_add_web_page_previews: bool | None = None,
    can_change_info: bool | None = None,
    can_invite_users: bool | None = None,
    can_pin_messages: bool | None = None,
    can_manage_topics: bool | None = None,
) -> ChatPermissions:
    return ChatPermissions(**get_params(locals()))


def input_media(
    type: typing.Literal["animation", "audio", "document", "photo", "video"],
    media: str | InputFile,
    *,
    caption: str | None = None,
    parse_mode: str | None = None,
    caption_entities: list[MessageEntity] | None = None,
    **other: typing.Any,
) -> InputMedia:
    return INPUT_MEDIA_TYPES[type](**get_params(locals()))


def input_contact_message_content(
    phone_number: str,
    first_name: str,
    *,
    last_name: str | None = None,
    vcard: str | None = None,
) -> InputContactMessageContent:
    return InputContactMessageContent(**get_params(locals()))


def input_invoice_message_content(
    title: str,
    description: str,
    payload: str,
    provider_token: str,
    currency: str,
    prices: list[LabeledPrice],
    *,
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
) -> InputInvoiceMessageContent:
    return InputInvoiceMessageContent(**get_params(locals()))


def input_location_message_content(
    latitude: float,
    longitude: float,
    *,
    horizontal_accuracy: float | None = None,
    live_period: int | None = None,
    heading: int | None = None,
    proximity_alert_radius: int | None = None,
) -> InputLocationMessageContent:
    return InputLocationMessageContent(**get_params(locals()))


def input_text_message_content(
    message_text: str,
    *,
    parse_mode: str | None = None,
    entities: list[MessageEntity] | None = None,
    disable_web_page_preview: bool | None = None,
) -> InputTextMessageContent:
    return InputTextMessageContent(**get_params(locals()))


def input_venue_message_content(
    latitude: float,
    longitude: float,
    title: str,
    address: str,
    *,
    foursquare_id: str | None = None,
    foursquare_type: str | None = None,
    google_place_id: str | None = None,
    google_place_type: str | None = None,
) -> InputVenueMessageContent:
    return InputVenueMessageContent(**get_params(locals()))


def inline_query_article(
    id: str,
    title: str,
    input_message_content: InputMessageContent,
    *,
    reply_markup: InlineKeyboardMarkup | None = None,
    url: str | None = None,
    hide_url: bool | None = None,
    description: str | None = None,
    thumbnail_url: str | None = None,
    thumbnail_width: int | None = None,
    thumbnail_height: int | None = None,
) -> InlineQueryResultArticle:
    return InlineQueryResultArticle(type="article", **get_params(locals()))


def inline_query_audio(
    id: str,
    audio_url: str,
    *,
    title: str | None = None,
    caption: str | None = None,
    parse_mode: str | None = None,
    caption_entities: list[MessageEntity] | None = None,
    performer: str | None = None,
    audio_duration: int | None = None,
    reply_markup: InlineKeyboardMarkup | None = None,
    input_message_content: InputMessageContent | None = None,
) -> InlineQueryResultAudio:
    return InlineQueryResultAudio(type="audio", **get_params(locals()))


def inline_query_contact(
    id: str,
    phone_number: str,
    first_name: str,
    *,
    last_name: str | None = None,
    vcard: str | None = None,
    reply_markup: InlineKeyboardMarkup | None = None,
    input_message_content: InputMessageContent | None = None,
    thumbnail_url: str | None = None,
    thumbnail_width: int | None = None,
    thumbnail_height: int | None = None,
) -> InlineQueryResultContact:
    return InlineQueryResultContact(type="contact", **get_params(locals()))


def inline_query_document(
    id: str,
    title: str,
    document_url: str,
    mime_type: str,
    *,
    description: str | None = None,
    caption: str | None = None,
    parse_mode: str | None = None,
    caption_entities: list[MessageEntity] | None = None,
    reply_markup: InlineKeyboardMarkup | None = None,
    input_message_content: InputMessageContent | None = None,
    thumbnail_url: str | None = None,
    thumbnail_width: int | None = None,
    thumbnail_height: int | None = None,
) -> InlineQueryResultDocument:
    return InlineQueryResultDocument(type="document", **get_params(locals()))


def inline_query_gif(
    id: str,
    gif_url: str,
    *,
    gif_width: int | None = None,
    gif_height: int | None = None,
    gif_duration: int | None = None,
    title: str | None = None,
    caption: str | None = None,
    parse_mode: str | None = None,
    caption_entities: list[MessageEntity] | None = None,
    reply_markup: InlineKeyboardMarkup | None = None,
    input_message_content: InputMessageContent | None = None,
    thumbnail_url: str | None = None,
    thumbnail_mime_type: str | None = None,
) -> InlineQueryResultGif:
    return InlineQueryResultGif(type="gif", **get_params(locals()))


def inline_query_location(
    id: str,
    latitude: float,
    longitude: float,
    *,
    title: str | None = None,
    horizontal_accuracy: float | None = None,
    live_period: int | None = None,
    heading: int | None = None,
    proximity_alert_radius: int | None = None,
    reply_markup: InlineKeyboardMarkup | None = None,
    input_message_content: InputMessageContent | None = None,
    thumbnail_url: str | None = None,
    thumbnail_width: int | None = None,
    thumbnail_height: int | None = None,
) -> InlineQueryResultLocation:
    return InlineQueryResultLocation(type="location", **get_params(locals()))


def inline_query_venue(
    id: str,
    latitude: float,
    longitude: float,
    title: str,
    address: str,
    *,
    foursquare_id: str | None = None,
    foursquare_type: str | None = None,
    google_place_id: str | None = None,
    google_place_type: str | None = None,
    reply_markup: InlineKeyboardMarkup | None = None,
    input_message_content: InputMessageContent | None = None,
    thumbnail_url: str | None = None,
    thumbnail_width: int | None = None,
    thumbnail_height: int | None = None,
) -> InlineQueryResultVenue:
    return InlineQueryResultVenue(type="venue", **get_params(locals()))


def inline_query_video(
    id: str,
    video_url: str,
    mime_type: str,
    thumb_url: str,
    *,
    title: str | None = None,
    caption: str | None = None,
    parse_mode: str | None = None,
    caption_entities: list[MessageEntity] | None = None,
    video_width: int | None = None,
    video_height: int | None = None,
    video_duration: int | None = None,
    description: str | None = None,
    reply_markup: InlineKeyboardMarkup | None = None,
    input_message_content: InputMessageContent | None = None,
    thumbnail_url: str | None = None,
    thumbnail_width: int | None = None,
    thumbnail_height: int | None = None,
) -> InlineQueryResultVideo:
    return InlineQueryResultVideo(type="video", **get_params(locals()))


def inline_query_game(
    id: str,
    game_short_name: str,
    *,
    reply_markup: InlineKeyboardMarkup | None = None,
) -> InlineQueryResultGame:
    return InlineQueryResultGame(type="game", **get_params(locals()))


def inline_query_voice(
    id: str,
    voice_url: str,
    title: str,
    *,
    caption: str | None = None,
    parse_mode: str | None = None,
    caption_entities: list[MessageEntity] | None = None,
    reply_markup: InlineKeyboardMarkup | None = None,
    input_message_content: InputMessageContent | None = None,
    duration: int | None = None,
) -> InlineQueryResultVoice:
    return InlineQueryResultVoice(type="voice", **get_params(locals()))


def inline_query_photo(
    id: str,
    photo_url: str,
    thumb_url: str,
    *,
    photo_width: int | None = None,
    photo_height: int | None = None,
    title: str | None = None,
    description: str | None = None,
    caption: str | None = None,
    parse_mode: str | None = None,
    caption_entities: list[MessageEntity] | None = None,
    reply_markup: InlineKeyboardMarkup | None = None,
    input_message_content: InputMessageContent | None = None,
) -> InlineQueryResultPhoto:
    return InlineQueryResultPhoto(type="photo", **get_params(locals()))


def inline_query_mpeg4_gif(
    id: str,
    mpeg4_url: str,
    *,
    mpeg4_width: int | None = None,
    mpeg4_height: int | None = None,
    mpeg4_duration: int | None = None,
    thumb_url: str | None = None,
    reply_markup: InlineKeyboardMarkup | None = None,
    input_message_content: InputMessageContent | None = None,
) -> InlineQueryResultMpeg4Gif:
    return InlineQueryResultMpeg4Gif(type="mpeg4_gif", **get_params(locals()))


def inline_query_cached_sticker(
    id: str,
    sticker_file_id: str,
    *,
    reply_markup: InlineKeyboardMarkup | None = None,
) -> InlineQueryResultCachedSticker:
    return InlineQueryResultCachedSticker(type="sticker", **get_params(locals()))


def inline_query_cached_document(
    id: str,
    document_file_id: str,
    *,
    title: str | None = None,
    description: str | None = None,
    caption: str | None = None,
    parse_mode: str | None = None,
    caption_entities: list[MessageEntity] | None = None,
    reply_markup: InlineKeyboardMarkup | None = None,
    input_message_content: InputMessageContent | None = None,
) -> InlineQueryResultCachedDocument:
    return InlineQueryResultCachedDocument(type="document", **get_params(locals()))


def inline_query_cached_audio(
    id: str,
    audio_file_id: str,
    *,
    caption: str | None = None,
    parse_mode: str | None = None,
    caption_entities: list[MessageEntity] | None = None,
    reply_markup: InlineKeyboardMarkup | None = None,
    input_message_content: InputMessageContent | None = None,
) -> InlineQueryResultCachedAudio:
    return InlineQueryResultCachedAudio(type="audio", **get_params(locals()))


def inline_query_cached_video(
    id: str,
    video_file_id: str,
    *,
    title: str | None = None,
    description: str | None = None,
    caption: str | None = None,
    parse_mode: str | None = None,
    caption_entities: list[MessageEntity] | None = None,
    reply_markup: InlineKeyboardMarkup | None = None,
    input_message_content: InputMessageContent | None = None,
) -> InlineQueryResultCachedVideo:
    return InlineQueryResultCachedVideo(type="video", **get_params(locals()))


def inline_query_cached_gif(
    id: str,
    gif_file_id: str,
    *,
    title: str | None = None,
    caption: str | None = None,
    parse_mode: str | None = None,
    caption_entities: list[MessageEntity] | None = None,
    reply_markup: InlineKeyboardMarkup | None = None,
    input_message_content: InputMessageContent | None = None,
) -> InlineQueryResultCachedGif:
    return InlineQueryResultCachedGif(type="gif", **get_params(locals()))


def inline_query_cached_mpeg4_gif(
    id: str,
    mpeg4_file_id: str,
    *,
    title: str | None = None,
    caption: str | None = None,
    parse_mode: str | None = None,
    caption_entities: list[MessageEntity] | None = None,
    reply_markup: InlineKeyboardMarkup | None = None,
    input_message_content: InputMessageContent | None = None,
) -> InlineQueryResultCachedMpeg4Gif:
    return InlineQueryResultCachedMpeg4Gif(type="mpeg4_gif", **get_params(locals()))


def inline_query_cached_voice(
    id: str,
    voice_file_id: str,
    *,
    caption: str | None = None,
    parse_mode: str | None = None,
    caption_entities: list[MessageEntity] | None = None,
    reply_markup: InlineKeyboardMarkup | None = None,
    input_message_content: InputMessageContent | None = None,
) -> InlineQueryResultCachedVoice:
    return InlineQueryResultCachedVoice(type="voice", **get_params(locals()))


def inline_query_cached_photo(
    id: str,
    photo_file_id: str,
    *,
    title: str | None = None,
    description: str | None = None,
    caption: str | None = None,
    parse_mode: str | None = None,
    caption_entities: list[MessageEntity] | None = None,
    reply_markup: InlineKeyboardMarkup | None = None,
    input_message_content: InputMessageContent | None = None,
) -> InlineQueryResultCachedPhoto:
    return InlineQueryResultCachedPhoto(type="photo", **get_params(locals()))


__all__ = (
    "compose_chat_permissions",
    "compose_link_preview_options",
    "compose_reactions",
    "compose_reply_params",
    "inline_query_article",
    "inline_query_audio",
    "inline_query_cached_audio",
    "inline_query_cached_document",
    "inline_query_cached_gif",
    "inline_query_cached_mpeg4_gif",
    "inline_query_cached_photo",
    "inline_query_cached_sticker",
    "inline_query_cached_video",
    "inline_query_cached_voice",
    "inline_query_contact",
    "inline_query_document",
    "inline_query_game",
    "inline_query_gif",
    "inline_query_location",
    "inline_query_mpeg4_gif",
    "inline_query_photo",
    "inline_query_venue",
    "inline_query_video",
    "inline_query_voice",
    "input_contact_message_content",
    "input_invoice_message_content",
    "input_location_message_content",
    "input_media",
    "input_text_message_content",
    "input_venue_message_content",
)
