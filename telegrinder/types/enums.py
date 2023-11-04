import enum


class UpdateType(str, enum.Enum):
    """Type of update."""

    MESSAGE = "message"
    EDITED_MESSAGE = "edited_message"
    CHANNEL_POST = "channel_post"
    EDITED_CHANNEL_POST = "edited_channel_post"
    INLINE_QUERY = "inline_query"
    CHOSEN_INLINE_RESULT = "chosen_inline_result"
    CALLBACK_QUERY = "callback_query"
    SHIPPING_QUERY = "shipping_query"
    PRE_CHECKOUT_QUERY = "pre_checkout_query"
    POLL = "poll"
    POLL_ANSWER = "poll_answer"
    MY_CHAT_MEMBER = "my_chat_member"
    CHAT_MEMBER = "chat_member"
    CHAT_JOIN_REQUEST = "chat_join_request"


class BotCommandScopeType(str, enum.Enum):
    """Type of BotCommandScope.
    Represents the scope to which bot commands are applied."""

    DEFAULT = "default"
    ALL_PRIVATE_CHATS = "all_private_chats"
    ALL_GROUP_CHATS = "all_group_chats"
    ALL_CHAT_ADMINISTRATORS = "all_chat_administrators"
    CHAT = "chat"
    CHAT_ADMINISTRATORS = "chat_administrators"
    CHAT_MEMBER = "chat_member"


class ChatType(str, enum.Enum):
    """Type of chat, can be either “private”, “group”, “supergroup” or “channel”"""

    PRIVATE = "private"
    GROUP = "group"
    SUPERGROUP = "supergroup"
    CHANNEL = "channel"


class ChatMemberStatus(str, enum.Enum):
    """This object represents chat member status."""

    CREATOR = "creator"
    ADMINISTRATOR = "administrator"
    MEMBER = "member"
    RESTRICTED = "restricted"
    LEFT = "left"
    KICKED = "kicked"


class DiceEmoji(str, enum.Enum):
    """Emoji on which the dice throw animation is based."""

    DICE = "🎲"
    DART = "🎯"
    BASKETBALL = "🏀"
    FOOTBALL = "⚽"
    SLOT_MACHINE = "🎰"
    BOWLING = "🎳"


class MessageEntityType(str, enum.Enum):
    """Type of the entity. Currently, can be “mention” (`@username`), “hashtag”
    (`#hashtag`), “cashtag” (`$USD`), “bot_command” (`/start@jobs_bot`),
    “url” (`https://telegram.org`), “email” (`do-not-reply@telegram.org`),
    “phone_number” (`+1-212-555-0123`), “bold” (**bold text**), “italic”
    (*italic text*), “underline” (underlined text), “strikethrough” (strikethrough
    text), “spoiler” (spoiler message), “code” (monowidth string), “pre”
    (monowidth block), “text_link” (for clickable text URLs), “text_mention”
    (for users [without usernames](https://telegram.org/blog/edit#new-mentions)),
    “custom_emoji” (for inline custom emoji stickers)"""

    MENTION = "mention"
    HASHTAG = "hashtag"
    CASHTAG = "cashtag"
    BOT_COMMAND = "bot_command"
    URL = "url"
    EMAIL = "email"
    PHONE_NUMBER = "phone_number"
    BOLD = "bold"
    ITALIC = "italic"
    UNDERLINE = "underline"
    STRIKETHROUGH = "strikethrough"
    SPOILER = "spoiler"
    CODE = "code"
    PRE = "pre"
    TEXT_LINK = "text_link"
    TEXT_MENTION = "text_mention"
    CUSTOM_EMOJI = "custom_emoji"


class PollType(str, enum.Enum):
    """Poll type, currently can be “regular” or “quiz”"""

    REGULAR = "regular"
    QUIZ = "quiz"


class StickerType(str, enum.Enum):
    """Type of the sticker, currently one of “regular”, “mask”, “custom_emoji”.
    The type of the sticker is independent from its format, which is determined
    by the fields *is_animated* and *is_video*."""

    REGULAR = "regular"
    MASK = "mask"
    CUSTOM_EMOJI = "custom_emoji"


