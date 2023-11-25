import typing

from telegrinder.model import *
from telegrinder.option import Nothing, Some
from telegrinder.option.msgspec_option import Option
from telegrinder.types.enums import *


class Error(Model):
    ok: bool
    error_code: int
    description: str
    parameters: Option["ResponseParameters"] = Nothing


class Update(Model):
    """This [object](https://core.telegram.org/bots/api/#available-types)
    represents an incoming update.
    At most **one** of the optional parameters
    can be present in any given update.
    Docs: https://core.telegram.org/bots/api/#update"""

    update_id: int
    message: Option["Message"] = Nothing
    edited_message: Option["Message"] = Nothing
    channel_post: Option["Message"] = Nothing
    edited_channel_post: Option["Message"] = Nothing
    inline_query: Option["InlineQuery"] = Nothing
    chosen_inline_result: Option["ChosenInlineResult"] = Nothing
    callback_query: Option["CallbackQuery"] = Nothing
    shipping_query: Option["ShippingQuery"] = Nothing
    pre_checkout_query: Option["PreCheckoutQuery"] = Nothing
    poll: Option["Poll"] = Nothing
    poll_answer: Option["PollAnswer"] = Nothing
    my_chat_member: Option["ChatMemberUpdated"] = Nothing
    chat_member: Option["ChatMemberUpdated"] = Nothing
    chat_join_request: Option["ChatJoinRequest"] = Nothing


class WebhookInfo(Model):
    """Describes the current status of a webhook.
    Docs: https://core.telegram.org/bots/api/#webhookinfo"""

    url: str
    has_custom_certificate: bool
    pending_update_count: int
    ip_address: Option[str] = Nothing
    last_error_date: Option[int] = Nothing
    last_error_message: Option[str] = Nothing
    last_synchronization_error_date: Option[int] = Nothing
    max_connections: Option[int] = Nothing
    allowed_updates: Option[list[str]] = Nothing


class User(Model):
    """This object represents a Telegram user or bot.
    Docs: https://core.telegram.org/bots/api/#user"""

    id: int
    is_bot: bool
    first_name: str
    last_name: Option[str] = Nothing
    username: Option[str] = Nothing
    language_code: Option[str] = Nothing
    is_premium: Option[bool] = Nothing
    added_to_attachment_menu: Option[bool] = Nothing
    can_join_groups: Option[bool] = Nothing
    can_read_all_group_messages: Option[bool] = Nothing
    supports_inline_queries: Option[bool] = Nothing

    @property
    def full_name(self) -> str:
        return self.first_name + self.last_name.map(lambda v: " " + v).unwrap_or("")


class Chat(Model):
    """This object represents a chat.
    Docs: https://core.telegram.org/bots/api/#chat"""

    id: int
    type: ChatType
    title: Option[str] = Nothing
    username: Option[str] = Nothing
    first_name: Option[str] = Nothing
    last_name: Option[str] = Nothing
    is_forum: Option[bool] = Nothing
    photo: Option["ChatPhoto"] = Nothing
    active_usernames: Option[list[str]] = Nothing
    emoji_status_custom_emoji_id: Option[str] = Nothing
    emoji_status_expiration_date: Option[int] = Nothing
    bio: Option[str] = Nothing
    has_private_forwards: Option[bool] = Nothing
    has_restricted_voice_and_video_messages: Option[bool] = Nothing
    join_to_send_messages: Option[bool] = Nothing
    join_by_request: Option[bool] = Nothing
    description: Option[str] = Nothing
    invite_link: Option[str] = Nothing
    pinned_message: Option["Message"] = Nothing
    permissions: Option["ChatPermissions"] = Nothing
    slow_mode_delay: Option[int] = Nothing
    message_auto_delete_time: Option[int] = Nothing
    has_aggressive_anti_spam_enabled: Option[bool] = Nothing
    has_hidden_members: Option[bool] = Nothing
    has_protected_content: Option[bool] = Nothing
    sticker_set_name: Option[str] = Nothing
    can_set_sticker_set: Option[bool] = Nothing
    linked_chat_id: Option[int] = Nothing
    location: Option["ChatLocation"] = Nothing


