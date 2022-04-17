import typing
import inspect
from pydantic import BaseModel


class Error(BaseModel):
    ok: typing.Optional[bool] = None
    error_code: typing.Optional[int] = None
    description: typing.Optional[str] = None
    parameters: typing.Optional["ResponseParameters"] = None


class Update(BaseModel):
    update_id: typing.Optional[int] = None
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


class WebhookInfo(BaseModel):
    url: typing.Optional[str] = None
    has_custom_certificate: typing.Optional[bool] = None
    pending_update_count: typing.Optional[int] = None
    ip_address: typing.Optional[str] = None
    last_error_date: typing.Optional[int] = None
    last_error_message: typing.Optional[str] = None
    last_synchronization_error_date: typing.Optional[int] = None
    max_connections: typing.Optional[int] = None
    allowed_updates: typing.Optional[typing.List[str]] = None


class User(BaseModel):
    id: typing.Optional[int] = None
    is_bot: typing.Optional[bool] = None
    first_name: typing.Optional[str] = None
    last_name: typing.Optional[str] = None
    username: typing.Optional[str] = None
    language_code: typing.Optional[str] = None
    can_join_groups: typing.Optional[bool] = None
    can_read_all_group_messages: typing.Optional[bool] = None
    supports_inline_queries: typing.Optional[bool] = None


class Chat(BaseModel):
    id: typing.Optional[int] = None
    type: typing.Optional[str] = None
    title: typing.Optional[str] = None
    username: typing.Optional[str] = None
    first_name: typing.Optional[str] = None
    last_name: typing.Optional[str] = None
    photo: typing.Optional["ChatPhoto"] = None
    bio: typing.Optional[str] = None
    has_private_forwards: typing.Optional[bool] = None
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


class Message(BaseModel):
    message_id: typing.Optional[int] = None
    from_: typing.Optional["User"] = None
    sender_chat: typing.Optional["Chat"] = None
    date: typing.Optional[int] = None
    chat: typing.Optional["Chat"] = None
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
    entities: typing.Optional[typing.List["MessageEntity"]] = None
    animation: typing.Optional["Animation"] = None
    audio: typing.Optional["Audio"] = None
    document: typing.Optional["Document"] = None
    photo: typing.Optional[typing.List["PhotoSize"]] = None
    sticker: typing.Optional["Sticker"] = None
    video: typing.Optional["Video"] = None
    video_note: typing.Optional["VideoNote"] = None
    voice: typing.Optional["Voice"] = None
    caption: typing.Optional[str] = None
    caption_entities: typing.Optional[typing.List["MessageEntity"]] = None
    contact: typing.Optional["Contact"] = None
    dice: typing.Optional["Dice"] = None
    game: typing.Optional["Game"] = None
    poll: typing.Optional["Poll"] = None
    venue: typing.Optional["Venue"] = None
    location: typing.Optional["Location"] = None
    new_chat_members: typing.Optional[typing.List["User"]] = None
    left_chat_member: typing.Optional["User"] = None
    new_chat_title: typing.Optional[str] = None
    new_chat_photo: typing.Optional[typing.List["PhotoSize"]] = None
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


class MessageId(BaseModel):
    message_id: typing.Optional[int] = None


class MessageEntity(BaseModel):
    type: typing.Optional[str] = None
    offset: typing.Optional[int] = None
    length: typing.Optional[int] = None
    url: typing.Optional[str] = None
    user: typing.Optional["User"] = None
    language: typing.Optional[str] = None


class PhotoSize(BaseModel):
    file_id: typing.Optional[str] = None
    file_unique_id: typing.Optional[str] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None
    file_size: typing.Optional[int] = None


class Animation(BaseModel):
    file_id: typing.Optional[str] = None
    file_unique_id: typing.Optional[str] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None
    duration: typing.Optional[int] = None
    thumb: typing.Optional["PhotoSize"] = None
    file_name: typing.Optional[str] = None
    mime_type: typing.Optional[str] = None
    file_size: typing.Optional[int] = None


class Audio(BaseModel):
    file_id: typing.Optional[str] = None
    file_unique_id: typing.Optional[str] = None
    duration: typing.Optional[int] = None
    performer: typing.Optional[str] = None
    title: typing.Optional[str] = None
    file_name: typing.Optional[str] = None
    mime_type: typing.Optional[str] = None
    file_size: typing.Optional[int] = None
    thumb: typing.Optional["PhotoSize"] = None


class Document(BaseModel):
    file_id: typing.Optional[str] = None
    file_unique_id: typing.Optional[str] = None
    thumb: typing.Optional["PhotoSize"] = None
    file_name: typing.Optional[str] = None
    mime_type: typing.Optional[str] = None
    file_size: typing.Optional[int] = None


