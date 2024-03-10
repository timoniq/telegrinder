import typing

from telegrinder.model import get_params
from telegrinder.msgspec_utils import Nothing, Option
from telegrinder.types import (
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

INPUT_MEDIA_TYPES: typing.Final[dict[str, type[InputMedia]]] = {
    "animation": InputMediaAnimation,
    "audio": InputMediaAudio,
    "document": InputMediaDocument,
    "photo": InputMediaPhoto,
    "video": InputMediaVideo,
}


def compose_reactions(
    reactions: str
    | ReactionEmoji
    | ReactionType
    | list[str | ReactionEmoji | ReactionType],
    /,
) -> list[ReactionType]:
    if not isinstance(reactions, list):
        reactions = [reactions]
    return [
        ReactionTypeEmoji("emoji", emoji)
        if isinstance(emoji, ReactionEmoji)
        else ReactionTypeEmoji("emoji", ReactionEmoji(emoji))
        if isinstance(emoji, str)
        else emoji
        for emoji in ([reactions] if isinstance(reactions, str) else reactions)
    ]


def compose_reply_params(
    message_id: int | Option[int],
    chat_id: int | str | Option[int | str],
    *,
    allow_sending_without_reply: bool | Option[bool] = Nothing,
    quote: str | Option[str] = Nothing,
    quote_parse_mode: str | Option[str] = Nothing,
    quote_entities: list[MessageEntity] | Option[list[MessageEntity]] = Nothing,
    quote_position: int | Option[int] = Nothing,
    **other: typing.Any,
) -> ReplyParameters:
    return ReplyParameters(**get_params(locals()))


def compose_link_preview_options(
    *,
    is_disabled: bool | Option[bool] = Nothing,
    url: str | Option[str] = Nothing,
    prefer_small_media: bool | Option[bool] = Nothing,
    prefer_large_media: bool | Option[bool] = Nothing,
    show_above_text: bool | Option[bool] = Nothing,
    **other: typing.Any,
) -> LinkPreviewOptions:
    return LinkPreviewOptions(**get_params(locals()))


def input_media(
    type: typing.Literal["animation", "audio", "document", "photo", "video"],
    media: str | InputFile,
    *,
    caption: str | Option[str] = Nothing,
    parse_mode: str | Option[str] = Nothing,
    caption_entities: list[MessageEntity] | Option[list[MessageEntity]] = Nothing,
    **other: typing.Any,
) -> InputMedia:
    return INPUT_MEDIA_TYPES[type](**get_params(locals()))


def input_contact_message_content(
    phone_number: str,
    first_name: str,
    *,
    last_name: str | Option[str] = Nothing,
    vcard: str | Option[str] = Nothing,
) -> InputContactMessageContent:
    return InputContactMessageContent(**get_params(locals()))


def input_invoice_message_content(
    title: str,
    description: str,
    payload: str,
    provider_token: str,
    currency: str,
    *,
    prices: list[LabeledPrice],
    max_tip_amount: int | Option[int] = Nothing,
    suggested_tip_amounts: list[int] | Option[list[int]] = Nothing,
    provider_data: str | Option[str] = Nothing,
    photo_url: str | Option[str] = Nothing,
    photo_size: int | Option[int] = Nothing,
    photo_width: int | Option[int] = Nothing,
    photo_height: int | Option[int] = Nothing,
    need_name: bool | Option[bool] = Nothing,
    need_phone_number: bool | Option[bool] = Nothing,
    need_email: bool | Option[bool] = Nothing,
    need_shipping_address: bool | Option[bool] = Nothing,
    send_phone_number_to_provider: bool | Option[bool] = Nothing,
) -> InputInvoiceMessageContent:
    return InputInvoiceMessageContent(**get_params(locals()))


def input_location_message_content(
    latitude: float,
    longitude: float,
    *,
    horizontal_accuracy: float | Option[float] = Nothing,
    live_period: int | Option[int] = Nothing,
    heading: int | Option[int] = Nothing,
    proximity_alert_radius: int | Option[int] = Nothing,
) -> InputLocationMessageContent:
    return InputLocationMessageContent(**get_params(locals()))


def input_text_message_content(
    message_text: str,
    *,
    parse_mode: str | Option[str] = Nothing,
    entities: list[MessageEntity] | Option[list[MessageEntity]] = Nothing,
    disable_web_page_preview: bool | Option[bool] = Nothing,
) -> InputTextMessageContent:
    return InputTextMessageContent(**get_params(locals()))


def input_venue_message_content(
    latitude: float,
    longitude: float,
    title: str,
    address: str,
    *,
    foursquare_id: str | Option[str] = Nothing,
    foursquare_type: str | Option[str] = Nothing,
    google_place_id: str | Option[str] = Nothing,
    google_place_type: str | Option[str] = Nothing,
) -> InputVenueMessageContent:
    return InputVenueMessageContent(**get_params(locals()))


def inline_query_article(
    id: str,
    title: str,
    input_message_content: typing.Union[
        InputTextMessageContent,
        InputLocationMessageContent,
        InputVenueMessageContent,
        InputContactMessageContent,
        InputInvoiceMessageContent,
    ],
    *,
    reply_markup: Option[InlineKeyboardMarkup] = Nothing,
    url: str | Option[str] = Nothing,
    hide_url: bool | Option[bool] = Nothing,
    description: str | Option[str] = Nothing,
    thumbnail_url: str | Option[str] = Nothing,
    thumbnail_width: int | Option[int] = Nothing,
    thumbnail_height: int | Option[int] = Nothing,
) -> InlineQueryResultArticle:
    return InlineQueryResultArticle(type="article", **get_params(locals()))


def inline_query_audio(
    id: str,
    audio_url: str,
    *,
    title: str | Option[str] = Nothing,
    caption: str | Option[str] = Nothing,
    parse_mode: str | Option[str] = Nothing,
    caption_entities: list[MessageEntity] | Option[list[MessageEntity]] = Nothing,
    performer: str | Option[str] = Nothing,
    audio_duration: int | Option[int] = Nothing,
    reply_markup: InlineKeyboardMarkup | Option[InlineKeyboardMarkup] = Nothing,
    input_message_content: typing.Union[
        InputTextMessageContent,
        InputLocationMessageContent,
        InputVenueMessageContent,
        InputContactMessageContent,
        InputInvoiceMessageContent,
    ]
    | Option[
        typing.Union[
            InputTextMessageContent,
            InputLocationMessageContent,
            InputVenueMessageContent,
            InputContactMessageContent,
            InputInvoiceMessageContent,
        ]
    ] = Nothing,
) -> InlineQueryResultAudio:
    return InlineQueryResultAudio(type="audio", **get_params(locals()))


def inline_query_contact(
    id: str,
    phone_number: str,
    first_name: str,
    *,
    last_name: str | Option[str] = Nothing,
    vcard: str | Option[str] = Nothing,
    reply_markup: InlineKeyboardMarkup | Option[InlineKeyboardMarkup] = Nothing,
    input_message_content: typing.Union[
        InputTextMessageContent,
        InputLocationMessageContent,
        InputVenueMessageContent,
        InputContactMessageContent,
        InputInvoiceMessageContent,
    ]
    | Option[
        typing.Union[
            InputTextMessageContent,
            InputLocationMessageContent,
            InputVenueMessageContent,
            InputContactMessageContent,
            InputInvoiceMessageContent,
        ]
    ] = Nothing,
    thumbnail_url: str | Option[str] = Nothing,
    thumbnail_width: int | Option[int] = Nothing,
    thumbnail_height: int | Option[int] = Nothing,
) -> InlineQueryResultContact:
    return InlineQueryResultContact(type="contact", **get_params(locals()))


def inline_query_document(
    id: str,
    title: str,
    document_url: str,
    mime_type: str,
    *,
    description: Option[str] = Nothing,
    caption: Option[str] = Nothing,
    parse_mode: Option[str] = Nothing,
    caption_entities: Option[list[MessageEntity]] = Nothing,
    reply_markup: Option[InlineKeyboardMarkup] = Nothing,
    input_message_content: typing.Union[
        InputTextMessageContent,
        InputLocationMessageContent,
        InputVenueMessageContent,
        InputContactMessageContent,
        InputInvoiceMessageContent,
    ]
    | Option[
        typing.Union[
            InputTextMessageContent,
            InputLocationMessageContent,
            InputVenueMessageContent,
            InputContactMessageContent,
            InputInvoiceMessageContent,
        ]
    ] = Nothing,
    thumbnail_url: Option[str] = Nothing,
    thumbnail_width: Option[int] = Nothing,
    thumbnail_height: Option[int] = Nothing,
) -> InlineQueryResultDocument:
    return InlineQueryResultDocument(type="document", **get_params(locals()))


def inline_query_gif(
    id: str,
    gif_url: str,
    *,
    gif_width: int | Option[int] = Nothing,
    gif_height: int | Option[int] = Nothing,
    gif_duration: int | Option[int] = Nothing,
    title: str | Option[str] = Nothing,
    caption: str | Option[str] = Nothing,
    parse_mode: str | Option[str] = Nothing,
    caption_entities: list[MessageEntity] | Option[list[MessageEntity]] = Nothing,
    reply_markup: InlineKeyboardMarkup | Option[InlineKeyboardMarkup] = Nothing,
    input_message_content: typing.Union[
        InputTextMessageContent,
        InputLocationMessageContent,
        InputVenueMessageContent,
        InputContactMessageContent,
        InputInvoiceMessageContent,
    ]
    | Option[
        typing.Union[
            InputTextMessageContent,
            InputLocationMessageContent,
            InputVenueMessageContent,
            InputContactMessageContent,
            InputInvoiceMessageContent,
        ]
    ] = Nothing,
    thumbnail_url: str | Option[str] = Nothing,
    thumbnail_mime_type: str | Option[str] = Nothing,
) -> InlineQueryResultGif:
    return InlineQueryResultGif(type="gif", **get_params(locals()))


def inline_query_location(
    id: str,
    latitude: float,
    longitude: float,
    *,
    title: str | Option[str] = Nothing,
    horizontal_accuracy: float | Option[float] = Nothing,
    live_period: int | Option[int] = Nothing,
    heading: int | Option[int] = Nothing,
    proximity_alert_radius: int | Option[int] = Nothing,
    reply_markup: InlineKeyboardMarkup | Option[InlineKeyboardMarkup] = Nothing,
    input_message_content: typing.Union[
        InputTextMessageContent,
        InputLocationMessageContent,
        InputVenueMessageContent,
        InputContactMessageContent,
        InputInvoiceMessageContent,
    ]
    | Option[
        typing.Union[
            InputTextMessageContent,
            InputLocationMessageContent,
            InputVenueMessageContent,
            InputContactMessageContent,
            InputInvoiceMessageContent,
        ]
    ] = Nothing,
    thumbnail_url: str | Option[str] = Nothing,
    thumbnail_width: int | Option[int] = Nothing,
    thumbnail_height: int | Option[int] = Nothing,
) -> InlineQueryResultLocation:
    return InlineQueryResultLocation(type="location", **get_params(locals()))


def inline_query_venue(
    id: str,
    latitude: float,
    longitude: float,
    title: str,
    address: str,
    *,
    foursquare_id: str | Option[str] = Nothing,
    foursquare_type: str | Option[str] = Nothing,
    google_place_id: str | Option[str] = Nothing,
    google_place_type: str | Option[str] = Nothing,
    reply_markup: InlineKeyboardMarkup | Option[InlineKeyboardMarkup] = Nothing,
    input_message_content: typing.Union[
        InputTextMessageContent,
        InputLocationMessageContent,
        InputVenueMessageContent,
        InputContactMessageContent,
        InputInvoiceMessageContent,
    ]
    | Option[
        typing.Union[
            InputTextMessageContent,
            InputLocationMessageContent,
            InputVenueMessageContent,
            InputContactMessageContent,
            InputInvoiceMessageContent,
        ]
    ] = Nothing,
    thumbnail_url: str | Option[str] = Nothing,
    thumbnail_width: int | Option[int] = Nothing,
    thumbnail_height: int | Option[int] = Nothing,
) -> InlineQueryResultVenue:
    return InlineQueryResultVenue(type="venue", **get_params(locals()))


def inline_query_video(
    id: str,
    video_url: str,
    mime_type: str,
    thumb_url: str,
    *,
    title: str | Option[str] = Nothing,
    caption: str | Option[str] = Nothing,
    parse_mode: str | Option[str] = Nothing,
    caption_entities: list[MessageEntity] | Option[list[MessageEntity]] = Nothing,
    video_width: int | Option[int] = Nothing,
    video_height: int | Option[int] = Nothing,
    video_duration: int | Option[int] = Nothing,
    description: str | Option[str] = Nothing,
    reply_markup: InlineKeyboardMarkup | Option[InlineKeyboardMarkup] = Nothing,
    input_message_content: typing.Union[
        InputTextMessageContent,
        InputLocationMessageContent,
        InputVenueMessageContent,
        InputContactMessageContent,
        InputInvoiceMessageContent,
    ]
    | Option[
        typing.Union[
            InputTextMessageContent,
            InputLocationMessageContent,
            InputVenueMessageContent,
            InputContactMessageContent,
            InputInvoiceMessageContent,
        ]
    ] = Nothing,
    thumbnail_url: str | Option[str] = Nothing,
    thumbnail_width: int | Option[int] = Nothing,
    thumbnail_height: int | Option[int] = Nothing,
) -> InlineQueryResultVideo:
    return InlineQueryResultVideo(type="video", **get_params(locals()))


def inline_query_game(
    id: str,
    game_short_name: str,
    *,
    reply_markup: InlineKeyboardMarkup | Option[InlineKeyboardMarkup] = Nothing,
) -> InlineQueryResultGame:
    return InlineQueryResultGame(type="game", **get_params(locals()))


def inline_query_voice(
    id: str,
    voice_url: str,
    title: str,
    *,
    caption: str | Option[str] = Nothing,
    parse_mode: str | Option[str] = Nothing,
    caption_entities: list[MessageEntity] | Option[list[MessageEntity]] = Nothing,
    reply_markup: InlineKeyboardMarkup | Option[InlineKeyboardMarkup] = Nothing,
    input_message_content: typing.Union[
        InputTextMessageContent,
        InputLocationMessageContent,
        InputVenueMessageContent,
        InputContactMessageContent,
        InputInvoiceMessageContent,
    ]
    | Option[
        typing.Union[
            InputTextMessageContent,
            InputLocationMessageContent,
            InputVenueMessageContent,
            InputContactMessageContent,
            InputInvoiceMessageContent,
        ]
    ] = Nothing,
    duration: int | Option[int] = Nothing,
) -> InlineQueryResultVoice:
    return InlineQueryResultVoice(type="voice", **get_params(locals()))


def inline_query_photo(
    id: str,
    photo_url: str,
    thumb_url: str,
    *,
    photo_width: int | Option[int] = Nothing,
    photo_height: int | Option[int] = Nothing,
    title: str | Option[str] = Nothing,
    description: str | Option[str] = Nothing,
    caption: str | Option[str] = Nothing,
    parse_mode: str | Option[str] = Nothing,
    caption_entities: list[MessageEntity] | Option[list[MessageEntity]] = Nothing,
    reply_markup: InlineKeyboardMarkup | Option[InlineKeyboardMarkup] = Nothing,
    input_message_content: typing.Union[
        InputTextMessageContent,
        InputLocationMessageContent,
        InputVenueMessageContent,
        InputContactMessageContent,
        InputInvoiceMessageContent,
    ]
    | Option[
        typing.Union[
            InputTextMessageContent,
            InputLocationMessageContent,
            InputVenueMessageContent,
            InputContactMessageContent,
            InputInvoiceMessageContent,
        ]
    ] = Nothing,
) -> InlineQueryResultPhoto:
    return InlineQueryResultPhoto(type="photo", **get_params(locals()))


def inline_query_mpeg4_gif(
    id: str,
    mpeg4_url: str,
    *,
    mpeg4_width: int | Option[int] = Nothing,
    mpeg4_height: int | Option[int] = Nothing,
    mpeg4_duration: int | Option[int] = Nothing,
    thumb_url: str | Option[str] = Nothing,
    reply_markup: InlineKeyboardMarkup | Option[InlineKeyboardMarkup] = Nothing,
    input_message_content: typing.Union[
        InputTextMessageContent,
        InputLocationMessageContent,
        InputVenueMessageContent,
        InputContactMessageContent,
        InputInvoiceMessageContent,
    ]
    | Option[
        typing.Union[
            InputTextMessageContent,
            InputLocationMessageContent,
            InputVenueMessageContent,
            InputContactMessageContent,
            InputInvoiceMessageContent,
        ]
    ] = Nothing,
) -> InlineQueryResultMpeg4Gif:
    return InlineQueryResultMpeg4Gif(type="mpeg4_gif", **get_params(locals()))


def inline_query_cached_sticker(
    id: str,
    sticker_file_id: str,
    *,
    reply_markup: InlineKeyboardMarkup | Option[InlineKeyboardMarkup] = Nothing,
) -> InlineQueryResultCachedSticker:
    return InlineQueryResultCachedSticker(type="sticker", **get_params(locals()))


def inline_query_cached_document(
    id: str,
    document_file_id: str,
    *,
    title: str | Option[str] = Nothing,
    description: str | Option[str] = Nothing,
    caption: str | Option[str] = Nothing,
    parse_mode: str | Option[str] = Nothing,
    caption_entities: list[MessageEntity] | Option[list[MessageEntity]] = Nothing,
    reply_markup: InlineKeyboardMarkup | Option[InlineKeyboardMarkup] = Nothing,
    input_message_content: typing.Union[
        InputTextMessageContent,
        InputLocationMessageContent,
        InputVenueMessageContent,
        InputContactMessageContent,
        InputInvoiceMessageContent,
    ]
    | Option[
        typing.Union[
            InputTextMessageContent,
            InputLocationMessageContent,
            InputVenueMessageContent,
            InputContactMessageContent,
            InputInvoiceMessageContent,
        ]
    ] = Nothing,
) -> InlineQueryResultCachedDocument:
    return InlineQueryResultCachedDocument(type="document", **get_params(locals()))


def inline_query_cached_audio(
    id: str,
    audio_file_id: str,
    *,
    caption: str | Option[str] = Nothing,
    parse_mode: str | Option[str] = Nothing,
    caption_entities: list[MessageEntity] | Option[list[MessageEntity]] = Nothing,
    reply_markup: InlineKeyboardMarkup | Option[InlineKeyboardMarkup] = Nothing,
    input_message_content: typing.Union[
        InputTextMessageContent,
        InputLocationMessageContent,
        InputVenueMessageContent,
        InputContactMessageContent,
        InputInvoiceMessageContent,
    ]
    | Option[
        typing.Union[
            InputTextMessageContent,
            InputLocationMessageContent,
            InputVenueMessageContent,
            InputContactMessageContent,
            InputInvoiceMessageContent,
        ]
    ] = Nothing,
) -> InlineQueryResultCachedAudio:
    return InlineQueryResultCachedAudio(type="audio", **get_params(locals()))


def inline_query_cached_video(
    id: str,
    video_file_id: str,
    *,
    title: str | Option[str] = Nothing,
    description: str | Option[str] = Nothing,
    caption: str | Option[str] = Nothing,
    parse_mode: str | Option[str] = Nothing,
    caption_entities: list[MessageEntity] | Option[list[MessageEntity]] = Nothing,
    reply_markup: InlineKeyboardMarkup | Option[InlineKeyboardMarkup] = Nothing,
    input_message_content: typing.Union[
        InputTextMessageContent,
        InputLocationMessageContent,
        InputVenueMessageContent,
        InputContactMessageContent,
        InputInvoiceMessageContent,
    ]
    | Option[
        typing.Union[
            InputTextMessageContent,
            InputLocationMessageContent,
            InputVenueMessageContent,
            InputContactMessageContent,
            InputInvoiceMessageContent,
        ]
    ] = Nothing,
) -> InlineQueryResultCachedVideo:
    return InlineQueryResultCachedVideo(type="video", **get_params(locals()))


def inline_query_cached_gif(
    id: str,
    gif_file_id: str,
    *,
    title: str | Option[str] = Nothing,
    caption: str | Option[str] = Nothing,
    parse_mode: str | Option[str] = Nothing,
    caption_entities: list[MessageEntity] | Option[list[MessageEntity]] = Nothing,
    reply_markup: InlineKeyboardMarkup | Option[InlineKeyboardMarkup] = Nothing,
    input_message_content: typing.Union[
        InputTextMessageContent,
        InputLocationMessageContent,
        InputVenueMessageContent,
        InputContactMessageContent,
        InputInvoiceMessageContent,
    ]
    | Option[
        typing.Union[
            InputTextMessageContent,
            InputLocationMessageContent,
            InputVenueMessageContent,
            InputContactMessageContent,
            InputInvoiceMessageContent,
        ]
    ] = Nothing,
) -> InlineQueryResultCachedGif:
    return InlineQueryResultCachedGif(type="gif", **get_params(locals()))


def inline_query_cached_mpeg4_gif(
    id: str,
    mpeg4_file_id: str,
    *,
    title: str | Option[str] = Nothing,
    caption: str | Option[str] = Nothing,
    parse_mode: str | Option[str] = Nothing,
    caption_entities: list[MessageEntity] | Option[list[MessageEntity]] = Nothing,
    reply_markup: InlineKeyboardMarkup | Option[InlineKeyboardMarkup] = Nothing,
    input_message_content: typing.Union[
        InputTextMessageContent,
        InputLocationMessageContent,
        InputVenueMessageContent,
        InputContactMessageContent,
        InputInvoiceMessageContent,
    ]
    | Option[
        typing.Union[
            InputTextMessageContent,
            InputLocationMessageContent,
            InputVenueMessageContent,
            InputContactMessageContent,
            InputInvoiceMessageContent,
        ]
    ] = Nothing,
) -> InlineQueryResultCachedMpeg4Gif:
    return InlineQueryResultCachedMpeg4Gif(type="mpeg4_gif", **get_params(locals()))


def inline_query_cached_voice(
    id: str,
    voice_file_id: str,
    *,
    caption: str | Option[str] = Nothing,
    parse_mode: str | Option[str] = Nothing,
    caption_entities: list[MessageEntity] | Option[list[MessageEntity]] = Nothing,
    reply_markup: InlineKeyboardMarkup | Option[InlineKeyboardMarkup] = Nothing,
    input_message_content: typing.Union[
        InputTextMessageContent,
        InputLocationMessageContent,
        InputVenueMessageContent,
        InputContactMessageContent,
        InputInvoiceMessageContent,
    ]
    | Option[
        typing.Union[
            InputTextMessageContent,
            InputLocationMessageContent,
            InputVenueMessageContent,
            InputContactMessageContent,
            InputInvoiceMessageContent,
        ]
    ] = Nothing,
) -> InlineQueryResultCachedVoice:
    return InlineQueryResultCachedVoice(type="voice", **get_params(locals()))


def inline_query_cached_photo(
    id: str,
    photo_file_id: str,
    *,
    title: str | Option[str] = Nothing,
    description: str | Option[str] = Nothing,
    caption: str | Option[str] = Nothing,
    parse_mode: str | Option[str] = Nothing,
    caption_entities: list[MessageEntity] | Option[list[MessageEntity]] = Nothing,
    reply_markup: InlineKeyboardMarkup | Option[InlineKeyboardMarkup] = Nothing,
    input_message_content: typing.Union[
        InputTextMessageContent,
        InputLocationMessageContent,
        InputVenueMessageContent,
        InputContactMessageContent,
        InputInvoiceMessageContent,
    ]
    | Option[
        typing.Union[
            InputTextMessageContent,
            InputLocationMessageContent,
            InputVenueMessageContent,
            InputContactMessageContent,
            InputInvoiceMessageContent,
        ]
    ] = Nothing,
) -> InlineQueryResultCachedPhoto:
    return InlineQueryResultCachedPhoto(type="photo", **get_params(locals()))


__all__ = (
    "compose_link_preview_options",
    "compose_reactions",
    "compose_reply_params",
    "inline_query_article",
    "inline_query_photo",
    "inline_query_mpeg4_gif",
    "inline_query_gif",
    "inline_query_video",
    "inline_query_audio",
    "inline_query_voice",
    "inline_query_document",
    "inline_query_location",
    "inline_query_venue",
    "inline_query_contact",
    "inline_query_game",
    "inline_query_cached_sticker",
    "inline_query_cached_document",
    "inline_query_cached_audio",
    "inline_query_cached_video",
    "inline_query_cached_gif",
    "inline_query_cached_mpeg4_gif",
    "inline_query_cached_voice",
    "inline_query_cached_photo",
    "input_media",
    "input_text_message_content",
    "input_location_message_content",
    "input_venue_message_content",
    "input_contact_message_content",
    "input_invoice_message_content",
)
