import typing
from telegrinder.model import *


class Error(Model):
    ok: bool
    error_code: int
    description: str
    parameters: typing.Optional["ResponseParameters"] = None


class Update(Model):
    update_id: int
    message: typing.Optional["Message"] = None
    edited_message: typing.Optional["Message"] = None
    channel_post: typing.Optional["Message"] = None
    edited_channel_post: typing.Optional["Message"] = None
    inline_query: typing.Optional["InlineQuery"] = None
    chosen_inline_result: typing.Optional["ChosenInlineResult"] = None
    callback_query: typing.Optional["CallbackQuery"] = None
    shipping_query: typing.Optional["ShippingQuery"] = None
    pre_checkout_query: typing.Optional["PreCheckoutQuery"] = None
    poll: typing.Optional["Poll"] = None
    poll_answer: typing.Optional["PollAnswer"] = None
    my_chat_member: typing.Optional["ChatMemberUpdated"] = None
    chat_member: typing.Optional["ChatMemberUpdated"] = None
    chat_join_request: typing.Optional["ChatJoinRequest"] = None


class WebhookInfo(Model):
    url: str
    has_custom_certificate: bool
    pending_update_count: int
    ip_address: typing.Optional[str] = None
    last_error_date: typing.Optional[int] = None
    last_error_message: typing.Optional[str] = None
    last_synchronization_error_date: typing.Optional[int] = None
    max_connections: typing.Optional[int] = None
    allowed_updates: typing.Optional[typing.List[typing.Optional[str]]] = None


class User(Model):
    id: int
    is_bot: bool
    first_name: str
    last_name: typing.Optional[str] = None
    username: typing.Optional[str] = None
    language_code: typing.Optional[str] = None
    is_premium: typing.Optional[bool] = None
    added_to_attachment_menu: typing.Optional[bool] = None
    can_join_groups: typing.Optional[bool] = None
    can_read_all_group_messages: typing.Optional[bool] = None
    supports_inline_queries: typing.Optional[bool] = None


class Chat(Model):
    id: int
    type: str
    title: typing.Optional[str] = None
    username: typing.Optional[str] = None
    first_name: typing.Optional[str] = None
    last_name: typing.Optional[str] = None
    photo: typing.Optional["ChatPhoto"] = None
    bio: typing.Optional[str] = None
    has_private_forwards: typing.Optional[bool] = None
    has_restricted_voice_and_video_messages: typing.Optional[bool] = None
    join_to_send_messages: typing.Optional[bool] = None
    join_by_request: typing.Optional[bool] = None
    description: typing.Optional[str] = None
    invite_link: typing.Optional[str] = None
    pinned_message: typing.Optional["Message"] = None
    permissions: typing.Optional["ChatPermissions"] = None
    slow_mode_delay: typing.Optional[int] = None
    message_auto_delete_time: typing.Optional[int] = None
    has_protected_content: typing.Optional[bool] = None
    sticker_set_name: typing.Optional[str] = None
    can_set_sticker_set: typing.Optional[bool] = None
    linked_chat_id: typing.Optional[int] = None
    location: typing.Optional["ChatLocation"] = None