class Video(BaseModel):
    file_id: typing.Optional[str] = None
    file_unique_id: typing.Optional[str] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None
    duration: typing.Optional[int] = None
    thumb: typing.Optional["PhotoSize"] = None
    file_name: typing.Optional[str] = None
    mime_type: typing.Optional[str] = None
    file_size: typing.Optional[int] = None


class VideoNote(BaseModel):
    file_id: typing.Optional[str] = None
    file_unique_id: typing.Optional[str] = None
    length: typing.Optional[int] = None
    duration: typing.Optional[int] = None
    thumb: typing.Optional["PhotoSize"] = None
    file_size: typing.Optional[int] = None


class Voice(BaseModel):
    file_id: typing.Optional[str] = None
    file_unique_id: typing.Optional[str] = None
    duration: typing.Optional[int] = None
    mime_type: typing.Optional[str] = None
    file_size: typing.Optional[int] = None


class Contact(BaseModel):
    phone_number: typing.Optional[str] = None
    first_name: typing.Optional[str] = None
    last_name: typing.Optional[str] = None
    user_id: typing.Optional[int] = None
    vcard: typing.Optional[str] = None


class Dice(BaseModel):
    emoji: typing.Optional[str] = None
    value: typing.Optional[int] = None


class PollOption(BaseModel):
    text: typing.Optional[str] = None
    voter_count: typing.Optional[int] = None


class PollAnswer(BaseModel):
    poll_id: typing.Optional[str] = None
    user: typing.Optional["User"] = None
    option_ids: typing.Optional[typing.List[int]] = None


class Poll(BaseModel):
    id: typing.Optional[str] = None
    question: typing.Optional[str] = None
    options: typing.Optional[typing.List["PollOption"]] = None
    total_voter_count: typing.Optional[int] = None
    is_closed: typing.Optional[bool] = None
    is_anonymous: typing.Optional[bool] = None
    type: typing.Optional[str] = None
    allows_multiple_answers: typing.Optional[bool] = None
    correct_option_id: typing.Optional[int] = None
    explanation: typing.Optional[str] = None
    explanation_entities: typing.Optional[typing.List["MessageEntity"]] = None
    open_period: typing.Optional[int] = None
    close_date: typing.Optional[int] = None


class Location(BaseModel):
    longitude: typing.Optional[float] = None
    latitude: typing.Optional[float] = None
    horizontal_accuracy: typing.Optional[float] = None
    live_period: typing.Optional[int] = None
    heading: typing.Optional[int] = None
    proximity_alert_radius: typing.Optional[int] = None


class Venue(BaseModel):
    location: typing.Optional["Location"] = None
    title: typing.Optional[str] = None
    address: typing.Optional[str] = None
    foursquare_id: typing.Optional[str] = None
    foursquare_type: typing.Optional[str] = None
    google_place_id: typing.Optional[str] = None
    google_place_type: typing.Optional[str] = None


class WebAppData(BaseModel):
    data: typing.Optional[str] = None
    button_text: typing.Optional[str] = None


class ProximityAlertTriggered(BaseModel):
    traveler: typing.Optional["User"] = None
    watcher: typing.Optional["User"] = None
    distance: typing.Optional[int] = None


class MessageAutoDeleteTimerChanged(BaseModel):
    message_auto_delete_time: typing.Optional[int] = None


class VideoChatScheduled(BaseModel):
    start_date: typing.Optional[int] = None


class VideoChatStarted(BaseModel):
    pass


class VideoChatEnded(BaseModel):
    duration: typing.Optional[int] = None


class VideoChatParticipantsInvited(BaseModel):
    users: typing.Optional[typing.List["User"]] = None


class UserProfilePhotos(BaseModel):
    total_count: typing.Optional[int] = None
    photos: typing.Optional[typing.List[typing.List["PhotoSize"]]] = None


class File(BaseModel):
    file_id: typing.Optional[str] = None
    file_unique_id: typing.Optional[str] = None
    file_size: typing.Optional[int] = None
    file_path: typing.Optional[str] = None


class WebAppInfo(BaseModel):
    url: typing.Optional[str] = None


class ReplyKeyboardMarkup(BaseModel):
    keyboard: typing.Optional[typing.List[typing.List["KeyboardButton"]]] = None
    resize_keyboard: typing.Optional[bool] = None
    one_time_keyboard: typing.Optional[bool] = None
    input_field_placeholder: typing.Optional[str] = None
    selective: typing.Optional[bool] = None


class KeyboardButton(BaseModel):
    text: typing.Optional[str] = None
    request_contact: typing.Optional[bool] = None
    request_location: typing.Optional[bool] = None
    request_poll: typing.Optional["KeyboardButtonPollType"] = None
    web_app: typing.Optional["WebAppInfo"] = None


