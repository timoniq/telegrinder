from msgspex import BaseEnumMeta, IntEnum, StrEnum


class ProgrammingLanguage(StrEnum, metaclass=BaseEnumMeta):
    """Type of ProgrammingLanguage."""

    ASSEMBLY = "assembly"
    PYTHON = "python"
    RUST = "rust"
    RUBY = "ruby"
    JAVA = "java"
    C = "c"
    C_SHARP = "cs"
    CPP = "cpp"
    CSS = "css"
    OBJECTIVE_C = "Objective-C"
    CYTHON = "cython"
    CARBON = "carbon"
    COBRA = "cobra"
    SWIFT = "swift"
    LAURELANG = "laurelang"
    DART = "dart"
    DELPHI = "delphi"
    ELIXIR = "elixir"
    HASKELL = "haskell"
    PASCAL = "pascal"
    TYPE_SCRIPT = "ts"
    JAVA_SCRIPT = "js"
    PHP = "php"
    GO = "go"
    SQL = "sql"
    F_SHARP = "fs"
    FORTRAN = "fortran"
    KOTLIN = "kotlin"
    HTML = "html"
    YAML = "yaml"
    JSON = "json"
    MARKDOWN = "markdown"
    MARKUP = "markup"


class ChatAction(StrEnum, metaclass=BaseEnumMeta):
    """Type of ChatAction.

    Choose one, depending on what the user is about to receive:
    - typing for text messages,
    - upload_photo for photos,
    - record_video or upload_video for videos,
    - record_voice or upload_voice for voice notes,
    - upload_document for general files,
    - choose_sticker for stickers,
    - find_location for location data,
    - record_video_note or upload_video_note for video notes.

    Docs: https://core.telegram.org/bots/api#sendchataction
    """

    TYPING = "typing"
    UPLOAD_PHOTO = "upload_photo"
    RECORD_VIDEO = "record_video"
    UPLOAD_VIDEO = "upload_video"
    RECORD_VOICE = "record_voice"
    UPLOAD_VOICE = "upload_voice"
    UPLOAD_DOCUMENT = "upload_document"
    CHOOSE_STICKER = "choose_sticker"
    FIND_LOCATION = "find_location"
    RECORD_VIDEO_NOTE = "record_video_note"
    UPLOAD_VIDEO_NOTE = "upload_video_note"