class Message(Model):
    message_id: int
    from_: typing.Optional["User"] = None
    sender_chat: typing.Optional["Chat"] = None
    date: int
    chat: "Chat"
    forward_from: typing.Optional["User"] = None
    forward_from_chat: typing.Optional["Chat"] = None
    forward_from_message_id: typing.Optional[int] = None
    forward_signature: typing.Optional[str] = None
    forward_sender_name: typing.Optional[str] = None
    forward_date: typing.Optional[int] = None
    is_automatic_forward: typing.Optional[bool] = None
    reply_to_message: typing.Optional["Message"] = None
    via_bot: typing.Optional["User"] = None
    edit_date: typing.Optional[int] = None
    has_protected_content: typing.Optional[bool] = None
    media_group_id: typing.Optional[str] = None
    author_signature: typing.Optional[str] = None
    text: typing.Optional[str] = None
    entities: typing.Optional[typing.List[typing.Optional["MessageEntity"]]] = None
    animation: typing.Optional["Animation"] = None
    audio: typing.Optional["Audio"] = None
    document: typing.Optional["Document"] = None
    photo: typing.Optional[typing.List[typing.Optional["PhotoSize"]]] = None
    sticker: typing.Optional["Sticker"] = None
    video: typing.Optional["Video"] = None
    video_note: typing.Optional["VideoNote"] = None
    voice: typing.Optional["Voice"] = None
    caption: typing.Optional[str] = None
    caption_entities: typing.Optional[
        typing.List[typing.Optional["MessageEntity"]]
    ] = None
    contact: typing.Optional["Contact"] = None
    dice: typing.Optional["Dice"] = None
    game: typing.Optional["Game"] = None
    poll: typing.Optional["Poll"] = None
    venue: typing.Optional["Venue"] = None
    location: typing.Optional["Location"] = None
    new_chat_members: typing.Optional[typing.List[typing.Optional["User"]]] = None
    left_chat_member: typing.Optional["User"] = None
    new_chat_title: typing.Optional[str] = None
    new_chat_photo: typing.Optional[typing.List[typing.Optional["PhotoSize"]]] = None
    delete_chat_photo: typing.Optional[bool] = None
    group_chat_created: typing.Optional[bool] = None
    supergroup_chat_created: typing.Optional[bool] = None
    channel_chat_created: typing.Optional[bool] = None
    message_auto_delete_timer_changed: typing.Optional[
        "MessageAutoDeleteTimerChanged"
    ] = None
    migrate_to_chat_id: typing.Optional[int] = None
    migrate_from_chat_id: typing.Optional[int] = None
    pinned_message: typing.Optional["Message"] = None
    invoice: typing.Optional["Invoice"] = None
    successful_payment: typing.Optional["SuccessfulPayment"] = None
    connected_website: typing.Optional[str] = None
    passport_data: typing.Optional["PassportData"] = None
    proximity_alert_triggered: typing.Optional["ProximityAlertTriggered"] = None
    video_chat_scheduled: typing.Optional["VideoChatScheduled"] = None
    video_chat_started: typing.Optional["VideoChatStarted"] = None
    video_chat_ended: typing.Optional["VideoChatEnded"] = None
    video_chat_participants_invited: typing.Optional[
        "VideoChatParticipantsInvited"
    ] = None
    web_app_data: typing.Optional["WebAppData"] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None

    @property
    def from_user(self) -> "User":
        return self.from_

    def __eq__(self, other: "Message"):
        return self.message_id == other.message_id and self.chat.id == other.chat.id


class MessageId(Model):
    message_id: int


class MessageEntity(Model):
    type: str
    offset: int
    length: int
    url: typing.Optional[str] = None
    user: typing.Optional["User"] = None
    language: typing.Optional[str] = None
    custom_emoji_id: typing.Optional[str] = None


class PhotoSize(Model):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: typing.Optional[int] = None


class Animation(Model):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumb: typing.Optional["PhotoSize"] = None
    file_name: typing.Optional[str] = None
    mime_type: typing.Optional[str] = None
    file_size: typing.Optional[int] = None


class Audio(Model):
    file_id: str
    file_unique_id: str
    duration: int
    performer: typing.Optional[str] = None
    title: typing.Optional[str] = None
    file_name: typing.Optional[str] = None
    mime_type: typing.Optional[str] = None
    file_size: typing.Optional[int] = None
    thumb: typing.Optional["PhotoSize"] = None


class Document(Model):
    file_id: str
    file_unique_id: str
    thumb: typing.Optional["PhotoSize"] = None
    file_name: typing.Optional[str] = None
    mime_type: typing.Optional[str] = None
    file_size: typing.Optional[int] = None


class Video(Model):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumb: typing.Optional["PhotoSize"] = None
    file_name: typing.Optional[str] = None
    mime_type: typing.Optional[str] = None
    file_size: typing.Optional[int] = None


class VideoNote(Model):
    file_id: str
    file_unique_id: str
    length: int
    duration: int
    thumb: typing.Optional["PhotoSize"] = None
    file_size: typing.Optional[int] = None


class Voice(Model):
    file_id: str
    file_unique_id: str
    duration: int
    mime_type: typing.Optional[str] = None
    file_size: typing.Optional[int] = None


class Contact(Model):
    phone_number: str
    first_name: str
    last_name: typing.Optional[str] = None
    user_id: typing.Optional[int] = None
    vcard: typing.Optional[str] = None


class Dice(Model):
    emoji: str
    value: int


class PollOption(Model):
    text: str
    voter_count: int


class PollAnswer(Model):
    poll_id: str
    user: "User"
    option_ids: typing.List[int]


class Poll(Model):
    id: str
    question: str
    options: typing.List["PollOption"]
    total_voter_count: int
    is_closed: bool
    is_anonymous: bool
    type: str
    allows_multiple_answers: bool
    correct_option_id: typing.Optional[int] = None
    explanation: typing.Optional[str] = None
    explanation_entities: typing.Optional[
        typing.List[typing.Optional["MessageEntity"]]
    ] = None
    open_period: typing.Optional[int] = None
    close_date: typing.Optional[int] = None