class Message(Model):
    """This object represents a message.
    Docs: https://core.telegram.org/bots/api/#message"""

    message_id: int
    date: int
    chat: "Chat"
    message_thread_id: Option[int] = Nothing
    from_: Option["User"] = Nothing
    sender_chat: Option["Chat"] = Nothing
    forward_from: Option["User"] = Nothing
    forward_from_chat: Option["Chat"] = Nothing
    forward_from_message_id: Option[int] = Nothing
    forward_signature: Option[str] = Nothing
    forward_sender_name: Option[str] = Nothing
    forward_date: Option[int] = Nothing
    is_topic_message: Option[bool] = Nothing
    is_automatic_forward: Option[bool] = Nothing
    reply_to_message: Option["Message"] = Nothing
    via_bot: Option["User"] = Nothing
    edit_date: Option[int] = Nothing
    has_protected_content: Option[bool] = Nothing
    media_group_id: Option[str] = Nothing
    author_signature: Option[str] = Nothing
    text: Option[str] = Nothing
    entities: Option[list["MessageEntity"]] = Nothing
    animation: Option["Animation"] = Nothing
    audio: Option["Audio"] = Nothing
    document: Option["Document"] = Nothing
    photo: Option[list["PhotoSize"]] = Nothing
    sticker: Option["Sticker"] = Nothing
    story: Option["Story"] = Nothing
    video: Option["Video"] = Nothing
    video_note: Option["VideoNote"] = Nothing
    voice: Option["Voice"] = Nothing
    caption: Option[str] = Nothing
    caption_entities: Option[list["MessageEntity"]] = Nothing
    has_media_spoiler: Option[bool] = Nothing
    contact: Option["Contact"] = Nothing
    dice: Option["Dice"] = Nothing
    game: Option["Game"] = Nothing
    poll: Option["Poll"] = Nothing
    venue: Option["Venue"] = Nothing
    location: Option["Location"] = Nothing
    new_chat_members: Option[list["User"]] = Nothing
    left_chat_member: Option["User"] = Nothing
    new_chat_title: Option[str] = Nothing
    new_chat_photo: Option[list["PhotoSize"]] = Nothing
    delete_chat_photo: Option[bool] = Nothing
    group_chat_created: Option[bool] = Nothing
    supergroup_chat_created: Option[bool] = Nothing
    channel_chat_created: Option[bool] = Nothing
    message_auto_delete_timer_changed: Option["MessageAutoDeleteTimerChanged"] = Nothing
    migrate_to_chat_id: Option[int] = Nothing
    migrate_from_chat_id: Option[int] = Nothing
    pinned_message: Option["Message"] = Nothing
    invoice: Option["Invoice"] = Nothing
    successful_payment: Option["SuccessfulPayment"] = Nothing
    user_shared: Option["UserShared"] = Nothing
    chat_shared: Option["ChatShared"] = Nothing
    connected_website: Option[str] = Nothing
    write_access_allowed: Option["WriteAccessAllowed"] = Nothing
    passport_data: Option["PassportData"] = Nothing
    proximity_alert_triggered: Option["ProximityAlertTriggered"] = Nothing
    forum_topic_created: Option["ForumTopicCreated"] = Nothing
    forum_topic_edited: Option["ForumTopicEdited"] = Nothing
    forum_topic_closed: Option["ForumTopicClosed"] = Nothing
    forum_topic_reopened: Option["ForumTopicReopened"] = Nothing
    general_forum_topic_hidden: Option["GeneralForumTopicHidden"] = Nothing
    general_forum_topic_unhidden: Option["GeneralForumTopicUnhidden"] = Nothing
    video_chat_scheduled: Option["VideoChatScheduled"] = Nothing
    video_chat_started: Option["VideoChatStarted"] = Nothing
    video_chat_ended: Option["VideoChatEnded"] = Nothing
    video_chat_participants_invited: Option["VideoChatParticipantsInvited"] = Nothing
    web_app_data: Option["WebAppData"] = Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Nothing

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
    url: Option[str] = Nothing
    user: Option["User"] = Nothing
    language: Option[str] = Nothing
    custom_emoji_id: Option[str] = Nothing


class PhotoSize(Model):
    """This object represents one size of a photo or a [file](https://core.telegram.org/bots/api/#document)
    / [sticker](https://core.telegram.org/bots/api/#sticker) thumbnail.

    Docs: https://core.telegram.org/bots/api/#photosize"""

    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: Option[int] = Nothing


class Animation(Model):
    """This object represents an animation file (GIF or H.264/MPEG-4 AVC video
    without sound).
    Docs: https://core.telegram.org/bots/api/#animation"""

    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumbnail: Option["PhotoSize"] = Nothing
    file_name: Option[str] = Nothing
    mime_type: Option[str] = Nothing
    file_size: Option[int] = Nothing


class Audio(Model):
    """This object represents an audio file to be treated as music by the Telegram
    clients.
    Docs: https://core.telegram.org/bots/api/#audio"""

    file_id: str
    file_unique_id: str
    duration: int
    performer: Option[str] = Nothing
    title: Option[str] = Nothing
    file_name: Option[str] = Nothing
    mime_type: Option[str] = Nothing
    file_size: Option[int] = Nothing
    thumbnail: Option["PhotoSize"] = Nothing


class Document(Model):
    """This object represents a general file (as opposed to [photos](https://core.telegram.org/bots/api/#photosize),
    [voice messages](https://core.telegram.org/bots/api/#voice) and
    [audio files](https://core.telegram.org/bots/api/#audio)).
    Docs: https://core.telegram.org/bots/api/#document"""

    file_id: str
    file_unique_id: str
    thumbnail: Option["PhotoSize"] = Nothing
    file_name: Option[str] = Nothing
    mime_type: Option[str] = Nothing
    file_size: Option[int] = Nothing


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
    thumbnail: Option["PhotoSize"] = Nothing
    file_name: Option[str] = Nothing
    mime_type: Option[str] = Nothing
    file_size: Option[int] = Nothing


class VideoNote(Model):
    """This object represents a [video message](https://telegram.org/blog/video-messages-and-telescope)
    (available in Telegram apps as of [v.4.0](https://telegram.org/blog/video-messages-and-telescope)).

    Docs: https://core.telegram.org/bots/api/#videonote"""

    file_id: str
    file_unique_id: str
    length: int
    duration: int
    thumbnail: Option["PhotoSize"] = Nothing
    file_size: Option[int] = Nothing


class Voice(Model):
    """This object represents a voice note.
    Docs: https://core.telegram.org/bots/api/#voice"""

    file_id: str
    file_unique_id: str
    duration: int
    mime_type: Option[str] = Nothing
    file_size: Option[int] = Nothing


class Contact(Model):
    """This object represents a phone contact.
    Docs: https://core.telegram.org/bots/api/#contact"""

    phone_number: str
    first_name: str
    last_name: Option[str] = Nothing
    user_id: Option[int] = Nothing
    vcard: Option[str] = Nothing


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
    voter_chat: Option["Chat"] = Nothing
    user: Option["User"] = Nothing


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
    correct_option_id: Option[int] = Nothing
    explanation: Option[str] = Nothing
    explanation_entities: Option[list["MessageEntity"]] = Nothing
    open_period: Option[int] = Nothing
    close_date: Option[int] = Nothing


