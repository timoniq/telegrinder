import typing
from telegrinder.model import *  # noqa: F403


class Error(Model):
    ok: bool
    error_code: int
    description: str
    parameters: typing.Optional["ResponseParameters"] = None


class Update(Model):
    """This [object](https://core.telegram.org/bots/api/#available-types)
    represents an incoming update.
    At most **one** of the optional parameters
    can be present in any given update.
    Docs: https://core.telegram.org/bots/api/#update"""

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
    """Describes the current status of a webhook.
    Docs: https://core.telegram.org/bots/api/#webhookinfo"""

    url: str
    has_custom_certificate: bool
    pending_update_count: int
    ip_address: typing.Optional[str] = None
    last_error_date: typing.Optional[int] = None
    last_error_message: typing.Optional[str] = None
    last_synchronization_error_date: typing.Optional[int] = None
    max_connections: typing.Optional[int] = None
    allowed_updates: typing.Optional[list[str]] = None


class User(Model):
    """This object represents a Telegram user or bot.
    Docs: https://core.telegram.org/bots/api/#user"""

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
    """This object represents a chat.
    Docs: https://core.telegram.org/bots/api/#chat"""

    id: int
    type: str
    title: typing.Optional[str] = None
    username: typing.Optional[str] = None
    first_name: typing.Optional[str] = None
    last_name: typing.Optional[str] = None
    is_forum: typing.Optional[bool] = None
    photo: typing.Optional["ChatPhoto"] = None
    active_usernames: typing.Optional[list[str]] = None
    emoji_status_custom_emoji_id: typing.Optional[str] = None
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
    has_aggressive_anti_spam_enabled: typing.Optional[bool] = None
    has_hidden_members: typing.Optional[bool] = None
    has_protected_content: typing.Optional[bool] = None
    sticker_set_name: typing.Optional[str] = None
    can_set_sticker_set: typing.Optional[bool] = None
    linked_chat_id: typing.Optional[int] = None
    location: typing.Optional["ChatLocation"] = None


class Message(Model):
    """This object represents a message.
    Docs: https://core.telegram.org/bots/api/#message"""

    message_id: int
    message_thread_id: typing.Optional[int] = None
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
    is_topic_message: typing.Optional[bool] = None
    is_automatic_forward: typing.Optional[bool] = None
    reply_to_message: typing.Optional["Message"] = None
    via_bot: typing.Optional["User"] = None
    edit_date: typing.Optional[int] = None
    has_protected_content: typing.Optional[bool] = None
    media_group_id: typing.Optional[str] = None
    author_signature: typing.Optional[str] = None
    text: typing.Optional[str] = None
    entities: typing.Optional[list["MessageEntity"]] = None
    animation: typing.Optional["Animation"] = None
    audio: typing.Optional["Audio"] = None
    document: typing.Optional["Document"] = None
    photo: typing.Optional[list["PhotoSize"]] = None
    sticker: typing.Optional["Sticker"] = None
    video: typing.Optional["Video"] = None
    video_note: typing.Optional["VideoNote"] = None
    voice: typing.Optional["Voice"] = None
    caption: typing.Optional[str] = None
    caption_entities: typing.Optional[list["MessageEntity"]] = None
    has_media_spoiler: typing.Optional[bool] = None
    contact: typing.Optional["Contact"] = None
    dice: typing.Optional["Dice"] = None
    game: typing.Optional["Game"] = None
    poll: typing.Optional["Poll"] = None
    venue: typing.Optional["Venue"] = None
    location: typing.Optional["Location"] = None
    new_chat_members: typing.Optional[list["User"]] = None
    left_chat_member: typing.Optional["User"] = None
    new_chat_title: typing.Optional[str] = None
    new_chat_photo: typing.Optional[list["PhotoSize"]] = None
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
    user_shared: typing.Optional["UserShared"] = None
    chat_shared: typing.Optional["ChatShared"] = None
    connected_website: typing.Optional[str] = None
    write_access_allowed: typing.Optional["WriteAccessAllowed"] = None
    passport_data: typing.Optional["PassportData"] = None
    proximity_alert_triggered: typing.Optional["ProximityAlertTriggered"] = None
    forum_topic_created: typing.Optional["ForumTopicCreated"] = None
    forum_topic_edited: typing.Optional["ForumTopicEdited"] = None
    forum_topic_closed: typing.Optional["ForumTopicClosed"] = None
    forum_topic_reopened: typing.Optional["ForumTopicReopened"] = None
    general_forum_topic_hidden: typing.Optional["GeneralForumTopicHidden"] = None
    general_forum_topic_unhidden: typing.Optional["GeneralForumTopicUnhidden"] = None
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
    """This object represents a unique message identifier.
    Docs: https://core.telegram.org/bots/api/#messageid"""

    message_id: int


class MessageEntity(Model):
    """This object represents one special entity in a text message. For example,
    hashtags, usernames, URLs, etc.
    Docs: https://core.telegram.org/bots/api/#messageentity"""

    type: str
    offset: int
    length: int
    url: typing.Optional[str] = None
    user: typing.Optional["User"] = None
    language: typing.Optional[str] = None
    custom_emoji_id: typing.Optional[str] = None


class PhotoSize(Model):
    """This object represents one size of a photo or a [file](https://core.telegram.org/bots/api/#document)
    / [sticker](https://core.telegram.org/bots/api/#sticker) thumbnail.

    Docs: https://core.telegram.org/bots/api/#photosize"""

    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: typing.Optional[int] = None


class Animation(Model):
    """This object represents an animation file (GIF or H.264/MPEG-4 AVC video
    without sound).
    Docs: https://core.telegram.org/bots/api/#animation"""

    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumbnail: typing.Optional["PhotoSize"] = None
    file_name: typing.Optional[str] = None
    mime_type: typing.Optional[str] = None
    file_size: typing.Optional[int] = None


class Audio(Model):
    """This object represents an audio file to be treated as music by the Telegram
    clients.
    Docs: https://core.telegram.org/bots/api/#audio"""

    file_id: str
    file_unique_id: str
    duration: int
    performer: typing.Optional[str] = None
    title: typing.Optional[str] = None
    file_name: typing.Optional[str] = None
    mime_type: typing.Optional[str] = None
    file_size: typing.Optional[int] = None
    thumbnail: typing.Optional["PhotoSize"] = None


class Document(Model):
    """This object represents a general file (as opposed to [photos](https://core.telegram.org/bots/api/#photosize),
    [voice messages](https://core.telegram.org/bots/api/#voice) and
    [audio files](https://core.telegram.org/bots/api/#audio)).
    Docs: https://core.telegram.org/bots/api/#document"""

    file_id: str
    file_unique_id: str
    thumbnail: typing.Optional["PhotoSize"] = None
    file_name: typing.Optional[str] = None
    mime_type: typing.Optional[str] = None
    file_size: typing.Optional[int] = None


class Video(Model):
    """This object represents a video file.
    Docs: https://core.telegram.org/bots/api/#video"""

    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumbnail: typing.Optional["PhotoSize"] = None
    file_name: typing.Optional[str] = None
    mime_type: typing.Optional[str] = None
    file_size: typing.Optional[int] = None


class VideoNote(Model):
    """This object represents a [video message](https://telegram.org/blog/video-messages-and-telescope)
    (available in Telegram apps as of [v.4.0](https://telegram.org/blog/video-messages-and-telescope)).

    Docs: https://core.telegram.org/bots/api/#videonote"""

    file_id: str
    file_unique_id: str
    length: int
    duration: int
    thumbnail: typing.Optional["PhotoSize"] = None
    file_size: typing.Optional[int] = None


class Voice(Model):
    """This object represents a voice note.
    Docs: https://core.telegram.org/bots/api/#voice"""

    file_id: str
    file_unique_id: str
    duration: int
    mime_type: typing.Optional[str] = None
    file_size: typing.Optional[int] = None