class ReactionEmoji(StrEnum, metaclass=BaseEnumMeta):
    """Type of ReactionEmoji.

    Currently, it can be one of `👍`, `👎`, `❤`, `🔥`, `🥰`, `👏`,
    `😁`, `🤔`, `🤯`, `😱`, `🤬`, `😢`, `🎉`, `🤩`, `🤮`, `💩`, `🙏`, `👌`, `🕊`, `🤡`, `🥱`,
    `🥴`, `😍`, `🐳`, `❤‍🔥`, `🌚`, `🌭`, `💯`, `🤣`, `⚡`, `🍌`, `🏆`, `💔`, `🤨`, `😐`, `🍓`,
    `🍾`, `💋`, `🖕`, `😈`, `😴`, `😭`, `🤓`, `👻`, `👨‍💻`, `👀`, `🎃`, `🙈`, `😇`, `😨`, `🤝`,
    `✍`, `🤗`, `🫡`, `🎅`, `🎄`, `☃`, `💅`, `🤪`, `🗿`, `🆒`, `💘`, `🙉`, `🦄`, `😘`, `💊`,
    `🙊`, `😎`, `👾`, `🤷‍♂`, `🤷`, `🤷‍♀`, `😡`.

    Docs: https://core.telegram.org/bots/api#reactiontypeemoji
    """

    THUMBS_UP = "👍"
    THUMBS_DOWN = "👎"
    RED_HEART = "❤"
    FIRE = "🔥"
    SMILING_FACE_WITH_HEARTS = "🥰"
    CLAPPING_HANDS = "👏"
    BEAMING_FACE_WITH_SMILING_EYES = "😁"
    THINKING_FACE = "🤔"
    EXPLODING_HEAD = "🤯"
    FACE_SCREAMING_IN_FEAR = "😱"
    FACE_WITH_SYMBOLS_ON_MOUTH = "🤬"
    CRYING_FACE = "😢"
    PARTY_POPPER = "🎉"
    STAR_STRUCK = "🤩"
    FACE_VOMITING = "🤮"
    PILE_OF_POO = "💩"
    FOLDED_HANDS = "🙏"
    OK_HAND = "👌"
    DOVE = "🕊"
    CLOWN_FACE = "🤡"
    YAWNING_FACE = "🥱"
    WOOZY_FACE = "🥴"
    SMILING_FACE_WITH_HEART_EYES = "😍"
    SPOUTING_WHALE = "🐳"
    HEART_ON_FIRE = "❤‍🔥"
    NEW_MOON_FACE = "🌚"
    HOT_DOG = "🌭"
    HUNDRED_POINTS = "💯"
    ROLLING_ON_THE_FLOOR_LAUGHING = "🤣"
    HIGH_VOLTAGE = "⚡"
    BANANA = "🍌"
    TROPHY = "🏆"
    BROKEN_HEART = "💔"
    FACE_WITH_RAISED_EYEBROW = "🤨"
    NEUTRAL_FACE = "😐"
    STRAWBERRY = "🍓"
    BOTTLE_WITH_POPPING_CORK = "🍾"
    KISS_MARK = "💋"
    MIDDLE_FINGER = "🖕"
    SMILING_FACE_WITH_HORNS = "😈"
    SLEEPING_FACE = "😴"
    LOUDLY_CRYING_FACE = "😭"
    NERD_FACE = "🤓"
    GHOST = "👻"
    MAN_TECHNOLOGIST = "👨‍💻"
    EYES = "👀"
    JACK_O_LANTERN = "🎃"
    SEE_NO_EVIL_MONKEY = "🙈"
    SMILING_FACE_WITH_HALO = "😇"
    FEARFUL_FACE = "😨"
    HANDSHAKE = "🤝"
    WRITING_HAND = "✍"
    SMILING_FACE_WITH_OPEN_HANDS = "🤗"
    SALUTING_FACE = "🫡"
    SANTA_CLAUS = "🎅"
    CHRISTMAS_TREE = "🎄"
    SNOWMAN = "☃"
    NAIL_POLISH = "💅"
    ZANY_FACE = "🤪"
    MOAI = "🗿"
    COOL_BUTTON = "🆒"
    HEART_WITH_ARROW = "💘"
    HEAR_NO_EVIL_MONKEY = "🙉"
    UNICORN = "🦄"
    FACE_BLOWING_A_KISS = "😘"
    PILL = "💊"
    SPEAK_NO_EVIL_MONKEY = "🙊"
    SMILING_FACE_WITH_SUNGLASSES = "😎"
    ALIEN_MONSTER = "👾"
    MAN_SHRUGGING = "🤷‍♂"
    PERSON_SHRUGGING = "🤷"
    WOMAN_SHRUGGING = "🤷‍♀"
    ENRAGED_FACE = "😡"


class DefaultAccentColor(IntEnum, metaclass=BaseEnumMeta):
    """Type of DefaultAccentColor.

    One of 7 possible user colors:
    - Red
    - Orange
    - Purple
    - Green
    - Cyan
    - Blue
    - Pink

    Docs: https://core.telegram.org/bots/api#accent-colors
    """

    RED = 0
    ORANGE = 1
    PURPLE = 2
    GREEN = 3
    CYAN = 4
    BLUE = 5
    PINK = 6


class TopicIconColor(IntEnum, metaclass=BaseEnumMeta):
    """Type of TopicIconColor.

    Docs: https://github.com/telegramdesktop/tdesktop/blob/991fe491c5ae62705d77aa8fdd44a79caf639c45/Telegram/SourceFiles/data/data_forum_topic.cpp#L51-L56
    """

    BLUE = 0x6FB9F0
    YELLOW = 0xFFD67E
    VIOLET = 0xCB86DB
    GREEN = 0x8EEE98
    ROSE = 0xFF93B2
    RED = 0xFB6F5F


class ChatBoostSourceType(StrEnum, metaclass=BaseEnumMeta):
    """Type of ChatBoostSourceType
    Docs: https://core.telegram.org/bots/api#chatboostsource
    """

    PREMIUM = "premium"
    GIFT_CODE = "gift_code"
    GIVEAWAY = "giveaway"