class StickerSetStickerType(str, enum.Enum):
    """Type of stickers in the set, currently one of “regular”, “mask”, “custom_emoji”"""

    REGULAR = "regular"
    MASK = "mask"
    CUSTOM_EMOJI = "custom_emoji"


class MaskPositionPoint(str, enum.Enum):
    """The part of the face relative to which the mask should be placed. One of “forehead”,
    “eyes”, “mouth”, or “chin”."""

    FOREHEAD = "forehead"
    EYES = "eyes"
    MOUTH = "mouth"
    CHIN = "chin"


class InlineQueryChatType(str, enum.Enum):
    """*Optional*. Type of the chat from which the inline query was sent. Can be
    either “sender” for a private chat with the inline query sender, “private”,
    “group”, “supergroup”, or “channel”. The chat type should be always known
    for requests sent from official clients and most third-party clients,
    unless the request was sent from a secret chat"""

    SENDER = "sender"
    PRIVATE = "private"
    GROUP = "group"
    SUPERGROUP = "supergroup"
    CHANNEL = "channel"


class InlineQueryResultMimeType(str, enum.Enum):
    """MIME type of the content of the video URL, “text/html” or “video/mp4”"""

    TEXT_HTML = "text/html"
    VIDEO_MP4 = "video/mp4"


class InlineQueryResultThumbnailMimeType(str, enum.Enum):
    """*Optional*. MIME type of the thumbnail, must be one of “image/jpeg”, “image/gif”,
    or “video/mp4”. Defaults to “image/jpeg”"""

    IMAGE_JPEG = "image/jpeg"
    IMAGE_GIF = "image/gif"
    VIDEO_MP4 = "video/mp4"


class InlineQueryResultGifThumbnailMimeType(str, enum.Enum):
    """*Optional*. MIME type of the thumbnail, must be one of “image/jpeg”, “image/gif”,
    or “video/mp4”. Defaults to “image/jpeg”"""

    IMAGE_JPEG = "image/jpeg"
    IMAGE_GIF = "image/gif"
    VIDEO_MP4 = "video/mp4"


class InlineQueryResultMpeg4GifThumbnailMimeType(str, enum.Enum):
    """*Optional*. MIME type of the thumbnail, must be one of “image/jpeg”, “image/gif”,
    or “video/mp4”. Defaults to “image/jpeg”"""

    IMAGE_JPEG = "image/jpeg"
    IMAGE_GIF = "image/gif"
    VIDEO_MP4 = "video/mp4"


class InlineQueryResultVideoMimeType(str, enum.Enum):
    """MIME type of the content of the video URL, “text/html” or “video/mp4”"""

    TEXT_HTML = "text/html"
    VIDEO_MP4 = "video/mp4"


class InlineQueryResultDocumentMimeType(str, enum.Enum):
    """MIME type of the content of the file, either “application/pdf” or “application/zip”"""

    APPLICATION_PDF = "application/pdf"
    APPLICATION_ZIP = "application/zip"


class EncryptedPassportElementType(str, enum.Enum):
    """Element type. One of “personal_details”, “passport”, “driver_license”,
    “identity_card”, “internal_passport”, “address”, “utility_bill”,
    “bank_statement”, “rental_agreement”, “passport_registration”,
    “temporary_registration”, “phone_number”, “email”."""

    PERSONAL_DETAILS = "personal_details"
    PASSPORT = "passport"
    DRIVER_LICENSE = "driver_license"
    IDENTITY_CARD = "identity_card"
    INTERNAL_PASSPORT = "internal_passport"
    ADDRESS = "address"
    UTILITY_BILL = "utility_bill"
    BANK_STATEMENT = "bank_statement"
    RENTAL_AGREEMENT = "rental_agreement"
    PASSPORT_REGISTRATION = "passport_registration"
    TEMPORARY_REGISTRATION = "temporary_registration"
    PHONE_NUMBER = "phone_number"
    EMAIL = "email"