class Contact(Model):
    """This object represents a phone contact.
    Docs: https://core.telegram.org/bots/api/#contact"""

    phone_number: str
    first_name: str
    last_name: typing.Optional[str] = None
    user_id: typing.Optional[int] = None
    vcard: typing.Optional[str] = None


class Dice(Model):
    """This object represents an animated emoji that displays a random value.

    Docs: https://core.telegram.org/bots/api/#dice"""

    emoji: str
    value: int


class PollOption(Model):
    """This object contains information about one answer option in a poll.
    Docs: https://core.telegram.org/bots/api/#polloption"""

    text: str
    voter_count: int


class PollAnswer(Model):
    """This object represents an answer of a user in a non-anonymous poll.
    Docs: https://core.telegram.org/bots/api/#pollanswer"""

    poll_id: str
    user: "User"
    option_ids: list[int]


class Poll(Model):
    """This object contains information about a poll.
    Docs: https://core.telegram.org/bots/api/#poll"""

    id: str
    question: str
    options: list["PollOption"]
    total_voter_count: int
    is_closed: bool
    is_anonymous: bool
    type: str
    allows_multiple_answers: bool
    correct_option_id: typing.Optional[int] = None
    explanation: typing.Optional[str] = None
    explanation_entities: typing.Optional[list["MessageEntity"]] = None
    open_period: typing.Optional[int] = None
    close_date: typing.Optional[int] = None


class Location(Model):
    """This object represents a point on the map.
    Docs: https://core.telegram.org/bots/api/#location"""

    longitude: float
    latitude: float
    horizontal_accuracy: typing.Optional[float] = None
    live_period: typing.Optional[int] = None
    heading: typing.Optional[int] = None
    proximity_alert_radius: typing.Optional[int] = None


class Venue(Model):
    """This object represents a venue.
    Docs: https://core.telegram.org/bots/api/#venue"""

    location: "Location"
    title: str
    address: str
    foursquare_id: typing.Optional[str] = None
    foursquare_type: typing.Optional[str] = None
    google_place_id: typing.Optional[str] = None
    google_place_type: typing.Optional[str] = None


class WebAppData(Model):
    """Describes data sent from a [Web App](https://core.telegram.org/bots/webapps)
    to the bot.
    Docs: https://core.telegram.org/bots/api/#webappdata"""

    data: str
    button_text: str


class ProximityAlertTriggered(Model):
    """This object represents the content of a service message, sent whenever
    a user in the chat triggers a proximity alert set by another user.
    Docs: https://core.telegram.org/bots/api/#proximityalerttriggered"""

    traveler: "User"
    watcher: "User"
    distance: int


class MessageAutoDeleteTimerChanged(Model):
    """This object represents a service message about a change in auto-delete
    timer settings.
    Docs: https://core.telegram.org/bots/api/#messageautodeletetimerchanged"""

    message_auto_delete_time: int


class ForumTopicCreated(Model):
    """This object represents a service message about a new forum topic created
    in the chat.
    Docs: https://core.telegram.org/bots/api/#forumtopiccreated"""

    name: str
    icon_color: int
    icon_custom_emoji_id: typing.Optional[str] = None


class ForumTopicClosed(Model):
    """This object represents a service message about a forum topic closed in the
    chat. Currently holds no information.
    Docs: https://core.telegram.org/bots/api/#forumtopicclosed"""

    pass


class ForumTopicEdited(Model):
    """This object represents a service message about an edited forum topic.
    Docs: https://core.telegram.org/bots/api/#forumtopicedited"""

    name: typing.Optional[str] = None
    icon_custom_emoji_id: typing.Optional[str] = None


class ForumTopicReopened(Model):
    """This object represents a service message about a forum topic reopened in
    the chat. Currently holds no information.
    Docs: https://core.telegram.org/bots/api/#forumtopicreopened"""

    pass


class GeneralForumTopicHidden(Model):
    """This object represents a service message about General forum topic hidden
    in the chat. Currently holds no information.
    Docs: https://core.telegram.org/bots/api/#generalforumtopichidden"""

    pass


class GeneralForumTopicUnhidden(Model):
    """This object represents a service message about General forum topic unhidden
    in the chat. Currently holds no information.
    Docs: https://core.telegram.org/bots/api/#generalforumtopicunhidden"""

    pass


class UserShared(Model):
    """This object contains information about the user whose identifier was shared
    with the bot using a [KeyboardButtonRequestUser](https://core.telegram.org/bots/api/#keyboardbuttonrequestuser)
    button.
    Docs: https://core.telegram.org/bots/api/#usershared"""

    request_id: int
    user_id: int


class ChatShared(Model):
    """This object contains information about the chat whose identifier was shared
    with the bot using a [KeyboardButtonRequestChat](https://core.telegram.org/bots/api/#keyboardbuttonrequestchat)
    button.
    Docs: https://core.telegram.org/bots/api/#chatshared"""

    request_id: int
    chat_id: int


class WriteAccessAllowed(Model):
    """This object represents a service message about a user allowing a bot to write
    messages after adding the bot to the attachment menu or launching a Web App
    from a link.
    Docs: https://core.telegram.org/bots/api/#writeaccessallowed"""

    web_app_name: typing.Optional[str] = None


class VideoChatScheduled(Model):
    """This object represents a service message about a video chat scheduled in
    the chat.
    Docs: https://core.telegram.org/bots/api/#videochatscheduled"""

    start_date: int


class VideoChatStarted(Model):
    """This object represents a service message about a video chat started in the
    chat. Currently holds no information.
    Docs: https://core.telegram.org/bots/api/#videochatstarted"""

    pass


class VideoChatEnded(Model):
    """This object represents a service message about a video chat ended in the
    chat.
    Docs: https://core.telegram.org/bots/api/#videochatended"""

    duration: int


class VideoChatParticipantsInvited(Model):
    """This object represents a service message about new members invited to a
    video chat.
    Docs: https://core.telegram.org/bots/api/#videochatparticipantsinvited"""

    users: list["User"]


class UserProfilePhotos(Model):
    """This object represent a user's profile pictures.
    Docs: https://core.telegram.org/bots/api/#userprofilephotos"""

    total_count: int
    photos: list[list["PhotoSize"]]


class File(Model):
    """This object represents a file ready to be downloaded. The file can be downloaded
    via the link `https://api.telegram.org/file/bot<token>/<file_path>`.
    It is guaranteed that the link will be valid for at least 1 hour. When the link
    expires, a new one can be requested by calling [getFile](https://core.telegram.org/bots/api/#getfile).

    The
    maximum file size to download is 20 MB
    Docs: https://core.telegram.org/bots/api/#file"""

    file_id: str
    file_unique_id: str
    file_size: typing.Optional[int] = None
    file_path: typing.Optional[str] = None


class WebAppInfo(Model):
    """Describes a [Web App](https://core.telegram.org/bots/webapps).
    Docs: https://core.telegram.org/bots/api/#webappinfo"""

    url: str


class ReplyKeyboardMarkup(Model):
    """This object represents a [custom keyboard](https://core.telegram.org/bots/features#keyboards)
    with reply options (see [Introduction to bots](https://core.telegram.org/bots/features#keyboards)
    for details and examples).
    Docs: https://core.telegram.org/bots/api/#replykeyboardmarkup"""

    keyboard: list[list["KeyboardButton"]]
    is_persistent: typing.Optional[bool] = False
    resize_keyboard: typing.Optional[bool] = False
    one_time_keyboard: typing.Optional[bool] = False
    input_field_placeholder: typing.Optional[str] = None
    selective: typing.Optional[bool] = None


class KeyboardButton(Model):
    """This object represents one button of the reply keyboard. For simple text
    buttons, *String* can be used instead of this object to specify the button
    text. The optional fields *web_app*, *request_user*, *request_chat*,
    *request_contact*, *request_location*, and *request_poll* are
    mutually exclusive.
    Docs: https://core.telegram.org/bots/api/#keyboardbutton"""

    text: str
    request_user: typing.Optional["KeyboardButtonRequestUser"] = None
    request_chat: typing.Optional["KeyboardButtonRequestChat"] = None
    request_contact: typing.Optional[bool] = None
    request_location: typing.Optional[bool] = None
    request_poll: typing.Optional["KeyboardButtonPollType"] = None
    web_app: typing.Optional["WebAppInfo"] = None