class Location(Model):
    longitude: float
    latitude: float
    horizontal_accuracy: typing.Optional[float] = None
    live_period: typing.Optional[int] = None
    heading: typing.Optional[int] = None
    proximity_alert_radius: typing.Optional[int] = None


class Venue(Model):
    location: "Location"
    title: str
    address: str
    foursquare_id: typing.Optional[str] = None
    foursquare_type: typing.Optional[str] = None
    google_place_id: typing.Optional[str] = None
    google_place_type: typing.Optional[str] = None


class WebAppData(Model):
    data: str
    button_text: str


class ProximityAlertTriggered(Model):
    traveler: "User"
    watcher: "User"
    distance: int


class MessageAutoDeleteTimerChanged(Model):
    message_auto_delete_time: int


class VideoChatScheduled(Model):
    start_date: int


class VideoChatStarted(Model):
    pass


class VideoChatEnded(Model):
    duration: int


class VideoChatParticipantsInvited(Model):
    users: typing.List["User"]


class UserProfilePhotos(Model):
    total_count: int
    photos: typing.List[typing.List["PhotoSize"]]


class File(Model):
    file_id: str
    file_unique_id: str
    file_size: typing.Optional[int] = None
    file_path: typing.Optional[str] = None


class WebAppInfo(Model):
    url: str


class ReplyKeyboardMarkup(Model):
    keyboard: typing.List[typing.List["KeyboardButton"]]
    resize_keyboard: typing.Optional[bool] = False
    one_time_keyboard: typing.Optional[bool] = False
    input_field_placeholder: typing.Optional[str] = None
    selective: typing.Optional[bool] = None


class KeyboardButton(Model):
    text: str
    request_contact: typing.Optional[bool] = None
    request_location: typing.Optional[bool] = None
    request_poll: typing.Optional["KeyboardButtonPollType"] = None
    web_app: typing.Optional["WebAppInfo"] = None


class KeyboardButtonPollType(Model):
    type: typing.Optional[str] = None


class ReplyKeyboardRemove(Model):
    remove_keyboard: bool
    selective: typing.Optional[bool] = None


class InlineKeyboardMarkup(Model):
    inline_keyboard: typing.List[typing.List["InlineKeyboardButton"]]


class InlineKeyboardButton(Model):
    text: str
    url: typing.Optional[str] = None
    callback_data: typing.Optional[str] = None
    web_app: typing.Optional["WebAppInfo"] = None
    login_url: typing.Optional["LoginUrl"] = None
    switch_inline_query: typing.Optional[str] = None
    switch_inline_query_current_chat: typing.Optional[str] = None
    callback_game: typing.Optional["CallbackGame"] = None
    pay: typing.Optional[bool] = None


class LoginUrl(Model):
    url: str
    forward_text: typing.Optional[str] = None
    bot_username: typing.Optional[str] = None
    request_write_access: typing.Optional[bool] = None


class CallbackQuery(Model):
    id: str
    from_: "User"
    message: typing.Optional["Message"] = None
    inline_message_id: typing.Optional[str] = None
    chat_instance: str
    data: typing.Optional[str] = None
    game_short_name: typing.Optional[str] = None


class ForceReply(Model):
    force_reply: bool
    input_field_placeholder: typing.Optional[str] = None
    selective: typing.Optional[bool] = None


class ChatPhoto(Model):
    small_file_id: str
    small_file_unique_id: str
    big_file_id: str
    big_file_unique_id: str


class ChatInviteLink(Model):
    invite_link: str
    creator: "User"
    creates_join_request: bool
    is_primary: bool
    is_revoked: bool
    name: typing.Optional[str] = None
    expire_date: typing.Optional[int] = None
    member_limit: typing.Optional[int] = None
    pending_join_request_count: typing.Optional[int] = None


class ChatAdministratorRights(Model):
    is_anonymous: bool
    can_manage_chat: bool
    can_delete_messages: bool
    can_manage_video_chats: bool
    can_restrict_members: bool
    can_promote_members: bool
    can_change_info: bool
    can_invite_users: bool
    can_post_messages: typing.Optional[bool] = None
    can_edit_messages: typing.Optional[bool] = None
    can_pin_messages: typing.Optional[bool] = None


