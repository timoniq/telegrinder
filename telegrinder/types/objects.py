import typing

from telegrinder.model import *
from telegrinder.option.msgspec_option import Option
from telegrinder.types.enums import *


class Error(Model):
    ok: bool
    error_code: int
    description: str
    parameters: Option["ResponseParameters"] = Option.Nothing


class Update(Model):
    """This [object](https://core.telegram.org/bots/api/#available-types)
    represents an incoming update.
    At most **one** of the optional parameters
    can be present in any given update.
    Docs: https://core.telegram.org/bots/api/#update"""

    update_id: int
    message: Option["Message"] = Option.Nothing
    edited_message: Option["Message"] = Option.Nothing
    channel_post: Option["Message"] = Option.Nothing
    edited_channel_post: Option["Message"] = Option.Nothing
    inline_query: Option["InlineQuery"] = Option.Nothing
    chosen_inline_result: Option["ChosenInlineResult"] = Option.Nothing
    callback_query: Option["CallbackQuery"] = Option.Nothing
    shipping_query: Option["ShippingQuery"] = Option.Nothing
    pre_checkout_query: Option["PreCheckoutQuery"] = Option.Nothing
    poll: Option["Poll"] = Option.Nothing
    poll_answer: Option["PollAnswer"] = Option.Nothing
    my_chat_member: Option["ChatMemberUpdated"] = Option.Nothing
    chat_member: Option["ChatMemberUpdated"] = Option.Nothing
    chat_join_request: Option["ChatJoinRequest"] = Option.Nothing


class WebhookInfo(Model):
    """Describes the current status of a webhook.
    Docs: https://core.telegram.org/bots/api/#webhookinfo"""

    url: str
    has_custom_certificate: bool
    pending_update_count: int
    ip_address: Option[str] = Option.Nothing
    last_error_date: Option[int] = Option.Nothing
    last_error_message: Option[str] = Option.Nothing
    last_synchronization_error_date: Option[int] = Option.Nothing
    max_connections: Option[int] = Option.Nothing
    allowed_updates: Option[list[str]] = Option.Nothing


class User(Model):
    """This object represents a Telegram user or bot.
    Docs: https://core.telegram.org/bots/api/#user"""

    id: int
    is_bot: bool
    first_name: str
    last_name: Option[str] = Option.Nothing
    username: Option[str] = Option.Nothing
    language_code: Option[str] = Option.Nothing
    is_premium: Option[bool] = Option.Nothing
    added_to_attachment_menu: Option[bool] = Option.Nothing
    can_join_groups: Option[bool] = Option.Nothing
    can_read_all_group_messages: Option[bool] = Option.Nothing
    supports_inline_queries: Option[bool] = Option.Nothing

    @property
    def full_name(self) -> str:
        return self.first_name + self.last_name.map(lambda v: " " + v).unwrap_or("")


class Chat(Model):
    """This object represents a chat.
    Docs: https://core.telegram.org/bots/api/#chat"""

    id: int
    type: ChatType
    title: Option[str] = Option.Nothing
    username: Option[str] = Option.Nothing
    first_name: Option[str] = Option.Nothing
    last_name: Option[str] = Option.Nothing
    is_forum: Option[bool] = Option.Nothing
    photo: Option["ChatPhoto"] = Option.Nothing
    active_usernames: Option[list[str]] = Option.Nothing
    emoji_status_custom_emoji_id: Option[str] = Option.Nothing
    emoji_status_expiration_date: Option[int] = Option.Nothing
    bio: Option[str] = Option.Nothing
    has_private_forwards: Option[bool] = Option.Nothing
    has_restricted_voice_and_video_messages: Option[bool] = Option.Nothing
    join_to_send_messages: Option[bool] = Option.Nothing
    join_by_request: Option[bool] = Option.Nothing
    description: Option[str] = Option.Nothing
    invite_link: Option[str] = Option.Nothing
    pinned_message: Option["Message"] = Option.Nothing
    permissions: Option["ChatPermissions"] = Option.Nothing
    slow_mode_delay: Option[int] = Option.Nothing
    message_auto_delete_time: Option[int] = Option.Nothing
    has_aggressive_anti_spam_enabled: Option[bool] = Option.Nothing
    has_hidden_members: Option[bool] = Option.Nothing
    has_protected_content: Option[bool] = Option.Nothing
    sticker_set_name: Option[str] = Option.Nothing
    can_set_sticker_set: Option[bool] = Option.Nothing
    linked_chat_id: Option[int] = Option.Nothing
    location: Option["ChatLocation"] = Option.Nothing


class Message(Model):
    """This object represents a message.
    Docs: https://core.telegram.org/bots/api/#message"""

    message_id: int
    date: int
    chat: "Chat"
    message_thread_id: Option[int] = Option.Nothing
    from_: Option["User"] = Option.Nothing
    sender_chat: Option["Chat"] = Option.Nothing
    forward_from: Option["User"] = Option.Nothing
    forward_from_chat: Option["Chat"] = Option.Nothing
    forward_from_message_id: Option[int] = Option.Nothing
    forward_signature: Option[str] = Option.Nothing
    forward_sender_name: Option[str] = Option.Nothing
    forward_date: Option[int] = Option.Nothing
    is_topic_message: Option[bool] = Option.Nothing
    is_automatic_forward: Option[bool] = Option.Nothing
    reply_to_message: Option["Message"] = Option.Nothing
    via_bot: Option["User"] = Option.Nothing
    edit_date: Option[int] = Option.Nothing
    has_protected_content: Option[bool] = Option.Nothing
    media_group_id: Option[str] = Option.Nothing
    author_signature: Option[str] = Option.Nothing
    text: Option[str] = Option.Nothing
    entities: Option[list["MessageEntity"]] = Option.Nothing
    animation: Option["Animation"] = Option.Nothing
    audio: Option["Audio"] = Option.Nothing
    document: Option["Document"] = Option.Nothing
    photo: Option[list["PhotoSize"]] = Option.Nothing
    sticker: Option["Sticker"] = Option.Nothing
    story: Option["Story"] = Option.Nothing
    video: Option["Video"] = Option.Nothing
    video_note: Option["VideoNote"] = Option.Nothing
    voice: Option["Voice"] = Option.Nothing
    caption: Option[str] = Option.Nothing
    caption_entities: Option[list["MessageEntity"]] = Option.Nothing
    has_media_spoiler: Option[bool] = Option.Nothing
    contact: Option["Contact"] = Option.Nothing
    dice: Option["Dice"] = Option.Nothing
    game: Option["Game"] = Option.Nothing
    poll: Option["Poll"] = Option.Nothing
    venue: Option["Venue"] = Option.Nothing
    location: Option["Location"] = Option.Nothing
    new_chat_members: Option[list["User"]] = Option.Nothing
    left_chat_member: Option["User"] = Option.Nothing
    new_chat_title: Option[str] = Option.Nothing
    new_chat_photo: Option[list["PhotoSize"]] = Option.Nothing
    delete_chat_photo: Option[bool] = Option.Nothing
    group_chat_created: Option[bool] = Option.Nothing
    supergroup_chat_created: Option[bool] = Option.Nothing
    channel_chat_created: Option[bool] = Option.Nothing
    message_auto_delete_timer_changed: Option[
        "MessageAutoDeleteTimerChanged"
    ] = Option.Nothing
    migrate_to_chat_id: Option[int] = Option.Nothing
    migrate_from_chat_id: Option[int] = Option.Nothing
    pinned_message: Option["Message"] = Option.Nothing
    invoice: Option["Invoice"] = Option.Nothing
    successful_payment: Option["SuccessfulPayment"] = Option.Nothing
    user_shared: Option["UserShared"] = Option.Nothing
    chat_shared: Option["ChatShared"] = Option.Nothing
    connected_website: Option[str] = Option.Nothing
    write_access_allowed: Option["WriteAccessAllowed"] = Option.Nothing
    passport_data: Option["PassportData"] = Option.Nothing
    proximity_alert_triggered: Option["ProximityAlertTriggered"] = Option.Nothing
    forum_topic_created: Option["ForumTopicCreated"] = Option.Nothing
    forum_topic_edited: Option["ForumTopicEdited"] = Option.Nothing
    forum_topic_closed: Option["ForumTopicClosed"] = Option.Nothing
    forum_topic_reopened: Option["ForumTopicReopened"] = Option.Nothing
    general_forum_topic_hidden: Option["GeneralForumTopicHidden"] = Option.Nothing
    general_forum_topic_unhidden: Option["GeneralForumTopicUnhidden"] = Option.Nothing
    video_chat_scheduled: Option["VideoChatScheduled"] = Option.Nothing
    video_chat_started: Option["VideoChatStarted"] = Option.Nothing
    video_chat_ended: Option["VideoChatEnded"] = Option.Nothing
    video_chat_participants_invited: Option[
        "VideoChatParticipantsInvited"
    ] = Option.Nothing
    web_app_data: Option["WebAppData"] = Option.Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Option.Nothing

    @property
    def from_user(self) -> "User":
        return self.from_.unwrap()

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

    type: MessageEntityType
    offset: int
    length: int
    url: Option[str] = Option.Nothing
    user: Option["User"] = Option.Nothing
    language: Option[str] = Option.Nothing
    custom_emoji_id: Option[str] = Option.Nothing