class KeyboardButtonRequestUser(Model):
    """This object defines the criteria used to request a suitable user. The identifier
    of the selected user will be shared with the bot when the corresponding button
    is pressed. [More about requesting users »](https://core.telegram.org/bots/features#chat-and-user-selection)

    Docs: https://core.telegram.org/bots/api/#keyboardbuttonrequestuser"""

    request_id: int
    user_is_bot: typing.Optional[bool] = None
    user_is_premium: typing.Optional[bool] = None


class KeyboardButtonRequestChat(Model):
    """This object defines the criteria used to request a suitable chat. The identifier
    of the selected chat will be shared with the bot when the corresponding button
    is pressed. [More about requesting chats »](https://core.telegram.org/bots/features#chat-and-user-selection)

    Docs: https://core.telegram.org/bots/api/#keyboardbuttonrequestchat"""

    request_id: int
    chat_is_channel: bool
    chat_is_forum: typing.Optional[bool] = None
    chat_has_username: typing.Optional[bool] = None
    chat_is_created: typing.Optional[bool] = None
    user_administrator_rights: typing.Optional["ChatAdministratorRights"] = None
    bot_administrator_rights: typing.Optional["ChatAdministratorRights"] = None
    bot_is_member: typing.Optional[bool] = None


class KeyboardButtonPollType(Model):
    """This object represents type of a poll, which is allowed to be created and
    sent when the corresponding button is pressed.
    Docs: https://core.telegram.org/bots/api/#keyboardbuttonpolltype"""

    type: typing.Optional[str] = None


class ReplyKeyboardRemove(Model):
    """Upon receiving a message with this object, Telegram clients will remove
    the current custom keyboard and display the default letter-keyboard.
    By default, custom keyboards are displayed until a new keyboard is sent
    by a bot. An exception is made for one-time keyboards that are hidden immediately
    after the user presses a button (see [ReplyKeyboardMarkup](https://core.telegram.org/bots/api/#replykeyboardmarkup)).

    Docs: https://core.telegram.org/bots/api/#replykeyboardremove"""

    remove_keyboard: bool
    selective: typing.Optional[bool] = None


class InlineKeyboardMarkup(Model):
    """This object represents an [inline keyboard](https://core.telegram.org/bots/features#inline-keyboards)
    that appears right next to the message it belongs to.
    Docs: https://core.telegram.org/bots/api/#inlinekeyboardmarkup"""

    inline_keyboard: list[list["InlineKeyboardButton"]]


class InlineKeyboardButton(Model):
    """This object represents one button of an inline keyboard. You **must** use
    exactly one of the optional fields.
    Docs: https://core.telegram.org/bots/api/#inlinekeyboardbutton"""

    text: str
    url: typing.Optional[str] = None
    callback_data: typing.Optional[str] = None
    web_app: typing.Optional["WebAppInfo"] = None
    login_url: typing.Optional["LoginUrl"] = None
    switch_inline_query: typing.Optional[str] = None
    switch_inline_query_current_chat: typing.Optional[str] = None
    switch_inline_query_chosen_chat: typing.Optional[
        "SwitchInlineQueryChosenChat"
    ] = None
    callback_game: typing.Optional["CallbackGame"] = None
    pay: typing.Optional[bool] = None


class LoginUrl(Model):
    """This object represents a parameter of the inline keyboard button used to
    automatically authorize a user. Serves as a great replacement for the [Telegram
    Login Widget](https://core.telegram.org/widgets/login) when the
    user is coming from Telegram. All the user needs to do is tap/click a button
    and confirm that they want to log in:

    Telegram apps support these buttons
    as of [version 5.7](https://telegram.org/blog/privacy-discussions-web-bots#meet-seamless-web-bots).

    Sample
    bot: [@discussbot](https://t.me/discussbot)
    Docs: https://core.telegram.org/bots/api/#loginurl"""

    url: str
    forward_text: typing.Optional[str] = None
    bot_username: typing.Optional[str] = None
    request_write_access: typing.Optional[bool] = None


class SwitchInlineQueryChosenChat(Model):
    """This object represents an inline button that switches the current user
    to inline mode in a chosen chat, with an optional default inline query.
    Docs: https://core.telegram.org/bots/api/#switchinlinequerychosenchat"""

    query: typing.Optional[str] = None
    allow_user_chats: typing.Optional[bool] = None
    allow_bot_chats: typing.Optional[bool] = None
    allow_group_chats: typing.Optional[bool] = None
    allow_channel_chats: typing.Optional[bool] = None


class CallbackQuery(Model):
    """This object represents an incoming callback query from a callback button
    in an [inline keyboard](https://core.telegram.org/bots/features#inline-keyboards).
    If the button that originated the query was attached to a message sent by
    the bot, the field *message* will be present. If the button was attached
    to a message sent via the bot (in [inline mode](https://core.telegram.org/bots/api/#inline-mode)),
    the field *inline_message_id* will be present. Exactly one of the fields
    *data* or *game_short_name* will be present.
    Docs: https://core.telegram.org/bots/api/#callbackquery"""

    id: str
    from_: "User"
    message: typing.Optional["Message"] = None
    inline_message_id: typing.Optional[str] = None
    chat_instance: str
    data: typing.Optional[str] = None
    game_short_name: typing.Optional[str] = None


class ForceReply(Model):
    """Upon receiving a message with this object, Telegram clients will display
    a reply interface to the user (act as if the user has selected the bot's message
    and tapped 'Reply'). This can be extremely useful if you want to create user-friendly
    step-by-step interfaces without having to sacrifice [privacy mode](https://core.telegram.org/bots/features#privacy-mode).

    Docs: https://core.telegram.org/bots/api/#forcereply"""

    force_reply: bool
    input_field_placeholder: typing.Optional[str] = None
    selective: typing.Optional[bool] = None


class ChatPhoto(Model):
    """This object represents a chat photo.
    Docs: https://core.telegram.org/bots/api/#chatphoto"""

    small_file_id: str
    small_file_unique_id: str
    big_file_id: str
    big_file_unique_id: str


class ChatInviteLink(Model):
    """Represents an invite link for a chat.
    Docs: https://core.telegram.org/bots/api/#chatinvitelink"""

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
    """Represents the rights of an administrator in a chat.
    Docs: https://core.telegram.org/bots/api/#chatadministratorrights"""

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
    can_manage_topics: typing.Optional[bool] = None


class ChatMember(Model):
    """This object contains information about one member of a chat. Currently,
    the following 6 types of chat members are supported:

    * [ChatMemberOwner](https://core.telegram.org/bots/api/#chatmemberowner)
    *
    [ChatMemberAdministrator](https://core.telegram.org/bots/api/#chatmemberadministrator)
    *
    [ChatMemberMember](https://core.telegram.org/bots/api/#chatmembermember)
    *
    [ChatMemberRestricted](https://core.telegram.org/bots/api/#chatmemberrestricted)
    *
    [ChatMemberLeft](https://core.telegram.org/bots/api/#chatmemberleft)
    *
    [ChatMemberBanned](https://core.telegram.org/bots/api/#chatmemberbanned)

    Docs: https://core.telegram.org/bots/api/#chatmember"""

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
    can_manage_topics: typing.Optional[bool] = None
    is_member: typing.Optional[bool] = None
    can_send_messages: typing.Optional[bool] = None
    can_send_audios: typing.Optional[bool] = None
    can_send_documents: typing.Optional[bool] = None
    can_send_photos: typing.Optional[bool] = None
    can_send_videos: typing.Optional[bool] = None
    can_send_video_notes: typing.Optional[bool] = None
    can_send_voice_notes: typing.Optional[bool] = None
    can_send_polls: typing.Optional[bool] = None
    can_send_other_messages: typing.Optional[bool] = None
    can_add_web_page_previews: typing.Optional[bool] = None
    until_date: typing.Optional[int] = None