class ContentType(StrEnum, metaclass=BaseEnumMeta):
    """Type of ContentType."""

    TEXT = "text"
    ANIMATION = "animation"
    AUDIO = "audio"
    DOCUMENT = "document"
    PAID_MEDIA = "paid_media"
    PHOTO = "photo"
    STICKER = "sticker"
    STORY = "story"
    VIDEO = "video"
    VIDEO_NOTE = "video_note"
    VOICE = "voice"
    CHECKLIST = "checklist"
    CONTACT = "contact"
    DICE = "dice"
    GAME = "game"
    POLL = "poll"
    VENUE = "venue"
    LOCATION = "location"
    NEW_CHAT_MEMBERS = "new_chat_members"
    LEFT_CHAT_MEMBER = "left_chat_member"
    CHAT_OWNER_LEFT = "chat_owner_left"
    CHAT_OWNER_CHANGED = "chat_owner_changed"
    NEW_CHAT_TITLE = "new_chat_title"
    NEW_CHAT_PHOTO = "new_chat_photo"
    DELETE_CHAT_PHOTO = "delete_chat_photo"
    GROUP_CHAT_CREATED = "group_chat_created"
    SUPERGROUP_CHAT_CREATED = "supergroup_chat_created"
    CHANNEL_CHAT_CREATED = "channel_chat_created"
    MESSAGE_AUTO_DELETE_TIMER_CHANGED = "message_auto_delete_timer_changed"
    MIGRATE_TO_CHAT_ID = "migrate_to_chat_id"
    MIGRATE_FROM_CHAT_ID = "migrate_from_chat_id"
    PINNED_MESSAGE = "pinned_message"
    INVOICE = "invoice"
    SUCCESSFUL_PAYMENT = "successful_payment"
    REFUNDED_PAYMENT = "refunded_payment"
    USERS_SHARED = "users_shared"
    CHAT_SHARED = "chat_shared"
    GIFT = "gift"
    UNIQUE_GIFT = "unique_gift"
    GIFT_UPGRADE_SENT = "gift_upgrade_sent"
    CONNECTED_WEBSITE = "connected_website"
    WRITE_ACCESS_ALLOWED = "write_access_allowed"
    PASSPORT_DATA = "passport_data"
    PROXIMITY_ALERT_TRIGGERED = "proximity_alert_triggered"
    BOOST_ADDED = "boost_added"
    CHAT_BACKGROUND_SET = "chat_background_set"
    CHECKLIST_TASKS_DONE = "checklist_tasks_done"
    CHECKLIST_TASKS_ADDED = "checklist_tasks_added"
    DIRECT_MESSAGE_PRICE_CHANGED = "direct_message_price_changed"
    FORUM_TOPIC_CREATED = "forum_topic_created"
    FORUM_TOPIC_EDITED = "forum_topic_edited"
    FORUM_TOPIC_CLOSED = "forum_topic_closed"
    FORUM_TOPIC_REOPENED = "forum_topic_reopened"
    GENERAL_FORUM_TOPIC_HIDDEN = "general_forum_topic_hidden"
    GENERAL_FORUM_TOPIC_UNHIDDEN = "general_forum_topic_unhidden"
    GIVEAWAY_CREATED = "giveaway_created"
    GIVEAWAY = "giveaway"
    GIVEAWAY_WINNERS = "giveaway_winners"
    GIVEAWAY_COMPLETED = "giveaway_completed"
    MANAGED_BOT_CREATED = "managed_bot_created"
    PAID_MESSAGE_PRICE_CHANGED = "paid_message_price_changed"
    POLL_OPTION_ADDED = "poll_option_added"
    POLL_OPTION_DELETED = "poll_option_deleted"
    SUGGESTED_POST_APPROVED = "suggested_post_approved"
    SUGGESTED_POST_APPROVAL_FAILED = "suggested_post_approval_failed"
    SUGGESTED_POST_DECLINED = "suggested_post_declined"
    SUGGESTED_POST_PAID = "suggested_post_paid"
    SUGGESTED_POST_REFUNDED = "suggested_post_refunded"
    VIDEO_CHAT_SCHEDULED = "video_chat_scheduled"
    VIDEO_CHAT_STARTED = "video_chat_started"
    VIDEO_CHAT_ENDED = "video_chat_ended"
    VIDEO_CHAT_PARTICIPANTS_INVITED = "video_chat_participants_invited"
    WEB_APP_DATA = "web_app_data"
    USER_SHARED = "user_shared"
    UNKNOWN = "unknown"