class Location(Model):
    """This object represents a point on the map.
    Docs: https://core.telegram.org/bots/api/#location"""

    longitude: float
    latitude: float
    horizontal_accuracy: Option[float] = Nothing
    live_period: Option[int] = Nothing
    heading: Option[int] = Nothing
    proximity_alert_radius: Option[int] = Nothing


class Venue(Model):
    """This object represents a venue.
    Docs: https://core.telegram.org/bots/api/#venue"""

    location: "Location"
    title: str
    address: str
    foursquare_id: Option[str] = Nothing
    foursquare_type: Option[str] = Nothing
    google_place_id: Option[str] = Nothing
    google_place_type: Option[str] = Nothing


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
    icon_custom_emoji_id: Option[str] = Nothing


class ForumTopicClosed(Model):
    """This object represents a service message about a forum topic closed in the
    chat. Currently holds no information.
    Docs: https://core.telegram.org/bots/api/#forumtopicclosed"""

    pass


class ForumTopicEdited(Model):
    """This object represents a service message about an edited forum topic.
    Docs: https://core.telegram.org/bots/api/#forumtopicedited"""

    name: Option[str] = Nothing
    icon_custom_emoji_id: Option[str] = Nothing


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

    from_request: Option[bool] = Nothing
    web_app_name: Option[str] = Nothing
    from_attachment_menu: Option[bool] = Nothing


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
    file_size: Option[int] = Nothing
    file_path: Option[str] = Nothing


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
    is_persistent: Option[bool] = Some(False)
    resize_keyboard: Option[bool] = Some(False)
    one_time_keyboard: Option[bool] = Some(False)
    input_field_placeholder: Option[str] = Nothing
    selective: Option[bool] = Nothing


class KeyboardButton(Model):
    """This object represents one button of the reply keyboard. For simple text
    buttons, *String* can be used instead of this object to specify the button
    text. The optional fields *web_app*, *request_user*, *request_chat*,
    *request_contact*, *request_location*, and *request_poll* are
    mutually exclusive.
    Docs: https://core.telegram.org/bots/api/#keyboardbutton"""

    text: str
    request_user: Option["KeyboardButtonRequestUser"] = Nothing
    request_chat: Option["KeyboardButtonRequestChat"] = Nothing
    request_contact: Option[bool] = Nothing
    request_location: Option[bool] = Nothing
    request_poll: Option["KeyboardButtonPollType"] = Nothing
    web_app: Option["WebAppInfo"] = Nothing


class KeyboardButtonRequestUser(Model):
    """This object defines the criteria used to request a suitable user. The identifier
    of the selected user will be shared with the bot when the corresponding button
    is pressed. [More about requesting users »](https://core.telegram.org/bots/features#chat-and-user-selection)

    Docs: https://core.telegram.org/bots/api/#keyboardbuttonrequestuser"""

    request_id: int
    user_is_bot: Option[bool] = Nothing
    user_is_premium: Option[bool] = Nothing


class KeyboardButtonRequestChat(Model):
    """This object defines the criteria used to request a suitable chat. The identifier
    of the selected chat will be shared with the bot when the corresponding button
    is pressed. [More about requesting chats »](https://core.telegram.org/bots/features#chat-and-user-selection)

    Docs: https://core.telegram.org/bots/api/#keyboardbuttonrequestchat"""

    request_id: int
    chat_is_channel: bool
    chat_is_forum: Option[bool] = Nothing
    chat_has_username: Option[bool] = Nothing
    chat_is_created: Option[bool] = Nothing
    user_administrator_rights: Option["ChatAdministratorRights"] = Nothing
    bot_administrator_rights: Option["ChatAdministratorRights"] = Nothing
    bot_is_member: Option[bool] = Nothing


class KeyboardButtonPollType(Model):
    """This object represents type of a poll, which is allowed to be created and
    sent when the corresponding button is pressed.
    Docs: https://core.telegram.org/bots/api/#keyboardbuttonpolltype"""

    type: Option[str] = Nothing


class ReplyKeyboardRemove(Model):
    """Upon receiving a message with this object, Telegram clients will remove
    the current custom keyboard and display the default letter-keyboard.
    By default, custom keyboards are displayed until a new keyboard is sent
    by a bot. An exception is made for one-time keyboards that are hidden immediately
    after the user presses a button (see [ReplyKeyboardMarkup](https://core.telegram.org/bots/api/#replykeyboardmarkup)).

    Docs: https://core.telegram.org/bots/api/#replykeyboardremove"""

    remove_keyboard: bool
    selective: Option[bool] = Nothing


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
    url: Option[str] = Nothing
    callback_data: Option[str] = Nothing
    web_app: Option["WebAppInfo"] = Nothing
    login_url: Option["LoginUrl"] = Nothing
    switch_inline_query: Option[str] = Nothing
    switch_inline_query_current_chat: Option[str] = Nothing
    switch_inline_query_chosen_chat: Option["SwitchInlineQueryChosenChat"] = Nothing
    callback_game: Option["CallbackGame"] = Nothing
    pay: Option[bool] = Nothing


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
    forward_text: Option[str] = Nothing
    bot_username: Option[str] = Nothing
    request_write_access: Option[bool] = Nothing


class SwitchInlineQueryChosenChat(Model):
    """This object represents an inline button that switches the current user
    to inline mode in a chosen chat, with an optional default inline query.
    Docs: https://core.telegram.org/bots/api/#switchinlinequerychosenchat"""

    query: Option[str] = Nothing
    allow_user_chats: Option[bool] = Nothing
    allow_bot_chats: Option[bool] = Nothing
    allow_group_chats: Option[bool] = Nothing
    allow_channel_chats: Option[bool] = Nothing


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
    message: Option["Message"] = Nothing
    inline_message_id: Option[str] = Nothing
    data: Option[str] = Nothing
    game_short_name: Option[str] = Nothing