class ChatMemberOwner(Model):
    """Represents a [chat member](https://core.telegram.org/bots/api/#chatmember)
    that owns the chat and has all administrator privileges.
    Docs: https://core.telegram.org/bots/api/#chatmemberowner"""

    status: str
    user: "User"
    is_anonymous: bool
    custom_title: typing.Optional[str] = None


class ChatMemberAdministrator(Model):
    """Represents a [chat member](https://core.telegram.org/bots/api/#chatmember)
    that has some additional privileges.
    Docs: https://core.telegram.org/bots/api/#chatmemberadministrator"""

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
    can_manage_topics: typing.Optional[bool] = None
    custom_title: typing.Optional[str] = None


class ChatMemberMember(Model):
    """Represents a [chat member](https://core.telegram.org/bots/api/#chatmember)
    that has no additional privileges or restrictions.
    Docs: https://core.telegram.org/bots/api/#chatmembermember"""

    status: str
    user: "User"


class ChatMemberRestricted(Model):
    """Represents a [chat member](https://core.telegram.org/bots/api/#chatmember)
    that is under certain restrictions in the chat. Supergroups only.
    Docs: https://core.telegram.org/bots/api/#chatmemberrestricted"""

    status: str
    user: "User"
    is_member: bool
    can_send_messages: bool
    can_send_audios: bool
    can_send_documents: bool
    can_send_photos: bool
    can_send_videos: bool
    can_send_video_notes: bool
    can_send_voice_notes: bool
    can_send_polls: bool
    can_send_other_messages: bool
    can_add_web_page_previews: bool
    can_change_info: bool
    can_invite_users: bool
    can_pin_messages: bool
    can_manage_topics: bool
    until_date: int


class ChatMemberLeft(Model):
    """Represents a [chat member](https://core.telegram.org/bots/api/#chatmember)
    that isn't currently a member of the chat, but may join it themselves.
    Docs: https://core.telegram.org/bots/api/#chatmemberleft"""

    status: str
    user: "User"


class ChatMemberBanned(Model):
    """Represents a [chat member](https://core.telegram.org/bots/api/#chatmember)
    that was banned in the chat and can't return to the chat or view chat messages.

    Docs: https://core.telegram.org/bots/api/#chatmemberbanned"""

    status: str
    user: "User"
    until_date: int


class ChatMemberUpdated(Model):
    """This object represents changes in the status of a chat member.
    Docs: https://core.telegram.org/bots/api/#chatmemberupdated"""

    chat: "Chat"
    from_: "User"
    date: int
    old_chat_member: "ChatMember"
    new_chat_member: "ChatMember"
    invite_link: typing.Optional["ChatInviteLink"] = None
    via_chat_folder_invite_link: typing.Optional[bool] = None


class ChatJoinRequest(Model):
    """Represents a join request sent to a chat.
    Docs: https://core.telegram.org/bots/api/#chatjoinrequest"""

    chat: "Chat"
    from_: "User"
    user_chat_id: int
    date: int
    bio: typing.Optional[str] = None
    invite_link: typing.Optional["ChatInviteLink"] = None


class ChatPermissions(Model):
    """Describes actions that a non-administrator user is allowed to take in a
    chat.
    Docs: https://core.telegram.org/bots/api/#chatpermissions"""

    can_send_messages: typing.Optional[bool] = None
    can_send_audios: typing.Optional[bool] = None
    can_send_documents: typing.Optional[bool] = None
    can_send_photos: typing.Optional[bool] = None
    can_send_videos: typing.Optional[bool] = None
    can_send_video_notes: typing.Optional[bool] = None
    can_send_voice_notes: typing.Optional[bool] = None
    can_send_polls: typing.Optional[bool] = None
    can_send_other_messages: typing.Optional[bool] = None
    can_add_web_page_previews: typing.Optional[bool] = None
    can_change_info: typing.Optional[bool] = None
    can_invite_users: typing.Optional[bool] = None
    can_pin_messages: typing.Optional[bool] = None
    can_manage_topics: typing.Optional[bool] = None


class ChatLocation(Model):
    """Represents a location to which a chat is connected.
    Docs: https://core.telegram.org/bots/api/#chatlocation"""

    location: "Location"
    address: str


class ForumTopic(Model):
    """This object represents a forum topic.
    Docs: https://core.telegram.org/bots/api/#forumtopic"""

    message_thread_id: int
    name: str
    icon_color: int
    icon_custom_emoji_id: typing.Optional[str] = None


class BotCommand(Model):
    """This object represents a bot command.
    Docs: https://core.telegram.org/bots/api/#botcommand"""

    command: str
    description: str


class BotCommandScope(Model):
    """This object represents the scope to which bot commands are applied. Currently,
    the following 7 scopes are supported:

    * [BotCommandScopeDefault](https://core.telegram.org/bots/api/#botcommandscopedefault)
    *
    [BotCommandScopeAllPrivateChats](https://core.telegram.org/bots/api/#botcommandscopeallprivatechats)
    *
    [BotCommandScopeAllGroupChats](https://core.telegram.org/bots/api/#botcommandscopeallgroupchats)
    *
    [BotCommandScopeAllChatAdministrators](https://core.telegram.org/bots/api/#botcommandscopeallchatadministrators)
    *
    [BotCommandScopeChat](https://core.telegram.org/bots/api/#botcommandscopechat)
    *
    [BotCommandScopeChatAdministrators](https://core.telegram.org/bots/api/#botcommandscopechatadministrators)
    *
    [BotCommandScopeChatMember](https://core.telegram.org/bots/api/#botcommandscopechatmember)

    Docs: https://core.telegram.org/bots/api/#botcommandscope"""

    type: typing.Optional[str] = "chat_member"
    chat_id: typing.Optional[typing.Union[int, str]] = None
    user_id: typing.Optional[int] = None


class BotCommandScopeDefault(Model):
    """Represents the default [scope](https://core.telegram.org/bots/api/#botcommandscope)
    of bot commands. Default commands are used if no commands with a [narrower
    scope](https://core.telegram.org/bots/api/#determining-list-of-commands)
    are specified for the user.
    Docs: https://core.telegram.org/bots/api/#botcommandscopedefault"""

    type: str


class BotCommandScopeAllPrivateChats(Model):
    """Represents the [scope](https://core.telegram.org/bots/api/#botcommandscope)
    of bot commands, covering all private chats.
    Docs: https://core.telegram.org/bots/api/#botcommandscopeallprivatechats"""

    type: str


class BotCommandScopeAllGroupChats(Model):
    """Represents the [scope](https://core.telegram.org/bots/api/#botcommandscope)
    of bot commands, covering all group and supergroup chats.
    Docs: https://core.telegram.org/bots/api/#botcommandscopeallgroupchats"""

    type: str


class BotCommandScopeAllChatAdministrators(Model):
    """Represents the [scope](https://core.telegram.org/bots/api/#botcommandscope)
    of bot commands, covering all group and supergroup chat administrators.

    Docs: https://core.telegram.org/bots/api/#botcommandscopeallchatadministrators"""

    type: str


class BotCommandScopeChat(Model):
    """Represents the [scope](https://core.telegram.org/bots/api/#botcommandscope)
    of bot commands, covering a specific chat.
    Docs: https://core.telegram.org/bots/api/#botcommandscopechat"""

    type: str
    chat_id: typing.Union[int, str]


class BotCommandScopeChatAdministrators(Model):
    """Represents the [scope](https://core.telegram.org/bots/api/#botcommandscope)
    of bot commands, covering all administrators of a specific group or supergroup
    chat.
    Docs: https://core.telegram.org/bots/api/#botcommandscopechatadministrators"""

    type: str
    chat_id: typing.Union[int, str]


class BotCommandScopeChatMember(Model):
    """Represents the [scope](https://core.telegram.org/bots/api/#botcommandscope)
    of bot commands, covering a specific member of a group or supergroup chat.

    Docs: https://core.telegram.org/bots/api/#botcommandscopechatmember"""

    type: str
    chat_id: typing.Union[int, str]
    user_id: int