class KeyboardButtonPollType(BaseModel):
    type: typing.Optional[str] = None


class ReplyKeyboardRemove(BaseModel):
    remove_keyboard: typing.Optional[bool] = None
    selective: typing.Optional[bool] = None


class InlineKeyboardMarkup(BaseModel):
    inline_keyboard: typing.Optional[
        typing.List[typing.List["InlineKeyboardButton"]]
    ] = None


class InlineKeyboardButton(BaseModel):
    text: typing.Optional[str] = None
    url: typing.Optional[str] = None
    callback_data: typing.Optional[str] = None
    web_app: typing.Optional["WebAppInfo"] = None
    login_url: typing.Optional["LoginUrl"] = None
    switch_inline_query: typing.Optional[str] = None
    switch_inline_query_current_chat: typing.Optional[str] = None
    callback_game: typing.Optional["CallbackGame"] = None
    pay: typing.Optional[bool] = None


class LoginUrl(BaseModel):
    url: typing.Optional[str] = None
    forward_text: typing.Optional[str] = None
    bot_username: typing.Optional[str] = None
    request_write_access: typing.Optional[bool] = None


class CallbackQuery(BaseModel):
    id: typing.Optional[str] = None
    from_: typing.Optional["User"] = None
    message: typing.Optional["Message"] = None
    inline_message_id: typing.Optional[str] = None
    chat_instance: typing.Optional[str] = None
    data: typing.Optional[str] = None
    game_short_name: typing.Optional[str] = None


class ForceReply(BaseModel):
    force_reply: typing.Optional[bool] = None
    input_field_placeholder: typing.Optional[str] = None
    selective: typing.Optional[bool] = None


class ChatPhoto(BaseModel):
    small_file_id: typing.Optional[str] = None
    small_file_unique_id: typing.Optional[str] = None
    big_file_id: typing.Optional[str] = None
    big_file_unique_id: typing.Optional[str] = None


class ChatInviteLink(BaseModel):
    invite_link: typing.Optional[str] = None
    creator: typing.Optional["User"] = None
    creates_join_request: typing.Optional[bool] = None
    is_primary: typing.Optional[bool] = None
    is_revoked: typing.Optional[bool] = None
    name: typing.Optional[str] = None
    expire_date: typing.Optional[int] = None
    member_limit: typing.Optional[int] = None
    pending_join_request_count: typing.Optional[int] = None


class ChatAdministratorRights(BaseModel):
    is_anonymous: typing.Optional[bool] = None
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


class ChatMember(BaseModel):
    pass


class ChatMemberOwner(BaseModel):
    status: typing.Optional[str] = None
    user: typing.Optional["User"] = None
    is_anonymous: typing.Optional[bool] = None
    custom_title: typing.Optional[str] = None


class ChatMemberAdministrator(BaseModel):
    status: typing.Optional[str] = None
    user: typing.Optional["User"] = None
    can_be_edited: typing.Optional[bool] = None
    is_anonymous: typing.Optional[bool] = None
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
    custom_title: typing.Optional[str] = None


class ChatMemberMember(BaseModel):
    status: typing.Optional[str] = None
    user: typing.Optional["User"] = None


class ChatMemberRestricted(BaseModel):
    status: typing.Optional[str] = None
    user: typing.Optional["User"] = None
    is_member: typing.Optional[bool] = None
    can_change_info: typing.Optional[bool] = None
    can_invite_users: typing.Optional[bool] = None
    can_pin_messages: typing.Optional[bool] = None
    can_send_messages: typing.Optional[bool] = None
    can_send_media_messages: typing.Optional[bool] = None
    can_send_polls: typing.Optional[bool] = None
    can_send_other_messages: typing.Optional[bool] = None
    can_add_web_page_previews: typing.Optional[bool] = None
    until_date: typing.Optional[int] = None


class ChatMemberLeft(BaseModel):
    status: typing.Optional[str] = None
    user: typing.Optional["User"] = None


class ChatMemberBanned(BaseModel):
    status: typing.Optional[str] = None
    user: typing.Optional["User"] = None
    until_date: typing.Optional[int] = None


class ChatMemberUpdated(BaseModel):
    chat: typing.Optional["Chat"] = None
    from_: typing.Optional["User"] = None
    date: typing.Optional[int] = None
    old_chat_member: typing.Optional["ChatMember"] = None
    new_chat_member: typing.Optional["ChatMember"] = None
    invite_link: typing.Optional["ChatInviteLink"] = None


class ChatJoinRequest(BaseModel):
    chat: typing.Optional["Chat"] = None
    from_: typing.Optional["User"] = None
    date: typing.Optional[int] = None
    bio: typing.Optional[str] = None
    invite_link: typing.Optional["ChatInviteLink"] = None