class Currency(StrEnum, metaclass=BaseEnumMeta):
    """Type of Currency.
    Docs: https://core.telegram.org/bots/payments#supported-currencies
    """

    AED = "AED"
    AFN = "AFN"
    ALL = "ALL"
    AMD = "AMD"
    ARS = "ARS"
    AUD = "AUD"
    AZN = "AZN"
    BAM = "BAM"
    BDT = "BDT"
    BGN = "BGN"
    BND = "BND"
    BOB = "BOB"
    BRL = "BRL"
    BYN = "BYN"
    CAD = "CAD"
    CHF = "CHF"
    CLP = "CLP"
    CNY = "CNY"
    COP = "COP"
    CRC = "CRC"
    CZK = "CZK"
    DKK = "DKK"
    DOP = "DOP"
    DZD = "DZD"
    EGP = "EGP"
    ETB = "ETB"
    EUR = "EUR"
    GBP = "GBP"
    GEL = "GEL"
    GTQ = "GTQ"
    HKD = "HKD"
    HNL = "HNL"
    HRK = "HRK"
    HUF = "HUF"
    IDR = "IDR"
    ILS = "ILS"
    INR = "INR"
    ISK = "ISK"
    JMD = "JMD"
    JPY = "JPY"
    KES = "KES"
    KGS = "KGS"
    KRW = "KRW"
    KZT = "KZT"
    LBP = "LBP"
    LKR = "LKR"
    MAD = "MAD"
    MDL = "MDL"
    MNT = "MNT"
    MUR = "MUR"
    MVR = "MVR"
    MXN = "MXN"
    MYR = "MYR"
    MZN = "MZN"
    NGN = "NGN"
    NIO = "NIO"
    NOK = "NOK"
    NPR = "NPR"
    NZD = "NZD"
    PAB = "PAB"
    PEN = "PEN"
    PHP = "PHP"
    PKR = "PKR"
    PLN = "PLN"
    PYG = "PYG"
    QAR = "QAR"
    RON = "RON"
    RSD = "RSD"
    RUB = "RUB"
    SAR = "SAR"
    SEK = "SEK"
    SGD = "SGD"
    THB = "THB"
    TJS = "TJS"
    TRY = "TRY"
    TTD = "TTD"
    TWD = "TWD"
    TZS = "TZS"
    UAH = "UAH"
    UGX = "UGX"
    USD = "USD"
    UYU = "UYU"
    UZS = "UZS"
    VND = "VND"
    YER = "YER"
    ZAR = "ZAR"
    XTR = "XTR"
    """Telegram stars."""
    TON = "TON"
    """Toncoin."""


class InlineQueryResultType(StrEnum, metaclass=BaseEnumMeta):
    """Type of InlineQueryResultType.
    Docs: https://core.telegram.org/bots/api#inlinequeryresult
    """

    AUDIO = "audio"
    DOCUMENT = "document"
    GIF = "gif"
    MPEG4_GIF = "mpeg4_gif"
    PHOTO = "photo"
    STICKER = "sticker"
    VIDEO = "video"
    VOICE = "voice"
    ARTICLE = "article"
    CONTACT = "contact"
    GAME = "game"
    LOCATION = "location"
    VENUE = "venue"


class MenuButtonType(StrEnum, metaclass=BaseEnumMeta):
    """TType of MenuButtonType.
    Docs: https://core.telegram.org/bots/api#menubuttondefault
    """

    DEFAULT = "default"
    COMMANDS = "commands"
    WEB_APP = "web_app"


class InputMediaType(StrEnum, metaclass=BaseEnumMeta):
    """Type of InputMediaType.
    Docs: https://core.telegram.org/bots/api#inputmedia
    """

    ANIMATION = "animation"
    AUDIO = "audio"
    DOCUMENT = "document"
    PHOTO = "photo"
    VIDEO = "video"