class BotName(Model):
    """This object represents the bot's name.
    Docs: https://core.telegram.org/bots/api/#botname"""

    name: str


class BotDescription(Model):
    """This object represents the bot's description.
    Docs: https://core.telegram.org/bots/api/#botdescription"""

    description: str


class BotShortDescription(Model):
    """This object represents the bot's short description.
    Docs: https://core.telegram.org/bots/api/#botshortdescription"""

    short_description: str


class MenuButton(Model):
    """This object describes the bot's menu button in a private chat. It should
    be one of

    * [MenuButtonCommands](https://core.telegram.org/bots/api/#menubuttoncommands)
    *
    [MenuButtonWebApp](https://core.telegram.org/bots/api/#menubuttonwebapp)
    *
    [MenuButtonDefault](https://core.telegram.org/bots/api/#menubuttondefault)

    Docs: https://core.telegram.org/bots/api/#menubutton"""

    type: typing.Optional[str] = "default"
    text: typing.Optional[str] = None
    web_app: typing.Optional["WebAppInfo"] = None


class MenuButtonCommands(Model):
    """Represents a menu button, which opens the bot's list of commands.
    Docs: https://core.telegram.org/bots/api/#menubuttoncommands"""

    type: str


class MenuButtonWebApp(Model):
    """Represents a menu button, which launches a [Web App](https://core.telegram.org/bots/webapps).

    Docs: https://core.telegram.org/bots/api/#menubuttonwebapp"""

    type: str
    text: str
    web_app: "WebAppInfo"


class MenuButtonDefault(Model):
    """Describes that no specific value for the menu button was set.
    Docs: https://core.telegram.org/bots/api/#menubuttondefault"""

    type: str


class ResponseParameters(Model):
    """Describes why a request was unsuccessful.
    Docs: https://core.telegram.org/bots/api/#responseparameters"""

    migrate_to_chat_id: typing.Optional[int] = None
    retry_after: typing.Optional[int] = None


class InputMedia(Model):
    """This object represents the content of a media message to be sent. It should
    be one of

    * [InputMediaAnimation](https://core.telegram.org/bots/api/#inputmediaanimation)
    *
    [InputMediaDocument](https://core.telegram.org/bots/api/#inputmediadocument)
    *
    [InputMediaAudio](https://core.telegram.org/bots/api/#inputmediaaudio)
    *
    [InputMediaPhoto](https://core.telegram.org/bots/api/#inputmediaphoto)
    *
    [InputMediaVideo](https://core.telegram.org/bots/api/#inputmediavideo)

    Docs: https://core.telegram.org/bots/api/#inputmedia"""

    type: typing.Optional[str] = "video"
    media: typing.Optional[str] = None
    thumbnail: typing.Optional[typing.Union["InputFile", str]] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[list["MessageEntity"]] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None
    duration: typing.Optional[int] = None
    has_spoiler: typing.Optional[bool] = None
    disable_content_type_detection: typing.Optional[bool] = None
    performer: typing.Optional[str] = None
    title: typing.Optional[str] = None
    supports_streaming: typing.Optional[bool] = None


class InputMediaPhoto(Model):
    """Represents a photo to be sent.
    Docs: https://core.telegram.org/bots/api/#inputmediaphoto"""

    type: str
    media: str
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[list["MessageEntity"]] = None
    has_spoiler: typing.Optional[bool] = None


class InputMediaVideo(Model):
    """Represents a video to be sent.
    Docs: https://core.telegram.org/bots/api/#inputmediavideo"""

    type: str
    media: str
    thumbnail: typing.Optional[typing.Union["InputFile", str]] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[list["MessageEntity"]] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None
    duration: typing.Optional[int] = None
    supports_streaming: typing.Optional[bool] = None
    has_spoiler: typing.Optional[bool] = None


class InputMediaAnimation(Model):
    """Represents an animation file (GIF or H.264/MPEG-4 AVC video without sound)
    to be sent.
    Docs: https://core.telegram.org/bots/api/#inputmediaanimation"""

    type: str
    media: str
    thumbnail: typing.Optional[typing.Union["InputFile", str]] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[list["MessageEntity"]] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None
    duration: typing.Optional[int] = None
    has_spoiler: typing.Optional[bool] = None


class InputMediaAudio(Model):
    """Represents an audio file to be treated as music to be sent.
    Docs: https://core.telegram.org/bots/api/#inputmediaaudio"""

    type: str
    media: str
    thumbnail: typing.Optional[typing.Union["InputFile", str]] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[list["MessageEntity"]] = None
    duration: typing.Optional[int] = None
    performer: typing.Optional[str] = None
    title: typing.Optional[str] = None


class InputMediaDocument(Model):
    """Represents a general file to be sent.
    Docs: https://core.telegram.org/bots/api/#inputmediadocument"""

    type: str
    media: str
    thumbnail: typing.Optional[typing.Union["InputFile", str]] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[list["MessageEntity"]] = None
    disable_content_type_detection: typing.Optional[bool] = None


InputFile = typing.NamedTuple("InputFile", [("filename", str), ("data", bytes)])


class Sticker(Model):
    """This object represents a sticker.
    Docs: https://core.telegram.org/bots/api/#sticker"""

    file_id: str
    file_unique_id: str
    type: str
    width: int
    height: int
    is_animated: bool
    is_video: bool
    thumbnail: typing.Optional["PhotoSize"] = None
    emoji: typing.Optional[str] = None
    set_name: typing.Optional[str] = None
    premium_animation: typing.Optional["File"] = None
    mask_position: typing.Optional["MaskPosition"] = None
    custom_emoji_id: typing.Optional[str] = None
    needs_repainting: typing.Optional[bool] = None
    file_size: typing.Optional[int] = None


class StickerSet(Model):
    """This object represents a sticker set.
    Docs: https://core.telegram.org/bots/api/#stickerset"""

    name: str
    title: str
    sticker_type: str
    is_animated: bool
    is_video: bool
    stickers: list["Sticker"]
    thumbnail: typing.Optional["PhotoSize"] = None


class MaskPosition(Model):
    """This object describes the position on faces where a mask should be placed
    by default.
    Docs: https://core.telegram.org/bots/api/#maskposition"""

    point: str
    x_shift: float
    y_shift: float
    scale: float


class InputSticker(Model):
    """This object describes a sticker to be added to a sticker set.
    Docs: https://core.telegram.org/bots/api/#inputsticker"""

    sticker: typing.Union["InputFile", str]
    emoji_list: list[str]
    mask_position: typing.Optional["MaskPosition"] = None
    keywords: typing.Optional[list[str]] = None


class InlineQuery(Model):
    """This object represents an incoming inline query. When the user sends an
    empty query, your bot could return some default or trending results.
    Docs: https://core.telegram.org/bots/api/#inlinequery"""

    id: str
    from_: "User"
    query: str
    offset: str
    chat_type: typing.Optional[str] = None
    location: typing.Optional["Location"] = None


class InlineQueryResultsButton(Model):
    """This object represents a button to be shown above inline query results.
    You **must** use exactly one of the optional fields.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultsbutton"""

    text: str
    web_app: typing.Optional["WebAppInfo"] = None
    start_parameter: typing.Optional[str] = None