class ForceReply(Model):
    """Upon receiving a message with this object, Telegram clients will display
    a reply interface to the user (act as if the user has selected the bot's message
    and tapped 'Reply'). This can be extremely useful if you want to create user-friendly
    step-by-step interfaces without having to sacrifice [privacy mode](https://core.telegram.org/bots/features#privacy-mode).

    Docs: https://core.telegram.org/bots/api/#forcereply"""

    force_reply: bool
    input_field_placeholder: Option[str] = Nothing
    selective: Option[bool] = Nothing


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
    name: Option[str] = Nothing
    expire_date: Option[int] = Nothing
    member_limit: Option[int] = Nothing
    pending_join_request_count: Option[int] = Nothing


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
    can_post_messages: Option[bool] = Nothing
    can_edit_messages: Option[bool] = Nothing
    can_pin_messages: Option[bool] = Nothing
    can_post_stories: Option[bool] = Nothing
    can_edit_stories: Option[bool] = Nothing
    can_delete_stories: Option[bool] = Nothing
    can_manage_topics: Option[bool] = Nothing


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

    status: Option[str] = Some("kicked")
    user: Option["User"] = Nothing
    is_anonymous: Option[bool] = Nothing
    custom_title: Option[str] = Nothing
    can_be_edited: Option[bool] = Nothing
    can_manage_chat: Option[bool] = Nothing
    can_delete_messages: Option[bool] = Nothing
    can_manage_video_chats: Option[bool] = Nothing
    can_restrict_members: Option[bool] = Nothing
    can_promote_members: Option[bool] = Nothing
    can_change_info: Option[bool] = Nothing
    can_invite_users: Option[bool] = Nothing
    can_post_messages: Option[bool] = Nothing
    can_edit_messages: Option[bool] = Nothing
    can_pin_messages: Option[bool] = Nothing
    can_post_stories: Option[bool] = Nothing
    can_edit_stories: Option[bool] = Nothing
    can_delete_stories: Option[bool] = Nothing
    can_manage_topics: Option[bool] = Nothing
    is_member: Option[bool] = Nothing
    can_send_messages: Option[bool] = Nothing
    can_send_audios: Option[bool] = Nothing
    can_send_documents: Option[bool] = Nothing
    can_send_photos: Option[bool] = Nothing
    can_send_videos: Option[bool] = Nothing
    can_send_video_notes: Option[bool] = Nothing
    can_send_voice_notes: Option[bool] = Nothing
    can_send_polls: Option[bool] = Nothing
    can_send_other_messages: Option[bool] = Nothing
    can_add_web_page_previews: Option[bool] = Nothing
    until_date: Option[int] = Nothing


class ChatMemberOwner(Model):
    """Represents a [chat member](https://core.telegram.org/bots/api/#chatmember)
    that owns the chat and has all administrator privileges.
    Docs: https://core.telegram.org/bots/api/#chatmemberowner"""

    status: str
    user: "User"
    is_anonymous: bool
    custom_title: Option[str] = Nothing


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
    can_post_messages: Option[bool] = Nothing
    can_edit_messages: Option[bool] = Nothing
    can_pin_messages: Option[bool] = Nothing
    can_post_stories: Option[bool] = Nothing
    can_edit_stories: Option[bool] = Nothing
    can_delete_stories: Option[bool] = Nothing
    can_manage_topics: Option[bool] = Nothing
    custom_title: Option[str] = Nothing


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
    invite_link: Option["ChatInviteLink"] = Nothing
    via_chat_folder_invite_link: Option[bool] = Nothing


class ChatJoinRequest(Model):
    """Represents a join request sent to a chat.
    Docs: https://core.telegram.org/bots/api/#chatjoinrequest"""

    chat: "Chat"
    from_: "User"
    user_chat_id: int
    date: int
    bio: Option[str] = Nothing
    invite_link: Option["ChatInviteLink"] = Nothing


class ChatPermissions(Model):
    """Describes actions that a non-administrator user is allowed to take in a
    chat.
    Docs: https://core.telegram.org/bots/api/#chatpermissions"""

    can_send_messages: Option[bool] = Nothing
    can_send_audios: Option[bool] = Nothing
    can_send_documents: Option[bool] = Nothing
    can_send_photos: Option[bool] = Nothing
    can_send_videos: Option[bool] = Nothing
    can_send_video_notes: Option[bool] = Nothing
    can_send_voice_notes: Option[bool] = Nothing
    can_send_polls: Option[bool] = Nothing
    can_send_other_messages: Option[bool] = Nothing
    can_add_web_page_previews: Option[bool] = Nothing
    can_change_info: Option[bool] = Nothing
    can_invite_users: Option[bool] = Nothing
    can_pin_messages: Option[bool] = Nothing
    can_manage_topics: Option[bool] = Nothing


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
    icon_custom_emoji_id: Option[str] = Nothing


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

    type: Option[str] = Some("chat_member")
    chat_id: Option[typing.Union[int, str]] = Nothing
    user_id: Option[int] = Nothing


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

    type: Option[str] = Some("default")
    text: Option[str] = Nothing
    web_app: Option["WebAppInfo"] = Nothing


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

    migrate_to_chat_id: Option[int] = Nothing
    retry_after: Option[int] = Nothing


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

    type: Option[str] = Some("video")
    media: Option[str] = Nothing
    thumbnail: Option[typing.Union["InputFile", str]] = Nothing
    caption: Option[str] = Nothing
    parse_mode: Option[str] = Nothing
    caption_entities: Option[list["MessageEntity"]] = Nothing
    width: Option[int] = Nothing
    height: Option[int] = Nothing
    duration: Option[int] = Nothing
    has_spoiler: Option[bool] = Nothing
    disable_content_type_detection: Option[bool] = Nothing
    performer: Option[str] = Nothing
    title: Option[str] = Nothing
    supports_streaming: Option[bool] = Nothing