class UpdateType(StrEnum, metaclass=BaseEnumMeta):
    """Type of update."""

    MESSAGE = "message"
    EDITED_MESSAGE = "edited_message"
    CHANNEL_POST = "channel_post"
    EDITED_CHANNEL_POST = "edited_channel_post"
    BUSINESS_CONNECTION = "business_connection"
    BUSINESS_MESSAGE = "business_message"
    EDITED_BUSINESS_MESSAGE = "edited_business_message"
    DELETED_BUSINESS_MESSAGES = "deleted_business_messages"
    MESSAGE_REACTION = "message_reaction"
    MESSAGE_REACTION_COUNT = "message_reaction_count"
    INLINE_QUERY = "inline_query"
    CHOSEN_INLINE_RESULT = "chosen_inline_result"
    CALLBACK_QUERY = "callback_query"
    SHIPPING_QUERY = "shipping_query"
    PRE_CHECKOUT_QUERY = "pre_checkout_query"
    PURCHASED_PAID_MEDIA = "purchased_paid_media"
    POLL = "poll"
    POLL_ANSWER = "poll_answer"
    MY_CHAT_MEMBER = "my_chat_member"
    CHAT_MEMBER = "chat_member"
    CHAT_JOIN_REQUEST = "chat_join_request"
    CHAT_BOOST = "chat_boost"
    REMOVED_CHAT_BOOST = "removed_chat_boost"
    MANAGED_BOT = "managed_bot"


class BotCommandScopeType(StrEnum, metaclass=BaseEnumMeta):
    """Type of BotCommandScope.
    Represents the scope to which bot commands are applied.
    """

    DEFAULT = "default"
    ALL_PRIVATE_CHATS = "all_private_chats"
    ALL_GROUP_CHATS = "all_group_chats"
    ALL_CHAT_ADMINISTRATORS = "all_chat_administrators"
    CHAT = "chat"
    CHAT_ADMINISTRATORS = "chat_administrators"
    CHAT_MEMBER = "chat_member"


class ChatType(StrEnum, metaclass=BaseEnumMeta):
    """Type of chat, can be either `private`, `group`, `supergroup` or `channel`."""

    PRIVATE = "private"
    GROUP = "group"
    SUPERGROUP = "supergroup"
    CHANNEL = "channel"
    SENDER = "sender"


class ChatMemberStatus(StrEnum, metaclass=BaseEnumMeta):
    """Type of ChatMemberStatus."""

    CREATOR = "creator"
    ADMINISTRATOR = "administrator"
    MEMBER = "member"
    RESTRICTED = "restricted"
    LEFT = "left"
    KICKED = "kicked"


class DiceEmoji(StrEnum, metaclass=BaseEnumMeta):
    """Emoji on which the dice throw animation is based."""

    DICE = "🎲"
    DART = "🎯"
    BASKETBALL = "🏀"
    FOOTBALL = "⚽"
    SLOT_MACHINE = "🎰"
    BOWLING = "🎳"


class MessageEntityType(StrEnum, metaclass=BaseEnumMeta):
    """Type of the entity.

    Read the [documentation](https://core.telegram.org/api/entities) about entities.

    Currently, can be `mention` (@username), `hashtag`
    (#hashtag or #hashtag@chatusername), `cashtag` ($USD or $USD@chatusername),
    `bot_command` (/start@jobs_bot), `url` (https://telegram.org), `email`
    (do-not-reply@telegram.org), `phone_number` (+1-212-555-0123),
    `bold` (bold text), `italic` (italic text), `underline` (underlined
    text), `strikethrough` (strikethrough text), `spoiler` (spoiler message),
    `blockquote` (block quotation), `expandable_blockquote` (collapsed-by-default
    block quotation), `code` (monowidth string), `pre` (monowidth block),
    `text_link` (for clickable text URLs), `text_mention` (for users without
    usernames), `custom_emoji` (for inline custom emoji stickers), or `date_time`
    (for formatted date and time)."""

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
    BLOCKQUOTE = "blockquote"
    EXPANDABLE_BLOCKQUOTE = "expandable_blockquote"
    CODE = "code"
    PRE = "pre"
    TEXT_LINK = "text_link"
    TEXT_MENTION = "text_mention"
    CUSTOM_EMOJI = "custom_emoji"
    DATETIME = "date_time"


class PollType(StrEnum, metaclass=BaseEnumMeta):
    """Poll type, currently can be `regular` or `quiz`."""

    REGULAR = "regular"
    QUIZ = "quiz"