class ChatPermissions(BaseModel):
    can_send_messages: typing.Optional[bool] = None
    can_send_media_messages: typing.Optional[bool] = None
    can_send_polls: typing.Optional[bool] = None
    can_send_other_messages: typing.Optional[bool] = None
    can_add_web_page_previews: typing.Optional[bool] = None
    can_change_info: typing.Optional[bool] = None
    can_invite_users: typing.Optional[bool] = None
    can_pin_messages: typing.Optional[bool] = None


class ChatLocation(BaseModel):
    location: typing.Optional["Location"] = None
    address: typing.Optional[str] = None


class BotCommand(BaseModel):
    command: typing.Optional[str] = None
    description: typing.Optional[str] = None


class BotCommandScope(BaseModel):
    pass


class BotCommandScopeDefault(BaseModel):
    type: typing.Optional[str] = None


class BotCommandScopeAllPrivateChats(BaseModel):
    type: typing.Optional[str] = None


class BotCommandScopeAllGroupChats(BaseModel):
    type: typing.Optional[str] = None


class BotCommandScopeAllChatAdministrators(BaseModel):
    type: typing.Optional[str] = None


class BotCommandScopeChat(BaseModel):
    type: typing.Optional[str] = None
    chat_id: typing.Optional[typing.Union[int, str]] = None


class BotCommandScopeChatAdministrators(BaseModel):
    type: typing.Optional[str] = None
    chat_id: typing.Optional[typing.Union[int, str]] = None


class BotCommandScopeChatMember(BaseModel):
    type: typing.Optional[str] = None
    chat_id: typing.Optional[typing.Union[int, str]] = None
    user_id: typing.Optional[int] = None


class MenuButton(BaseModel):
    pass


class MenuButtonCommands(BaseModel):
    type: typing.Optional[str] = None


class MenuButtonWebApp(BaseModel):
    type: typing.Optional[str] = None
    text: typing.Optional[str] = None
    web_app: typing.Optional["WebAppInfo"] = None


class MenuButtonDefault(BaseModel):
    type: typing.Optional[str] = None


class ResponseParameters(BaseModel):
    migrate_to_chat_id: typing.Optional[int] = None
    retry_after: typing.Optional[int] = None


class InputMedia(BaseModel):
    pass


class InputMediaPhoto(BaseModel):
    type: typing.Optional[str] = None
    media: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[typing.List["MessageEntity"]] = None


class InputMediaVideo(BaseModel):
    type: typing.Optional[str] = None
    media: typing.Optional[str] = None
    thumb: typing.Optional[typing.Union["InputFile", str]] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[typing.List["MessageEntity"]] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None
    duration: typing.Optional[int] = None
    supports_streaming: typing.Optional[bool] = None


class InputMediaAnimation(BaseModel):
    type: typing.Optional[str] = None
    media: typing.Optional[str] = None
    thumb: typing.Optional[typing.Union["InputFile", str]] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[typing.List["MessageEntity"]] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None
    duration: typing.Optional[int] = None


class InputMediaAudio(BaseModel):
    type: typing.Optional[str] = None
    media: typing.Optional[str] = None
    thumb: typing.Optional[typing.Union["InputFile", str]] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[typing.List["MessageEntity"]] = None
    duration: typing.Optional[int] = None
    performer: typing.Optional[str] = None
    title: typing.Optional[str] = None


class InputMediaDocument(BaseModel):
    type: typing.Optional[str] = None
    media: typing.Optional[str] = None
    thumb: typing.Optional[typing.Union["InputFile", str]] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[typing.List["MessageEntity"]] = None
    disable_content_type_detection: typing.Optional[bool] = None


class InputFile(BaseModel):
    pass


class Sticker(BaseModel):
    file_id: typing.Optional[str] = None
    file_unique_id: typing.Optional[str] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None
    is_animated: typing.Optional[bool] = None
    is_video: typing.Optional[bool] = None
    thumb: typing.Optional["PhotoSize"] = None
    emoji: typing.Optional[str] = None
    set_name: typing.Optional[str] = None
    mask_position: typing.Optional["MaskPosition"] = None
    file_size: typing.Optional[int] = None


class StickerSet(BaseModel):
    name: typing.Optional[str] = None
    title: typing.Optional[str] = None
    is_animated: typing.Optional[bool] = None
    is_video: typing.Optional[bool] = None
    contains_masks: typing.Optional[bool] = None
    stickers: typing.Optional[typing.List["Sticker"]] = None
    thumb: typing.Optional["PhotoSize"] = None


class MaskPosition(BaseModel):
    point: typing.Optional[str] = None
    x_shift: typing.Optional[float] = None
    y_shift: typing.Optional[float] = None
    scale: typing.Optional[float] = None