class PhotoSize(Model):
    """This object represents one size of a photo or a [file](https://core.telegram.org/bots/api/#document)
    / [sticker](https://core.telegram.org/bots/api/#sticker) thumbnail.

    Docs: https://core.telegram.org/bots/api/#photosize"""

    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: Option[int] = Option.Nothing


class Animation(Model):
    """This object represents an animation file (GIF or H.264/MPEG-4 AVC video
    without sound).
    Docs: https://core.telegram.org/bots/api/#animation"""

    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumbnail: Option["PhotoSize"] = Option.Nothing
    file_name: Option[str] = Option.Nothing
    mime_type: Option[str] = Option.Nothing
    file_size: Option[int] = Option.Nothing


class Audio(Model):
    """This object represents an audio file to be treated as music by the Telegram
    clients.
    Docs: https://core.telegram.org/bots/api/#audio"""

    file_id: str
    file_unique_id: str
    duration: int
    performer: Option[str] = Option.Nothing
    title: Option[str] = Option.Nothing
    file_name: Option[str] = Option.Nothing
    mime_type: Option[str] = Option.Nothing
    file_size: Option[int] = Option.Nothing
    thumbnail: Option["PhotoSize"] = Option.Nothing


class Document(Model):
    """This object represents a general file (as opposed to [photos](https://core.telegram.org/bots/api/#photosize),
    [voice messages](https://core.telegram.org/bots/api/#voice) and
    [audio files](https://core.telegram.org/bots/api/#audio)).
    Docs: https://core.telegram.org/bots/api/#document"""

    file_id: str
    file_unique_id: str
    thumbnail: Option["PhotoSize"] = Option.Nothing
    file_name: Option[str] = Option.Nothing
    mime_type: Option[str] = Option.Nothing
    file_size: Option[int] = Option.Nothing


class Story(Model):
    """This object represents a message about a forwarded story in the chat. Currently
    holds no information.
    Docs: https://core.telegram.org/bots/api/#story"""

    pass


class Video(Model):
    """This object represents a video file.
    Docs: https://core.telegram.org/bots/api/#video"""

    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumbnail: Option["PhotoSize"] = Option.Nothing
    file_name: Option[str] = Option.Nothing
    mime_type: Option[str] = Option.Nothing
    file_size: Option[int] = Option.Nothing


class VideoNote(Model):
    """This object represents a [video message](https://telegram.org/blog/video-messages-and-telescope)
    (available in Telegram apps as of [v.4.0](https://telegram.org/blog/video-messages-and-telescope)).

    Docs: https://core.telegram.org/bots/api/#videonote"""

    file_id: str
    file_unique_id: str
    length: int
    duration: int
    thumbnail: Option["PhotoSize"] = Option.Nothing
    file_size: Option[int] = Option.Nothing


class Voice(Model):
    """This object represents a voice note.
    Docs: https://core.telegram.org/bots/api/#voice"""

    file_id: str
    file_unique_id: str
    duration: int
    mime_type: Option[str] = Option.Nothing
    file_size: Option[int] = Option.Nothing


class Contact(Model):
    """This object represents a phone contact.
    Docs: https://core.telegram.org/bots/api/#contact"""

    phone_number: str
    first_name: str
    last_name: Option[str] = Option.Nothing
    user_id: Option[int] = Option.Nothing
    vcard: Option[str] = Option.Nothing


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
    option_ids: list[int]
    voter_chat: Option["Chat"] = Option.Nothing
    user: Option["User"] = Option.Nothing


class Poll(Model):
    """This object contains information about a poll.
    Docs: https://core.telegram.org/bots/api/#poll"""

    id: str
    question: str
    options: list["PollOption"]
    total_voter_count: int
    is_closed: bool
    is_anonymous: bool
    type: PollType
    allows_multiple_answers: bool
    correct_option_id: Option[int] = Option.Nothing
    explanation: Option[str] = Option.Nothing
    explanation_entities: Option[list["MessageEntity"]] = Option.Nothing
    open_period: Option[int] = Option.Nothing
    close_date: Option[int] = Option.Nothing


class Location(Model):
    """This object represents a point on the map.
    Docs: https://core.telegram.org/bots/api/#location"""

    longitude: float
    latitude: float
    horizontal_accuracy: Option[float] = Option.Nothing
    live_period: Option[int] = Option.Nothing
    heading: Option[int] = Option.Nothing
    proximity_alert_radius: Option[int] = Option.Nothing


class Venue(Model):
    """This object represents a venue.
    Docs: https://core.telegram.org/bots/api/#venue"""

    location: "Location"
    title: str
    address: str
    foursquare_id: Option[str] = Option.Nothing
    foursquare_type: Option[str] = Option.Nothing
    google_place_id: Option[str] = Option.Nothing
    google_place_type: Option[str] = Option.Nothing


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
    icon_custom_emoji_id: Option[str] = Option.Nothing