class ChatMember(Model):
    status: typing.Optional[str] = "kicked"
    user: typing.Optional["User"] = None
    is_anonymous: typing.Optional[bool] = None
    custom_title: typing.Optional[str] = None
    can_be_edited: typing.Optional[bool] = None
    can_manage_chat: typing.Optional[bool] = None
    can_delete_messages: typing.Optional[bool] = None
    can_manage_video_chats: typing.Optional[bool] = None
    can_restrict_members: typing.Optional[bool] = None
    can_promote_members: typing.Optional[bool] = None
    can_change_info: typing.Optional[bool] = None
    can_invite_users: typing.Optional[bool] = None
    can_post_messages: typing.Optional[bool] = None
    can_edit_messages: typing.Optional[bool] = None
    can_pin_messages: typing.Optional[bool] = None
    is_member: typing.Optional[bool] = None
    can_send_messages: typing.Optional[bool] = None
    can_send_media_messages: typing.Optional[bool] = None
    can_send_polls: typing.Optional[bool] = None
    can_send_other_messages: typing.Optional[bool] = None
    can_add_web_page_previews: typing.Optional[bool] = None
    until_date: typing.Optional[int] = None


class ChatMemberOwner(Model):
    status: str
    user: "User"
    is_anonymous: bool
    custom_title: typing.Optional[str] = None


class ChatMemberAdministrator(Model):
    status: str
    user: "User"
    can_be_edited: bool
    is_anonymous: bool
    can_manage_chat: bool
    can_delete_messages: bool
    can_manage_video_chats: bool
    can_restrict_members: bool
    can_promote_members: bool
    can_change_info: bool
    can_invite_users: bool
    can_post_messages: typing.Optional[bool] = None
    can_edit_messages: typing.Optional[bool] = None
    can_pin_messages: typing.Optional[bool] = None
    custom_title: typing.Optional[str] = None


class ChatMemberMember(Model):
    status: str
    user: "User"


class ChatMemberRestricted(Model):
    status: str
    user: "User"
    is_member: bool
    can_change_info: bool
    can_invite_users: bool
    can_pin_messages: bool
    can_send_messages: bool
    can_send_media_messages: bool
    can_send_polls: bool
    can_send_other_messages: bool
    can_add_web_page_previews: bool
    until_date: int


class ChatMemberLeft(Model):
    status: str
    user: "User"


class ChatMemberBanned(Model):
    status: str
    user: "User"
    until_date: int


class ChatMemberUpdated(Model):
    chat: "Chat"
    from_: "User"
    date: int
    old_chat_member: "ChatMember"
    new_chat_member: "ChatMember"
    invite_link: typing.Optional["ChatInviteLink"] = None


class ChatJoinRequest(Model):
    chat: "Chat"
    from_: "User"
    date: int
    bio: typing.Optional[str] = None
    invite_link: typing.Optional["ChatInviteLink"] = None


class ChatPermissions(Model):
    can_send_messages: typing.Optional[bool] = None
    can_send_media_messages: typing.Optional[bool] = None
    can_send_polls: typing.Optional[bool] = None
    can_send_other_messages: typing.Optional[bool] = None
    can_add_web_page_previews: typing.Optional[bool] = None
    can_change_info: typing.Optional[bool] = None
    can_invite_users: typing.Optional[bool] = None
    can_pin_messages: typing.Optional[bool] = None


class ChatLocation(Model):
    location: "Location"
    address: str


class BotCommand(Model):
    command: str
    description: str


class BotCommandScope(Model):
    type: typing.Optional[str] = "chat_member"
    chat_id: typing.Optional[
        typing.Union[typing.Optional[int], typing.Optional[str]]
    ] = None
    user_id: typing.Optional[int] = None


class BotCommandScopeDefault(Model):
    type: str


class BotCommandScopeAllPrivateChats(Model):
    type: str


class BotCommandScopeAllGroupChats(Model):
    type: str


class BotCommandScopeAllChatAdministrators(Model):
    type: str


class BotCommandScopeChat(Model):
    type: str
    chat_id: typing.Union[int, str]


class BotCommandScopeChatAdministrators(Model):
    type: str
    chat_id: typing.Union[int, str]


class BotCommandScopeChatMember(Model):
    type: str
    chat_id: typing.Union[int, str]
    user_id: int


class MenuButton(Model):
    type: typing.Optional[str] = "default"
    text: typing.Optional[str] = None
    web_app: typing.Optional["WebAppInfo"] = None


class MenuButtonCommands(Model):
    type: str


class MenuButtonWebApp(Model):
    type: str
    text: str
    web_app: "WebAppInfo"


class MenuButtonDefault(Model):
    type: str


class ResponseParameters(Model):
    migrate_to_chat_id: typing.Optional[int] = None
    retry_after: typing.Optional[int] = None


class InputMedia(Model):
    type: typing.Optional[str] = "video"
    media: typing.Optional[str] = None
    thumb: typing.Optional[
        typing.Union[typing.Optional["InputFile"], typing.Optional[str]]
    ] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[
        typing.List[typing.Optional["MessageEntity"]]
    ] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None
    duration: typing.Optional[int] = None
    disable_content_type_detection: typing.Optional[bool] = None
    performer: typing.Optional[str] = None
    title: typing.Optional[str] = None
    supports_streaming: typing.Optional[bool] = None