class InputMediaPhoto(Model):
    """Represents a photo to be sent.
    Docs: https://core.telegram.org/bots/api/#inputmediaphoto"""

    type: str
    media: str
    caption: Option[str] = Nothing
    parse_mode: Option[str] = Nothing
    caption_entities: Option[list["MessageEntity"]] = Nothing
    has_spoiler: Option[bool] = Nothing


class InputMediaVideo(Model):
    """Represents a video to be sent.
    Docs: https://core.telegram.org/bots/api/#inputmediavideo"""

    type: str
    media: str
    thumbnail: Option[typing.Union["InputFile", str]] = Nothing
    caption: Option[str] = Nothing
    parse_mode: Option[str] = Nothing
    caption_entities: Option[list["MessageEntity"]] = Nothing
    width: Option[int] = Nothing
    height: Option[int] = Nothing
    duration: Option[int] = Nothing
    supports_streaming: Option[bool] = Nothing
    has_spoiler: Option[bool] = Nothing


class InputMediaAnimation(Model):
    """Represents an animation file (GIF or H.264/MPEG-4 AVC video without sound)
    to be sent.
    Docs: https://core.telegram.org/bots/api/#inputmediaanimation"""

    type: str
    media: str
    thumbnail: Option[typing.Union["InputFile", str]] = Nothing
    caption: Option[str] = Nothing
    parse_mode: Option[str] = Nothing
    caption_entities: Option[list["MessageEntity"]] = Nothing
    width: Option[int] = Nothing
    height: Option[int] = Nothing
    duration: Option[int] = Nothing
    has_spoiler: Option[bool] = Nothing


class InputMediaAudio(Model):
    """Represents an audio file to be treated as music to be sent.
    Docs: https://core.telegram.org/bots/api/#inputmediaaudio"""

    type: str
    media: str
    thumbnail: Option[typing.Union["InputFile", str]] = Nothing
    caption: Option[str] = Nothing
    parse_mode: Option[str] = Nothing
    caption_entities: Option[list["MessageEntity"]] = Nothing
    duration: Option[int] = Nothing
    performer: Option[str] = Nothing
    title: Option[str] = Nothing


class InputMediaDocument(Model):
    """Represents a general file to be sent.
    Docs: https://core.telegram.org/bots/api/#inputmediadocument"""

    type: str
    media: str
    thumbnail: Option[typing.Union["InputFile", str]] = Nothing
    caption: Option[str] = Nothing
    parse_mode: Option[str] = Nothing
    caption_entities: Option[list["MessageEntity"]] = Nothing
    disable_content_type_detection: Option[bool] = Nothing


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
    thumbnail: Option["PhotoSize"] = Nothing
    emoji: Option[str] = Nothing
    set_name: Option[str] = Nothing
    premium_animation: Option["File"] = Nothing
    mask_position: Option["MaskPosition"] = Nothing
    custom_emoji_id: Option[str] = Nothing
    needs_repainting: Option[bool] = Nothing
    file_size: Option[int] = Nothing


class StickerSet(Model):
    """This object represents a sticker set.
    Docs: https://core.telegram.org/bots/api/#stickerset"""

    name: str
    title: str
    sticker_type: StickerSetStickerType
    is_animated: bool
    is_video: bool
    stickers: list["Sticker"]
    thumbnail: Option["PhotoSize"] = Nothing


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
    mask_position: Option["MaskPosition"] = Nothing
    keywords: Option[list[str]] = Nothing


class InlineQuery(Model):
    """This object represents an incoming inline query. When the user sends an
    empty query, your bot could return some default or trending results.
    Docs: https://core.telegram.org/bots/api/#inlinequery"""

    id: str
    from_: "User"
    query: str
    offset: str
    chat_type: Option[InlineQueryChatType] = Nothing
    location: Option["Location"] = Nothing