class InlineQueryResult(Model):
    """This object represents one result of an inline query. Telegram clients
    currently support results of the following 20 types:

    * [InlineQueryResultCachedAudio](https://core.telegram.org/bots/api/#inlinequeryresultcachedaudio)
    *
    [InlineQueryResultCachedDocument](https://core.telegram.org/bots/api/#inlinequeryresultcacheddocument)
    *
    [InlineQueryResultCachedGif](https://core.telegram.org/bots/api/#inlinequeryresultcachedgif)
    *
    [InlineQueryResultCachedMpeg4Gif](https://core.telegram.org/bots/api/#inlinequeryresultcachedmpeg4gif)
    *
    [InlineQueryResultCachedPhoto](https://core.telegram.org/bots/api/#inlinequeryresultcachedphoto)
    *
    [InlineQueryResultCachedSticker](https://core.telegram.org/bots/api/#inlinequeryresultcachedsticker)
    *
    [InlineQueryResultCachedVideo](https://core.telegram.org/bots/api/#inlinequeryresultcachedvideo)
    *
    [InlineQueryResultCachedVoice](https://core.telegram.org/bots/api/#inlinequeryresultcachedvoice)
    *
    [InlineQueryResultArticle](https://core.telegram.org/bots/api/#inlinequeryresultarticle)
    *
    [InlineQueryResultAudio](https://core.telegram.org/bots/api/#inlinequeryresultaudio)
    *
    [InlineQueryResultContact](https://core.telegram.org/bots/api/#inlinequeryresultcontact)
    *
    [InlineQueryResultGame](https://core.telegram.org/bots/api/#inlinequeryresultgame)
    *
    [InlineQueryResultDocument](https://core.telegram.org/bots/api/#inlinequeryresultdocument)
    *
    [InlineQueryResultGif](https://core.telegram.org/bots/api/#inlinequeryresultgif)
    *
    [InlineQueryResultLocation](https://core.telegram.org/bots/api/#inlinequeryresultlocation)
    *
    [InlineQueryResultMpeg4Gif](https://core.telegram.org/bots/api/#inlinequeryresultmpeg4gif)
    *
    [InlineQueryResultPhoto](https://core.telegram.org/bots/api/#inlinequeryresultphoto)
    *
    [InlineQueryResultVenue](https://core.telegram.org/bots/api/#inlinequeryresultvenue)
    *
    [InlineQueryResultVideo](https://core.telegram.org/bots/api/#inlinequeryresultvideo)
    *
    [InlineQueryResultVoice](https://core.telegram.org/bots/api/#inlinequeryresultvoice)

    Docs: https://core.telegram.org/bots/api/#inlinequeryresult"""

    type: typing.Optional[str] = "voice"
    id: typing.Optional[str] = None
    audio_file_id: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[list["MessageEntity"]] = None
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
    thumbnail_url: typing.Optional[str] = None
    thumbnail_width: typing.Optional[int] = None
    thumbnail_height: typing.Optional[int] = None
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
    thumbnail_mime_type: typing.Optional[str] = "image/jpeg"
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
    """Represents a link to an article or web page.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultarticle"""

    type: str
    id: str
    title: str
    input_message_content: "InputMessageContent"
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    url: typing.Optional[str] = None
    hide_url: typing.Optional[bool] = None
    description: typing.Optional[str] = None
    thumbnail_url: typing.Optional[str] = None
    thumbnail_width: typing.Optional[int] = None
    thumbnail_height: typing.Optional[int] = None


class InlineQueryResultPhoto(Model):
    """Represents a link to a photo. By default, this photo will be sent by the user
    with optional caption. Alternatively, you can use *input_message_content*
    to send a message with the specified content instead of the photo.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultphoto"""

    type: str
    id: str
    photo_url: str
    thumbnail_url: str
    photo_width: typing.Optional[int] = None
    photo_height: typing.Optional[int] = None
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[list["MessageEntity"]] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultGif(Model):
    """Represents a link to an animated GIF file. By default, this animated GIF
    file will be sent by the user with optional caption. Alternatively, you
    can use *input_message_content* to send a message with the specified
    content instead of the animation.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultgif"""

    type: str
    id: str
    gif_url: str
    gif_width: typing.Optional[int] = None
    gif_height: typing.Optional[int] = None
    gif_duration: typing.Optional[int] = None
    thumbnail_url: str
    thumbnail_mime_type: typing.Optional[str] = "image/jpeg"
    title: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[list["MessageEntity"]] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultMpeg4Gif(Model):
    """Represents a link to a video animation (H.264/MPEG-4 AVC video without
    sound). By default, this animated MPEG-4 file will be sent by the user with
    optional caption. Alternatively, you can use *input_message_content*
    to send a message with the specified content instead of the animation.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultmpeg4gif"""

    type: str
    id: str
    mpeg4_url: str
    mpeg4_width: typing.Optional[int] = None
    mpeg4_height: typing.Optional[int] = None
    mpeg4_duration: typing.Optional[int] = None
    thumbnail_url: str
    thumbnail_mime_type: typing.Optional[str] = "image/jpeg"
    title: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[list["MessageEntity"]] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultVideo(Model):
    """Represents a link to a page containing an embedded video player or a video
    file. By default, this video file will be sent by the user with an optional
    caption. Alternatively, you can use *input_message_content* to send
    a message with the specified content instead of the video.

    If an InlineQueryResultVideo
    message contains an embedded video (e.g., YouTube), you **must** replace
    its content using *input_message_content*.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultvideo"""

    type: str
    id: str
    video_url: str
    mime_type: str
    thumbnail_url: str
    title: str
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[list["MessageEntity"]] = None
    video_width: typing.Optional[int] = None
    video_height: typing.Optional[int] = None
    video_duration: typing.Optional[int] = None
    description: typing.Optional[str] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultAudio(Model):
    """Represents a link to an MP3 audio file. By default, this audio file will be
    sent by the user. Alternatively, you can use *input_message_content*
    to send a message with the specified content instead of the audio.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultaudio"""

    type: str
    id: str
    audio_url: str
    title: str
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[list["MessageEntity"]] = None
    performer: typing.Optional[str] = None
    audio_duration: typing.Optional[int] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultVoice(Model):
    """Represents a link to a voice recording in an .OGG container encoded with
    OPUS. By default, this voice recording will be sent by the user. Alternatively,
    you can use *input_message_content* to send a message with the specified
    content instead of the the voice message.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultvoice"""

    type: str
    id: str
    voice_url: str
    title: str
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[list["MessageEntity"]] = None
    voice_duration: typing.Optional[int] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultDocument(Model):
    """Represents a link to a file. By default, this file will be sent by the user
    with an optional caption. Alternatively, you can use *input_message_content*
    to send a message with the specified content instead of the file. Currently,
    only **.PDF** and **.ZIP** files can be sent using this method.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultdocument"""

    type: str
    id: str
    title: str
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[list["MessageEntity"]] = None
    document_url: str
    mime_type: str
    description: typing.Optional[str] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None
    thumbnail_url: typing.Optional[str] = None
    thumbnail_width: typing.Optional[int] = None
    thumbnail_height: typing.Optional[int] = None


class InlineQueryResultLocation(Model):
    """Represents a location on a map. By default, the location will be sent by the
    user. Alternatively, you can use *input_message_content* to send a
    message with the specified content instead of the location.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultlocation"""

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
    thumbnail_url: typing.Optional[str] = None
    thumbnail_width: typing.Optional[int] = None
    thumbnail_height: typing.Optional[int] = None


class InlineQueryResultVenue(Model):
    """Represents a venue. By default, the venue will be sent by the user. 
    Alternatively, you can use *input_message_content* to send a message 
    with the specified content instead of the venue.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultvenue"""

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
    thumbnail_url: typing.Optional[str] = None
    thumbnail_width: typing.Optional[int] = None
    thumbnail_height: typing.Optional[int] = None


class InlineQueryResultContact(Model):
    """Represents a contact with a phone number. By default, this contact will
    be sent by the user. Alternatively, you can use *input_message_content*
    to send a message with the specified content instead of the contact.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultcontact"""

    type: str
    id: str
    phone_number: str
    first_name: str
    last_name: typing.Optional[str] = None
    vcard: typing.Optional[str] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None
    thumbnail_url: typing.Optional[str] = None
    thumbnail_width: typing.Optional[int] = None
    thumbnail_height: typing.Optional[int] = None


class InlineQueryResultGame(Model):
    """Represents a [Game](https://core.telegram.org/bots/api/#games).

    Docs: https://core.telegram.org/bots/api/#inlinequeryresultgame"""

    type: str
    id: str
    game_short_name: str
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None