class InputMediaPhoto(Model):
    type: str
    media: str
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[
        typing.List[typing.Optional["MessageEntity"]]
    ] = None


class InputMediaVideo(Model):
    type: str
    media: str
    thumb: typing.Optional[
        typing.Union[typing.Optional["InputFile"], typing.Optional[str]]
    ] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[
        typing.List[typing.Optional["MessageEntity"]]
    ] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None
    duration: typing.Optional[int] = None
    supports_streaming: typing.Optional[bool] = None


class InputMediaAnimation(Model):
    type: str
    media: str
    thumb: typing.Optional[
        typing.Union[typing.Optional["InputFile"], typing.Optional[str]]
    ] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[
        typing.List[typing.Optional["MessageEntity"]]
    ] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None
    duration: typing.Optional[int] = None


class InputMediaAudio(Model):
    type: str
    media: str
    thumb: typing.Optional[
        typing.Union[typing.Optional["InputFile"], typing.Optional[str]]
    ] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[
        typing.List[typing.Optional["MessageEntity"]]
    ] = None
    duration: typing.Optional[int] = None
    performer: typing.Optional[str] = None
    title: typing.Optional[str] = None


class InputMediaDocument(Model):
    type: str
    media: str
    thumb: typing.Optional[
        typing.Union[typing.Optional["InputFile"], typing.Optional[str]]
    ] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[
        typing.List[typing.Optional["MessageEntity"]]
    ] = None
    disable_content_type_detection: typing.Optional[bool] = None


class InputFile(Model):
    pass


class Sticker(Model):
    file_id: str
    file_unique_id: str
    type: str
    width: int
    height: int
    is_animated: bool
    is_video: bool
    thumb: typing.Optional["PhotoSize"] = None
    emoji: typing.Optional[str] = None
    set_name: typing.Optional[str] = None
    premium_animation: typing.Optional["File"] = None
    mask_position: typing.Optional["MaskPosition"] = None
    custom_emoji_id: typing.Optional[str] = None
    file_size: typing.Optional[int] = None


class StickerSet(Model):
    name: str
    title: str
    sticker_type: str
    is_animated: bool
    is_video: bool
    stickers: typing.List["Sticker"]
    thumb: typing.Optional["PhotoSize"] = None


class MaskPosition(Model):
    point: str
    x_shift: float
    y_shift: float
    scale: float


class InlineQuery(Model):
    id: str
    from_: "User"
    query: str
    offset: str
    chat_type: typing.Optional[str] = None
    location: typing.Optional["Location"] = None


class InlineQueryResult(Model):
    type: typing.Optional[str] = "voice"
    id: typing.Optional[str] = None
    audio_file_id: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[
        typing.List[typing.Optional["MessageEntity"]]
    ] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None
    title: typing.Optional[str] = None
    document_file_id: typing.Optional[str] = None
    description: typing.Optional[str] = None
    gif_file_id: typing.Optional[str] = None
    mpeg4_file_id: typing.Optional[str] = None
    photo_file_id: typing.Optional[str] = None
    sticker_file_id: typing.Optional[str] = None
    video_file_id: typing.Optional[str] = None
    voice_file_id: typing.Optional[str] = None
    url: typing.Optional[str] = None
    hide_url: typing.Optional[bool] = None
    thumb_url: typing.Optional[str] = None
    thumb_width: typing.Optional[int] = None
    thumb_height: typing.Optional[int] = None
    audio_url: typing.Optional[str] = None
    performer: typing.Optional[str] = None
    audio_duration: typing.Optional[int] = None
    phone_number: typing.Optional[str] = None
    first_name: typing.Optional[str] = None
    last_name: typing.Optional[str] = None
    vcard: typing.Optional[str] = None
    game_short_name: typing.Optional[str] = None
    document_url: typing.Optional[str] = None
    mime_type: typing.Optional[str] = None
    gif_url: typing.Optional[str] = None
    gif_width: typing.Optional[int] = None
    gif_height: typing.Optional[int] = None
    gif_duration: typing.Optional[int] = None
    thumb_mime_type: typing.Optional[str] = "image/jpeg"
    latitude: typing.Optional[float] = None
    longitude: typing.Optional[float] = None
    horizontal_accuracy: typing.Optional[float] = None
    live_period: typing.Optional[int] = None
    heading: typing.Optional[int] = None
    proximity_alert_radius: typing.Optional[int] = None
    mpeg4_url: typing.Optional[str] = None
    mpeg4_width: typing.Optional[int] = None
    mpeg4_height: typing.Optional[int] = None
    mpeg4_duration: typing.Optional[int] = None
    photo_url: typing.Optional[str] = None
    photo_width: typing.Optional[int] = None
    photo_height: typing.Optional[int] = None
    address: typing.Optional[str] = None
    foursquare_id: typing.Optional[str] = None
    foursquare_type: typing.Optional[str] = None
    google_place_id: typing.Optional[str] = None
    google_place_type: typing.Optional[str] = None
    video_url: typing.Optional[str] = None
    video_width: typing.Optional[int] = None
    video_height: typing.Optional[int] = None
    video_duration: typing.Optional[int] = None
    voice_url: typing.Optional[str] = None
    voice_duration: typing.Optional[int] = None