class InlineQueryResultsButton(Model):
    """This object represents a button to be shown above inline query results.
    You **must** use exactly one of the optional fields.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultsbutton"""

    text: str
    web_app: Option["WebAppInfo"] = Nothing
    start_parameter: Option[str] = Nothing


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

    type: Option[str] = Some("voice")
    id: Option[str] = Nothing
    audio_file_id: Option[str] = Nothing
    caption: Option[str] = Nothing
    parse_mode: Option[str] = Nothing
    caption_entities: Option[list["MessageEntity"]] = Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    input_message_content: Option["InputMessageContent"] = Nothing
    title: Option[str] = Nothing
    document_file_id: Option[str] = Nothing
    description: Option[str] = Nothing
    gif_file_id: Option[str] = Nothing
    mpeg4_file_id: Option[str] = Nothing
    photo_file_id: Option[str] = Nothing
    sticker_file_id: Option[str] = Nothing
    video_file_id: Option[str] = Nothing
    voice_file_id: Option[str] = Nothing
    url: Option[str] = Nothing
    hide_url: Option[bool] = Nothing
    thumbnail_url: Option[str] = Nothing
    thumbnail_width: Option[int] = Nothing
    thumbnail_height: Option[int] = Nothing
    audio_url: Option[str] = Nothing
    performer: Option[str] = Nothing
    audio_duration: Option[int] = Nothing
    phone_number: Option[str] = Nothing
    first_name: Option[str] = Nothing
    last_name: Option[str] = Nothing
    vcard: Option[str] = Nothing
    game_short_name: Option[str] = Nothing
    document_url: Option[str] = Nothing
    mime_type: Option[InlineQueryResultMimeType] = Nothing
    gif_url: Option[str] = Nothing
    gif_width: Option[int] = Nothing
    gif_height: Option[int] = Nothing
    gif_duration: Option[int] = Nothing
    thumbnail_mime_type: Option[InlineQueryResultThumbnailMimeType] = Some(
        InlineQueryResultThumbnailMimeType("image/jpeg")
    )
    latitude: Option[float] = Nothing
    longitude: Option[float] = Nothing
    horizontal_accuracy: Option[float] = Nothing
    live_period: Option[int] = Nothing
    heading: Option[int] = Nothing
    proximity_alert_radius: Option[int] = Nothing
    mpeg4_url: Option[str] = Nothing
    mpeg4_width: Option[int] = Nothing
    mpeg4_height: Option[int] = Nothing
    mpeg4_duration: Option[int] = Nothing
    photo_url: Option[str] = Nothing
    photo_width: Option[int] = Nothing
    photo_height: Option[int] = Nothing
    address: Option[str] = Nothing
    foursquare_id: Option[str] = Nothing
    foursquare_type: Option[str] = Nothing
    google_place_id: Option[str] = Nothing
    google_place_type: Option[str] = Nothing
    video_url: Option[str] = Nothing
    video_width: Option[int] = Nothing
    video_height: Option[int] = Nothing
    video_duration: Option[int] = Nothing
    voice_url: Option[str] = Nothing
    voice_duration: Option[int] = Nothing


class InlineQueryResultArticle(Model):
    """Represents a link to an article or web page.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultarticle"""

    type: str
    id: str
    title: str
    input_message_content: "InputMessageContent"
    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    url: Option[str] = Nothing
    hide_url: Option[bool] = Nothing
    description: Option[str] = Nothing
    thumbnail_url: Option[str] = Nothing
    thumbnail_width: Option[int] = Nothing
    thumbnail_height: Option[int] = Nothing


class InlineQueryResultPhoto(Model):
    """Represents a link to a photo. By default, this photo will be sent by the user
    with optional caption. Alternatively, you can use *input_message_content*
    to send a message with the specified content instead of the photo.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultphoto"""

    type: str
    id: str
    photo_url: str
    thumbnail_url: str
    photo_width: Option[int] = Nothing
    photo_height: Option[int] = Nothing
    title: Option[str] = Nothing
    description: Option[str] = Nothing
    caption: Option[str] = Nothing
    parse_mode: Option[str] = Nothing
    caption_entities: Option[list["MessageEntity"]] = Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    input_message_content: Option["InputMessageContent"] = Nothing


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
    gif_width: Option[int] = Nothing
    gif_height: Option[int] = Nothing
    gif_duration: Option[int] = Nothing
    thumbnail_mime_type: Option[InlineQueryResultGifThumbnailMimeType] = Some(
        InlineQueryResultGifThumbnailMimeType("image/jpeg")
    )
    title: Option[str] = Nothing
    caption: Option[str] = Nothing
    parse_mode: Option[str] = Nothing
    caption_entities: Option[list["MessageEntity"]] = Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    input_message_content: Option["InputMessageContent"] = Nothing


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
    mpeg4_width: Option[int] = Nothing
    mpeg4_height: Option[int] = Nothing
    mpeg4_duration: Option[int] = Nothing
    thumbnail_mime_type: Option[InlineQueryResultMpeg4GifThumbnailMimeType] = Some(
        InlineQueryResultMpeg4GifThumbnailMimeType("image/jpeg")
    )
    title: Option[str] = Nothing
    caption: Option[str] = Nothing
    parse_mode: Option[str] = Nothing
    caption_entities: Option[list["MessageEntity"]] = Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    input_message_content: Option["InputMessageContent"] = Nothing


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
    caption: Option[str] = Nothing
    parse_mode: Option[str] = Nothing
    caption_entities: Option[list["MessageEntity"]] = Nothing
    video_width: Option[int] = Nothing
    video_height: Option[int] = Nothing
    video_duration: Option[int] = Nothing
    description: Option[str] = Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    input_message_content: Option["InputMessageContent"] = Nothing


class InlineQueryResultAudio(Model):
    """Represents a link to an MP3 audio file. By default, this audio file will be
    sent by the user. Alternatively, you can use *input_message_content*
    to send a message with the specified content instead of the audio.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultaudio"""

    type: str
    id: str
    audio_url: str
    title: str
    caption: Option[str] = Nothing
    parse_mode: Option[str] = Nothing
    caption_entities: Option[list["MessageEntity"]] = Nothing
    performer: Option[str] = Nothing
    audio_duration: Option[int] = Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    input_message_content: Option["InputMessageContent"] = Nothing


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
    caption: Option[str] = Nothing
    parse_mode: Option[str] = Nothing
    caption_entities: Option[list["MessageEntity"]] = Nothing
    voice_duration: Option[int] = Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    input_message_content: Option["InputMessageContent"] = Nothing


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
    caption: Option[str] = Nothing
    parse_mode: Option[str] = Nothing
    caption_entities: Option[list["MessageEntity"]] = Nothing
    description: Option[str] = Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    input_message_content: Option["InputMessageContent"] = Nothing
    thumbnail_url: Option[str] = Nothing
    thumbnail_width: Option[int] = Nothing
    thumbnail_height: Option[int] = Nothing


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
    horizontal_accuracy: Option[float] = Nothing
    live_period: Option[int] = Nothing
    heading: Option[int] = Nothing
    proximity_alert_radius: Option[int] = Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    input_message_content: Option["InputMessageContent"] = Nothing
    thumbnail_url: Option[str] = Nothing
    thumbnail_width: Option[int] = Nothing
    thumbnail_height: Option[int] = Nothing


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
    foursquare_id: Option[str] = Nothing
    foursquare_type: Option[str] = Nothing
    google_place_id: Option[str] = Nothing
    google_place_type: Option[str] = Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    input_message_content: Option["InputMessageContent"] = Nothing
    thumbnail_url: Option[str] = Nothing
    thumbnail_width: Option[int] = Nothing
    thumbnail_height: Option[int] = Nothing