class InlineQuery(BaseModel):
    id: typing.Optional[str] = None
    from_: typing.Optional["User"] = None
    query: typing.Optional[str] = None
    offset: typing.Optional[str] = None
    chat_type: typing.Optional[str] = None
    location: typing.Optional["Location"] = None


class InlineQueryResult(BaseModel):
    pass


class InlineQueryResultArticle(BaseModel):
    type: typing.Optional[str] = None
    id: typing.Optional[str] = None
    title: typing.Optional[str] = None
    input_message_content: typing.Optional["InputMessageContent"] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    url: typing.Optional[str] = None
    hide_url: typing.Optional[bool] = None
    description: typing.Optional[str] = None
    thumb_url: typing.Optional[str] = None
    thumb_width: typing.Optional[int] = None
    thumb_height: typing.Optional[int] = None


class InlineQueryResultPhoto(BaseModel):
    type: typing.Optional[str] = None
    id: typing.Optional[str] = None
    photo_url: typing.Optional[str] = None
    thumb_url: typing.Optional[str] = None
    photo_width: typing.Optional[int] = None
    photo_height: typing.Optional[int] = None
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[typing.List["MessageEntity"]] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultGif(BaseModel):
    type: typing.Optional[str] = None
    id: typing.Optional[str] = None
    gif_url: typing.Optional[str] = None
    gif_width: typing.Optional[int] = None
    gif_height: typing.Optional[int] = None
    gif_duration: typing.Optional[int] = None
    thumb_url: typing.Optional[str] = None
    thumb_mime_type: typing.Optional[str] = None
    title: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[typing.List["MessageEntity"]] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultMpeg4Gif(BaseModel):
    type: typing.Optional[str] = None
    id: typing.Optional[str] = None
    mpeg4_url: typing.Optional[str] = None
    mpeg4_width: typing.Optional[int] = None
    mpeg4_height: typing.Optional[int] = None
    mpeg4_duration: typing.Optional[int] = None
    thumb_url: typing.Optional[str] = None
    thumb_mime_type: typing.Optional[str] = None
    title: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[typing.List["MessageEntity"]] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultVideo(BaseModel):
    type: typing.Optional[str] = None
    id: typing.Optional[str] = None
    video_url: typing.Optional[str] = None
    mime_type: typing.Optional[str] = None
    thumb_url: typing.Optional[str] = None
    title: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[typing.List["MessageEntity"]] = None
    video_width: typing.Optional[int] = None
    video_height: typing.Optional[int] = None
    video_duration: typing.Optional[int] = None
    description: typing.Optional[str] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultAudio(BaseModel):
    type: typing.Optional[str] = None
    id: typing.Optional[str] = None
    audio_url: typing.Optional[str] = None
    title: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[typing.List["MessageEntity"]] = None
    performer: typing.Optional[str] = None
    audio_duration: typing.Optional[int] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultVoice(BaseModel):
    type: typing.Optional[str] = None
    id: typing.Optional[str] = None
    voice_url: typing.Optional[str] = None
    title: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[typing.List["MessageEntity"]] = None
    voice_duration: typing.Optional[int] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultDocument(BaseModel):
    type: typing.Optional[str] = None
    id: typing.Optional[str] = None
    title: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[typing.List["MessageEntity"]] = None
    document_url: typing.Optional[str] = None
    mime_type: typing.Optional[str] = None
    description: typing.Optional[str] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None
    thumb_url: typing.Optional[str] = None
    thumb_width: typing.Optional[int] = None
    thumb_height: typing.Optional[int] = None


class InlineQueryResultLocation(BaseModel):
    type: typing.Optional[str] = None
    id: typing.Optional[str] = None
    latitude: typing.Optional[float] = None
    longitude: typing.Optional[float] = None
    title: typing.Optional[str] = None
    horizontal_accuracy: typing.Optional[float] = None
    live_period: typing.Optional[int] = None
    heading: typing.Optional[int] = None
    proximity_alert_radius: typing.Optional[int] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None
    thumb_url: typing.Optional[str] = None
    thumb_width: typing.Optional[int] = None
    thumb_height: typing.Optional[int] = None


class InlineQueryResultVenue(BaseModel):
    type: typing.Optional[str] = None
    id: typing.Optional[str] = None
    latitude: typing.Optional[float] = None
    longitude: typing.Optional[float] = None
    title: typing.Optional[str] = None
    address: typing.Optional[str] = None
    foursquare_id: typing.Optional[str] = None
    foursquare_type: typing.Optional[str] = None
    google_place_id: typing.Optional[str] = None
    google_place_type: typing.Optional[str] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None
    thumb_url: typing.Optional[str] = None
    thumb_width: typing.Optional[int] = None
    thumb_height: typing.Optional[int] = None