class PassportElementErrorDataFieldType(str, enum.Enum):
    """The section of the user's Telegram Passport which has the error, one of “personal_details”,
    “passport”, “driver_license”, “identity_card”, “internal_passport”,
    “address”"""

    PERSONAL_DETAILS = "personal_details"
    PASSPORT = "passport"
    DRIVER_LICENSE = "driver_license"
    IDENTITY_CARD = "identity_card"
    INTERNAL_PASSPORT = "internal_passport"
    ADDRESS = "address"


class PassportElementErrorFrontSideType(str, enum.Enum):
    """The section of the user's Telegram Passport which has the issue, one of “passport”,
    “driver_license”, “identity_card”, “internal_passport”"""

    PASSPORT = "passport"
    DRIVER_LICENSE = "driver_license"
    IDENTITY_CARD = "identity_card"
    INTERNAL_PASSPORT = "internal_passport"


class PassportElementErrorReverseSideType(str, enum.Enum):
    """The section of the user's Telegram Passport which has the issue, one of “driver_license”,
    “identity_card”"""

    DRIVER_LICENSE = "driver_license"
    IDENTITY_CARD = "identity_card"


class PassportElementErrorSelfieType(str, enum.Enum):
    """The section of the user's Telegram Passport which has the issue, one of “passport”,
    “driver_license”, “identity_card”, “internal_passport”"""

    PASSPORT = "passport"
    DRIVER_LICENSE = "driver_license"
    IDENTITY_CARD = "identity_card"
    INTERNAL_PASSPORT = "internal_passport"


class PassportElementErrorFileType(str, enum.Enum):
    """The section of the user's Telegram Passport which has the issue, one of “utility_bill”,
    “bank_statement”, “rental_agreement”, “passport_registration”,
    “temporary_registration”"""

    UTILITY_BILL = "utility_bill"
    BANK_STATEMENT = "bank_statement"
    RENTAL_AGREEMENT = "rental_agreement"
    PASSPORT_REGISTRATION = "passport_registration"
    TEMPORARY_REGISTRATION = "temporary_registration"


class PassportElementErrorFilesType(str, enum.Enum):
    """The section of the user's Telegram Passport which has the issue, one of “utility_bill”,
    “bank_statement”, “rental_agreement”, “passport_registration”,
    “temporary_registration”"""

    UTILITY_BILL = "utility_bill"
    BANK_STATEMENT = "bank_statement"
    RENTAL_AGREEMENT = "rental_agreement"
    PASSPORT_REGISTRATION = "passport_registration"
    TEMPORARY_REGISTRATION = "temporary_registration"


class PassportElementErrorTranslationFileType(str, enum.Enum):
    """Type of element of the user's Telegram Passport which has the issue, one
    of “passport”, “driver_license”, “identity_card”, “internal_passport”,
    “utility_bill”, “bank_statement”, “rental_agreement”, “passport_registration”,
    “temporary_registration”"""

    PASSPORT = "passport"
    DRIVER_LICENSE = "driver_license"
    IDENTITY_CARD = "identity_card"
    INTERNAL_PASSPORT = "internal_passport"
    UTILITY_BILL = "utility_bill"
    BANK_STATEMENT = "bank_statement"
    RENTAL_AGREEMENT = "rental_agreement"
    PASSPORT_REGISTRATION = "passport_registration"
    TEMPORARY_REGISTRATION = "temporary_registration"


class PassportElementErrorTranslationFilesType(str, enum.Enum):
    """Type of element of the user's Telegram Passport which has the issue, one
    of “passport”, “driver_license”, “identity_card”, “internal_passport”,
    “utility_bill”, “bank_statement”, “rental_agreement”, “passport_registration”,
    “temporary_registration”"""

    PASSPORT = "passport"
    DRIVER_LICENSE = "driver_license"
    IDENTITY_CARD = "identity_card"
    INTERNAL_PASSPORT = "internal_passport"
    UTILITY_BILL = "utility_bill"
    BANK_STATEMENT = "bank_statement"
    RENTAL_AGREEMENT = "rental_agreement"
    PASSPORT_REGISTRATION = "passport_registration"
    TEMPORARY_REGISTRATION = "temporary_registration"


class StickerFormat(str, enum.Enum):
    """Format of the sticker."""

    STATIC = "static"
    ANIMATED = "animated"
    VIDEO = "video"