class InlineQueryResultContact(Model):
    """Represents a contact with a phone number. By default, this contact will
    be sent by the user. Alternatively, you can use *input_message_content*
    to send a message with the specified content instead of the contact.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultcontact"""

    type: str
    id: str
    phone_number: str
    first_name: str
    last_name: Option[str] = Nothing
    vcard: Option[str] = Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    input_message_content: Option["InputMessageContent"] = Nothing
    thumbnail_url: Option[str] = Nothing
    thumbnail_width: Option[int] = Nothing
    thumbnail_height: Option[int] = Nothing


class InlineQueryResultGame(Model):
    """Represents a [Game](https://core.telegram.org/bots/api/#games).

    Docs: https://core.telegram.org/bots/api/#inlinequeryresultgame"""

    type: str
    id: str
    game_short_name: str
    reply_markup: Option["InlineKeyboardMarkup"] = Nothing


class InlineQueryResultCachedPhoto(Model):
    """Represents a link to a photo stored on the Telegram servers. By default,
    this photo will be sent by the user with an optional caption. Alternatively,
    you can use *input_message_content* to send a message with the specified
    content instead of the photo.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultcachedphoto"""

    type: str
    id: str
    photo_file_id: str
    title: Option[str] = Nothing
    description: Option[str] = Nothing
    caption: Option[str] = Nothing
    parse_mode: Option[str] = Nothing
    caption_entities: Option[list["MessageEntity"]] = Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    input_message_content: Option["InputMessageContent"] = Nothing


class InlineQueryResultCachedGif(Model):
    """Represents a link to an animated GIF file stored on the Telegram servers.
    By default, this animated GIF file will be sent by the user with an optional
    caption. Alternatively, you can use *input_message_content* to send
    a message with specified content instead of the animation.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultcachedgif"""

    type: str
    id: str
    gif_file_id: str
    title: Option[str] = Nothing
    caption: Option[str] = Nothing
    parse_mode: Option[str] = Nothing
    caption_entities: Option[list["MessageEntity"]] = Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    input_message_content: Option["InputMessageContent"] = Nothing


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
    title: Option[str] = Nothing
    caption: Option[str] = Nothing
    parse_mode: Option[str] = Nothing
    caption_entities: Option[list["MessageEntity"]] = Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    input_message_content: Option["InputMessageContent"] = Nothing


class InlineQueryResultCachedSticker(Model):
    """Represents a link to a sticker stored on the Telegram servers. By default,
    this sticker will be sent by the user. Alternatively, you can use *input_message_content*
    to send a message with the specified content instead of the sticker.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultcachedsticker"""

    type: str
    id: str
    sticker_file_id: str
    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    input_message_content: Option["InputMessageContent"] = Nothing


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
    description: Option[str] = Nothing
    caption: Option[str] = Nothing
    parse_mode: Option[str] = Nothing
    caption_entities: Option[list["MessageEntity"]] = Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    input_message_content: Option["InputMessageContent"] = Nothing


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
    description: Option[str] = Nothing
    caption: Option[str] = Nothing
    parse_mode: Option[str] = Nothing
    caption_entities: Option[list["MessageEntity"]] = Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    input_message_content: Option["InputMessageContent"] = Nothing


class InlineQueryResultCachedVoice(Model):
    """Represents a link to a voice message stored on the Telegram servers. By default,
    this voice message will be sent by the user. Alternatively, you can use *input_message_content*
    to send a message with the specified content instead of the voice message.

    Docs: https://core.telegram.org/bots/api/#inlinequeryresultcachedvoice"""

    type: str
    id: str
    voice_file_id: str
    title: str
    caption: Option[str] = Nothing
    parse_mode: Option[str] = Nothing
    caption_entities: Option[list["MessageEntity"]] = Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    input_message_content: Option["InputMessageContent"] = Nothing


class InlineQueryResultCachedAudio(Model):
    """Represents a link to an MP3 audio file stored on the Telegram servers. By
    default, this audio file will be sent by the user. Alternatively, you can
    use *input_message_content* to send a message with the specified content
    instead of the audio.
    Docs: https://core.telegram.org/bots/api/#inlinequeryresultcachedaudio"""

    type: str
    id: str
    audio_file_id: str
    caption: Option[str] = Nothing
    parse_mode: Option[str] = Nothing
    caption_entities: Option[list["MessageEntity"]] = Nothing
    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    input_message_content: Option["InputMessageContent"] = Nothing


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

    message_text: Option[str] = Nothing
    parse_mode: Option[str] = Nothing
    entities: Option[list["MessageEntity"]] = Nothing
    disable_web_page_preview: Option[bool] = Nothing
    latitude: Option[float] = Nothing
    longitude: Option[float] = Nothing
    horizontal_accuracy: Option[float] = Nothing
    live_period: Option[int] = Nothing
    heading: Option[int] = Nothing
    proximity_alert_radius: Option[int] = Nothing
    title: Option[str] = Nothing
    address: Option[str] = Nothing
    foursquare_id: Option[str] = Nothing
    foursquare_type: Option[str] = Nothing
    google_place_id: Option[str] = Nothing
    google_place_type: Option[str] = Nothing
    phone_number: Option[str] = Nothing
    first_name: Option[str] = Nothing
    last_name: Option[str] = Nothing
    vcard: Option[str] = Nothing
    description: Option[str] = Nothing
    payload: Option[str] = Nothing
    provider_token: Option[str] = Nothing
    currency: Option[str] = Nothing
    prices: Option[list["LabeledPrice"]] = Nothing
    max_tip_amount: Option[int] = Some(0)
    suggested_tip_amounts: Option[list[int]] = Nothing
    provider_data: Option[str] = Nothing
    photo_url: Option[str] = Nothing
    photo_size: Option[int] = Nothing
    photo_width: Option[int] = Nothing
    photo_height: Option[int] = Nothing
    need_name: Option[bool] = Nothing
    need_phone_number: Option[bool] = Nothing
    need_email: Option[bool] = Nothing
    need_shipping_address: Option[bool] = Nothing
    send_phone_number_to_provider: Option[bool] = Nothing
    send_email_to_provider: Option[bool] = Nothing
    is_flexible: Option[bool] = Nothing