class StickerType(StrEnum, metaclass=BaseEnumMeta):
    """Type of the sticker, currently one of `regular`, `mask`, `custom_emoji`.
    The type of the sticker is independent from its format, which is determined
    by the fields `is_animated` and `is_video`.
    """

    REGULAR = "regular"
    MASK = "mask"
    CUSTOM_EMOJI = "custom_emoji"


class MessageOriginType(StrEnum, metaclass=BaseEnumMeta):
    """Type of MessageOriginType
    Docs: https://core.telegram.org/bots/api#messageorigin
    """

    USER = "user"
    HIDDEN_USER = "hidden_user"
    CHAT = "chat"
    CHANNEL = "channel"


class StickerSetStickerType(StrEnum, metaclass=BaseEnumMeta):
    """Type of stickers in the set, currently one of `regular`, `mask`, `custom_emoji`."""

    REGULAR = "regular"
    MASK = "mask"
    CUSTOM_EMOJI = "custom_emoji"


class MaskPositionPoint(StrEnum, metaclass=BaseEnumMeta):
    """The part of the face relative to which the mask should be placed. One of `forehead`,
    `eyes`, `mouth`, or `chin`.
    """

    FOREHEAD = "forehead"
    EYES = "eyes"
    MOUTH = "mouth"
    CHIN = "chin"


class InlineQueryChatType(StrEnum, metaclass=BaseEnumMeta):
    """Type of the chat from which the inline query was sent. Can be
    either `sender` for a private chat with the inline query sender, `private`,
    `group`, `supergroup`, or `channel`. The chat type should be always known
    for requests sent from official clients and most third-party clients,
    unless the request was sent from a secret chat.
    """

    SENDER = "sender"
    PRIVATE = "private"
    GROUP = "group"
    SUPERGROUP = "supergroup"
    CHANNEL = "channel"


class InlineQueryResultMimeType(StrEnum, metaclass=BaseEnumMeta):
    """MIME type of the content of the video URL, `text/html` or `video/mp4`."""

    TEXT_HTML = "text/html"
    VIDEO_MP4 = "video/mp4"


class InlineQueryResultThumbnailMimeType(StrEnum, metaclass=BaseEnumMeta):
    """MIME type of the thumbnail, must be one of `image/jpeg`, `image/gif`,
    or `video/mp4`. Defaults to `image/jpeg`
    """

    IMAGE_JPEG = "image/jpeg"
    IMAGE_GIF = "image/gif"
    VIDEO_MP4 = "video/mp4"


class PassportElementErrorType(StrEnum, metaclass=BaseEnumMeta):
    """Type of PassportElementErrorType.
    Docs: https://core.telegram.org/bots/api#passportelementerror
    """

    DATA = "data"
    FRONT_SIDE = "front_side"
    REVERSE_SIDE = "reverse_side"
    SELFIE = "selfie"
    FILE = "file"
    FILES = "files"
    TRANSLATION_FILE = "translation_file"
    TRANSLATION_FILES = "translation_files"
    UNSPECIFIED = "unspecified"


class ReactionTypeType(StrEnum, metaclass=BaseEnumMeta):
    """Type of ReactionTypeType.
    Docs: https://core.telegram.org/bots/api#reactiontype
    """

    EMOJI = "emoji"
    CUSTOM_EMOJI = "custom_emoji"


class InlineQueryResultGifThumbnailMimeType(StrEnum, metaclass=BaseEnumMeta):
    """MIME type of the thumbnail, must be one of `image/jpeg`, `image/gif`,
    or `video/mp4`. Defaults to `image/jpeg`.
    """

    IMAGE_JPEG = "image/jpeg"
    IMAGE_GIF = "image/gif"
    VIDEO_MP4 = "video/mp4"


class InlineQueryResultMpeg4GifThumbnailMimeType(StrEnum, metaclass=BaseEnumMeta):
    """MIME type of the thumbnail, must be one of `image/jpeg`, `image/gif`,
    or `video/mp4`. Defaults to `image/jpeg`.
    """

    IMAGE_JPEG = "image/jpeg"
    IMAGE_GIF = "image/gif"
    VIDEO_MP4 = "video/mp4"


class InlineQueryResultVideoMimeType(StrEnum, metaclass=BaseEnumMeta):
    """MIME type of the content of the video URL, `text/html` or `video/mp4`."""

    TEXT_HTML = "text/html"
    VIDEO_MP4 = "video/mp4"