class InlineQueryResultArticle(Model):
    type: str
    id: str
    title: str
    input_message_content: "InputMessageContent"
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    url: typing.Optional[str] = None
    hide_url: typing.Optional[bool] = None
    description: typing.Optional[str] = None
    thumb_url: typing.Optional[str] = None
    thumb_width: typing.Optional[int] = None
    thumb_height: typing.Optional[int] = None


class InlineQueryResultPhoto(Model):
    type: str
    id: str
    photo_url: str
    thumb_url: str
    photo_width: typing.Optional[int] = None
    photo_height: typing.Optional[int] = None
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[
        typing.List[typing.Optional["MessageEntity"]]
    ] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultGif(Model):
    type: str
    id: str
    gif_url: str
    gif_width: typing.Optional[int] = None
    gif_height: typing.Optional[int] = None
    gif_duration: typing.Optional[int] = None
    thumb_url: str
    thumb_mime_type: typing.Optional[str] = "image/jpeg"
    title: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[
        typing.List[typing.Optional["MessageEntity"]]
    ] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultMpeg4Gif(Model):
    type: str
    id: str
    mpeg4_url: str
    mpeg4_width: typing.Optional[int] = None
    mpeg4_height: typing.Optional[int] = None
    mpeg4_duration: typing.Optional[int] = None
    thumb_url: str
    thumb_mime_type: typing.Optional[str] = "image/jpeg"
    title: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[
        typing.List[typing.Optional["MessageEntity"]]
    ] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultVideo(Model):
    type: str
    id: str
    video_url: str
    mime_type: str
    thumb_url: str
    title: str
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[
        typing.List[typing.Optional["MessageEntity"]]
    ] = None
    video_width: typing.Optional[int] = None
    video_height: typing.Optional[int] = None
    video_duration: typing.Optional[int] = None
    description: typing.Optional[str] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultAudio(Model):
    type: str
    id: str
    audio_url: str
    title: str
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[
        typing.List[typing.Optional["MessageEntity"]]
    ] = None
    performer: typing.Optional[str] = None
    audio_duration: typing.Optional[int] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultVoice(Model):
    type: str
    id: str
    voice_url: str
    title: str
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[
        typing.List[typing.Optional["MessageEntity"]]
    ] = None
    voice_duration: typing.Optional[int] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultDocument(Model):
    type: str
    id: str
    title: str
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[
        typing.List[typing.Optional["MessageEntity"]]
    ] = None
    document_url: str
    mime_type: str
    description: typing.Optional[str] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None
    thumb_url: typing.Optional[str] = None
    thumb_width: typing.Optional[int] = None
    thumb_height: typing.Optional[int] = None


class InlineQueryResultLocation(Model):
    type: str
    id: str
    latitude: float
    longitude: float
    title: str
    horizontal_accuracy: typing.Optional[float] = None
    live_period: typing.Optional[int] = None
    heading: typing.Optional[int] = None
    proximity_alert_radius: typing.Optional[int] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None
    thumb_url: typing.Optional[str] = None
    thumb_width: typing.Optional[int] = None
    thumb_height: typing.Optional[int] = None


class InlineQueryResultVenue(Model):
    type: str
    id: str
    latitude: float
    longitude: float
    title: str
    address: str
    foursquare_id: typing.Optional[str] = None
    foursquare_type: typing.Optional[str] = None
    google_place_id: typing.Optional[str] = None
    google_place_type: typing.Optional[str] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None
    thumb_url: typing.Optional[str] = None
    thumb_width: typing.Optional[int] = None
    thumb_height: typing.Optional[int] = None


class InlineQueryResultContact(Model):
    type: str
    id: str
    phone_number: str
    first_name: str
    last_name: typing.Optional[str] = None
    vcard: typing.Optional[str] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None
    thumb_url: typing.Optional[str] = None
    thumb_width: typing.Optional[int] = None
    thumb_height: typing.Optional[int] = None