class InputTextMessageContent(Model):
    """Represents the [content](https://core.telegram.org/bots/api/#inputmessagecontent)
    of a text message to be sent as the result of an inline query.
    Docs: https://core.telegram.org/bots/api/#inputtextmessagecontent"""

    message_text: str
    parse_mode: Option[str] = Nothing
    entities: Option[list["MessageEntity"]] = Nothing
    disable_web_page_preview: Option[bool] = Nothing


class InputLocationMessageContent(Model):
    """Represents the [content](https://core.telegram.org/bots/api/#inputmessagecontent)
    of a location message to be sent as the result of an inline query.
    Docs: https://core.telegram.org/bots/api/#inputlocationmessagecontent"""

    latitude: float
    longitude: float
    horizontal_accuracy: Option[float] = Nothing
    live_period: Option[int] = Nothing
    heading: Option[int] = Nothing
    proximity_alert_radius: Option[int] = Nothing


class InputVenueMessageContent(Model):
    """Represents the [content](https://core.telegram.org/bots/api/#inputmessagecontent)
    of a venue message to be sent as the result of an inline query.
    Docs: https://core.telegram.org/bots/api/#inputvenuemessagecontent"""

    latitude: float
    longitude: float
    title: str
    address: str
    foursquare_id: Option[str] = Nothing
    foursquare_type: Option[str] = Nothing
    google_place_id: Option[str] = Nothing
    google_place_type: Option[str] = Nothing


class InputContactMessageContent(Model):
    """Represents the [content](https://core.telegram.org/bots/api/#inputmessagecontent)
    of a contact message to be sent as the result of an inline query.
    Docs: https://core.telegram.org/bots/api/#inputcontactmessagecontent"""

    phone_number: str
    first_name: str
    last_name: Option[str] = Nothing
    vcard: Option[str] = Nothing


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
    max_tip_amount: Option[int] = Some(0)
    suggested_tip_amounts: Option[list[int]] = Nothing
    provider_data: Option[str] = Nothing
    photo_url: Option[str] = Nothing
    photo_size: Option[int] = Nothing
    photo_width: Option[int] = Nothing
    photo_height: Option[int] = Nothing
    need_name: Option[bool] = Nothing
    need_phone_number: Option[bool] = Nothing
    need_email: Option[bool] = Nothing
    need_shipping_address: Option[bool] = Nothing
    send_phone_number_to_provider: Option[bool] = Nothing
    send_email_to_provider: Option[bool] = Nothing
    is_flexible: Option[bool] = Nothing


class ChosenInlineResult(Model):
    """Represents a [result](https://core.telegram.org/bots/api/#inlinequeryresult)
    of an inline query that was chosen by the user and sent to their chat partner.

    Docs: https://core.telegram.org/bots/api/#choseninlineresult"""

    result_id: str
    from_: "User"
    query: str
    location: Option["Location"] = Nothing
    inline_message_id: Option[str] = Nothing


class SentWebAppMessage(Model):
    """Describes an inline message sent by a [Web App](https://core.telegram.org/bots/webapps)
    on behalf of a user.
    Docs: https://core.telegram.org/bots/api/#sentwebappmessage"""

    inline_message_id: Option[str] = Nothing


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

    name: Option[str] = Nothing
    phone_number: Option[str] = Nothing
    email: Option[str] = Nothing
    shipping_address: Option["ShippingAddress"] = Nothing


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
    shipping_option_id: Option[str] = Nothing
    order_info: Option["OrderInfo"] = Nothing


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
    shipping_option_id: Option[str] = Nothing
    order_info: Option["OrderInfo"] = Nothing


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
    data: Option[str] = Nothing
    phone_number: Option[str] = Nothing
    email: Option[str] = Nothing
    files: Option[list["PassportFile"]] = Nothing
    front_side: Option["PassportFile"] = Nothing
    reverse_side: Option["PassportFile"] = Nothing
    selfie: Option["PassportFile"] = Nothing
    translation: Option[list["PassportFile"]] = Nothing


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

    source: Option[str] = Some("unspecified")
    type: Option[str] = Nothing
    field_name: Option[str] = Nothing
    data_hash: Option[str] = Nothing
    message: Option[str] = Nothing
    file_hash: Option[str] = Nothing
    file_hashes: Option[list[str]] = Nothing
    element_hash: Option[str] = Nothing


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
    text: Option[str] = Nothing
    text_entities: Option[list["MessageEntity"]] = Nothing
    animation: Option["Animation"] = Nothing


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