class ForumTopicClosed(Model):
    """This object represents a service message about a forum topic closed in the
    chat. Currently holds no information.
    Docs: https://core.telegram.org/bots/api/#forumtopicclosed"""

    pass


class ForumTopicEdited(Model):
    """This object represents a service message about an edited forum topic.
    Docs: https://core.telegram.org/bots/api/#forumtopicedited"""

    name: Option[str] = Option.Nothing
    icon_custom_emoji_id: Option[str] = Option.Nothing


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
    messages after adding it to the attachment menu, launching a Web App from
    a link, or accepting an explicit request from a Web App sent by the method
    [requestWriteAccess](https://core.telegram.org/bots/webapps#initializing-mini-apps).

    Docs: https://core.telegram.org/bots/api/#writeaccessallowed"""

    from_request: Option[bool] = Option.Nothing
    web_app_name: Option[str] = Option.Nothing
    from_attachment_menu: Option[bool] = Option.Nothing


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
    file_size: Option[int] = Option.Nothing
    file_path: Option[str] = Option.Nothing


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
    is_persistent: Option[bool] = Option(False)
    resize_keyboard: Option[bool] = Option(False)
    one_time_keyboard: Option[bool] = Option(False)
    input_field_placeholder: Option[str] = Option.Nothing
    selective: Option[bool] = Option.Nothing


class KeyboardButton(Model):
    """This object represents one button of the reply keyboard. For simple text
    buttons, *String* can be used instead of this object to specify the button
    text. The optional fields *web_app*, *request_user*, *request_chat*,
    *request_contact*, *request_location*, and *request_poll* are
    mutually exclusive.
    Docs: https://core.telegram.org/bots/api/#keyboardbutton"""

    text: str
    request_user: Option["KeyboardButtonRequestUser"] = Option.Nothing
    request_chat: Option["KeyboardButtonRequestChat"] = Option.Nothing
    request_contact: Option[bool] = Option.Nothing
    request_location: Option[bool] = Option.Nothing
    request_poll: Option["KeyboardButtonPollType"] = Option.Nothing
    web_app: Option["WebAppInfo"] = Option.Nothing


class KeyboardButtonRequestUser(Model):
    """This object defines the criteria used to request a suitable user. The identifier
    of the selected user will be shared with the bot when the corresponding button
    is pressed. [More about requesting users »](https://core.telegram.org/bots/features#chat-and-user-selection)

    Docs: https://core.telegram.org/bots/api/#keyboardbuttonrequestuser"""

    request_id: int
    user_is_bot: Option[bool] = Option.Nothing
    user_is_premium: Option[bool] = Option.Nothing


class KeyboardButtonRequestChat(Model):
    """This object defines the criteria used to request a suitable chat. The identifier
    of the selected chat will be shared with the bot when the corresponding button
    is pressed. [More about requesting chats »](https://core.telegram.org/bots/features#chat-and-user-selection)

    Docs: https://core.telegram.org/bots/api/#keyboardbuttonrequestchat"""

    request_id: int
    chat_is_channel: bool
    chat_is_forum: Option[bool] = Option.Nothing
    chat_has_username: Option[bool] = Option.Nothing
    chat_is_created: Option[bool] = Option.Nothing
    user_administrator_rights: Option["ChatAdministratorRights"] = Option.Nothing
    bot_administrator_rights: Option["ChatAdministratorRights"] = Option.Nothing
    bot_is_member: Option[bool] = Option.Nothing


class KeyboardButtonPollType(Model):
    """This object represents type of a poll, which is allowed to be created and
    sent when the corresponding button is pressed.
    Docs: https://core.telegram.org/bots/api/#keyboardbuttonpolltype"""

    type: Option[str] = Option.Nothing


class ReplyKeyboardRemove(Model):
    """Upon receiving a message with this object, Telegram clients will remove
    the current custom keyboard and display the default letter-keyboard.
    By default, custom keyboards are displayed until a new keyboard is sent
    by a bot. An exception is made for one-time keyboards that are hidden immediately
    after the user presses a button (see [ReplyKeyboardMarkup](https://core.telegram.org/bots/api/#replykeyboardmarkup)).

    Docs: https://core.telegram.org/bots/api/#replykeyboardremove"""

    remove_keyboard: bool
    selective: Option[bool] = Option.Nothing


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
    url: Option[str] = Option.Nothing
    callback_data: Option[str] = Option.Nothing
    web_app: Option["WebAppInfo"] = Option.Nothing
    login_url: Option["LoginUrl"] = Option.Nothing
    switch_inline_query: Option[str] = Option.Nothing
    switch_inline_query_current_chat: Option[str] = Option.Nothing
    switch_inline_query_chosen_chat: Option[
        "SwitchInlineQueryChosenChat"
    ] = Option.Nothing
    callback_game: Option["CallbackGame"] = Option.Nothing
    pay: Option[bool] = Option.Nothing


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
    forward_text: Option[str] = Option.Nothing
    bot_username: Option[str] = Option.Nothing
    request_write_access: Option[bool] = Option.Nothing


class SwitchInlineQueryChosenChat(Model):
    """This object represents an inline button that switches the current user
    to inline mode in a chosen chat, with an optional default inline query.
    Docs: https://core.telegram.org/bots/api/#switchinlinequerychosenchat"""

    query: Option[str] = Option.Nothing
    allow_user_chats: Option[bool] = Option.Nothing
    allow_bot_chats: Option[bool] = Option.Nothing
    allow_group_chats: Option[bool] = Option.Nothing
    allow_channel_chats: Option[bool] = Option.Nothing


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
    chat_instance: str
    message: Option["Message"] = Option.Nothing
    inline_message_id: Option[str] = Option.Nothing
    data: Option[str] = Option.Nothing
    game_short_name: Option[str] = Option.Nothing


class ForceReply(Model):
    """Upon receiving a message with this object, Telegram clients will display
    a reply interface to the user (act as if the user has selected the bot's message
    and tapped 'Reply'). This can be extremely useful if you want to create user-friendly
    step-by-step interfaces without having to sacrifice [privacy mode](https://core.telegram.org/bots/features#privacy-mode).

    Docs: https://core.telegram.org/bots/api/#forcereply"""

    force_reply: bool
    input_field_placeholder: Option[str] = Option.Nothing
    selective: Option[bool] = Option.Nothing


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
    name: Option[str] = Option.Nothing
    expire_date: Option[int] = Option.Nothing
    member_limit: Option[int] = Option.Nothing
    pending_join_request_count: Option[int] = Option.Nothing


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
    can_post_messages: Option[bool] = Option.Nothing
    can_edit_messages: Option[bool] = Option.Nothing
    can_pin_messages: Option[bool] = Option.Nothing
    can_post_stories: Option[bool] = Option.Nothing
    can_edit_stories: Option[bool] = Option.Nothing
    can_delete_stories: Option[bool] = Option.Nothing
    can_manage_topics: Option[bool] = Option.Nothing


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

    status: Option[str] = Option("kicked")
    user: Option["User"] = Option.Nothing
    is_anonymous: Option[bool] = Option.Nothing
    custom_title: Option[str] = Option.Nothing
    can_be_edited: Option[bool] = Option.Nothing
    can_manage_chat: Option[bool] = Option.Nothing
    can_delete_messages: Option[bool] = Option.Nothing
    can_manage_video_chats: Option[bool] = Option.Nothing
    can_restrict_members: Option[bool] = Option.Nothing
    can_promote_members: Option[bool] = Option.Nothing
    can_change_info: Option[bool] = Option.Nothing
    can_invite_users: Option[bool] = Option.Nothing
    can_post_messages: Option[bool] = Option.Nothing
    can_edit_messages: Option[bool] = Option.Nothing
    can_pin_messages: Option[bool] = Option.Nothing
    can_post_stories: Option[bool] = Option.Nothing
    can_edit_stories: Option[bool] = Option.Nothing
    can_delete_stories: Option[bool] = Option.Nothing
    can_manage_topics: Option[bool] = Option.Nothing
    is_member: Option[bool] = Option.Nothing
    can_send_messages: Option[bool] = Option.Nothing
    can_send_audios: Option[bool] = Option.Nothing
    can_send_documents: Option[bool] = Option.Nothing
    can_send_photos: Option[bool] = Option.Nothing
    can_send_videos: Option[bool] = Option.Nothing
    can_send_video_notes: Option[bool] = Option.Nothing
    can_send_voice_notes: Option[bool] = Option.Nothing
    can_send_polls: Option[bool] = Option.Nothing
    can_send_other_messages: Option[bool] = Option.Nothing
    can_add_web_page_previews: Option[bool] = Option.Nothing
    until_date: Option[int] = Option.Nothing


class ChatMemberOwner(Model):
    """Represents a [chat member](https://core.telegram.org/bots/api/#chatmember)
    that owns the chat and has all administrator privileges.
    Docs: https://core.telegram.org/bots/api/#chatmemberowner"""

    status: str
    user: "User"
    is_anonymous: bool
    custom_title: Option[str] = Option.Nothing


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
    can_post_messages: Option[bool] = Option.Nothing
    can_edit_messages: Option[bool] = Option.Nothing
    can_pin_messages: Option[bool] = Option.Nothing
    can_post_stories: Option[bool] = Option.Nothing
    can_edit_stories: Option[bool] = Option.Nothing
    can_delete_stories: Option[bool] = Option.Nothing
    can_manage_topics: Option[bool] = Option.Nothing
    custom_title: Option[str] = Option.Nothing


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
    invite_link: Option["ChatInviteLink"] = Option.Nothing
    via_chat_folder_invite_link: Option[bool] = Option.Nothing


class ChatJoinRequest(Model):
    """Represents a join request sent to a chat.
    Docs: https://core.telegram.org/bots/api/#chatjoinrequest"""

    chat: "Chat"
    from_: "User"
    user_chat_id: int
    date: int
    bio: Option[str] = Option.Nothing
    invite_link: Option["ChatInviteLink"] = Option.Nothing


class ChatPermissions(Model):
    """Describes actions that a non-administrator user is allowed to take in a
    chat.
    Docs: https://core.telegram.org/bots/api/#chatpermissions"""

    can_send_messages: Option[bool] = Option.Nothing
    can_send_audios: Option[bool] = Option.Nothing
    can_send_documents: Option[bool] = Option.Nothing
    can_send_photos: Option[bool] = Option.Nothing
    can_send_videos: Option[bool] = Option.Nothing
    can_send_video_notes: Option[bool] = Option.Nothing
    can_send_voice_notes: Option[bool] = Option.Nothing
    can_send_polls: Option[bool] = Option.Nothing
    can_send_other_messages: Option[bool] = Option.Nothing
    can_add_web_page_previews: Option[bool] = Option.Nothing
    can_change_info: Option[bool] = Option.Nothing
    can_invite_users: Option[bool] = Option.Nothing
    can_pin_messages: Option[bool] = Option.Nothing
    can_manage_topics: Option[bool] = Option.Nothing


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
    icon_custom_emoji_id: Option[str] = Option.Nothing


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

    type: Option[str] = Option("chat_member")
    chat_id: Option[typing.Union[int, str]] = Option.Nothing
    user_id: Option[int] = Option.Nothing


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

    type: Option[str] = Option("default")
    text: Option[str] = Option.Nothing
    web_app: Option["WebAppInfo"] = Option.Nothing


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

    migrate_to_chat_id: Option[int] = Option.Nothing
    retry_after: Option[int] = Option.Nothing


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

    type: Option[str] = Option("video")
    media: Option[str] = Option.Nothing
    thumbnail: Option[typing.Union["InputFile", str]] = Option.Nothing
    caption: Option[str] = Option.Nothing
    parse_mode: Option[str] = Option.Nothing
    caption_entities: Option[list["MessageEntity"]] = Option.Nothing
    width: Option[int] = Option.Nothing
    height: Option[int] = Option.Nothing
    duration: Option[int] = Option.Nothing
    has_spoiler: Option[bool] = Option.Nothing
    disable_content_type_detection: Option[bool] = Option.Nothing
    performer: Option[str] = Option.Nothing
    title: Option[str] = Option.Nothing
    supports_streaming: Option[bool] = Option.Nothing


class InputMediaPhoto(Model):
    """Represents a photo to be sent.
    Docs: https://core.telegram.org/bots/api/#inputmediaphoto"""

    type: str
    media: str
    caption: Option[str] = Option.Nothing
    parse_mode: Option[str] = Option.Nothing
    caption_entities: Option[list["MessageEntity"]] = Option.Nothing
    has_spoiler: Option[bool] = Option.Nothing


class InputMediaVideo(Model):
    """Represents a video to be sent.
    Docs: https://core.telegram.org/bots/api/#inputmediavideo"""

    type: str
    media: str
    thumbnail: Option[typing.Union["InputFile", str]] = Option.Nothing
    caption: Option[str] = Option.Nothing
    parse_mode: Option[str] = Option.Nothing
    caption_entities: Option[list["MessageEntity"]] = Option.Nothing
    width: Option[int] = Option.Nothing
    height: Option[int] = Option.Nothing
    duration: Option[int] = Option.Nothing
    supports_streaming: Option[bool] = Option.Nothing
    has_spoiler: Option[bool] = Option.Nothing


class InputMediaAnimation(Model):
    """Represents an animation file (GIF or H.264/MPEG-4 AVC video without sound)
    to be sent.
    Docs: https://core.telegram.org/bots/api/#inputmediaanimation"""

    type: str
    media: str
    thumbnail: Option[typing.Union["InputFile", str]] = Option.Nothing
    caption: Option[str] = Option.Nothing
    parse_mode: Option[str] = Option.Nothing
    caption_entities: Option[list["MessageEntity"]] = Option.Nothing
    width: Option[int] = Option.Nothing
    height: Option[int] = Option.Nothing
    duration: Option[int] = Option.Nothing
    has_spoiler: Option[bool] = Option.Nothing


class InputMediaAudio(Model):
    """Represents an audio file to be treated as music to be sent.
    Docs: https://core.telegram.org/bots/api/#inputmediaaudio"""

    type: str
    media: str
    thumbnail: Option[typing.Union["InputFile", str]] = Option.Nothing
    caption: Option[str] = Option.Nothing
    parse_mode: Option[str] = Option.Nothing
    caption_entities: Option[list["MessageEntity"]] = Option.Nothing
    duration: Option[int] = Option.Nothing
    performer: Option[str] = Option.Nothing
    title: Option[str] = Option.Nothing


class InputMediaDocument(Model):
    """Represents a general file to be sent.
    Docs: https://core.telegram.org/bots/api/#inputmediadocument"""

    type: str
    media: str
    thumbnail: Option[typing.Union["InputFile", str]] = Option.Nothing
    caption: Option[str] = Option.Nothing
    parse_mode: Option[str] = Option.Nothing
    caption_entities: Option[list["MessageEntity"]] = Option.Nothing
    disable_content_type_detection: Option[bool] = Option.Nothing


InputFile = typing.NamedTuple("InputFile", [("filename", str), ("data", bytes)])


class Sticker(Model):
    """This object represents a sticker.
    Docs: https://core.telegram.org/bots/api/#sticker"""

    file_id: str
    file_unique_id: str
    type: StickerType
    width: int
    height: int
    is_animated: bool
    is_video: bool
    thumbnail: Option["PhotoSize"] = Option.Nothing
    emoji: Option[str] = Option.Nothing
    set_name: Option[str] = Option.Nothing
    premium_animation: Option["File"] = Option.Nothing
    mask_position: Option["MaskPosition"] = Option.Nothing
    custom_emoji_id: Option[str] = Option.Nothing
    needs_repainting: Option[bool] = Option.Nothing
    file_size: Option[int] = Option.Nothing


class StickerSet(Model):
    """This object represents a sticker set.
    Docs: https://core.telegram.org/bots/api/#stickerset"""

    name: str
    title: str
    sticker_type: StickerSetStickerType
    is_animated: bool
    is_video: bool
    stickers: list["Sticker"]
    thumbnail: Option["PhotoSize"] = Option.Nothing


class MaskPosition(Model):
    """This object describes the position on faces where a mask should be placed
    by default.
    Docs: https://core.telegram.org/bots/api/#maskposition"""

    point: MaskPositionPoint
    x_shift: float
    y_shift: float
    scale: float


class InputSticker(Model):
    """This object describes a sticker to be added to a sticker set.
    Docs: https://core.telegram.org/bots/api/#inputsticker"""

    sticker: typing.Union["InputFile", str]
    emoji_list: list[str]
    mask_position: Option["MaskPosition"] = Option.Nothing
    keywords: Option[list[str]] = Option.Nothing


class InlineQuery(Model):
    """This object represents an incoming inline query. When the user sends an
    empty query, your bot could return some default or trending results.
    Docs: https://core.telegram.org/bots/api/#inlinequery"""

    id: str
    from_: "User"
    query: str
    offset: str
    chat_type: Option[InlineQueryChatType] = Option.Nothing
    location: Option["Location"] = Option.Nothing


class InlineQueryResultsButton(Model):
    """This object represents a button to be shown above inline query results.
    You **must** use exactly one of the optional fields.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultsbutton"""

    text: str
    web_app: Option["WebAppInfo"] = Option.Nothing
    start_parameter: Option[str] = Option.Nothing


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

    type: Option[str] = Option("voice")
    id: Option[str] = Option.Nothing
    audio_file_id: Option[str] = Option.Nothing
    caption: Option[str] = Option.Nothing
    parse_mode: Option[str] = Option.Nothing
    caption_entities: Option[list["MessageEntity"]] = Option.Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Option.Nothing
    input_message_content: Option["InputMessageContent"] = Option.Nothing
    title: Option[str] = Option.Nothing
    document_file_id: Option[str] = Option.Nothing
    description: Option[str] = Option.Nothing
    gif_file_id: Option[str] = Option.Nothing
    mpeg4_file_id: Option[str] = Option.Nothing
    photo_file_id: Option[str] = Option.Nothing
    sticker_file_id: Option[str] = Option.Nothing
    video_file_id: Option[str] = Option.Nothing
    voice_file_id: Option[str] = Option.Nothing
    url: Option[str] = Option.Nothing
    hide_url: Option[bool] = Option.Nothing
    thumbnail_url: Option[str] = Option.Nothing
    thumbnail_width: Option[int] = Option.Nothing
    thumbnail_height: Option[int] = Option.Nothing
    audio_url: Option[str] = Option.Nothing
    performer: Option[str] = Option.Nothing
    audio_duration: Option[int] = Option.Nothing
    phone_number: Option[str] = Option.Nothing
    first_name: Option[str] = Option.Nothing
    last_name: Option[str] = Option.Nothing
    vcard: Option[str] = Option.Nothing
    game_short_name: Option[str] = Option.Nothing
    document_url: Option[str] = Option.Nothing
    mime_type: Option[InlineQueryResultMimeType] = Option.Nothing
    gif_url: Option[str] = Option.Nothing
    gif_width: Option[int] = Option.Nothing
    gif_height: Option[int] = Option.Nothing
    gif_duration: Option[int] = Option.Nothing
    thumbnail_mime_type: Option[InlineQueryResultThumbnailMimeType] = Option(
        InlineQueryResultThumbnailMimeType("image/jpeg")
    )
    latitude: Option[float] = Option.Nothing
    longitude: Option[float] = Option.Nothing
    horizontal_accuracy: Option[float] = Option.Nothing
    live_period: Option[int] = Option.Nothing
    heading: Option[int] = Option.Nothing
    proximity_alert_radius: Option[int] = Option.Nothing
    mpeg4_url: Option[str] = Option.Nothing
    mpeg4_width: Option[int] = Option.Nothing
    mpeg4_height: Option[int] = Option.Nothing
    mpeg4_duration: Option[int] = Option.Nothing
    photo_url: Option[str] = Option.Nothing
    photo_width: Option[int] = Option.Nothing
    photo_height: Option[int] = Option.Nothing
    address: Option[str] = Option.Nothing
    foursquare_id: Option[str] = Option.Nothing
    foursquare_type: Option[str] = Option.Nothing
    google_place_id: Option[str] = Option.Nothing
    google_place_type: Option[str] = Option.Nothing
    video_url: Option[str] = Option.Nothing
    video_width: Option[int] = Option.Nothing
    video_height: Option[int] = Option.Nothing
    video_duration: Option[int] = Option.Nothing
    voice_url: Option[str] = Option.Nothing
    voice_duration: Option[int] = Option.Nothing


class InlineQueryResultArticle(Model):
    """Represents a link to an article or web page.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultarticle"""

    type: str
    id: str
    title: str
    input_message_content: "InputMessageContent"
    reply_markup: Option["InlineKeyboardMarkup"] = Option.Nothing
    url: Option[str] = Option.Nothing
    hide_url: Option[bool] = Option.Nothing
    description: Option[str] = Option.Nothing
    thumbnail_url: Option[str] = Option.Nothing
    thumbnail_width: Option[int] = Option.Nothing
    thumbnail_height: Option[int] = Option.Nothing


class InlineQueryResultPhoto(Model):
    """Represents a link to a photo. By default, this photo will be sent by the user
    with optional caption. Alternatively, you can use *input_message_content*
    to send a message with the specified content instead of the photo.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultphoto"""

    type: str
    id: str
    photo_url: str
    thumbnail_url: str
    photo_width: Option[int] = Option.Nothing
    photo_height: Option[int] = Option.Nothing
    title: Option[str] = Option.Nothing
    description: Option[str] = Option.Nothing
    caption: Option[str] = Option.Nothing
    parse_mode: Option[str] = Option.Nothing
    caption_entities: Option[list["MessageEntity"]] = Option.Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Option.Nothing
    input_message_content: Option["InputMessageContent"] = Option.Nothing


class InlineQueryResultGif(Model):
    """Represents a link to an animated GIF file. By default, this animated GIF
    file will be sent by the user with optional caption. Alternatively, you
    can use *input_message_content* to send a message with the specified
    content instead of the animation.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultgif"""

    type: str
    id: str
    gif_url: str
    thumbnail_url: str
    gif_width: Option[int] = Option.Nothing
    gif_height: Option[int] = Option.Nothing
    gif_duration: Option[int] = Option.Nothing
    thumbnail_mime_type: Option[InlineQueryResultGifThumbnailMimeType] = Option(
        InlineQueryResultGifThumbnailMimeType("image/jpeg")
    )
    title: Option[str] = Option.Nothing
    caption: Option[str] = Option.Nothing
    parse_mode: Option[str] = Option.Nothing
    caption_entities: Option[list["MessageEntity"]] = Option.Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Option.Nothing
    input_message_content: Option["InputMessageContent"] = Option.Nothing


class InlineQueryResultMpeg4Gif(Model):
    """Represents a link to a video animation (H.264/MPEG-4 AVC video without
    sound). By default, this animated MPEG-4 file will be sent by the user with
    optional caption. Alternatively, you can use *input_message_content*
    to send a message with the specified content instead of the animation.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultmpeg4gif"""

    type: str
    id: str
    mpeg4_url: str
    thumbnail_url: str
    mpeg4_width: Option[int] = Option.Nothing
    mpeg4_height: Option[int] = Option.Nothing
    mpeg4_duration: Option[int] = Option.Nothing
    thumbnail_mime_type: Option[InlineQueryResultMpeg4GifThumbnailMimeType] = Option(
        InlineQueryResultMpeg4GifThumbnailMimeType("image/jpeg")
    )
    title: Option[str] = Option.Nothing
    caption: Option[str] = Option.Nothing
    parse_mode: Option[str] = Option.Nothing
    caption_entities: Option[list["MessageEntity"]] = Option.Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Option.Nothing
    input_message_content: Option["InputMessageContent"] = Option.Nothing


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
    mime_type: InlineQueryResultVideoMimeType
    thumbnail_url: str
    title: str
    caption: Option[str] = Option.Nothing
    parse_mode: Option[str] = Option.Nothing
    caption_entities: Option[list["MessageEntity"]] = Option.Nothing
    video_width: Option[int] = Option.Nothing
    video_height: Option[int] = Option.Nothing
    video_duration: Option[int] = Option.Nothing
    description: Option[str] = Option.Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Option.Nothing
    input_message_content: Option["InputMessageContent"] = Option.Nothing


class InlineQueryResultAudio(Model):
    """Represents a link to an MP3 audio file. By default, this audio file will be
    sent by the user. Alternatively, you can use *input_message_content*
    to send a message with the specified content instead of the audio.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultaudio"""

    type: str
    id: str
    audio_url: str
    title: str
    caption: Option[str] = Option.Nothing
    parse_mode: Option[str] = Option.Nothing
    caption_entities: Option[list["MessageEntity"]] = Option.Nothing
    performer: Option[str] = Option.Nothing
    audio_duration: Option[int] = Option.Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Option.Nothing
    input_message_content: Option["InputMessageContent"] = Option.Nothing


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
    caption: Option[str] = Option.Nothing
    parse_mode: Option[str] = Option.Nothing
    caption_entities: Option[list["MessageEntity"]] = Option.Nothing
    voice_duration: Option[int] = Option.Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Option.Nothing
    input_message_content: Option["InputMessageContent"] = Option.Nothing


class InlineQueryResultDocument(Model):
    """Represents a link to a file. By default, this file will be sent by the user
    with an optional caption. Alternatively, you can use *input_message_content*
    to send a message with the specified content instead of the file. Currently,
    only **.PDF** and **.ZIP** files can be sent using this method.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultdocument"""

    type: str
    id: str
    title: str
    document_url: str
    mime_type: InlineQueryResultDocumentMimeType
    caption: Option[str] = Option.Nothing
    parse_mode: Option[str] = Option.Nothing
    caption_entities: Option[list["MessageEntity"]] = Option.Nothing
    description: Option[str] = Option.Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Option.Nothing
    input_message_content: Option["InputMessageContent"] = Option.Nothing
    thumbnail_url: Option[str] = Option.Nothing
    thumbnail_width: Option[int] = Option.Nothing
    thumbnail_height: Option[int] = Option.Nothing


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
    horizontal_accuracy: Option[float] = Option.Nothing
    live_period: Option[int] = Option.Nothing
    heading: Option[int] = Option.Nothing
    proximity_alert_radius: Option[int] = Option.Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Option.Nothing
    input_message_content: Option["InputMessageContent"] = Option.Nothing
    thumbnail_url: Option[str] = Option.Nothing
    thumbnail_width: Option[int] = Option.Nothing
    thumbnail_height: Option[int] = Option.Nothing


class InlineQueryResultVenue(Model):
    """Represents a venue. By default, the venue will be sent by the user. Alternatively,
    you can use *input_message_content* to send a message with the specified
    content instead of the venue.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultvenue"""

    type: str
    id: str
    latitude: float
    longitude: float
    title: str
    address: str
    foursquare_id: Option[str] = Option.Nothing
    foursquare_type: Option[str] = Option.Nothing
    google_place_id: Option[str] = Option.Nothing
    google_place_type: Option[str] = Option.Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Option.Nothing
    input_message_content: Option["InputMessageContent"] = Option.Nothing
    thumbnail_url: Option[str] = Option.Nothing
    thumbnail_width: Option[int] = Option.Nothing
    thumbnail_height: Option[int] = Option.Nothing


class InlineQueryResultContact(Model):
    """Represents a contact with a phone number. By default, this contact will
    be sent by the user. Alternatively, you can use *input_message_content*
    to send a message with the specified content instead of the contact.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultcontact"""

    type: str
    id: str
    phone_number: str
    first_name: str
    last_name: Option[str] = Option.Nothing
    vcard: Option[str] = Option.Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Option.Nothing
    input_message_content: Option["InputMessageContent"] = Option.Nothing
    thumbnail_url: Option[str] = Option.Nothing
    thumbnail_width: Option[int] = Option.Nothing
    thumbnail_height: Option[int] = Option.Nothing


class InlineQueryResultGame(Model):
    """Represents a [Game](https://core.telegram.org/bots/api/#games).

    Docs: https://core.telegram.org/bots/api/#inlinequeryresultgame"""

    type: str
    id: str
    game_short_name: str
    reply_markup: Option["InlineKeyboardMarkup"] = Option.Nothing


class InlineQueryResultCachedPhoto(Model):
    """Represents a link to a photo stored on the Telegram servers. By default,
    this photo will be sent by the user with an optional caption. Alternatively,
    you can use *input_message_content* to send a message with the specified
    content instead of the photo.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultcachedphoto"""

    type: str
    id: str
    photo_file_id: str
    title: Option[str] = Option.Nothing
    description: Option[str] = Option.Nothing
    caption: Option[str] = Option.Nothing
    parse_mode: Option[str] = Option.Nothing
    caption_entities: Option[list["MessageEntity"]] = Option.Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Option.Nothing
    input_message_content: Option["InputMessageContent"] = Option.Nothing


class InlineQueryResultCachedGif(Model):
    """Represents a link to an animated GIF file stored on the Telegram servers.
    By default, this animated GIF file will be sent by the user with an optional
    caption. Alternatively, you can use *input_message_content* to send
    a message with specified content instead of the animation.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultcachedgif"""

    type: str
    id: str
    gif_file_id: str
    title: Option[str] = Option.Nothing
    caption: Option[str] = Option.Nothing
    parse_mode: Option[str] = Option.Nothing
    caption_entities: Option[list["MessageEntity"]] = Option.Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Option.Nothing
    input_message_content: Option["InputMessageContent"] = Option.Nothing


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
    title: Option[str] = Option.Nothing
    caption: Option[str] = Option.Nothing
    parse_mode: Option[str] = Option.Nothing
    caption_entities: Option[list["MessageEntity"]] = Option.Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Option.Nothing
    input_message_content: Option["InputMessageContent"] = Option.Nothing


class InlineQueryResultCachedSticker(Model):
    """Represents a link to a sticker stored on the Telegram servers. By default,
    this sticker will be sent by the user. Alternatively, you can use *input_message_content*
    to send a message with the specified content instead of the sticker.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultcachedsticker"""

    type: str
    id: str
    sticker_file_id: str
    reply_markup: Option["InlineKeyboardMarkup"] = Option.Nothing
    input_message_content: Option["InputMessageContent"] = Option.Nothing


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
    description: Option[str] = Option.Nothing
    caption: Option[str] = Option.Nothing
    parse_mode: Option[str] = Option.Nothing
    caption_entities: Option[list["MessageEntity"]] = Option.Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Option.Nothing
    input_message_content: Option["InputMessageContent"] = Option.Nothing


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
    description: Option[str] = Option.Nothing
    caption: Option[str] = Option.Nothing
    parse_mode: Option[str] = Option.Nothing
    caption_entities: Option[list["MessageEntity"]] = Option.Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Option.Nothing
    input_message_content: Option["InputMessageContent"] = Option.Nothing


class InlineQueryResultCachedVoice(Model):
    """Represents a link to a voice message stored on the Telegram servers. By default,
    this voice message will be sent by the user. Alternatively, you can use *input_message_content*
    to send a message with the specified content instead of the voice message.

    Docs: https://core.telegram.org/bots/api/#inlinequeryresultcachedvoice"""

    type: str
    id: str
    voice_file_id: str
    title: str
    caption: Option[str] = Option.Nothing
    parse_mode: Option[str] = Option.Nothing
    caption_entities: Option[list["MessageEntity"]] = Option.Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Option.Nothing
    input_message_content: Option["InputMessageContent"] = Option.Nothing


class InlineQueryResultCachedAudio(Model):
    """Represents a link to an MP3 audio file stored on the Telegram servers. By
    default, this audio file will be sent by the user. Alternatively, you can
    use *input_message_content* to send a message with the specified content
    instead of the audio.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultcachedaudio"""

    type: str
    id: str
    audio_file_id: str
    caption: Option[str] = Option.Nothing
    parse_mode: Option[str] = Option.Nothing
    caption_entities: Option[list["MessageEntity"]] = Option.Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Option.Nothing
    input_message_content: Option["InputMessageContent"] = Option.Nothing


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

    message_text: Option[str] = Option.Nothing
    parse_mode: Option[str] = Option.Nothing
    entities: Option[list["MessageEntity"]] = Option.Nothing
    disable_web_page_preview: Option[bool] = Option.Nothing
    latitude: Option[float] = Option.Nothing
    longitude: Option[float] = Option.Nothing
    horizontal_accuracy: Option[float] = Option.Nothing
    live_period: Option[int] = Option.Nothing
    heading: Option[int] = Option.Nothing
    proximity_alert_radius: Option[int] = Option.Nothing
    title: Option[str] = Option.Nothing
    address: Option[str] = Option.Nothing
    foursquare_id: Option[str] = Option.Nothing
    foursquare_type: Option[str] = Option.Nothing
    google_place_id: Option[str] = Option.Nothing
    google_place_type: Option[str] = Option.Nothing
    phone_number: Option[str] = Option.Nothing
    first_name: Option[str] = Option.Nothing
    last_name: Option[str] = Option.Nothing
    vcard: Option[str] = Option.Nothing
    description: Option[str] = Option.Nothing
    payload: Option[str] = Option.Nothing
    provider_token: Option[str] = Option.Nothing
    currency: Option[str] = Option.Nothing
    prices: Option[list["LabeledPrice"]] = Option.Nothing
    max_tip_amount: Option[int] = Option(0)
    suggested_tip_amounts: Option[list[int]] = Option.Nothing
    provider_data: Option[str] = Option.Nothing
    photo_url: Option[str] = Option.Nothing
    photo_size: Option[int] = Option.Nothing
    photo_width: Option[int] = Option.Nothing
    photo_height: Option[int] = Option.Nothing
    need_name: Option[bool] = Option.Nothing
    need_phone_number: Option[bool] = Option.Nothing
    need_email: Option[bool] = Option.Nothing
    need_shipping_address: Option[bool] = Option.Nothing
    send_phone_number_to_provider: Option[bool] = Option.Nothing
    send_email_to_provider: Option[bool] = Option.Nothing
    is_flexible: Option[bool] = Option.Nothing


class InputTextMessageContent(Model):
    """Represents the [content](https://core.telegram.org/bots/api/#inputmessagecontent)
    of a text message to be sent as the result of an inline query.
    Docs: https://core.telegram.org/bots/api/#inputtextmessagecontent"""

    message_text: str
    parse_mode: Option[str] = Option.Nothing
    entities: Option[list["MessageEntity"]] = Option.Nothing
    disable_web_page_preview: Option[bool] = Option.Nothing


class InputLocationMessageContent(Model):
    """Represents the [content](https://core.telegram.org/bots/api/#inputmessagecontent)
    of a location message to be sent as the result of an inline query.
    Docs: https://core.telegram.org/bots/api/#inputlocationmessagecontent"""

    latitude: float
    longitude: float
    horizontal_accuracy: Option[float] = Option.Nothing
    live_period: Option[int] = Option.Nothing
    heading: Option[int] = Option.Nothing
    proximity_alert_radius: Option[int] = Option.Nothing


class InputVenueMessageContent(Model):
    """Represents the [content](https://core.telegram.org/bots/api/#inputmessagecontent)
    of a venue message to be sent as the result of an inline query.
    Docs: https://core.telegram.org/bots/api/#inputvenuemessagecontent"""

    latitude: float
    longitude: float
    title: str
    address: str
    foursquare_id: Option[str] = Option.Nothing
    foursquare_type: Option[str] = Option.Nothing
    google_place_id: Option[str] = Option.Nothing
    google_place_type: Option[str] = Option.Nothing


class InputContactMessageContent(Model):
    """Represents the [content](https://core.telegram.org/bots/api/#inputmessagecontent)
    of a contact message to be sent as the result of an inline query.
    Docs: https://core.telegram.org/bots/api/#inputcontactmessagecontent"""

    phone_number: str
    first_name: str
    last_name: Option[str] = Option.Nothing
    vcard: Option[str] = Option.Nothing


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
    max_tip_amount: Option[int] = Option(0)
    suggested_tip_amounts: Option[list[int]] = Option.Nothing
    provider_data: Option[str] = Option.Nothing
    photo_url: Option[str] = Option.Nothing
    photo_size: Option[int] = Option.Nothing
    photo_width: Option[int] = Option.Nothing
    photo_height: Option[int] = Option.Nothing
    need_name: Option[bool] = Option.Nothing
    need_phone_number: Option[bool] = Option.Nothing
    need_email: Option[bool] = Option.Nothing
    need_shipping_address: Option[bool] = Option.Nothing
    send_phone_number_to_provider: Option[bool] = Option.Nothing
    send_email_to_provider: Option[bool] = Option.Nothing
    is_flexible: Option[bool] = Option.Nothing


class ChosenInlineResult(Model):
    """Represents a [result](https://core.telegram.org/bots/api/#inlinequeryresult)
    of an inline query that was chosen by the user and sent to their chat partner.

    Docs: https://core.telegram.org/bots/api/#choseninlineresult"""

    result_id: str
    from_: "User"
    query: str
    location: Option["Location"] = Option.Nothing
    inline_message_id: Option[str] = Option.Nothing


class SentWebAppMessage(Model):
    """Describes an inline message sent by a [Web App](https://core.telegram.org/bots/webapps)
    on behalf of a user.
    Docs: https://core.telegram.org/bots/api/#sentwebappmessage"""

    inline_message_id: Option[str] = Option.Nothing


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

    name: Option[str] = Option.Nothing
    phone_number: Option[str] = Option.Nothing
    email: Option[str] = Option.Nothing
    shipping_address: Option["ShippingAddress"] = Option.Nothing


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
    telegram_payment_charge_id: str
    provider_payment_charge_id: str
    shipping_option_id: Option[str] = Option.Nothing
    order_info: Option["OrderInfo"] = Option.Nothing


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
    shipping_option_id: Option[str] = Option.Nothing
    order_info: Option["OrderInfo"] = Option.Nothing


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

    type: EncryptedPassportElementType
    hash: str
    data: Option[str] = Option.Nothing
    phone_number: Option[str] = Option.Nothing
    email: Option[str] = Option.Nothing
    files: Option[list["PassportFile"]] = Option.Nothing
    front_side: Option["PassportFile"] = Option.Nothing
    reverse_side: Option["PassportFile"] = Option.Nothing
    selfie: Option["PassportFile"] = Option.Nothing
    translation: Option[list["PassportFile"]] = Option.Nothing


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

    source: Option[str] = Option("unspecified")
    type: Option[str] = Option.Nothing
    field_name: Option[str] = Option.Nothing
    data_hash: Option[str] = Option.Nothing
    message: Option[str] = Option.Nothing
    file_hash: Option[str] = Option.Nothing
    file_hashes: Option[list[str]] = Option.Nothing
    element_hash: Option[str] = Option.Nothing


class PassportElementErrorDataField(Model):
    """Represents an issue in one of the data fields that was provided by the user.
    The error is considered resolved when the field's value changes.
    Docs: https://core.telegram.org/bots/api/#passportelementerrordatafield"""

    source: str
    type: PassportElementErrorDataFieldType
    field_name: str
    data_hash: str
    message: str


class PassportElementErrorFrontSide(Model):
    """Represents an issue with the front side of a document. The error is considered
    resolved when the file with the front side of the document changes.
    Docs: https://core.telegram.org/bots/api/#passportelementerrorfrontside"""

    source: str
    type: PassportElementErrorFrontSideType
    file_hash: str
    message: str


class PassportElementErrorReverseSide(Model):
    """Represents an issue with the reverse side of a document. The error is considered
    resolved when the file with reverse side of the document changes.
    Docs: https://core.telegram.org/bots/api/#passportelementerrorreverseside"""

    source: str
    type: PassportElementErrorReverseSideType
    file_hash: str
    message: str


class PassportElementErrorSelfie(Model):
    """Represents an issue with the selfie with a document. The error is considered
    resolved when the file with the selfie changes.
    Docs: https://core.telegram.org/bots/api/#passportelementerrorselfie"""

    source: str
    type: PassportElementErrorSelfieType
    file_hash: str
    message: str


class PassportElementErrorFile(Model):
    """Represents an issue with a document scan. The error is considered resolved
    when the file with the document scan changes.
    Docs: https://core.telegram.org/bots/api/#passportelementerrorfile"""

    source: str
    type: PassportElementErrorFileType
    file_hash: str
    message: str


class PassportElementErrorFiles(Model):
    """Represents an issue with a list of scans. The error is considered resolved
    when the list of files containing the scans changes.
    Docs: https://core.telegram.org/bots/api/#passportelementerrorfiles"""

    source: str
    type: PassportElementErrorFilesType
    file_hashes: list[str]
    message: str


class PassportElementErrorTranslationFile(Model):
    """Represents an issue with one of the files that constitute the translation
    of a document. The error is considered resolved when the file changes.
    Docs: https://core.telegram.org/bots/api/#passportelementerrortranslationfile"""

    source: str
    type: PassportElementErrorTranslationFileType
    file_hash: str
    message: str


class PassportElementErrorTranslationFiles(Model):
    """Represents an issue with the translated version of a document. The error
    is considered resolved when a file with the document translation change.

    Docs: https://core.telegram.org/bots/api/#passportelementerrortranslationfiles"""

    source: str
    type: PassportElementErrorTranslationFilesType
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
    text: Option[str] = Option.Nothing
    text_entities: Option[list["MessageEntity"]] = Option.Nothing
    animation: Option["Animation"] = Option.Nothing


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