class InlineQueryResultCachedPhoto(Model):
    """Represents a link to a photo stored on the Telegram servers. By default,
    this photo will be sent by the user with an optional caption. Alternatively,
    you can use *input_message_content* to send a message with the specified
    content instead of the photo.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultcachedphoto"""

    type: str
    id: str
    photo_file_id: str
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[list["MessageEntity"]] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultCachedGif(Model):
    """Represents a link to an animated GIF file stored on the Telegram servers.
    By default, this animated GIF file will be sent by the user with an optional
    caption. Alternatively, you can use *input_message_content* to send
    a message with specified content instead of the animation.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultcachedgif"""

    type: str
    id: str
    gif_file_id: str
    title: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[list["MessageEntity"]] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultCachedMpeg4Gif(Model):
    """Represents a link to a video animation (H.264/MPEG-4 AVC video without
    sound) stored on the Telegram servers. By default, this animated MPEG-4
    file will be sent by the user with an optional caption. Alternatively, you
    can use *input_message_content* to send a message with the specified
    content instead of the animation.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultcachedmpeg4gif"""

    type: str
    id: str
    mpeg4_file_id: str
    title: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[list["MessageEntity"]] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultCachedSticker(Model):
    """Represents a link to a sticker stored on the Telegram servers. By default,
    this sticker will be sent by the user. Alternatively, you can use *input_message_content*
    to send a message with the specified content instead of the sticker.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultcachedsticker"""

    type: str
    id: str
    sticker_file_id: str
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultCachedDocument(Model):
    """Represents a link to a file stored on the Telegram servers. By default, this
    file will be sent by the user with an optional caption. Alternatively, you
    can use *input_message_content* to send a message with the specified
    content instead of the file.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultcacheddocument"""

    type: str
    id: str
    title: str
    document_file_id: str
    description: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[list["MessageEntity"]] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultCachedVideo(Model):
    """Represents a link to a video file stored on the Telegram servers. By default,
    this video file will be sent by the user with an optional caption. Alternatively,
    you can use *input_message_content* to send a message with the specified
    content instead of the video.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultcachedvideo"""

    type: str
    id: str
    video_file_id: str
    title: str
    description: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[list["MessageEntity"]] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultCachedVoice(Model):
    """Represents a link to a voice message stored on the Telegram servers. By default,
    this voice message will be sent by the user. Alternatively, you can use *input_message_content*
    to send a message with the specified content instead of the voice message.

    Docs: https://core.telegram.org/bots/api/#inlinequeryresultcachedvoice"""

    type: str
    id: str
    voice_file_id: str
    title: str
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[list["MessageEntity"]] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InlineQueryResultCachedAudio(Model):
    """Represents a link to an MP3 audio file stored on the Telegram servers. By
    default, this audio file will be sent by the user. Alternatively, you can
    use *input_message_content* to send a message with the specified content
    instead of the audio.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultcachedaudio"""

    type: str
    id: str
    audio_file_id: str
    caption: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    caption_entities: typing.Optional[list["MessageEntity"]] = None
    reply_markup: typing.Optional["InlineKeyboardMarkup"] = None
    input_message_content: typing.Optional["InputMessageContent"] = None


class InputMessageContent(Model):
    """This object represents the content of a message to be sent as a result of an
    inline query. Telegram clients currently support the following 5 types:

    *
    [InputTextMessageContent](https://core.telegram.org/bots/api/#inputtextmessagecontent)
    *
    [InputLocationMessageContent](https://core.telegram.org/bots/api/#inputlocationmessagecontent)
    *
    [InputVenueMessageContent](https://core.telegram.org/bots/api/#inputvenuemessagecontent)
    *
    [InputContactMessageContent](https://core.telegram.org/bots/api/#inputcontactmessagecontent)
    *
    [InputInvoiceMessageContent](https://core.telegram.org/bots/api/#inputinvoicemessagecontent)

    Docs: https://core.telegram.org/bots/api/#inputmessagecontent"""

    message_text: typing.Optional[str] = None
    parse_mode: typing.Optional[str] = None
    entities: typing.Optional[list["MessageEntity"]] = None
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
    prices: typing.Optional[list["LabeledPrice"]] = None
    max_tip_amount: typing.Optional[int] = 0
    suggested_tip_amounts: typing.Optional[list[int]] = None
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
    """Represents the [content](https://core.telegram.org/bots/api/#inputmessagecontent)
    of a text message to be sent as the result of an inline query.
    Docs: https://core.telegram.org/bots/api/#inputtextmessagecontent"""

    message_text: str
    parse_mode: typing.Optional[str] = None
    entities: typing.Optional[list["MessageEntity"]] = None
    disable_web_page_preview: typing.Optional[bool] = None


class InputLocationMessageContent(Model):
    """Represents the [content](https://core.telegram.org/bots/api/#inputmessagecontent)
    of a location message to be sent as the result of an inline query.
    Docs: https://core.telegram.org/bots/api/#inputlocationmessagecontent"""

    latitude: float
    longitude: float
    horizontal_accuracy: typing.Optional[float] = None
    live_period: typing.Optional[int] = None
    heading: typing.Optional[int] = None
    proximity_alert_radius: typing.Optional[int] = None


class InputVenueMessageContent(Model):
    """Represents the [content](https://core.telegram.org/bots/api/#inputmessagecontent)
    of a venue message to be sent as the result of an inline query.
    Docs: https://core.telegram.org/bots/api/#inputvenuemessagecontent"""

    latitude: float
    longitude: float
    title: str
    address: str
    foursquare_id: typing.Optional[str] = None
    foursquare_type: typing.Optional[str] = None
    google_place_id: typing.Optional[str] = None
    google_place_type: typing.Optional[str] = None


class InputContactMessageContent(Model):
    """Represents the [content](https://core.telegram.org/bots/api/#inputmessagecontent)
    of a contact message to be sent as the result of an inline query.
    Docs: https://core.telegram.org/bots/api/#inputcontactmessagecontent"""

    phone_number: str
    first_name: str
    last_name: typing.Optional[str] = None
    vcard: typing.Optional[str] = None


class InputInvoiceMessageContent(Model):
    """Represents the [content](https://core.telegram.org/bots/api/#inputmessagecontent)
    of an invoice message to be sent as the result of an inline query.
    Docs: https://core.telegram.org/bots/api/#inputinvoicemessagecontent"""

    title: str
    description: str
    payload: str
    provider_token: str
    currency: str
    prices: list["LabeledPrice"]
    max_tip_amount: typing.Optional[int] = 0
    suggested_tip_amounts: typing.Optional[list[int]] = None
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
    """Represents a [result](https://core.telegram.org/bots/api/#inlinequeryresult)
    of an inline query that was chosen by the user and sent to their chat partner.

    Docs: https://core.telegram.org/bots/api/#choseninlineresult"""

    result_id: str
    from_: "User"
    location: typing.Optional["Location"] = None
    inline_message_id: typing.Optional[str] = None
    query: str


class SentWebAppMessage(Model):
    """Describes an inline message sent by a [Web App](https://core.telegram.org/bots/webapps)
    on behalf of a user.
    Docs: https://core.telegram.org/bots/api/#sentwebappmessage"""

    inline_message_id: typing.Optional[str] = None


class LabeledPrice(Model):
    """This object represents a portion of the price for goods or services.
    Docs: https://core.telegram.org/bots/api/#labeledprice"""

    label: str
    amount: int


class Invoice(Model):
    """This object contains basic information about an invoice.
    Docs: https://core.telegram.org/bots/api/#invoice"""

    title: str
    description: str
    start_parameter: str
    currency: str
    total_amount: int


class ShippingAddress(Model):
    """This object represents a shipping address.
    Docs: https://core.telegram.org/bots/api/#shippingaddress"""

    country_code: str
    state: str
    city: str
    street_line1: str
    street_line2: str
    post_code: str