class InlineQueryResultContact(BaseModel):
    type: typing.Optional[str] = None
    id: typing.Optional[str] = None
    phone_number: typing.Optional[str] = None
    first_name: typing.Optional[str] = None
    last_name: typing.Optional[str] = None
    vcard: typing.Optional[str] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None
    thumb_url: typing.Optional[str] = None
    thumb_width: typing.Optional[int] = None
    thumb_height: typing.Optional[int] = None


class InlineQueryResultGame(BaseModel):
    type: typing.Optional[str] = None
    id: typing.Optional[str] = None
    game_short_name: typing.Optional[str] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None


class InlineQueryResultCachedPhoto(BaseModel):
    type: typing.Optional[str] = None
    id: typing.Optional[str] = None
    photo_file_id: typing.Optional[str] = None
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[typing.List["MessageEntity"]] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultCachedGif(BaseModel):
    type: typing.Optional[str] = None
    id: typing.Optional[str] = None
    gif_file_id: typing.Optional[str] = None
    title: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[typing.List["MessageEntity"]] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultCachedMpeg4Gif(BaseModel):
    type: typing.Optional[str] = None
    id: typing.Optional[str] = None
    mpeg4_file_id: typing.Optional[str] = None
    title: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[typing.List["MessageEntity"]] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultCachedSticker(BaseModel):
    type: typing.Optional[str] = None
    id: typing.Optional[str] = None
    sticker_file_id: typing.Optional[str] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultCachedDocument(BaseModel):
    type: typing.Optional[str] = None
    id: typing.Optional[str] = None
    title: typing.Optional[str] = None
    document_file_id: typing.Optional[str] = None
    description: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[typing.List["MessageEntity"]] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultCachedVideo(BaseModel):
    type: typing.Optional[str] = None
    id: typing.Optional[str] = None
    video_file_id: typing.Optional[str] = None
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[typing.List["MessageEntity"]] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultCachedVoice(BaseModel):
    type: typing.Optional[str] = None
    id: typing.Optional[str] = None
    voice_file_id: typing.Optional[str] = None
    title: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[typing.List["MessageEntity"]] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultCachedAudio(BaseModel):
    type: typing.Optional[str] = None
    id: typing.Optional[str] = None
    audio_file_id: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[typing.List["MessageEntity"]] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InputMessageContent(BaseModel):
    pass


class InputTextMessageContent(BaseModel):
    message_text: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    entities: typing.Optional[typing.List["MessageEntity"]] = None
    disable_web_page_preview: typing.Optional[bool] = None


class InputLocationMessageContent(BaseModel):
    latitude: typing.Optional[float] = None
    longitude: typing.Optional[float] = None
    horizontal_accuracy: typing.Optional[float] = None
    live_period: typing.Optional[int] = None
    heading: typing.Optional[int] = None
    proximity_alert_radius: typing.Optional[int] = None


class InputVenueMessageContent(BaseModel):
    latitude: typing.Optional[float] = None
    longitude: typing.Optional[float] = None
    title: typing.Optional[str] = None
    address: typing.Optional[str] = None
    foursquare_id: typing.Optional[str] = None
    foursquare_type: typing.Optional[str] = None
    google_place_id: typing.Optional[str] = None
    google_place_type: typing.Optional[str] = None


class InputContactMessageContent(BaseModel):
    phone_number: typing.Optional[str] = None
    first_name: typing.Optional[str] = None
    last_name: typing.Optional[str] = None
    vcard: typing.Optional[str] = None


class InputInvoiceMessageContent(BaseModel):
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    payload: typing.Optional[str] = None
    provider_token: typing.Optional[str] = None
    currency: typing.Optional[str] = None
    prices: typing.Optional[typing.List["LabeledPrice"]] = None
    max_tip_amount: typing.Optional[int] = None
    suggested_tip_amounts: typing.Optional[typing.List[int]] = None
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


class ChosenInlineResult(BaseModel):
    result_id: typing.Optional[str] = None
    from_: typing.Optional["User"] = None
    location: typing.Optional["Location"] = None
    inline_message_id: typing.Optional[str] = None
    query: typing.Optional[str] = None


class SentWebAppMessage(BaseModel):
    inline_message_id: typing.Optional[str] = None


class LabeledPrice(BaseModel):
    label: typing.Optional[str] = None
    amount: typing.Optional[int] = None


class Invoice(BaseModel):
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    start_parameter: typing.Optional[str] = None
    currency: typing.Optional[str] = None
    total_amount: typing.Optional[int] = None


class ShippingAddress(BaseModel):
    country_code: typing.Optional[str] = None
    state: typing.Optional[str] = None
    city: typing.Optional[str] = None
    street_line1: typing.Optional[str] = None
    street_line2: typing.Optional[str] = None
    post_code: typing.Optional[str] = None