class InlineQueryResultDocumentMimeType(StrEnum, metaclass=BaseEnumMeta):
    """MIME type of the content of the file, either `application/pdf` or `application/zip`."""

    APPLICATION_PDF = "application/pdf"
    APPLICATION_ZIP = "application/zip"


class EncryptedPassportElementType(StrEnum, metaclass=BaseEnumMeta):
    """Element type. One of `personal_details`, `passport`, `driver_license`,
    `identity_card`, `internal_passport`, `address`, `utility_bill`,
    `bank_statement`, `rental_agreement`, `passport_registration`,
    `temporary_registration`, `phone_number`, `email`.
    """

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


class StickerFormat(StrEnum, metaclass=BaseEnumMeta):
    """Format of the sticker."""

    STATIC = "static"
    ANIMATED = "animated"
    VIDEO = "video"


class TransactionPartnerUserTransactionType(StrEnum, metaclass=BaseEnumMeta):
    """This object represents type of the transaction that were made by partner user."""

    INVOICE_PAYMENT = "invoice_payment"
    PAID_MEDIA_PAYMENT = "paid_media_payment"
    GIFT_PURCHASE = "gift_purchase"
    PREMIUM_PURCHASE = "premium_purchase"
    BUSINESS_ACCOUNT_TRANSFER = "business_account_transfer"


class UniqueGiftInfoOriginType(StrEnum, metaclass=BaseEnumMeta):
    """Origin of the gift.

    Currently, either `upgrade`, `transfer`, `resale`, `gifted_upgrade` or `offer`.
    """

    UPGRADE = "upgrade"
    TRANSFER = "transfer"
    RESALE = "resale"
    GIFTED_UPGRADE = "gifted_upgrade"
    OFFER = "offer"


class UniqueGiftModelRarity(StrEnum, metaclass=BaseEnumMeta):
    """Rarity of the unique gift model. Currently, can be
    `uncommon`, `rare`, `epic`, or `legendary`.
    Docs: https://core.telegram.org/bots/api#uniquegiftmodel
    """

    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


class KeyboardButtonStyle(StrEnum, metaclass=BaseEnumMeta):
    """Style of the keyboard button. Currently, can be
    `danger`, `success`, or `primary`.
    """

    DANGER = "danger"
    """Red button."""

    SUCCESS = "success"
    """Green button."""

    PRIMARY = "primary"
    """Blue button."""


class VideoQualityCodec(StrEnum, metaclass=BaseEnumMeta):
    """Codec of the video quality. Currently, can be
    `h264`, `h265`, or `av01`.
    Docs: https://core.telegram.org/bots/api#videoquality
    """

    H264 = "h264"
    H265 = "h265"
    AV01 = "av01"


class DateTimeFormat(StrEnum, metaclass=BaseEnumMeta):
    """Type of the formatting of the date and time.
    See date-time entity formatting for more details."""

    SHORT_DATE = "d"
    SHORT_TIME = "t"
    LONG_DATE = "D"
    LONG_TIME = "T"
    DAY_OF_WEEK = "W"
    RELATIVE = "R"


__all__ = (
    "BotCommandScopeType",
    "ChatAction",
    "ChatBoostSourceType",
    "ChatMemberStatus",
    "ChatType",
    "ContentType",
    "Currency",
    "DateTimeFormat",
    "DefaultAccentColor",
    "DiceEmoji",
    "EncryptedPassportElementType",
    "InlineQueryChatType",
    "InlineQueryResultDocumentMimeType",
    "InlineQueryResultGifThumbnailMimeType",
    "InlineQueryResultMimeType",
    "InlineQueryResultMpeg4GifThumbnailMimeType",
    "InlineQueryResultThumbnailMimeType",
    "InlineQueryResultVideoMimeType",
    "KeyboardButtonStyle",
    "MaskPositionPoint",
    "MessageEntityType",
    "MessageOriginType",
    "PassportElementErrorType",
    "PollType",
    "ProgrammingLanguage",
    "ReactionEmoji",
    "ReactionTypeType",
    "StickerFormat",
    "StickerSetStickerType",
    "StickerType",
    "TopicIconColor",
    "TransactionPartnerUserTransactionType",
    "UniqueGiftInfoOriginType",
    "UniqueGiftModelRarity",
    "UpdateType",
    "VideoQualityCodec",
)