class InlineQueryResultGame(Model):
    type: str
    id: str
    game_short_name: str
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None


class InlineQueryResultCachedPhoto(Model):
    type: str
    id: str
    photo_file_id: str
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[
        typing.List[typing.Optional["MessageEntity"]]
    ] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultCachedGif(Model):
    type: str
    id: str
    gif_file_id: str
    title: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[
        typing.List[typing.Optional["MessageEntity"]]
    ] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultCachedMpeg4Gif(Model):
    type: str
    id: str
    mpeg4_file_id: str
    title: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[
        typing.List[typing.Optional["MessageEntity"]]
    ] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultCachedSticker(Model):
    type: str
    id: str
    sticker_file_id: str
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultCachedDocument(Model):
    type: str
    id: str
    title: str
    document_file_id: str
    description: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[
        typing.List[typing.Optional["MessageEntity"]]
    ] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultCachedVideo(Model):
    type: str
    id: str
    video_file_id: str
    title: str
    description: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[
        typing.List[typing.Optional["MessageEntity"]]
    ] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultCachedVoice(Model):
    type: str
    id: str
    voice_file_id: str
    title: str
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[
        typing.List[typing.Optional["MessageEntity"]]
    ] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultCachedAudio(Model):
    type: str
    id: str
    audio_file_id: str
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[
        typing.List[typing.Optional["MessageEntity"]]
    ] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InputMessageContent(Model):
    message_text: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    entities: typing.Optional[typing.List[typing.Optional["MessageEntity"]]] = None
    disable_web_page_preview: typing.Optional[bool] = None
    latitude: typing.Optional[float] = None
    longitude: typing.Optional[float] = None
    horizontal_accuracy: typing.Optional[float] = None
    live_period: typing.Optional[int] = None
    heading: typing.Optional[int] = None
    proximity_alert_radius: typing.Optional[int] = None
    title: typing.Optional[str] = None
    address: typing.Optional[str] = None
    foursquare_id: typing.Optional[str] = None
    foursquare_type: typing.Optional[str] = None
    google_place_id: typing.Optional[str] = None
    google_place_type: typing.Optional[str] = None
    phone_number: typing.Optional[str] = None
    first_name: typing.Optional[str] = None
    last_name: typing.Optional[str] = None
    vcard: typing.Optional[str] = None
    description: typing.Optional[str] = None
    payload: typing.Optional[str] = None
    provider_token: typing.Optional[str] = None
    currency: typing.Optional[str] = None
    prices: typing.Optional[typing.List[typing.Optional["LabeledPrice"]]] = None
    max_tip_amount: typing.Optional[int] = 0
    suggested_tip_amounts: typing.Optional[typing.List[typing.Optional[int]]] = None
    provider_data: typing.Optional[str] = None
    photo_url: typing.Optional[str] = None
    photo_size: typing.Optional[int] = None
    photo_width: typing.Optional[int] = None
    photo_height: typing.Optional[int] = None
    need_name: typing.Optional[bool] = None
    need_phone_number: typing.Optional[bool] = None
    need_email: typing.Optional[bool] = None
    need_shipping_address: typing.Optional[bool] = None
    send_phone_number_to_provider: typing.Optional[bool] = None
    send_email_to_provider: typing.Optional[bool] = None
    is_flexible: typing.Optional[bool] = None


class InputTextMessageContent(Model):
    message_text: str
    parse_mode: typing.Optional[str] = None
    entities: typing.Optional[typing.List[typing.Optional["MessageEntity"]]] = None
    disable_web_page_preview: typing.Optional[bool] = None


class InputLocationMessageContent(Model):
    latitude: float
    longitude: float
    horizontal_accuracy: typing.Optional[float] = None
    live_period: typing.Optional[int] = None
    heading: typing.Optional[int] = None
    proximity_alert_radius: typing.Optional[int] = None


class InputVenueMessageContent(Model):
    latitude: float
    longitude: float
    title: str
    address: str
    foursquare_id: typing.Optional[str] = None
    foursquare_type: typing.Optional[str] = None
    google_place_id: typing.Optional[str] = None
    google_place_type: typing.Optional[str] = None


class InputContactMessageContent(Model):
    phone_number: str
    first_name: str
    last_name: typing.Optional[str] = None
    vcard: typing.Optional[str] = None