class OrderInfo(BaseModel):
    name: typing.Optional[str] = None
    phone_number: typing.Optional[str] = None
    email: typing.Optional[str] = None
    shipping_address: typing.Optional["ShippingAddress"] = None


class ShippingOption(BaseModel):
    id: typing.Optional[str] = None
    title: typing.Optional[str] = None
    prices: typing.Optional[typing.List["LabeledPrice"]] = None


class SuccessfulPayment(BaseModel):
    currency: typing.Optional[str] = None
    total_amount: typing.Optional[int] = None
    invoice_payload: typing.Optional[str] = None
    shipping_option_id: typing.Optional[str] = None
    order_info: typing.Optional["OrderInfo"] = None
    telegram_payment_charge_id: typing.Optional[str] = None
    provider_payment_charge_id: typing.Optional[str] = None


class ShippingQuery(BaseModel):
    id: typing.Optional[str] = None
    from_: typing.Optional["User"] = None
    invoice_payload: typing.Optional[str] = None
    shipping_address: typing.Optional["ShippingAddress"] = None


class PreCheckoutQuery(BaseModel):
    id: typing.Optional[str] = None
    from_: typing.Optional["User"] = None
    currency: typing.Optional[str] = None
    total_amount: typing.Optional[int] = None
    invoice_payload: typing.Optional[str] = None
    shipping_option_id: typing.Optional[str] = None
    order_info: typing.Optional["OrderInfo"] = None


class PassportData(BaseModel):
    data: typing.Optional[typing.List["EncryptedPassportElement"]] = None
    credentials: typing.Optional["EncryptedCredentials"] = None


class PassportFile(BaseModel):
    file_id: typing.Optional[str] = None
    file_unique_id: typing.Optional[str] = None
    file_size: typing.Optional[int] = None
    file_date: typing.Optional[int] = None


class EncryptedPassportElement(BaseModel):
    type: typing.Optional[str] = None
    data: typing.Optional[str] = None
    phone_number: typing.Optional[str] = None
    email: typing.Optional[str] = None
    files: typing.Optional[typing.List["PassportFile"]] = None
    front_side: typing.Optional["PassportFile"] = None
    reverse_side: typing.Optional["PassportFile"] = None
    selfie: typing.Optional["PassportFile"] = None
    translation: typing.Optional[typing.List["PassportFile"]] = None
    hash: typing.Optional[str] = None


class EncryptedCredentials(BaseModel):
    data: typing.Optional[str] = None
    hash: typing.Optional[str] = None
    secret: typing.Optional[str] = None


class PassportElementError(BaseModel):
    pass


class PassportElementErrorDataField(BaseModel):
    source: typing.Optional[str] = None
    type: typing.Optional[str] = None
    field_name: typing.Optional[str] = None
    data_hash: typing.Optional[str] = None
    message: typing.Optional[str] = None


class PassportElementErrorFrontSide(BaseModel):
    source: typing.Optional[str] = None
    type: typing.Optional[str] = None
    file_hash: typing.Optional[str] = None
    message: typing.Optional[str] = None


class PassportElementErrorReverseSide(BaseModel):
    source: typing.Optional[str] = None
    type: typing.Optional[str] = None
    file_hash: typing.Optional[str] = None
    message: typing.Optional[str] = None


class PassportElementErrorSelfie(BaseModel):
    source: typing.Optional[str] = None
    type: typing.Optional[str] = None
    file_hash: typing.Optional[str] = None
    message: typing.Optional[str] = None


class PassportElementErrorFile(BaseModel):
    source: typing.Optional[str] = None
    type: typing.Optional[str] = None
    file_hash: typing.Optional[str] = None
    message: typing.Optional[str] = None


class PassportElementErrorFiles(BaseModel):
    source: typing.Optional[str] = None
    type: typing.Optional[str] = None
    file_hashes: typing.Optional[typing.List[str]] = None
    message: typing.Optional[str] = None


class PassportElementErrorTranslationFile(BaseModel):
    source: typing.Optional[str] = None
    type: typing.Optional[str] = None
    file_hash: typing.Optional[str] = None
    message: typing.Optional[str] = None


class PassportElementErrorTranslationFiles(BaseModel):
    source: typing.Optional[str] = None
    type: typing.Optional[str] = None
    file_hashes: typing.Optional[typing.List[str]] = None
    message: typing.Optional[str] = None


class PassportElementErrorUnspecified(BaseModel):
    source: typing.Optional[str] = None
    type: typing.Optional[str] = None
    element_hash: typing.Optional[str] = None
    message: typing.Optional[str] = None