class OrderInfo(Model):
    """This object represents information about an order.
    Docs: https://core.telegram.org/bots/api/#orderinfo"""

    name: typing.Optional[str] = None
    phone_number: typing.Optional[str] = None
    email: typing.Optional[str] = None
    shipping_address: typing.Optional["ShippingAddress"] = None


class ShippingOption(Model):
    """This object represents one shipping option.
    Docs: https://core.telegram.org/bots/api/#shippingoption"""

    id: str
    title: str
    prices: list["LabeledPrice"]


class SuccessfulPayment(Model):
    """This object contains basic information about a successful payment.
    Docs: https://core.telegram.org/bots/api/#successfulpayment"""

    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: typing.Optional[str] = None
    order_info: typing.Optional["OrderInfo"] = None
    telegram_payment_charge_id: str
    provider_payment_charge_id: str


class ShippingQuery(Model):
    """This object contains information about an incoming shipping query.
    Docs: https://core.telegram.org/bots/api/#shippingquery"""

    id: str
    from_: "User"
    invoice_payload: str
    shipping_address: "ShippingAddress"


class PreCheckoutQuery(Model):
    """This object contains information about an incoming pre-checkout query.

    Docs: https://core.telegram.org/bots/api/#precheckoutquery"""

    id: str
    from_: "User"
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: typing.Optional[str] = None
    order_info: typing.Optional["OrderInfo"] = None


class PassportData(Model):
    """Describes Telegram Passport data shared with the bot by the user.
    Docs: https://core.telegram.org/bots/api/#passportdata"""

    data: list["EncryptedPassportElement"]
    credentials: "EncryptedCredentials"


class PassportFile(Model):
    """This object represents a file uploaded to Telegram Passport. Currently
    all Telegram Passport files are in JPEG format when decrypted and don't
    exceed 10MB.
    Docs: https://core.telegram.org/bots/api/#passportfile"""

    file_id: str
    file_unique_id: str
    file_size: int
    file_date: int


class EncryptedPassportElement(Model):
    """Describes documents or other Telegram Passport elements shared with the
    bot by the user.
    Docs: https://core.telegram.org/bots/api/#encryptedpassportelement"""

    type: str
    data: typing.Optional[str] = None
    phone_number: typing.Optional[str] = None
    email: typing.Optional[str] = None
    files: typing.Optional[list["PassportFile"]] = None
    front_side: typing.Optional["PassportFile"] = None
    reverse_side: typing.Optional["PassportFile"] = None
    selfie: typing.Optional["PassportFile"] = None
    translation: typing.Optional[list["PassportFile"]] = None
    hash: str


class EncryptedCredentials(Model):
    """Describes data required for decrypting and authenticating [EncryptedPassportElement](https://core.telegram.org/bots/api/#encryptedpassportelement).
    See the [Telegram Passport Documentation](https://core.telegram.org/passport#receiving-information)
    for a complete description of the data decryption and authentication processes.

    Docs: https://core.telegram.org/bots/api/#encryptedcredentials"""

    data: str
    hash: str
    secret: str


class PassportElementError(Model):
    """This object represents an error in the Telegram Passport element which
    was submitted that should be resolved by the user. It should be one of:

    *
    [PassportElementErrorDataField](https://core.telegram.org/bots/api/#passportelementerrordatafield)
    *
    [PassportElementErrorFrontSide](https://core.telegram.org/bots/api/#passportelementerrorfrontside)
    *
    [PassportElementErrorReverseSide](https://core.telegram.org/bots/api/#passportelementerrorreverseside)
    *
    [PassportElementErrorSelfie](https://core.telegram.org/bots/api/#passportelementerrorselfie)
    *
    [PassportElementErrorFile](https://core.telegram.org/bots/api/#passportelementerrorfile)
    *
    [PassportElementErrorFiles](https://core.telegram.org/bots/api/#passportelementerrorfiles)
    *
    [PassportElementErrorTranslationFile](https://core.telegram.org/bots/api/#passportelementerrortranslationfile)
    *
    [PassportElementErrorTranslationFiles](https://core.telegram.org/bots/api/#passportelementerrortranslationfiles)
    *
    [PassportElementErrorUnspecified](https://core.telegram.org/bots/api/#passportelementerrorunspecified)

    Docs: https://core.telegram.org/bots/api/#passportelementerror"""

    source: typing.Optional[str] = "unspecified"
    type: typing.Optional[str] = None
    field_name: typing.Optional[str] = None
    data_hash: typing.Optional[str] = None
    message: typing.Optional[str] = None
    file_hash: typing.Optional[str] = None
    file_hashes: typing.Optional[list[str]] = None
    element_hash: typing.Optional[str] = None


class PassportElementErrorDataField(Model):
    """Represents an issue in one of the data fields that was provided by the user.
    The error is considered resolved when the field's value changes.
    Docs: https://core.telegram.org/bots/api/#passportelementerrordatafield"""

    source: str
    type: str
    field_name: str
    data_hash: str
    message: str


class PassportElementErrorFrontSide(Model):
    """Represents an issue with the front side of a document. The error is considered
    resolved when the file with the front side of the document changes.
    Docs: https://core.telegram.org/bots/api/#passportelementerrorfrontside"""

    source: str
    type: str
    file_hash: str
    message: str


class PassportElementErrorReverseSide(Model):
    """Represents an issue with the reverse side of a document. The error is considered
    resolved when the file with reverse side of the document changes.
    Docs: https://core.telegram.org/bots/api/#passportelementerrorreverseside"""

    source: str
    type: str
    file_hash: str
    message: str


class PassportElementErrorSelfie(Model):
    """Represents an issue with the selfie with a document. The error is considered
    resolved when the file with the selfie changes.
    Docs: https://core.telegram.org/bots/api/#passportelementerrorselfie"""

    source: str
    type: str
    file_hash: str
    message: str


class PassportElementErrorFile(Model):
    """Represents an issue with a document scan. The error is considered resolved
    when the file with the document scan changes.
    Docs: https://core.telegram.org/bots/api/#passportelementerrorfile"""

    source: str
    type: str
    file_hash: str
    message: str


class PassportElementErrorFiles(Model):
    """Represents an issue with a list of scans. The error is considered resolved
    when the list of files containing the scans changes.
    Docs: https://core.telegram.org/bots/api/#passportelementerrorfiles"""

    source: str
    type: str
    file_hashes: list[str]
    message: str


class PassportElementErrorTranslationFile(Model):
    """Represents an issue with one of the files that constitute the translation
    of a document. The error is considered resolved when the file changes.
    Docs: https://core.telegram.org/bots/api/#passportelementerrortranslationfile"""

    source: str
    type: str
    file_hash: str
    message: str


class PassportElementErrorTranslationFiles(Model):
    """Represents an issue with the translated version of a document. The error
    is considered resolved when a file with the document translation change.

    Docs: https://core.telegram.org/bots/api/#passportelementerrortranslationfiles"""

    source: str
    type: str
    file_hashes: list[str]
    message: str


class PassportElementErrorUnspecified(Model):
    """Represents an issue in an unspecified place. The error is considered resolved
    when new data is added.
    Docs: https://core.telegram.org/bots/api/#passportelementerrorunspecified"""

    source: str
    type: str
    element_hash: str
    message: str


class Game(Model):
    """This object represents a game. Use BotFather to create and edit games, their
    short names will act as unique identifiers.
    Docs: https://core.telegram.org/bots/api/#game"""

    title: str
    description: str
    photo: list["PhotoSize"]
    text: typing.Optional[str] = None
    text_entities: typing.Optional[list["MessageEntity"]] = None
    animation: typing.Optional["Animation"] = None


class CallbackGame(Model):
    """A placeholder, currently holds no information. Use [BotFather](https://t.me/botfather)
    to set up your game.
    Docs: https://core.telegram.org/bots/api/#callbackgame"""

    pass


class GameHighScore(Model):
    """This object represents one row of the high scores table for a game.
    Docs: https://core.telegram.org/bots/api/#gamehighscore"""

    position: int
    user: "User"
    score: int