class InputInvoiceMessageContent(Model):
    title: str
    description: str
    payload: str
    provider_token: str
    currency: str
    prices: typing.List["LabeledPrice"]
    max_tip_amount: typing.Optional[int] = 0
    suggested_tip_amounts: typing.Optional[typing.List[typing.Optional[int]]] = None
    provider_data: typing.Optional[str] = None
    photo_url: typing.Optional[str] = None
    photo_size: typing.Optional[int] = None
    photo_width: typing.Optional[int] = None
    photo_height: typing.Optional[int] = None
    need_name: typing.Optional[bool] = None
    need_phone_number: typing.Optional[bool] = None
    need_email: typing.Optional[bool] = None
    need_shipping_address: typing.Optional[bool] = None
    send_phone_number_to_provider: typing.Optional[bool] = None
    send_email_to_provider: typing.Optional[bool] = None
    is_flexible: typing.Optional[bool] = None


class ChosenInlineResult(Model):
    result_id: str
    from_: "User"
    location: typing.Optional["Location"] = None
    inline_message_id: typing.Optional[str] = None
    query: str


class SentWebAppMessage(Model):
    inline_message_id: typing.Optional[str] = None


class LabeledPrice(Model):
    label: str
    amount: int


class Invoice(Model):
    title: str
    description: str
    start_parameter: str
    currency: str
    total_amount: int


class ShippingAddress(Model):
    country_code: str
    state: str
    city: str
    street_line1: str
    street_line2: str
    post_code: str


class OrderInfo(Model):
    name: typing.Optional[str] = None
    phone_number: typing.Optional[str] = None
    email: typing.Optional[str] = None
    shipping_address: typing.Optional["ShippingAddress"] = None


class ShippingOption(Model):
    id: str
    title: str
    prices: typing.List["LabeledPrice"]


class SuccessfulPayment(Model):
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: typing.Optional[str] = None
    order_info: typing.Optional["OrderInfo"] = None
    telegram_payment_charge_id: str
    provider_payment_charge_id: str


class ShippingQuery(Model):
    id: str
    from_: "User"
    invoice_payload: str
    shipping_address: "ShippingAddress"


class PreCheckoutQuery(Model):
    id: str
    from_: "User"
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: typing.Optional[str] = None
    order_info: typing.Optional["OrderInfo"] = None


class PassportData(Model):
    data: typing.List["EncryptedPassportElement"]
    credentials: "EncryptedCredentials"


class PassportFile(Model):
    file_id: str
    file_unique_id: str
    file_size: int
    file_date: int


class EncryptedPassportElement(Model):
    type: str
    data: typing.Optional[str] = None
    phone_number: typing.Optional[str] = None
    email: typing.Optional[str] = None
    files: typing.Optional[typing.List[typing.Optional["PassportFile"]]] = None
    front_side: typing.Optional["PassportFile"] = None
    reverse_side: typing.Optional["PassportFile"] = None
    selfie: typing.Optional["PassportFile"] = None
    translation: typing.Optional[typing.List[typing.Optional["PassportFile"]]] = None
    hash: str


class EncryptedCredentials(Model):
    data: str
    hash: str
    secret: str


class PassportElementError(Model):
    source: typing.Optional[str] = "unspecified"
    type: typing.Optional[str] = None
    field_name: typing.Optional[str] = None
    data_hash: typing.Optional[str] = None
    message: typing.Optional[str] = None
    file_hash: typing.Optional[str] = None
    file_hashes: typing.Optional[typing.List[typing.Optional[str]]] = None
    element_hash: typing.Optional[str] = None


class PassportElementErrorDataField(Model):
    source: str
    type: str
    field_name: str
    data_hash: str
    message: str


class PassportElementErrorFrontSide(Model):
    source: str
    type: str
    file_hash: str
    message: str


class PassportElementErrorReverseSide(Model):
    source: str
    type: str
    file_hash: str
    message: str


class PassportElementErrorSelfie(Model):
    source: str
    type: str
    file_hash: str
    message: str


class PassportElementErrorFile(Model):
    source: str
    type: str
    file_hash: str
    message: str


class PassportElementErrorFiles(Model):
    source: str
    type: str
    file_hashes: typing.List[str]
    message: str


class PassportElementErrorTranslationFile(Model):
    source: str
    type: str
    file_hash: str
    message: str


class PassportElementErrorTranslationFiles(Model):
    source: str
    type: str
    file_hashes: typing.List[str]
    message: str


class PassportElementErrorUnspecified(Model):
    source: str
    type: str
    element_hash: str
    message: str


class Game(Model):
    title: str
    description: str
    photo: typing.List["PhotoSize"]
    text: typing.Optional[str] = None
    text_entities: typing.Optional[typing.List[typing.Optional["MessageEntity"]]] = None
    animation: typing.Optional["Animation"] = None


class CallbackGame(Model):
    pass


class GameHighScore(Model):
    position: int
    user: "User"
    score: int