class Game(BaseModel):
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    photo: typing.Optional[typing.List["PhotoSize"]] = None
    text: typing.Optional[str] = None
    text_entities: typing.Optional[typing.List["MessageEntity"]] = None
    animation: typing.Optional["Animation"] = None


class CallbackGame(BaseModel):
    pass


class GameHighScore(BaseModel):
    position: typing.Optional[int] = None
    user: typing.Optional["User"] = None
    score: typing.Optional[int] = None


for v in locals().copy().values():
    if inspect.isclass(v) and issubclass(v, BaseModel):
        v.update_forward_refs()

__all__ = (
    "Error",
    "Update",
    "WebhookInfo",
    "User",
    "Chat",
    "Message",
    "MessageId",
    "MessageEntity",
    "PhotoSize",
    "Animation",
    "Audio",
    "Document",
    "Video",
    "VideoNote",
    "Voice",
    "Contact",
    "Dice",
    "PollOption",
    "PollAnswer",
    "Poll",
    "Location",
    "Venue",
    "WebAppData",
    "ProximityAlertTriggered",
    "MessageAutoDeleteTimerChanged",
    "VideoChatScheduled",
    "VideoChatStarted",
    "VideoChatEnded",
    "VideoChatParticipantsInvited",
    "UserProfilePhotos",
    "File",
    "WebAppInfo",
    "ReplyKeyboardMarkup",
    "KeyboardButton",
    "KeyboardButtonPollType",
    "ReplyKeyboardRemove",
    "InlineKeyboardMarkup",
    "InlineKeyboardButton",
    "LoginUrl",
    "CallbackQuery",
    "ForceReply",
    "ChatPhoto",
    "ChatInviteLink",
    "ChatAdministratorRights",
    "ChatMember",
    "ChatMemberOwner",
    "ChatMemberAdministrator",
    "ChatMemberMember",
    "ChatMemberRestricted",
    "ChatMemberLeft",
    "ChatMemberBanned",
    "ChatMemberUpdated",
    "ChatJoinRequest",
    "ChatPermissions",
    "ChatLocation",
    "BotCommand",
    "BotCommandScope",
    "BotCommandScopeDefault",
    "BotCommandScopeAllPrivateChats",
    "BotCommandScopeAllGroupChats",
    "BotCommandScopeAllChatAdministrators",
    "BotCommandScopeChat",
    "BotCommandScopeChatAdministrators",
    "BotCommandScopeChatMember",
    "MenuButton",
    "MenuButtonCommands",
    "MenuButtonWebApp",
    "MenuButtonDefault",
    "ResponseParameters",
    "InputMedia",
    "InputMediaPhoto",
    "InputMediaVideo",
    "InputMediaAnimation",
    "InputMediaAudio",
    "InputMediaDocument",
    "InputFile",
    "Sticker",
    "StickerSet",
    "MaskPosition",
    "InlineQuery",
    "InlineQueryResult",
    "InlineQueryResultArticle",
    "InlineQueryResultPhoto",
    "InlineQueryResultGif",
    "InlineQueryResultMpeg4Gif",
    "InlineQueryResultVideo",
    "InlineQueryResultAudio",
    "InlineQueryResultVoice",
    "InlineQueryResultDocument",
    "InlineQueryResultLocation",
    "InlineQueryResultVenue",
    "InlineQueryResultContact",
    "InlineQueryResultGame",
    "InlineQueryResultCachedPhoto",
    "InlineQueryResultCachedGif",
    "InlineQueryResultCachedMpeg4Gif",
    "InlineQueryResultCachedSticker",
    "InlineQueryResultCachedDocument",
    "InlineQueryResultCachedVideo",
    "InlineQueryResultCachedVoice",
    "InlineQueryResultCachedAudio",
    "InputMessageContent",
    "InputTextMessageContent",
    "InputLocationMessageContent",
    "InputVenueMessageContent",
    "InputContactMessageContent",
    "InputInvoiceMessageContent",
    "ChosenInlineResult",
    "SentWebAppMessage",
    "LabeledPrice",
    "Invoice",
    "ShippingAddress",
    "OrderInfo",
    "ShippingOption",
    "SuccessfulPayment",
    "ShippingQuery",
    "PreCheckoutQuery",
    "PassportData",
    "PassportFile",
    "EncryptedPassportElement",
    "EncryptedCredentials",
    "PassportElementError",
    "PassportElementErrorDataField",
    "PassportElementErrorFrontSide",
    "PassportElementErrorReverseSide",
    "PassportElementErrorSelfie",
    "PassportElementErrorFile",
    "PassportElementErrorFiles",
    "PassportElementErrorTranslationFile",
    "PassportElementErrorTranslationFiles",
    "PassportElementErrorUnspecified",
    "Game",
    "CallbackGame",
    "GameHighScore",
)
