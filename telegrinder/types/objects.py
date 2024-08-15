import pathlib
import typing
from functools import cached_property

from fntypes.co import Variative

from telegrinder.model import Model
from telegrinder.msgspec_utils import Nothing, Option, datetime
from telegrinder.types.enums import *  # noqa: F403


class TransactionPartner(Model):
    """Base object `TransactionPartner`, see the [documentation](https://core.telegram.org/bots/api#transactionpartner).

    This object describes the source of a transaction, or its recipient for outgoing transactions. Currently, it can be one of
    - TransactionPartnerUser
    - TransactionPartnerFragment
    - TransactionPartnerTelegramAds
    - TransactionPartnerOther
    """


class RevenueWithdrawalState(Model):
    """Base object `RevenueWithdrawalState`, see the [documentation](https://core.telegram.org/bots/api#revenuewithdrawalstate).

    This object describes the state of a revenue withdrawal operation. Currently, it can be one of
    - RevenueWithdrawalStatePending
    - RevenueWithdrawalStateSucceeded
    - RevenueWithdrawalStateFailed
    """


class ReactionType(Model):
    """Base object `ReactionType`, see the [documentation](https://core.telegram.org/bots/api#reactiontype).

    This object describes the type of a reaction. Currently, it can be one of
    - ReactionTypeEmoji
    - ReactionTypeCustomEmoji
    - ReactionTypePaid
    """


class PassportElementError(Model):
    """Base object `PassportElementError`, see the [documentation](https://core.telegram.org/bots/api#passportelementerror).

    This object represents an error in the Telegram Passport element which was submitted that should be resolved by the user. It should be one of:
    - PassportElementErrorDataField
    - PassportElementErrorFrontSide
    - PassportElementErrorReverseSide
    - PassportElementErrorSelfie
    - PassportElementErrorFile
    - PassportElementErrorFiles
    - PassportElementErrorTranslationFile
    - PassportElementErrorTranslationFiles
    - PassportElementErrorUnspecified
    """


class PaidMedia(Model):
    """Base object `PaidMedia`, see the [documentation](https://core.telegram.org/bots/api#paidmedia).

    This object describes paid media. Currently, it can be one of
    - PaidMediaPreview
    - PaidMediaPhoto
    - PaidMediaVideo
    """


class MessageOrigin(Model):
    """Base object `MessageOrigin`, see the [documentation](https://core.telegram.org/bots/api#messageorigin).

    This object describes the origin of a message. It can be one of
    - MessageOriginUser
    - MessageOriginHiddenUser
    - MessageOriginChat
    - MessageOriginChannel
    """


class MaybeInaccessibleMessage(Model):
    """Base object `MaybeInaccessibleMessage`, see the [documentation](https://core.telegram.org/bots/api#maybeinaccessiblemessage).

    This object describes a message that can be inaccessible to the bot. It can be one of
    - Message
    - InaccessibleMessage
    """


class MenuButton(Model):
    """Base object `MenuButton`, see the [documentation](https://core.telegram.org/bots/api#menubutton).

    This object describes the bot's menu button in a private chat. It should be one of
    - MenuButtonCommands
    - MenuButtonWebApp
    - MenuButtonDefault
    If a menu button other than MenuButtonDefault is set for a private chat, then it is applied in the chat. Otherwise the default menu button is applied. By default, the menu button opens the list of bot commands.
    """


class InputMessageContent(Model):
    """Base object `InputMessageContent`, see the [documentation](https://core.telegram.org/bots/api#inputmessagecontent).

    This object represents the content of a message to be sent as a result of an inline query. Telegram clients currently support the following 5 types:
    - InputTextMessageContent
    - InputLocationMessageContent
    - InputVenueMessageContent
    - InputContactMessageContent
    - InputInvoiceMessageContent
    """


class InputPaidMedia(Model):
    """Base object `InputPaidMedia`, see the [documentation](https://core.telegram.org/bots/api#inputpaidmedia).

    This object describes the paid media to be sent. Currently, it can be one of
    - InputPaidMediaPhoto
    - InputPaidMediaVideo
    """


class InputMedia(Model):
    """Base object `InputMedia`, see the [documentation](https://core.telegram.org/bots/api#inputmedia).

    This object represents the content of a media message to be sent. It should be one of
    - InputMediaAnimation
    - InputMediaDocument
    - InputMediaAudio
    - InputMediaPhoto
    - InputMediaVideo
    """


class InlineQueryResult(Model):
    """Base object `InlineQueryResult`, see the [documentation](https://core.telegram.org/bots/api#inlinequeryresult).

    This object represents one result of an inline query. Telegram clients currently support results of the following 20 types:
    - InlineQueryResultCachedAudio
    - InlineQueryResultCachedDocument
    - InlineQueryResultCachedGif
    - InlineQueryResultCachedMpeg4Gif
    - InlineQueryResultCachedPhoto
    - InlineQueryResultCachedSticker
    - InlineQueryResultCachedVideo
    - InlineQueryResultCachedVoice
    - InlineQueryResultArticle
    - InlineQueryResultAudio
    - InlineQueryResultContact
    - InlineQueryResultGame
    - InlineQueryResultDocument
    - InlineQueryResultGif
    - InlineQueryResultLocation
    - InlineQueryResultMpeg4Gif
    - InlineQueryResultPhoto
    - InlineQueryResultVenue
    - InlineQueryResultVideo
    - InlineQueryResultVoice
    Note: All URLs passed in inline query results will be available to end users and therefore must be assumed to be public.
    """


class ChatMember(Model):
    """Base object `ChatMember`, see the [documentation](https://core.telegram.org/bots/api#chatmember).

    This object contains information about one member of a chat. Currently, the following 6 types of chat members are supported:
    - ChatMemberOwner
    - ChatMemberAdministrator
    - ChatMemberMember
    - ChatMemberRestricted
    - ChatMemberLeft
    - ChatMemberBanned
    """


class ChatBoostSource(Model):
    """Base object `ChatBoostSource`, see the [documentation](https://core.telegram.org/bots/api#chatboostsource).

    This object describes the source of a chat boost. It can be one of
    - ChatBoostSourcePremium
    - ChatBoostSourceGiftCode
    - ChatBoostSourceGiveaway
    """


class BotCommandScope(Model):
    """Base object `BotCommandScope`, see the [documentation](https://core.telegram.org/bots/api#botcommandscope).

    This object represents the scope to which bot commands are applied. Currently, the following 7 scopes are supported:
    - BotCommandScopeDefault
    - BotCommandScopeAllPrivateChats
    - BotCommandScopeAllGroupChats
    - BotCommandScopeAllChatAdministrators
    - BotCommandScopeChat
    - BotCommandScopeChatAdministrators
    - BotCommandScopeChatMember
    """


class BackgroundType(Model):
    """Base object `BackgroundType`, see the [documentation](https://core.telegram.org/bots/api#backgroundtype).

    This object describes the type of a background. Currently, it can be one of
    - BackgroundTypeFill
    - BackgroundTypeWallpaper
    - BackgroundTypePattern
    - BackgroundTypeChatTheme
    """


class BackgroundFill(Model):
    """Base object `BackgroundFill`, see the [documentation](https://core.telegram.org/bots/api#backgroundfill).

    This object describes the way a background is filled based on the selected colors. Currently, it can be one of
    - BackgroundFillSolid
    - BackgroundFillGradient
    - BackgroundFillFreeformGradient
    """


class Update(Model):
    """Object `Update`, see the [documentation](https://core.telegram.org/bots/api#update).

    This object represents an incoming update.
    At most one of the optional parameters can be present in any given update.
    """

    update_id: int
    """The update's unique identifier. Update identifiers start from a certain
    positive number and increase sequentially. This identifier becomes especially
    handy if you're using webhooks, since it allows you to ignore repeated updates
    or to restore the correct update sequence, should they get out of order.
    If there are no new updates for at least a week, then identifier of the next
    update will be chosen randomly instead of sequentially."""

    message: Option["Message"] = Nothing
    """Optional. New incoming message of any kind - text, photo, sticker, etc."""

    edited_message: Option["Message"] = Nothing
    """Optional. New version of a message that is known to the bot and was edited.
    This update may at times be triggered by changes to message fields that are
    either unavailable or not actively used by your bot."""

    channel_post: Option["Message"] = Nothing
    """Optional. New incoming channel post of any kind - text, photo, sticker,
    etc."""

    edited_channel_post: Option["Message"] = Nothing
    """Optional. New version of a channel post that is known to the bot and was edited.
    This update may at times be triggered by changes to message fields that are
    either unavailable or not actively used by your bot."""

    business_connection: Option["BusinessConnection"] = Nothing
    """Optional. The bot was connected to or disconnected from a business account,
    or a user edited an existing connection with the bot."""

    business_message: Option["Message"] = Nothing
    """Optional. New message from a connected business account."""

    edited_business_message: Option["Message"] = Nothing
    """Optional. New version of a message from a connected business account."""

    deleted_business_messages: Option["BusinessMessagesDeleted"] = Nothing
    """Optional. Messages were deleted from a connected business account."""

    message_reaction: Option["MessageReactionUpdated"] = Nothing
    """Optional. A reaction to a message was changed by a user. The bot must be an
    administrator in the chat and must explicitly specify `message_reaction`
    in the list of allowed_updates to receive these updates. The update isn't
    received for reactions set by bots."""

    message_reaction_count: Option["MessageReactionCountUpdated"] = Nothing
    """Optional. Reactions to a message with anonymous reactions were changed.
    The bot must be an administrator in the chat and must explicitly specify
    `message_reaction_count` in the list of allowed_updates to receive these
    updates. The updates are grouped and can be sent with delay up to a few minutes."""

    inline_query: Option["InlineQuery"] = Nothing
    """Optional. New incoming inline query."""

    chosen_inline_result: Option["ChosenInlineResult"] = Nothing
    """Optional. The result of an inline query that was chosen by a user and sent
    to their chat partner. Please see our documentation on the feedback collecting
    for details on how to enable these updates for your bot."""

    callback_query: Option["CallbackQuery"] = Nothing
    """Optional. New incoming callback query."""

    shipping_query: Option["ShippingQuery"] = Nothing
    """Optional. New incoming shipping query. Only for invoices with flexible
    price."""

    pre_checkout_query: Option["PreCheckoutQuery"] = Nothing
    """Optional. New incoming pre-checkout query. Contains full information
    about checkout."""

    poll: Option["Poll"] = Nothing
    """Optional. New poll state. Bots receive only updates about manually stopped
    polls and polls, which are sent by the bot."""

    poll_answer: Option["PollAnswer"] = Nothing
    """Optional. A user changed their answer in a non-anonymous poll. Bots receive
    new votes only in polls that were sent by the bot itself."""

    my_chat_member: Option["ChatMemberUpdated"] = Nothing
    """Optional. The bot's chat member status was updated in a chat. For private
    chats, this update is received only when the bot is blocked or unblocked
    by the user."""

    chat_member: Option["ChatMemberUpdated"] = Nothing
    """Optional. A chat member's status was updated in a chat. The bot must be an
    administrator in the chat and must explicitly specify `chat_member` in
    the list of allowed_updates to receive these updates."""

    chat_join_request: Option["ChatJoinRequest"] = Nothing
    """Optional. A request to join the chat has been sent. The bot must have the can_invite_users
    administrator right in the chat to receive these updates."""

    chat_boost: Option["ChatBoostUpdated"] = Nothing
    """Optional. A chat boost was added or changed. The bot must be an administrator
    in the chat to receive these updates."""

    removed_chat_boost: Option["ChatBoostRemoved"] = Nothing
    """Optional. A boost was removed from a chat. The bot must be an administrator
    in the chat to receive these updates."""

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.update_type == other.update_type

    @cached_property
    def update_type(self) -> UpdateType:
        """Incoming update type."""

        return UpdateType(
            next(
                (
                    x
                    for x in self.__struct_fields__
                    if x != "update_id" and not isinstance(getattr(self, x), type(Nothing))
                )
            ),
        )


class WebhookInfo(Model):
    """Object `WebhookInfo`, see the [documentation](https://core.telegram.org/bots/api#webhookinfo).

    Describes the current status of a webhook.
    """

    url: str
    """Webhook URL, may be empty if webhook is not set up."""

    has_custom_certificate: bool
    """True, if a custom certificate was provided for webhook certificate checks."""

    pending_update_count: int
    """Number of updates awaiting delivery."""

    ip_address: Option[str] = Nothing
    """Optional. Currently used webhook IP address."""

    last_error_date: Option[datetime] = Nothing
    """Optional. Unix time for the most recent error that happened when trying
    to deliver an update via webhook."""

    last_error_message: Option[str] = Nothing
    """Optional. Error message in human-readable format for the most recent error
    that happened when trying to deliver an update via webhook."""

    last_synchronization_error_date: Option[datetime] = Nothing
    """Optional. Unix time of the most recent error that happened when trying to
    synchronize available updates with Telegram datacenters."""

    max_connections: Option[int] = Nothing
    """Optional. The maximum allowed number of simultaneous HTTPS connections
    to the webhook for update delivery."""

    allowed_updates: Option[list[str]] = Nothing
    """Optional. A list of update types the bot is subscribed to. Defaults to all
    update types except chat_member."""


class User(Model):
    """Object `User`, see the [documentation](https://core.telegram.org/bots/api#user).

    This object represents a Telegram user or bot.
    """

    id: int
    """Unique identifier for this user or bot. This number may have more than 32
    significant bits and some programming languages may have difficulty/silent
    defects in interpreting it. But it has at most 52 significant bits, so a 64-bit
    integer or double-precision float type are safe for storing this identifier."""

    is_bot: bool
    """True, if this user is a bot."""

    first_name: str
    """User's or bot's first name."""

    last_name: Option[str] = Nothing
    """Optional. User's or bot's last name."""

    username: Option[str] = Nothing
    """Optional. User's or bot's username."""

    language_code: Option[str] = Nothing
    """Optional. IETF language tag of the user's language."""

    is_premium: Option[bool] = Nothing
    """Optional. True, if this user is a Telegram Premium user."""

    added_to_attachment_menu: Option[bool] = Nothing
    """Optional. True, if this user added the bot to the attachment menu."""

    can_join_groups: Option[bool] = Nothing
    """Optional. True, if the bot can be invited to groups. Returned only in getMe."""

    can_read_all_group_messages: Option[bool] = Nothing
    """Optional. True, if privacy mode is disabled for the bot. Returned only in
    getMe."""

    supports_inline_queries: Option[bool] = Nothing
    """Optional. True, if the bot supports inline queries. Returned only in getMe."""

    can_connect_to_business: Option[bool] = Nothing
    """Optional. True, if the bot can be connected to a Telegram Business account
    to receive its messages. Returned only in getMe."""

    has_main_web_app: Option[bool] = Nothing
    """Optional. True, if the bot has a main Web App. Returned only in getMe."""

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.id == other.id

    @property
    def default_accent_color(self) -> DefaultAccentColor:
        """User's or bot's accent color (non-premium)."""

        return DefaultAccentColor(self.id % 7)

    @property
    def full_name(self) -> str:
        """User's or bot's full name (`first_name` + `last_name`)."""

        return self.first_name + self.last_name.map(lambda v: " " + v).unwrap_or("")


class Chat(Model):
    """Object `Chat`, see the [documentation](https://core.telegram.org/bots/api#chat).

    This object represents a chat.
    """

    id: int
    """Unique identifier for this chat. This number may have more than 32 significant
    bits and some programming languages may have difficulty/silent defects
    in interpreting it. But it has at most 52 significant bits, so a signed 64-bit
    integer or double-precision float type are safe for storing this identifier."""

    type: ChatType
    """Type of the chat, can be either `private`, `group`, `supergroup` or `channel`."""

    title: Option[str] = Nothing
    """Optional. Title, for supergroups, channels and group chats."""

    username: Option[str] = Nothing
    """Optional. Username, for private chats, supergroups and channels if available."""

    first_name: Option[str] = Nothing
    """Optional. First name of the other party in a private chat."""

    last_name: Option[str] = Nothing
    """Optional. Last name of the other party in a private chat."""

    is_forum: Option[bool] = Nothing
    """Optional. True, if the supergroup chat is a forum (has topics enabled)."""

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.id == other.id

    @property
    def full_name(self) -> Option[str]:
        """Optional. Full name (`first_name` + `last_name`) of the
        other party in a `private` chat."""

        return self.first_name.map(lambda x: x + " " + self.last_name.unwrap_or(""))


class ChatFullInfo(Model):
    """Object `ChatFullInfo`, see the [documentation](https://core.telegram.org/bots/api#chatfullinfo).

    This object contains full information about a chat.
    """

    id: int
    """Unique identifier for this chat. This number may have more than 32 significant
    bits and some programming languages may have difficulty/silent defects
    in interpreting it. But it has at most 52 significant bits, so a signed 64-bit
    integer or double-precision float type are safe for storing this identifier."""

    type: ChatType
    """Type of the chat, can be either `private`, `group`, `supergroup` or `channel`."""

    accent_color_id: int
    """Identifier of the accent color for the chat name and backgrounds of the chat
    photo, reply header, and link preview. See accent colors for more details."""

    max_reaction_count: int
    """The maximum number of reactions that can be set on a message in the chat."""

    title: Option[str] = Nothing
    """Optional. Title, for supergroups, channels and group chats."""

    username: Option[str] = Nothing
    """Optional. Username, for private chats, supergroups and channels if available."""

    first_name: Option[str] = Nothing
    """Optional. First name of the other party in a private chat."""

    last_name: Option[str] = Nothing
    """Optional. Last name of the other party in a private chat."""

    is_forum: Option[bool] = Nothing
    """Optional. True, if the supergroup chat is a forum (has topics enabled)."""

    photo: Option["ChatPhoto"] = Nothing
    """Optional. Chat photo."""

    active_usernames: Option[list[str]] = Nothing
    """Optional. If non-empty, the list of all active chat usernames; for private
    chats, supergroups and channels."""

    birthdate: Option["Birthdate"] = Nothing
    """Optional. For private chats, the date of birth of the user."""

    business_intro: Option["BusinessIntro"] = Nothing
    """Optional. For private chats with business accounts, the intro of the business."""

    business_location: Option["BusinessLocation"] = Nothing
    """Optional. For private chats with business accounts, the location of the
    business."""

    business_opening_hours: Option["BusinessOpeningHours"] = Nothing
    """Optional. For private chats with business accounts, the opening hours
    of the business."""

    personal_chat: Option["Chat"] = Nothing
    """Optional. For private chats, the personal channel of the user."""

    available_reactions: Option[
        list[Variative["ReactionTypeEmoji", "ReactionTypeCustomEmoji", "ReactionTypePaid"]]
    ] = Nothing
    """Optional. List of available reactions allowed in the chat. If omitted,
    then all emoji reactions are allowed."""

    background_custom_emoji_id: Option[str] = Nothing
    """Optional. Custom emoji identifier of the emoji chosen by the chat for the
    reply header and link preview background."""

    profile_accent_color_id: Option[int] = Nothing
    """Optional. Identifier of the accent color for the chat's profile background.
    See profile accent colors for more details."""

    profile_background_custom_emoji_id: Option[str] = Nothing
    """Optional. Custom emoji identifier of the emoji chosen by the chat for its
    profile background."""

    emoji_status_custom_emoji_id: Option[str] = Nothing
    """Optional. Custom emoji identifier of the emoji status of the chat or the
    other party in a private chat."""

    emoji_status_expiration_date: Option[datetime] = Nothing
    """Optional. Expiration date of the emoji status of the chat or the other party
    in a private chat, in Unix time, if any."""

    bio: Option[str] = Nothing
    """Optional. Bio of the other party in a private chat."""

    has_private_forwards: Option[bool] = Nothing
    """Optional. True, if privacy settings of the other party in the private chat
    allows to use tg://user?id=<user_id> links only in chats with the user."""

    has_restricted_voice_and_video_messages: Option[bool] = Nothing
    """Optional. True, if the privacy settings of the other party restrict sending
    voice and video note messages in the private chat."""

    join_to_send_messages: Option[bool] = Nothing
    """Optional. True, if users need to join the supergroup before they can send
    messages."""

    join_by_request: Option[bool] = Nothing
    """Optional. True, if all users directly joining the supergroup without using
    an invite link need to be approved by supergroup administrators."""

    description: Option[str] = Nothing
    """Optional. Description, for groups, supergroups and channel chats."""

    invite_link: Option[str] = Nothing
    """Optional. Primary invite link, for groups, supergroups and channel chats."""

    pinned_message: Option["Message"] = Nothing
    """Optional. The most recent pinned message (by sending date)."""

    permissions: Option["ChatPermissions"] = Nothing
    """Optional. Default chat member permissions, for groups and supergroups."""

    can_send_paid_media: Option[bool] = Nothing
    """Optional. True, if paid media messages can be sent or forwarded to the channel
    chat. The field is available only for channel chats."""

    slow_mode_delay: Option[int] = Nothing
    """Optional. For supergroups, the minimum allowed delay between consecutive
    messages sent by each unprivileged user; in seconds."""

    unrestrict_boost_count: Option[int] = Nothing
    """Optional. For supergroups, the minimum number of boosts that a non-administrator
    user needs to add in order to ignore slow mode and chat permissions."""

    message_auto_delete_time: Option[int] = Nothing
    """Optional. The time after which all messages sent to the chat will be automatically
    deleted; in seconds."""

    has_aggressive_anti_spam_enabled: Option[bool] = Nothing
    """Optional. True, if aggressive anti-spam checks are enabled in the supergroup.
    The field is only available to chat administrators."""

    has_hidden_members: Option[bool] = Nothing
    """Optional. True, if non-administrators can only get the list of bots and
    administrators in the chat."""

    has_protected_content: Option[bool] = Nothing
    """Optional. True, if messages from the chat can't be forwarded to other chats."""

    has_visible_history: Option[bool] = Nothing
    """Optional. True, if new chat members will have access to old messages; available
    only to chat administrators."""

    sticker_set_name: Option[str] = Nothing
    """Optional. For supergroups, name of the group sticker set."""

    can_set_sticker_set: Option[bool] = Nothing
    """Optional. True, if the bot can change the group sticker set."""

    custom_emoji_sticker_set_name: Option[str] = Nothing
    """Optional. For supergroups, the name of the group's custom emoji sticker
    set. Custom emoji from this set can be used by all users and bots in the group."""

    linked_chat_id: Option[int] = Nothing
    """Optional. Unique identifier for the linked chat, i.e. the discussion group
    identifier for a channel and vice versa; for supergroups and channel chats.
    This identifier may be greater than 32 bits and some programming languages
    may have difficulty/silent defects in interpreting it. But it is smaller
    than 52 bits, so a signed 64 bit integer or double-precision float type are
    safe for storing this identifier."""

    location: Option["ChatLocation"] = Nothing
    """Optional. For supergroups, the location to which the supergroup is connected."""


class Message(MaybeInaccessibleMessage):
    """Object `Message`, see the [documentation](https://core.telegram.org/bots/api#message).

    This object represents a message.
    """

    message_id: int
    """Unique message identifier inside this chat."""

    date: datetime
    """Date the message was sent in Unix time. It is always a positive number, representing
    a valid date."""

    chat: "Chat"
    """Chat the message belongs to."""

    message_thread_id: Option[int] = Nothing
    """Optional. Unique identifier of a message thread to which the message belongs;
    for supergroups only."""

    from_: Option["User"] = Nothing
    """Optional. Sender of the message; may be empty for messages sent to channels.
    For backward compatibility, if the message was sent on behalf of a chat,
    the field contains a fake sender user in non-channel chats."""

    sender_chat: Option["Chat"] = Nothing
    """Optional. Sender of the message when sent on behalf of a chat. For example,
    the supergroup itself for messages sent by its anonymous administrators
    or a linked channel for messages automatically forwarded to the channel's
    discussion group. For backward compatibility, if the message was sent
    on behalf of a chat, the field from contains a fake sender user in non-channel
    chats."""

    sender_boost_count: Option[int] = Nothing
    """Optional. If the sender of the message boosted the chat, the number of boosts
    added by the user."""

    sender_business_bot: Option["User"] = Nothing
    """Optional. The bot that actually sent the message on behalf of the business
    account. Available only for outgoing messages sent on behalf of the connected
    business account."""

    business_connection_id: Option[str] = Nothing
    """Optional. Unique identifier of the business connection from which the
    message was received. If non-empty, the message belongs to a chat of the
    corresponding business account that is independent from any potential
    bot chat which might share the same identifier."""

    forward_origin: Option[
        Variative["MessageOriginUser", "MessageOriginHiddenUser", "MessageOriginChat", "MessageOriginChannel"]
    ] = Nothing
    """Optional. Information about the original message for forwarded messages."""

    is_topic_message: Option[bool] = Nothing
    """Optional. True, if the message is sent to a forum topic."""

    is_automatic_forward: Option[bool] = Nothing
    """Optional. True, if the message is a channel post that was automatically
    forwarded to the connected discussion group."""

    reply_to_message: Option["Message"] = Nothing
    """Optional. For replies in the same chat and message thread, the original
    message. Note that the Message object in this field will not contain further
    reply_to_message fields even if it itself is a reply."""

    external_reply: Option["ExternalReplyInfo"] = Nothing
    """Optional. Information about the message that is being replied to, which
    may come from another chat or forum topic."""

    quote: Option["TextQuote"] = Nothing
    """Optional. For replies that quote part of the original message, the quoted
    part of the message."""

    reply_to_story: Option["Story"] = Nothing
    """Optional. For replies to a story, the original story."""

    via_bot: Option["User"] = Nothing
    """Optional. Bot through which the message was sent."""

    edit_date: Option[datetime] = Nothing
    """Optional. Date the message was last edited in Unix time."""

    has_protected_content: Option[bool] = Nothing
    """Optional. True, if the message can't be forwarded."""

    is_from_offline: Option[bool] = Nothing
    """Optional. True, if the message was sent by an implicit action, for example,
    as an away or a greeting business message, or as a scheduled message."""

    media_group_id: Option[str] = Nothing
    """Optional. The unique identifier of a media message group this message belongs
    to."""

    author_signature: Option[str] = Nothing
    """Optional. Signature of the post author for messages in channels, or the
    custom title of an anonymous group administrator."""

    text: Option[str] = Nothing
    """Optional. For text messages, the actual UTF-8 text of the message."""

    entities: Option[list["MessageEntity"]] = Nothing
    """Optional. For text messages, special entities like usernames, URLs, bot
    commands, etc. that appear in the text."""

    link_preview_options: Option["LinkPreviewOptions"] = Nothing
    """Optional. Options used for link preview generation for the message, if
    it is a text message and link preview options were changed."""

    effect_id: Option[str] = Nothing
    """Optional. Unique identifier of the message effect added to the message."""

    animation: Option["Animation"] = Nothing
    """Optional. Message is an animation, information about the animation. For
    backward compatibility, when this field is set, the document field will
    also be set."""

    audio: Option["Audio"] = Nothing
    """Optional. Message is an audio file, information about the file."""

    document: Option["Document"] = Nothing
    """Optional. Message is a general file, information about the file."""

    paid_media: Option["PaidMediaInfo"] = Nothing
    """Optional. Message contains paid media; information about the paid media."""

    photo: Option[list["PhotoSize"]] = Nothing
    """Optional. Message is a photo, available sizes of the photo."""

    sticker: Option["Sticker"] = Nothing
    """Optional. Message is a sticker, information about the sticker."""

    story: Option["Story"] = Nothing
    """Optional. Message is a forwarded story."""

    video: Option["Video"] = Nothing
    """Optional. Message is a video, information about the video."""

    video_note: Option["VideoNote"] = Nothing
    """Optional. Message is a video note, information about the video message."""

    voice: Option["Voice"] = Nothing
    """Optional. Message is a voice message, information about the file."""

    caption: Option[str] = Nothing
    """Optional. Caption for the animation, audio, document, paid media, photo,
    video or voice."""

    caption_entities: Option[list["MessageEntity"]] = Nothing
    """Optional. For messages with a caption, special entities like usernames,
    URLs, bot commands, etc. that appear in the caption."""

    show_caption_above_media: Option[bool] = Nothing
    """Optional. True, if the caption must be shown above the message media."""

    has_media_spoiler: Option[bool] = Nothing
    """Optional. True, if the message media is covered by a spoiler animation."""

    contact: Option["Contact"] = Nothing
    """Optional. Message is a shared contact, information about the contact."""

    dice: Option["Dice"] = Nothing
    """Optional. Message is a dice with random value."""

    game: Option["Game"] = Nothing
    """Optional. Message is a game, information about the game. More about games:
    https://core.telegram.org/bots/api#games."""

    poll: Option["Poll"] = Nothing
    """Optional. Message is a native poll, information about the poll."""

    venue: Option["Venue"] = Nothing
    """Optional. Message is a venue, information about the venue. For backward
    compatibility, when this field is set, the location field will also be set."""

    location: Option["Location"] = Nothing
    """Optional. Message is a shared location, information about the location."""

    new_chat_members: Option[list["User"]] = Nothing
    """Optional. New members that were added to the group or supergroup and information
    about them (the bot itself may be one of these members)."""

    left_chat_member: Option["User"] = Nothing
    """Optional. A member was removed from the group, information about them (this
    member may be the bot itself)."""

    new_chat_title: Option[str] = Nothing
    """Optional. A chat title was changed to this value."""

    new_chat_photo: Option[list["PhotoSize"]] = Nothing
    """Optional. A chat photo was change to this value."""

    delete_chat_photo: Option[bool] = Nothing
    """Optional. Service message: the chat photo was deleted."""

    group_chat_created: Option[bool] = Nothing
    """Optional. Service message: the group has been created."""

    supergroup_chat_created: Option[bool] = Nothing
    """Optional. Service message: the supergroup has been created. This field
    can't be received in a message coming through updates, because bot can't
    be a member of a supergroup when it is created. It can only be found in reply_to_message
    if someone replies to a very first message in a directly created supergroup."""

    channel_chat_created: Option[bool] = Nothing
    """Optional. Service message: the channel has been created. This field can't
    be received in a message coming through updates, because bot can't be a member
    of a channel when it is created. It can only be found in reply_to_message
    if someone replies to a very first message in a channel."""

    message_auto_delete_timer_changed: Option["MessageAutoDeleteTimerChanged"] = Nothing
    """Optional. Service message: auto-delete timer settings changed in the
    chat."""

    migrate_to_chat_id: Option[int] = Nothing
    """Optional. The group has been migrated to a supergroup with the specified
    identifier. This number may have more than 32 significant bits and some
    programming languages may have difficulty/silent defects in interpreting
    it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision
    float type are safe for storing this identifier."""

    migrate_from_chat_id: Option[int] = Nothing
    """Optional. The supergroup has been migrated from a group with the specified
    identifier. This number may have more than 32 significant bits and some
    programming languages may have difficulty/silent defects in interpreting
    it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision
    float type are safe for storing this identifier."""

    pinned_message: Option[Variative["Message", "InaccessibleMessage"]] = Nothing
    """Optional. Specified message was pinned. Note that the Message object in
    this field will not contain further reply_to_message fields even if it
    itself is a reply."""

    invoice: Option["Invoice"] = Nothing
    """Optional. Message is an invoice for a payment, information about the invoice.
    More about payments: https://core.telegram.org/bots/api#payments."""

    successful_payment: Option["SuccessfulPayment"] = Nothing
    """Optional. Message is a service message about a successful payment, information
    about the payment. More about payments: https://core.telegram.org/bots/api#payments."""

    refunded_payment: Option["RefundedPayment"] = Nothing
    """Optional. Message is a service message about a refunded payment, information
    about the payment. More about payments: https://core.telegram.org/bots/api#payments."""

    users_shared: Option["UsersShared"] = Nothing
    """Optional. Service message: users were shared with the bot."""

    chat_shared: Option["ChatShared"] = Nothing
    """Optional. Service message: a chat was shared with the bot."""

    connected_website: Option[str] = Nothing
    """Optional. The domain name of the website on which the user has logged in.
    More about Telegram Login: https://core.telegram.org/widgets/login."""

    write_access_allowed: Option["WriteAccessAllowed"] = Nothing
    """Optional. Service message: the user allowed the bot to write messages after
    adding it to the attachment or side menu, launching a Web App from a link,
    or accepting an explicit request from a Web App sent by the method requestWriteAccess."""

    passport_data: Option["PassportData"] = Nothing
    """Optional. Telegram Passport data."""

    proximity_alert_triggered: Option["ProximityAlertTriggered"] = Nothing
    """Optional. Service message. A user in the chat triggered another user's
    proximity alert while sharing Live Location."""

    boost_added: Option["ChatBoostAdded"] = Nothing
    """Optional. Service message: user boosted the chat."""

    chat_background_set: Option["ChatBackground"] = Nothing
    """Optional. Service message: chat background set."""

    forum_topic_created: Option["ForumTopicCreated"] = Nothing
    """Optional. Service message: forum topic created."""

    forum_topic_edited: Option["ForumTopicEdited"] = Nothing
    """Optional. Service message: forum topic edited."""

    forum_topic_closed: Option["ForumTopicClosed"] = Nothing
    """Optional. Service message: forum topic closed."""

    forum_topic_reopened: Option["ForumTopicReopened"] = Nothing
    """Optional. Service message: forum topic reopened."""

    general_forum_topic_hidden: Option["GeneralForumTopicHidden"] = Nothing
    """Optional. Service message: the 'General' forum topic hidden."""

    general_forum_topic_unhidden: Option["GeneralForumTopicUnhidden"] = Nothing
    """Optional. Service message: the 'General' forum topic unhidden."""

    giveaway_created: Option["GiveawayCreated"] = Nothing
    """Optional. Service message: a scheduled giveaway was created."""

    giveaway: Option["Giveaway"] = Nothing
    """Optional. The message is a scheduled giveaway message."""

    giveaway_winners: Option["GiveawayWinners"] = Nothing
    """Optional. A giveaway with public winners was completed."""

    giveaway_completed: Option["GiveawayCompleted"] = Nothing
    """Optional. Service message: a giveaway without public winners was completed."""

    video_chat_scheduled: Option["VideoChatScheduled"] = Nothing
    """Optional. Service message: video chat scheduled."""

    video_chat_started: Option["VideoChatStarted"] = Nothing
    """Optional. Service message: video chat started."""

    video_chat_ended: Option["VideoChatEnded"] = Nothing
    """Optional. Service message: video chat ended."""

    video_chat_participants_invited: Option["VideoChatParticipantsInvited"] = Nothing
    """Optional. Service message: new participants invited to a video chat."""

    web_app_data: Option["WebAppData"] = Nothing
    """Optional. Service message: data sent by a Web App."""

    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    """Optional. Inline keyboard attached to the message. login_url buttons
    are represented as ordinary url buttons."""

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.message_id == other.message_id
            and self.chat_id == other.chat_id
        )

    @cached_property
    def content_type(self) -> ContentType:
        """Type of content that the message contains."""

        for content in ContentType:
            if (
                content.value in self.__struct_fields__
                and getattr(self, content.value, Nothing) is not Nothing
            ):
                return content
        return ContentType.UNKNOWN

    @property
    def from_user(self) -> "User":
        """`from_user` instead of `from_.unwrap()`."""

        return self.from_.unwrap()

    @property
    def chat_id(self) -> int:
        """`chat_id` instead of `chat.id`."""

        return self.chat.id

    @property
    def chat_title(self) -> str:
        """Chat title, for `supergroups`, `channels` and `group` chats.
        Full name, for `private` chat."""

        return (
            self.chat.full_name.unwrap() if self.chat.type == ChatType.PRIVATE else self.chat.title.unwrap()
        )


class MessageId(Model):
    """Object `MessageId`, see the [documentation](https://core.telegram.org/bots/api#messageid).

    This object represents a unique message identifier.
    """

    message_id: int
    """Unique message identifier."""


class InaccessibleMessage(MaybeInaccessibleMessage):
    """Object `InaccessibleMessage`, see the [documentation](https://core.telegram.org/bots/api#inaccessiblemessage).

    This object describes a message that was deleted or is otherwise inaccessible to the bot.
    """

    chat: "Chat"
    """Chat the message belonged to."""

    message_id: int
    """Unique message identifier inside the chat."""

    date: typing.Literal[0]
    """Always 0. The field can be used to differentiate regular and inaccessible
    messages."""


class MessageEntity(Model):
    """Object `MessageEntity`, see the [documentation](https://core.telegram.org/bots/api#messageentity).

    This object represents one special entity in a text message. For example, hashtags, usernames, URLs, etc.
    """

    type: MessageEntityType
    """Type of the entity. Currently, can be `mention` (@username), `hashtag`
    (#hashtag), `cashtag` ($USD), `bot_command` (/start@jobs_bot), `url`
    (https://telegram.org), `email` (do-not-reply@telegram.org), `phone_number`
    (+1-212-555-0123), `bold` (bold text), `italic` (italic text), `underline`
    (underlined text), `strikethrough` (strikethrough text), `spoiler`
    (spoiler message), `blockquote` (block quotation), `expandable_blockquote`
    (collapsed-by-default block quotation), `code` (monowidth string),
    `pre` (monowidth block), `text_link` (for clickable text URLs), `text_mention`
    (for users without usernames), `custom_emoji` (for inline custom emoji
    stickers)."""

    offset: int
    """Offset in UTF-16 code units to the start of the entity."""

    length: int
    """Length of the entity in UTF-16 code units."""

    url: Option[str] = Nothing
    """Optional. For `text_link` only, URL that will be opened after user taps
    on the text."""

    user: Option["User"] = Nothing
    """Optional. For `text_mention` only, the mentioned user."""

    language: Option[str] = Nothing
    """Optional. For `pre` only, the programming language of the entity text."""

    custom_emoji_id: Option[str] = Nothing
    """Optional. For `custom_emoji` only, unique identifier of the custom emoji.
    Use getCustomEmojiStickers to get full information about the sticker."""


class TextQuote(Model):
    """Object `TextQuote`, see the [documentation](https://core.telegram.org/bots/api#textquote).

    This object contains information about the quoted part of a message that is replied to by the given message.
    """

    text: str
    """Text of the quoted part of a message that is replied to by the given message."""

    position: int
    """Approximate quote position in the original message in UTF-16 code units
    as specified by the sender."""

    entities: Option[list["MessageEntity"]] = Nothing
    """Optional. Special entities that appear in the quote. Currently, only bold,
    italic, underline, strikethrough, spoiler, and custom_emoji entities
    are kept in quotes."""

    is_manual: Option[bool] = Nothing
    """Optional. True, if the quote was chosen manually by the message sender.
    Otherwise, the quote was added automatically by the server."""


class ExternalReplyInfo(Model):
    """Object `ExternalReplyInfo`, see the [documentation](https://core.telegram.org/bots/api#externalreplyinfo).

    This object contains information about a message that is being replied to, which may come from another chat or forum topic.
    """

    origin: Variative[
        "MessageOriginUser", "MessageOriginHiddenUser", "MessageOriginChat", "MessageOriginChannel"
    ]
    """Origin of the message replied to by the given message."""

    chat: Option["Chat"] = Nothing
    """Optional. Chat the original message belongs to. Available only if the chat
    is a supergroup or a channel."""

    message_id: Option[int] = Nothing
    """Optional. Unique message identifier inside the original chat. Available
    only if the original chat is a supergroup or a channel."""

    link_preview_options: Option["LinkPreviewOptions"] = Nothing
    """Optional. Options used for link preview generation for the original message,
    if it is a text message."""

    animation: Option["Animation"] = Nothing
    """Optional. Message is an animation, information about the animation."""

    audio: Option["Audio"] = Nothing
    """Optional. Message is an audio file, information about the file."""

    document: Option["Document"] = Nothing
    """Optional. Message is a general file, information about the file."""

    paid_media: Option["PaidMediaInfo"] = Nothing
    """Optional. Message contains paid media; information about the paid media."""

    photo: Option[list["PhotoSize"]] = Nothing
    """Optional. Message is a photo, available sizes of the photo."""

    sticker: Option["Sticker"] = Nothing
    """Optional. Message is a sticker, information about the sticker."""

    story: Option["Story"] = Nothing
    """Optional. Message is a forwarded story."""

    video: Option["Video"] = Nothing
    """Optional. Message is a video, information about the video."""

    video_note: Option["VideoNote"] = Nothing
    """Optional. Message is a video note, information about the video message."""

    voice: Option["Voice"] = Nothing
    """Optional. Message is a voice message, information about the file."""

    has_media_spoiler: Option[bool] = Nothing
    """Optional. True, if the message media is covered by a spoiler animation."""

    contact: Option["Contact"] = Nothing
    """Optional. Message is a shared contact, information about the contact."""

    dice: Option["Dice"] = Nothing
    """Optional. Message is a dice with random value."""

    game: Option["Game"] = Nothing
    """Optional. Message is a game, information about the game. More about games:
    https://core.telegram.org/bots/api#games."""

    giveaway: Option["Giveaway"] = Nothing
    """Optional. Message is a scheduled giveaway, information about the giveaway."""

    giveaway_winners: Option["GiveawayWinners"] = Nothing
    """Optional. A giveaway with public winners was completed."""

    invoice: Option["Invoice"] = Nothing
    """Optional. Message is an invoice for a payment, information about the invoice.
    More about payments: https://core.telegram.org/bots/api#payments."""

    location: Option["Location"] = Nothing
    """Optional. Message is a shared location, information about the location."""

    poll: Option["Poll"] = Nothing
    """Optional. Message is a native poll, information about the poll."""

    venue: Option["Venue"] = Nothing
    """Optional. Message is a venue, information about the venue."""


class ReplyParameters(Model):
    """Object `ReplyParameters`, see the [documentation](https://core.telegram.org/bots/api#replyparameters).

    Describes reply parameters for the message that is being sent.
    """

    message_id: int
    """Identifier of the message that will be replied to in the current chat, or
    in the chat chat_id if it is specified."""

    chat_id: Option[Variative[int, str]] = Nothing
    """Optional. If the message to be replied to is from a different chat, unique
    identifier for the chat or username of the channel (in the format @channelusername).
    Not supported for messages sent on behalf of a business account."""

    allow_sending_without_reply: Option[bool] = Nothing
    """Optional. Pass True if the message should be sent even if the specified message
    to be replied to is not found. Always False for replies in another chat or
    forum topic. Always True for messages sent on behalf of a business account."""

    quote: Option[str] = Nothing
    """Optional. Quoted part of the message to be replied to; 0-1024 characters
    after entities parsing. The quote must be an exact substring of the message
    to be replied to, including bold, italic, underline, strikethrough, spoiler,
    and custom_emoji entities. The message will fail to send if the quote isn't
    found in the original message."""

    quote_parse_mode: Option[str] = Nothing
    """Optional. Mode for parsing entities in the quote. See formatting options
    for more details."""

    quote_entities: Option[list["MessageEntity"]] = Nothing
    """Optional. A JSON-serialized list of special entities that appear in the
    quote. It can be specified instead of quote_parse_mode."""

    quote_position: Option[int] = Nothing
    """Optional. Position of the quote in the original message in UTF-16 code units."""


class MessageOriginUser(MessageOrigin):
    """Object `MessageOriginUser`, see the [documentation](https://core.telegram.org/bots/api#messageoriginuser).

    The message was originally sent by a known user.
    """

    type: typing.Literal["user"]
    """Type of the message origin, always `user`."""

    date: datetime
    """Date the message was sent originally in Unix time."""

    sender_user: "User"
    """User that sent the message originally."""


class MessageOriginHiddenUser(MessageOrigin):
    """Object `MessageOriginHiddenUser`, see the [documentation](https://core.telegram.org/bots/api#messageoriginhiddenuser).

    The message was originally sent by an unknown user.
    """

    type: typing.Literal["hidden_user"]
    """Type of the message origin, always `hidden_user`."""

    date: datetime
    """Date the message was sent originally in Unix time."""

    sender_user_name: str
    """Name of the user that sent the message originally."""


class MessageOriginChat(MessageOrigin):
    """Object `MessageOriginChat`, see the [documentation](https://core.telegram.org/bots/api#messageoriginchat).

    The message was originally sent on behalf of a chat to a group chat.
    """

    type: typing.Literal["chat"]
    """Type of the message origin, always `chat`."""

    date: datetime
    """Date the message was sent originally in Unix time."""

    sender_chat: "Chat"
    """Chat that sent the message originally."""

    author_signature: Option[str] = Nothing
    """Optional. For messages originally sent by an anonymous chat administrator,
    original message author signature."""


class MessageOriginChannel(MessageOrigin):
    """Object `MessageOriginChannel`, see the [documentation](https://core.telegram.org/bots/api#messageoriginchannel).

    The message was originally sent to a channel chat.
    """

    type: typing.Literal["channel"]
    """Type of the message origin, always `channel`."""

    date: datetime
    """Date the message was sent originally in Unix time."""

    chat: "Chat"
    """Channel chat to which the message was originally sent."""

    message_id: int
    """Unique message identifier inside the chat."""

    author_signature: Option[str] = Nothing
    """Optional. Signature of the original post author."""


class PhotoSize(Model):
    """Object `PhotoSize`, see the [documentation](https://core.telegram.org/bots/api#photosize).

    This object represents one size of a photo or a file / sticker thumbnail.
    """

    file_id: str
    """Identifier for this file, which can be used to download or reuse the file."""

    file_unique_id: str
    """Unique identifier for this file, which is supposed to be the same over time
    and for different bots. Can't be used to download or reuse the file."""

    width: int
    """Photo width."""

    height: int
    """Photo height."""

    file_size: Option[int] = Nothing
    """Optional. File size in bytes."""


class Animation(Model):
    """Object `Animation`, see the [documentation](https://core.telegram.org/bots/api#animation).

    This object represents an animation file (GIF or H.264/MPEG-4 AVC video without sound).
    """

    file_id: str
    """Identifier for this file, which can be used to download or reuse the file."""

    file_unique_id: str
    """Unique identifier for this file, which is supposed to be the same over time
    and for different bots. Can't be used to download or reuse the file."""

    width: int
    """Video width as defined by the sender."""

    height: int
    """Video height as defined by the sender."""

    duration: int
    """Duration of the video in seconds as defined by the sender."""

    thumbnail: Option["PhotoSize"] = Nothing
    """Optional. Animation thumbnail as defined by the sender."""

    file_name: Option[str] = Nothing
    """Optional. Original animation filename as defined by the sender."""

    mime_type: Option[str] = Nothing
    """Optional. MIME type of the file as defined by the sender."""

    file_size: Option[int] = Nothing
    """Optional. File size in bytes. It can be bigger than 2^31 and some programming
    languages may have difficulty/silent defects in interpreting it. But
    it has at most 52 significant bits, so a signed 64-bit integer or double-precision
    float type are safe for storing this value."""


class Audio(Model):
    """Object `Audio`, see the [documentation](https://core.telegram.org/bots/api#audio).

    This object represents an audio file to be treated as music by the Telegram clients.
    """

    file_id: str
    """Identifier for this file, which can be used to download or reuse the file."""

    file_unique_id: str
    """Unique identifier for this file, which is supposed to be the same over time
    and for different bots. Can't be used to download or reuse the file."""

    duration: int
    """Duration of the audio in seconds as defined by the sender."""

    performer: Option[str] = Nothing
    """Optional. Performer of the audio as defined by the sender or by audio tags."""

    title: Option[str] = Nothing
    """Optional. Title of the audio as defined by the sender or by audio tags."""

    file_name: Option[str] = Nothing
    """Optional. Original filename as defined by the sender."""

    mime_type: Option[str] = Nothing
    """Optional. MIME type of the file as defined by the sender."""

    file_size: Option[int] = Nothing
    """Optional. File size in bytes. It can be bigger than 2^31 and some programming
    languages may have difficulty/silent defects in interpreting it. But
    it has at most 52 significant bits, so a signed 64-bit integer or double-precision
    float type are safe for storing this value."""

    thumbnail: Option["PhotoSize"] = Nothing
    """Optional. Thumbnail of the album cover to which the music file belongs."""


class Document(Model):
    """Object `Document`, see the [documentation](https://core.telegram.org/bots/api#document).

    This object represents a general file (as opposed to photos, voice messages and audio files).
    """

    file_id: str
    """Identifier for this file, which can be used to download or reuse the file."""

    file_unique_id: str
    """Unique identifier for this file, which is supposed to be the same over time
    and for different bots. Can't be used to download or reuse the file."""

    thumbnail: Option["PhotoSize"] = Nothing
    """Optional. Document thumbnail as defined by the sender."""

    file_name: Option[str] = Nothing
    """Optional. Original filename as defined by the sender."""

    mime_type: Option[str] = Nothing
    """Optional. MIME type of the file as defined by the sender."""

    file_size: Option[int] = Nothing
    """Optional. File size in bytes. It can be bigger than 2^31 and some programming
    languages may have difficulty/silent defects in interpreting it. But
    it has at most 52 significant bits, so a signed 64-bit integer or double-precision
    float type are safe for storing this value."""


class Story(Model):
    """Object `Story`, see the [documentation](https://core.telegram.org/bots/api#story).

    This object represents a story.
    """

    chat: "Chat"
    """Chat that posted the story."""

    id: int
    """Unique identifier for the story in the chat."""


class Video(Model):
    """Object `Video`, see the [documentation](https://core.telegram.org/bots/api#video).

    This object represents a video file.
    """

    file_id: str
    """Identifier for this file, which can be used to download or reuse the file."""

    file_unique_id: str
    """Unique identifier for this file, which is supposed to be the same over time
    and for different bots. Can't be used to download or reuse the file."""

    width: int
    """Video width as defined by the sender."""

    height: int
    """Video height as defined by the sender."""

    duration: int
    """Duration of the video in seconds as defined by the sender."""

    thumbnail: Option["PhotoSize"] = Nothing
    """Optional. Video thumbnail."""

    file_name: Option[str] = Nothing
    """Optional. Original filename as defined by the sender."""

    mime_type: Option[str] = Nothing
    """Optional. MIME type of the file as defined by the sender."""

    file_size: Option[int] = Nothing
    """Optional. File size in bytes. It can be bigger than 2^31 and some programming
    languages may have difficulty/silent defects in interpreting it. But
    it has at most 52 significant bits, so a signed 64-bit integer or double-precision
    float type are safe for storing this value."""


class VideoNote(Model):
    """Object `VideoNote`, see the [documentation](https://core.telegram.org/bots/api#videonote).

    This object represents a video message (available in Telegram apps as of v.4.0).
    """

    file_id: str
    """Identifier for this file, which can be used to download or reuse the file."""

    file_unique_id: str
    """Unique identifier for this file, which is supposed to be the same over time
    and for different bots. Can't be used to download or reuse the file."""

    length: int
    """Video width and height (diameter of the video message) as defined by the
    sender."""

    duration: int
    """Duration of the video in seconds as defined by the sender."""

    thumbnail: Option["PhotoSize"] = Nothing
    """Optional. Video thumbnail."""

    file_size: Option[int] = Nothing
    """Optional. File size in bytes."""


class Voice(Model):
    """Object `Voice`, see the [documentation](https://core.telegram.org/bots/api#voice).

    This object represents a voice note.
    """

    file_id: str
    """Identifier for this file, which can be used to download or reuse the file."""

    file_unique_id: str
    """Unique identifier for this file, which is supposed to be the same over time
    and for different bots. Can't be used to download or reuse the file."""

    duration: int
    """Duration of the audio in seconds as defined by the sender."""

    mime_type: Option[str] = Nothing
    """Optional. MIME type of the file as defined by the sender."""

    file_size: Option[int] = Nothing
    """Optional. File size in bytes. It can be bigger than 2^31 and some programming
    languages may have difficulty/silent defects in interpreting it. But
    it has at most 52 significant bits, so a signed 64-bit integer or double-precision
    float type are safe for storing this value."""


class PaidMediaInfo(Model):
    """Object `PaidMediaInfo`, see the [documentation](https://core.telegram.org/bots/api#paidmediainfo).

    Describes the paid media added to a message.
    """

    star_count: int
    """The number of Telegram Stars that must be paid to buy access to the media."""

    paid_media: list[Variative["PaidMediaPreview", "PaidMediaPhoto", "PaidMediaVideo"]]
    """Information about the paid media."""


class PaidMediaPreview(PaidMedia):
    """Object `PaidMediaPreview`, see the [documentation](https://core.telegram.org/bots/api#paidmediapreview).

    The paid media isn't available before the payment.
    """

    type: typing.Literal["preview"]
    """Type of the paid media, always `preview`."""

    width: Option[int] = Nothing
    """Optional. Media width as defined by the sender."""

    height: Option[int] = Nothing
    """Optional. Media height as defined by the sender."""

    duration: Option[int] = Nothing
    """Optional. Duration of the media in seconds as defined by the sender."""


class PaidMediaPhoto(PaidMedia):
    """Object `PaidMediaPhoto`, see the [documentation](https://core.telegram.org/bots/api#paidmediaphoto).

    The paid media is a photo.
    """

    type: typing.Literal["photo"]
    """Type of the paid media, always `photo`."""

    photo: list["PhotoSize"]
    """The photo."""


class PaidMediaVideo(PaidMedia):
    """Object `PaidMediaVideo`, see the [documentation](https://core.telegram.org/bots/api#paidmediavideo).

    The paid media is a video.
    """

    type: typing.Literal["video"]
    """Type of the paid media, always `video`."""

    video: "Video"
    """The video."""


class Contact(Model):
    """Object `Contact`, see the [documentation](https://core.telegram.org/bots/api#contact).

    This object represents a phone contact.
    """

    phone_number: str
    """Contact's phone number."""

    first_name: str
    """Contact's first name."""

    last_name: Option[str] = Nothing
    """Optional. Contact's last name."""

    user_id: Option[int] = Nothing
    """Optional. Contact's user identifier in Telegram. This number may have
    more than 32 significant bits and some programming languages may have difficulty/silent
    defects in interpreting it. But it has at most 52 significant bits, so a 64-bit
    integer or double-precision float type are safe for storing this identifier."""

    vcard: Option[str] = Nothing
    """Optional. Additional data about the contact in the form of a vCard."""


class Dice(Model):
    """Object `Dice`, see the [documentation](https://core.telegram.org/bots/api#dice).

    This object represents an animated emoji that displays a random value.
    """

    emoji: DiceEmoji
    """Emoji on which the dice throw animation is based."""

    value: int
    """Value of the dice, 1-6 for `🎲`, `🎯` and `🎳` base emoji, 1-5 for `🏀` and `⚽` base
    emoji, 1-64 for `🎰` base emoji."""


class PollOption(Model):
    """Object `PollOption`, see the [documentation](https://core.telegram.org/bots/api#polloption).

    This object contains information about one answer option in a poll.
    """

    text: str
    """Option text, 1-100 characters."""

    voter_count: int
    """Number of users that voted for this option."""

    text_entities: Option[list["MessageEntity"]] = Nothing
    """Optional. Special entities that appear in the option text. Currently,
    only custom emoji entities are allowed in poll option texts."""


class InputPollOption(Model):
    """Object `InputPollOption`, see the [documentation](https://core.telegram.org/bots/api#inputpolloption).

    This object contains information about one answer option in a poll to be sent.
    """

    text: str
    """Option text, 1-100 characters."""

    text_parse_mode: Option[str] = Nothing
    """Optional. Mode for parsing entities in the text. See formatting options
    for more details. Currently, only custom emoji entities are allowed."""

    text_entities: Option[list["MessageEntity"]] = Nothing
    """Optional. A JSON-serialized list of special entities that appear in the
    poll option text. It can be specified instead of text_parse_mode."""


class PollAnswer(Model):
    """Object `PollAnswer`, see the [documentation](https://core.telegram.org/bots/api#pollanswer).

    This object represents an answer of a user in a non-anonymous poll.
    """

    poll_id: str
    """Unique poll identifier."""

    option_ids: list[int]
    """0-based identifiers of chosen answer options. May be empty if the vote was
    retracted."""

    voter_chat: Option["Chat"] = Nothing
    """Optional. The chat that changed the answer to the poll, if the voter is anonymous."""

    user: Option["User"] = Nothing
    """Optional. The user that changed the answer to the poll, if the voter isn't
    anonymous."""


class Poll(Model):
    """Object `Poll`, see the [documentation](https://core.telegram.org/bots/api#poll).

    This object contains information about a poll.
    """

    id: str
    """Unique poll identifier."""

    question: str
    """Poll question, 1-300 characters."""

    options: list["PollOption"]
    """List of poll options."""

    total_voter_count: int
    """Total number of users that voted in the poll."""

    is_closed: bool
    """True, if the poll is closed."""

    is_anonymous: bool
    """True, if the poll is anonymous."""

    type: typing.Literal["regular", "quiz"]
    """Poll type, currently can be `regular` or `quiz`."""

    allows_multiple_answers: bool
    """True, if the poll allows multiple answers."""

    question_entities: Option[list["MessageEntity"]] = Nothing
    """Optional. Special entities that appear in the question. Currently, only
    custom emoji entities are allowed in poll questions."""

    correct_option_id: Option[int] = Nothing
    """Optional. 0-based identifier of the correct answer option. Available
    only for polls in the quiz mode, which are closed, or was sent (not forwarded)
    by the bot or to the private chat with the bot."""

    explanation: Option[str] = Nothing
    """Optional. Text that is shown when a user chooses an incorrect answer or taps
    on the lamp icon in a quiz-style poll, 0-200 characters."""

    explanation_entities: Option[list["MessageEntity"]] = Nothing
    """Optional. Special entities like usernames, URLs, bot commands, etc. that
    appear in the explanation."""

    open_period: Option[int] = Nothing
    """Optional. Amount of time in seconds the poll will be active after creation."""

    close_date: Option[datetime] = Nothing
    """Optional. Point in time (Unix timestamp) when the poll will be automatically
    closed."""


class Location(Model):
    """Object `Location`, see the [documentation](https://core.telegram.org/bots/api#location).

    This object represents a point on the map.
    """

    latitude: float
    """Latitude as defined by the sender."""

    longitude: float
    """Longitude as defined by the sender."""

    horizontal_accuracy: Option[float] = Nothing
    """Optional. The radius of uncertainty for the location, measured in meters;
    0-1500."""

    live_period: Option[int] = Nothing
    """Optional. Time relative to the message sending date, during which the location
    can be updated; in seconds. For active live locations only."""

    heading: Option[int] = Nothing
    """Optional. The direction in which user is moving, in degrees; 1-360. For
    active live locations only."""

    proximity_alert_radius: Option[int] = Nothing
    """Optional. The maximum distance for proximity alerts about approaching
    another chat member, in meters. For sent live locations only."""


class Venue(Model):
    """Object `Venue`, see the [documentation](https://core.telegram.org/bots/api#venue).

    This object represents a venue.
    """

    location: "Location"
    """Venue location. Can't be a live location."""

    title: str
    """Name of the venue."""

    address: str
    """Address of the venue."""

    foursquare_id: Option[str] = Nothing
    """Optional. Foursquare identifier of the venue."""

    foursquare_type: Option[str] = Nothing
    """Optional. Foursquare type of the venue. (For example, `arts_entertainment/default`,
    `arts_entertainment/aquarium` or `food/icecream`.)."""

    google_place_id: Option[str] = Nothing
    """Optional. Google Places identifier of the venue."""

    google_place_type: Option[str] = Nothing
    """Optional. Google Places type of the venue. (See supported types.)."""


class WebAppData(Model):
    """Object `WebAppData`, see the [documentation](https://core.telegram.org/bots/api#webappdata).

    Describes data sent from a Web App to the bot.
    """

    data: str
    """The data. Be aware that a bad client can send arbitrary data in this field."""

    button_text: str
    """Text of the web_app keyboard button from which the Web App was opened. Be
    aware that a bad client can send arbitrary data in this field."""


class ProximityAlertTriggered(Model):
    """Object `ProximityAlertTriggered`, see the [documentation](https://core.telegram.org/bots/api#proximityalerttriggered).

    This object represents the content of a service message, sent whenever a user in the chat triggers a proximity alert set by another user.
    """

    traveler: "User"
    """User that triggered the alert."""

    watcher: "User"
    """User that set the alert."""

    distance: int
    """The distance between the users."""


class MessageAutoDeleteTimerChanged(Model):
    """Object `MessageAutoDeleteTimerChanged`, see the [documentation](https://core.telegram.org/bots/api#messageautodeletetimerchanged).

    This object represents a service message about a change in auto-delete timer settings.
    """

    message_auto_delete_time: int
    """New auto-delete time for messages in the chat; in seconds."""


class ChatBoostAdded(Model):
    """Object `ChatBoostAdded`, see the [documentation](https://core.telegram.org/bots/api#chatboostadded).

    This object represents a service message about a user boosting a chat.
    """

    boost_count: int
    """Number of boosts added by the user."""


class BackgroundFillSolid(BackgroundFill):
    """Object `BackgroundFillSolid`, see the [documentation](https://core.telegram.org/bots/api#backgroundfillsolid).

    The background is filled using the selected color.
    """

    type: typing.Literal["solid"]
    """Type of the background fill, always `solid`."""

    color: int
    """The color of the background fill in the RGB24 format."""


class BackgroundFillGradient(BackgroundFill):
    """Object `BackgroundFillGradient`, see the [documentation](https://core.telegram.org/bots/api#backgroundfillgradient).

    The background is a gradient fill.
    """

    type: typing.Literal["gradient"]
    """Type of the background fill, always `gradient`."""

    top_color: int
    """Top color of the gradient in the RGB24 format."""

    bottom_color: int
    """Bottom color of the gradient in the RGB24 format."""

    rotation_angle: int
    """Clockwise rotation angle of the background fill in degrees; 0-359."""


class BackgroundFillFreeformGradient(BackgroundFill):
    """Object `BackgroundFillFreeformGradient`, see the [documentation](https://core.telegram.org/bots/api#backgroundfillfreeformgradient).

    The background is a freeform gradient that rotates after every message in the chat.
    """

    type: typing.Literal["freeform_gradient"]
    """Type of the background fill, always `freeform_gradient`."""

    colors: list[int]
    """A list of the 3 or 4 base colors that are used to generate the freeform gradient
    in the RGB24 format."""


class BackgroundTypeFill(BackgroundType):
    """Object `BackgroundTypeFill`, see the [documentation](https://core.telegram.org/bots/api#backgroundtypefill).

    The background is automatically filled based on the selected colors.
    """

    type: typing.Literal["fill"]
    """Type of the background, always `fill`."""

    fill: Variative["BackgroundFillSolid", "BackgroundFillGradient", "BackgroundFillFreeformGradient"]
    """The background fill."""

    dark_theme_dimming: int
    """Dimming of the background in dark themes, as a percentage; 0-100."""


class BackgroundTypeWallpaper(BackgroundType):
    """Object `BackgroundTypeWallpaper`, see the [documentation](https://core.telegram.org/bots/api#backgroundtypewallpaper).

    The background is a wallpaper in the JPEG format.
    """

    type: typing.Literal["wallpaper"]
    """Type of the background, always `wallpaper`."""

    document: "Document"
    """Document with the wallpaper."""

    dark_theme_dimming: int
    """Dimming of the background in dark themes, as a percentage; 0-100."""

    is_blurred: Option[bool] = Nothing
    """Optional. True, if the wallpaper is downscaled to fit in a 450x450 square
    and then box-blurred with radius 12."""

    is_moving: Option[bool] = Nothing
    """Optional. True, if the background moves slightly when the device is tilted."""


class BackgroundTypePattern(BackgroundType):
    """Object `BackgroundTypePattern`, see the [documentation](https://core.telegram.org/bots/api#backgroundtypepattern).

    The background is a PNG or TGV (gzipped subset of SVG with MIME type "application/x-tgwallpattern") pattern to be combined with the background fill chosen by the user.
    """

    type: typing.Literal["pattern"]
    """Type of the background, always `pattern`."""

    document: "Document"
    """Document with the pattern."""

    fill: Variative["BackgroundFillSolid", "BackgroundFillGradient", "BackgroundFillFreeformGradient"]
    """The background fill that is combined with the pattern."""

    intensity: int
    """Intensity of the pattern when it is shown above the filled background; 0-100."""

    is_inverted: Option[bool] = Nothing
    """Optional. True, if the background fill must be applied only to the pattern
    itself. All other pixels are black in this case. For dark themes only."""

    is_moving: Option[bool] = Nothing
    """Optional. True, if the background moves slightly when the device is tilted."""


class BackgroundTypeChatTheme(BackgroundType):
    """Object `BackgroundTypeChatTheme`, see the [documentation](https://core.telegram.org/bots/api#backgroundtypechattheme).

    The background is taken directly from a built-in chat theme.
    """

    type: typing.Literal["chat_theme"]
    """Type of the background, always `chat_theme`."""

    theme_name: str
    """Name of the chat theme, which is usually an emoji."""


class ChatBackground(Model):
    """Object `ChatBackground`, see the [documentation](https://core.telegram.org/bots/api#chatbackground).

    This object represents a chat background.
    """

    type: Variative[
        "BackgroundTypeFill", "BackgroundTypeWallpaper", "BackgroundTypePattern", "BackgroundTypeChatTheme"
    ]
    """Type of the background."""


class ForumTopicCreated(Model):
    """Object `ForumTopicCreated`, see the [documentation](https://core.telegram.org/bots/api#forumtopiccreated).

    This object represents a service message about a new forum topic created in the chat.
    """

    name: str
    """Name of the topic."""

    icon_color: TopicIconColor
    """Color of the topic icon in RGB format."""

    icon_custom_emoji_id: Option[str] = Nothing
    """Optional. Unique identifier of the custom emoji shown as the topic icon."""


class ForumTopicClosed(Model):
    """Object `ForumTopicClosed`, see the [documentation](https://core.telegram.org/bots/api#forumtopicclosed).

    This object represents a service message about a forum topic closed in the chat. Currently holds no information.
    """


class ForumTopicEdited(Model):
    """Object `ForumTopicEdited`, see the [documentation](https://core.telegram.org/bots/api#forumtopicedited).

    This object represents a service message about an edited forum topic.
    """

    name: Option[str] = Nothing
    """Optional. New name of the topic, if it was edited."""

    icon_custom_emoji_id: Option[str] = Nothing
    """Optional. New identifier of the custom emoji shown as the topic icon, if
    it was edited; an empty string if the icon was removed."""


class ForumTopicReopened(Model):
    """Object `ForumTopicReopened`, see the [documentation](https://core.telegram.org/bots/api#forumtopicreopened).

    This object represents a service message about a forum topic reopened in the chat. Currently holds no information.
    """


class GeneralForumTopicHidden(Model):
    """Object `GeneralForumTopicHidden`, see the [documentation](https://core.telegram.org/bots/api#generalforumtopichidden).

    This object represents a service message about General forum topic hidden in the chat. Currently holds no information.
    """


class GeneralForumTopicUnhidden(Model):
    """Object `GeneralForumTopicUnhidden`, see the [documentation](https://core.telegram.org/bots/api#generalforumtopicunhidden).

    This object represents a service message about General forum topic unhidden in the chat. Currently holds no information.
    """


class SharedUser(Model):
    """Object `SharedUser`, see the [documentation](https://core.telegram.org/bots/api#shareduser).

    This object contains information about a user that was shared with the bot using a KeyboardButtonRequestUsers button.
    """

    user_id: int
    """Identifier of the shared user. This number may have more than 32 significant
    bits and some programming languages may have difficulty/silent defects
    in interpreting it. But it has at most 52 significant bits, so 64-bit integers
    or double-precision float types are safe for storing these identifiers.
    The bot may not have access to the user and could be unable to use this identifier,
    unless the user is already known to the bot by some other means."""

    first_name: Option[str] = Nothing
    """Optional. First name of the user, if the name was requested by the bot."""

    last_name: Option[str] = Nothing
    """Optional. Last name of the user, if the name was requested by the bot."""

    username: Option[str] = Nothing
    """Optional. Username of the user, if the username was requested by the bot."""

    photo: Option[list["PhotoSize"]] = Nothing
    """Optional. Available sizes of the chat photo, if the photo was requested
    by the bot."""


class UsersShared(Model):
    """Object `UsersShared`, see the [documentation](https://core.telegram.org/bots/api#usersshared).

    This object contains information about the users whose identifiers were shared with the bot using a KeyboardButtonRequestUsers button.
    """

    request_id: int
    """Identifier of the request."""

    users: list["SharedUser"]
    """Information about users shared with the bot."""


class ChatShared(Model):
    """Object `ChatShared`, see the [documentation](https://core.telegram.org/bots/api#chatshared).

    This object contains information about a chat that was shared with the bot using a KeyboardButtonRequestChat button.
    """

    request_id: int
    """Identifier of the request."""

    chat_id: int
    """Identifier of the shared chat. This number may have more than 32 significant
    bits and some programming languages may have difficulty/silent defects
    in interpreting it. But it has at most 52 significant bits, so a 64-bit integer
    or double-precision float type are safe for storing this identifier. The
    bot may not have access to the chat and could be unable to use this identifier,
    unless the chat is already known to the bot by some other means."""

    title: Option[str] = Nothing
    """Optional. Title of the chat, if the title was requested by the bot."""

    username: Option[str] = Nothing
    """Optional. Username of the chat, if the username was requested by the bot
    and available."""

    photo: Option[list["PhotoSize"]] = Nothing
    """Optional. Available sizes of the chat photo, if the photo was requested
    by the bot."""


class WriteAccessAllowed(Model):
    """Object `WriteAccessAllowed`, see the [documentation](https://core.telegram.org/bots/api#writeaccessallowed).

    This object represents a service message about a user allowing a bot to write messages after adding it to the attachment menu, launching a Web App from a link, or accepting an explicit request from a Web App sent by the method requestWriteAccess.
    """

    from_request: Option[bool] = Nothing
    """Optional. True, if the access was granted after the user accepted an explicit
    request from a Web App sent by the method requestWriteAccess."""

    web_app_name: Option[str] = Nothing
    """Optional. Name of the Web App, if the access was granted when the Web App was
    launched from a link."""

    from_attachment_menu: Option[bool] = Nothing
    """Optional. True, if the access was granted when the bot was added to the attachment
    or side menu."""


class VideoChatScheduled(Model):
    """Object `VideoChatScheduled`, see the [documentation](https://core.telegram.org/bots/api#videochatscheduled).

    This object represents a service message about a video chat scheduled in the chat.
    """

    start_date: datetime
    """Point in time (Unix timestamp) when the video chat is supposed to be started
    by a chat administrator."""


class VideoChatStarted(Model):
    """Object `VideoChatStarted`, see the [documentation](https://core.telegram.org/bots/api#videochatstarted).

    This object represents a service message about a video chat started in the chat. Currently holds no information.
    """


class VideoChatEnded(Model):
    """Object `VideoChatEnded`, see the [documentation](https://core.telegram.org/bots/api#videochatended).

    This object represents a service message about a video chat ended in the chat.
    """

    duration: int
    """Video chat duration in seconds."""


class VideoChatParticipantsInvited(Model):
    """Object `VideoChatParticipantsInvited`, see the [documentation](https://core.telegram.org/bots/api#videochatparticipantsinvited).

    This object represents a service message about new members invited to a video chat.
    """

    users: list["User"]
    """New members that were invited to the video chat."""


class GiveawayCreated(Model):
    """Object `GiveawayCreated`, see the [documentation](https://core.telegram.org/bots/api#giveawaycreated).

    This object represents a service message about the creation of a scheduled giveaway. Currently holds no information.
    """


class Giveaway(Model):
    """Object `Giveaway`, see the [documentation](https://core.telegram.org/bots/api#giveaway).

    This object represents a message about a scheduled giveaway.
    """

    chats: list["Chat"]
    """The list of chats which the user must join to participate in the giveaway."""

    winners_selection_date: datetime
    """Point in time (Unix timestamp) when winners of the giveaway will be selected."""

    winner_count: int
    """The number of users which are supposed to be selected as winners of the giveaway."""

    only_new_members: Option[bool] = Nothing
    """Optional. True, if only users who join the chats after the giveaway started
    should be eligible to win."""

    has_public_winners: Option[bool] = Nothing
    """Optional. True, if the list of giveaway winners will be visible to everyone."""

    prize_description: Option[str] = Nothing
    """Optional. Description of additional giveaway prize."""

    country_codes: Option[list[str]] = Nothing
    """Optional. A list of two-letter ISO 3166-1 alpha-2 country codes indicating
    the countries from which eligible users for the giveaway must come. If empty,
    then all users can participate in the giveaway. Users with a phone number
    that was bought on Fragment can always participate in giveaways."""

    premium_subscription_month_count: Option[int] = Nothing
    """Optional. The number of months the Telegram Premium subscription won from
    the giveaway will be active for."""


class GiveawayWinners(Model):
    """Object `GiveawayWinners`, see the [documentation](https://core.telegram.org/bots/api#giveawaywinners).

    This object represents a message about the completion of a giveaway with public winners.
    """

    chat: "Chat"
    """The chat that created the giveaway."""

    giveaway_message_id: int
    """Identifier of the message with the giveaway in the chat."""

    winners_selection_date: datetime
    """Point in time (Unix timestamp) when winners of the giveaway were selected."""

    winner_count: int
    """Total number of winners in the giveaway."""

    winners: list["User"]
    """List of up to 100 winners of the giveaway."""

    additional_chat_count: Option[int] = Nothing
    """Optional. The number of other chats the user had to join in order to be eligible
    for the giveaway."""

    premium_subscription_month_count: Option[int] = Nothing
    """Optional. The number of months the Telegram Premium subscription won from
    the giveaway will be active for."""

    unclaimed_prize_count: Option[int] = Nothing
    """Optional. Number of undistributed prizes."""

    only_new_members: Option[bool] = Nothing
    """Optional. True, if only users who had joined the chats after the giveaway
    started were eligible to win."""

    was_refunded: Option[bool] = Nothing
    """Optional. True, if the giveaway was canceled because the payment for it
    was refunded."""

    prize_description: Option[str] = Nothing
    """Optional. Description of additional giveaway prize."""


class GiveawayCompleted(Model):
    """Object `GiveawayCompleted`, see the [documentation](https://core.telegram.org/bots/api#giveawaycompleted).

    This object represents a service message about the completion of a giveaway without public winners.
    """

    winner_count: int
    """Number of winners in the giveaway."""

    unclaimed_prize_count: Option[int] = Nothing
    """Optional. Number of undistributed prizes."""

    giveaway_message: Option["Message"] = Nothing
    """Optional. Message with the giveaway that was completed, if it wasn't deleted."""


class LinkPreviewOptions(Model):
    """Object `LinkPreviewOptions`, see the [documentation](https://core.telegram.org/bots/api#linkpreviewoptions).

    Describes the options used for link preview generation.
    """

    is_disabled: Option[bool] = Nothing
    """Optional. True, if the link preview is disabled."""

    url: Option[str] = Nothing
    """Optional. URL to use for the link preview. If empty, then the first URL found
    in the message text will be used."""

    prefer_small_media: Option[bool] = Nothing
    """Optional. True, if the media in the link preview is supposed to be shrunk;
    ignored if the URL isn't explicitly specified or media size change isn't
    supported for the preview."""

    prefer_large_media: Option[bool] = Nothing
    """Optional. True, if the media in the link preview is supposed to be enlarged;
    ignored if the URL isn't explicitly specified or media size change isn't
    supported for the preview."""

    show_above_text: Option[bool] = Nothing
    """Optional. True, if the link preview must be shown above the message text;
    otherwise, the link preview will be shown below the message text."""


class UserProfilePhotos(Model):
    """Object `UserProfilePhotos`, see the [documentation](https://core.telegram.org/bots/api#userprofilephotos).

    This object represent a user's profile pictures.
    """

    total_count: int
    """Total number of profile pictures the target user has."""

    photos: list[list["PhotoSize"]]
    """Requested profile pictures (in up to 4 sizes each)."""


class File(Model):
    """Object `File`, see the [documentation](https://core.telegram.org/bots/api#file).

    This object represents a file ready to be downloaded. The file can be downloaded via the link https://api.telegram.org/file/bot<token>/<file_path>. It is guaranteed that the link will be valid for at least 1 hour. When the link expires, a new one can be requested by calling getFile.
    """

    file_id: str
    """Identifier for this file, which can be used to download or reuse the file."""

    file_unique_id: str
    """Unique identifier for this file, which is supposed to be the same over time
    and for different bots. Can't be used to download or reuse the file."""

    file_size: Option[int] = Nothing
    """Optional. File size in bytes. It can be bigger than 2^31 and some programming
    languages may have difficulty/silent defects in interpreting it. But
    it has at most 52 significant bits, so a signed 64-bit integer or double-precision
    float type are safe for storing this value."""

    file_path: Option[str] = Nothing
    """Optional. File path. Use https://api.telegram.org/file/bot<token>/<file_path>
    to get the file."""


class WebAppInfo(Model):
    """Object `WebAppInfo`, see the [documentation](https://core.telegram.org/bots/api#webappinfo).

    Describes a Web App.
    """

    url: str
    """An HTTPS URL of a Web App to be opened with additional data as specified in
    Initializing Web Apps."""


class ReplyKeyboardMarkup(Model):
    """Object `ReplyKeyboardMarkup`, see the [documentation](https://core.telegram.org/bots/api#replykeyboardmarkup).

    This object represents a custom keyboard with reply options (see Introduction to bots for details and examples). Not supported in channels and for messages sent on behalf of a Telegram Business account.
    """

    keyboard: list[list["KeyboardButton"]]
    """Array of button rows, each represented by an Array of KeyboardButton objects."""

    is_persistent: Option[bool] = Nothing
    """Optional. Requests clients to always show the keyboard when the regular
    keyboard is hidden. Defaults to false, in which case the custom keyboard
    can be hidden and opened with a keyboard icon."""

    resize_keyboard: Option[bool] = Nothing
    """Optional. Requests clients to resize the keyboard vertically for optimal
    fit (e.g., make the keyboard smaller if there are just two rows of buttons).
    Defaults to false, in which case the custom keyboard is always of the same
    height as the app's standard keyboard."""

    one_time_keyboard: Option[bool] = Nothing
    """Optional. Requests clients to hide the keyboard as soon as it's been used.
    The keyboard will still be available, but clients will automatically display
    the usual letter-keyboard in the chat - the user can press a special button
    in the input field to see the custom keyboard again. Defaults to false."""

    input_field_placeholder: Option[str] = Nothing
    """Optional. The placeholder to be shown in the input field when the keyboard
    is active; 1-64 characters."""

    selective: Option[bool] = Nothing
    """Optional. Use this parameter if you want to show the keyboard to specific
    users only. Targets: 1) users that are @mentioned in the text of the Message
    object; 2) if the bot's message is a reply to a message in the same chat and
    forum topic, sender of the original message. Example: A user requests to
    change the bot's language, bot replies to the request with a keyboard to
    select the new language. Other users in the group don't see the keyboard."""

    @property
    def empty_markup(self) -> "ReplyKeyboardRemove":
        """Empty keyboard to remove the custom keyboard."""

        return ReplyKeyboardRemove(remove_keyboard=True, selective=self.selective)


class KeyboardButton(Model):
    """Object `KeyboardButton`, see the [documentation](https://core.telegram.org/bots/api#keyboardbutton).

    This object represents one button of the reply keyboard. At most one of the optional fields must be used to specify type of the button. For simple text buttons, String can be used instead of this object to specify the button text.
    Note: request_users and request_chat options will only work in Telegram versions released after 3 February, 2023. Older clients will display unsupported message.
    """

    text: str
    """Text of the button. If none of the optional fields are used, it will be sent
    as a message when the button is pressed."""

    request_users: Option["KeyboardButtonRequestUsers"] = Nothing
    """Optional. If specified, pressing the button will open a list of suitable
    users. Identifiers of selected users will be sent to the bot in a `users_shared`
    service message. Available in private chats only."""

    request_chat: Option["KeyboardButtonRequestChat"] = Nothing
    """Optional. If specified, pressing the button will open a list of suitable
    chats. Tapping on a chat will send its identifier to the bot in a `chat_shared`
    service message. Available in private chats only."""

    request_contact: Option[bool] = Nothing
    """Optional. If True, the user's phone number will be sent as a contact when
    the button is pressed. Available in private chats only."""

    request_location: Option[bool] = Nothing
    """Optional. If True, the user's current location will be sent when the button
    is pressed. Available in private chats only."""

    request_poll: Option["KeyboardButtonPollType"] = Nothing
    """Optional. If specified, the user will be asked to create a poll and send it
    to the bot when the button is pressed. Available in private chats only."""

    web_app: Option["WebAppInfo"] = Nothing
    """Optional. If specified, the described Web App will be launched when the
    button is pressed. The Web App will be able to send a `web_app_data` service
    message. Available in private chats only."""


class KeyboardButtonRequestUsers(Model):
    """Object `KeyboardButtonRequestUsers`, see the [documentation](https://core.telegram.org/bots/api#keyboardbuttonrequestusers).

    This object defines the criteria used to request suitable users. Information about the selected users will be shared with the bot when the corresponding button is pressed. More about requesting users: https://core.telegram.org/bots/features#chat-and-user-selection
    """

    request_id: int
    """Signed 32-bit identifier of the request that will be received back in the
    UsersShared object. Must be unique within the message."""

    user_is_bot: Option[bool] = Nothing
    """Optional. Pass True to request bots, pass False to request regular users.
    If not specified, no additional restrictions are applied."""

    user_is_premium: Option[bool] = Nothing
    """Optional. Pass True to request premium users, pass False to request non-premium
    users. If not specified, no additional restrictions are applied."""

    max_quantity: Option[int] = Nothing
    """Optional. The maximum number of users to be selected; 1-10. Defaults to
    1."""

    request_name: Option[bool] = Nothing
    """Optional. Pass True to request the users' first and last names."""

    request_username: Option[bool] = Nothing
    """Optional. Pass True to request the users' usernames."""

    request_photo: Option[bool] = Nothing
    """Optional. Pass True to request the users' photos."""


class KeyboardButtonRequestChat(Model):
    """Object `KeyboardButtonRequestChat`, see the [documentation](https://core.telegram.org/bots/api#keyboardbuttonrequestchat).

    This object defines the criteria used to request a suitable chat. Information about the selected chat will be shared with the bot when the corresponding button is pressed. The bot will be granted requested rights in the chat if appropriate. More about requesting chats: https://core.telegram.org/bots/features#chat-and-user-selection.
    """

    request_id: int
    """Signed 32-bit identifier of the request, which will be received back in
    the ChatShared object. Must be unique within the message."""

    chat_is_channel: bool
    """Pass True to request a channel chat, pass False to request a group or a supergroup
    chat."""

    chat_is_forum: Option[bool] = Nothing
    """Optional. Pass True to request a forum supergroup, pass False to request
    a non-forum chat. If not specified, no additional restrictions are applied."""

    chat_has_username: Option[bool] = Nothing
    """Optional. Pass True to request a supergroup or a channel with a username,
    pass False to request a chat without a username. If not specified, no additional
    restrictions are applied."""

    chat_is_created: Option[bool] = Nothing
    """Optional. Pass True to request a chat owned by the user. Otherwise, no additional
    restrictions are applied."""

    user_administrator_rights: Option["ChatAdministratorRights"] = Nothing
    """Optional. A JSON-serialized object listing the required administrator
    rights of the user in the chat. The rights must be a superset of bot_administrator_rights.
    If not specified, no additional restrictions are applied."""

    bot_administrator_rights: Option["ChatAdministratorRights"] = Nothing
    """Optional. A JSON-serialized object listing the required administrator
    rights of the bot in the chat. The rights must be a subset of user_administrator_rights.
    If not specified, no additional restrictions are applied."""

    bot_is_member: Option[bool] = Nothing
    """Optional. Pass True to request a chat with the bot as a member. Otherwise,
    no additional restrictions are applied."""

    request_title: Option[bool] = Nothing
    """Optional. Pass True to request the chat's title."""

    request_username: Option[bool] = Nothing
    """Optional. Pass True to request the chat's username."""

    request_photo: Option[bool] = Nothing
    """Optional. Pass True to request the chat's photo."""


class KeyboardButtonPollType(Model):
    """Object `KeyboardButtonPollType`, see the [documentation](https://core.telegram.org/bots/api#keyboardbuttonpolltype).

    This object represents type of a poll, which is allowed to be created and sent when the corresponding button is pressed.
    """

    type: Option[typing.Literal["quiz", "regular"]] = Nothing
    """Optional. If quiz is passed, the user will be allowed to create only polls
    in the quiz mode. If regular is passed, only regular polls will be allowed.
    Otherwise, the user will be allowed to create a poll of any type."""


class ReplyKeyboardRemove(Model):
    """Object `ReplyKeyboardRemove`, see the [documentation](https://core.telegram.org/bots/api#replykeyboardremove).

    Upon receiving a message with this object, Telegram clients will remove the current custom keyboard and display the default letter-keyboard. By default, custom keyboards are displayed until a new keyboard is sent by a bot. An exception is made for one-time keyboards that are hidden immediately after the user presses a button (see ReplyKeyboardMarkup). Not supported in channels and for messages sent on behalf of a Telegram Business account.
    """

    remove_keyboard: bool
    """Requests clients to remove the custom keyboard (user will not be able to
    summon this keyboard; if you want to hide the keyboard from sight but keep
    it accessible, use one_time_keyboard in ReplyKeyboardMarkup)."""

    selective: Option[bool] = Nothing
    """Optional. Use this parameter if you want to remove the keyboard for specific
    users only. Targets: 1) users that are @mentioned in the text of the Message
    object; 2) if the bot's message is a reply to a message in the same chat and
    forum topic, sender of the original message. Example: A user votes in a poll,
    bot returns confirmation message in reply to the vote and removes the keyboard
    for that user, while still showing the keyboard with poll options to users
    who haven't voted yet."""


class InlineKeyboardMarkup(Model):
    """Object `InlineKeyboardMarkup`, see the [documentation](https://core.telegram.org/bots/api#inlinekeyboardmarkup).

    This object represents an inline keyboard that appears right next to the message it belongs to.
    """

    inline_keyboard: list[list["InlineKeyboardButton"]]
    """Array of button rows, each represented by an Array of InlineKeyboardButton
    objects."""


class InlineKeyboardButton(Model):
    """Object `InlineKeyboardButton`, see the [documentation](https://core.telegram.org/bots/api#inlinekeyboardbutton).

    This object represents one button of an inline keyboard. Exactly one of the optional fields must be used to specify type of the button.
    """

    text: str
    """Label text on the button."""

    url: Option[str] = Nothing
    """Optional. HTTP or tg:// URL to be opened when the button is pressed. Links
    tg://user?id=<user_id> can be used to mention a user by their identifier
    without using a username, if this is allowed by their privacy settings."""

    callback_data: Option[str] = Nothing
    """Optional. Data to be sent in a callback query to the bot when the button is
    pressed, 1-64 bytes."""

    web_app: Option["WebAppInfo"] = Nothing
    """Optional. Description of the Web App that will be launched when the user
    presses the button. The Web App will be able to send an arbitrary message
    on behalf of the user using the method answerWebAppQuery. Available only
    in private chats between a user and the bot. Not supported for messages sent
    on behalf of a Telegram Business account."""

    login_url: Option["LoginUrl"] = Nothing
    """Optional. An HTTPS URL used to automatically authorize the user. Can be
    used as a replacement for the Telegram Login Widget."""

    switch_inline_query: Option[str] = Nothing
    """Optional. If set, pressing the button will prompt the user to select one
    of their chats, open that chat and insert the bot's username and the specified
    inline query in the input field. May be empty, in which case just the bot's
    username will be inserted. Not supported for messages sent on behalf of
    a Telegram Business account."""

    switch_inline_query_current_chat: Option[str] = Nothing
    """Optional. If set, pressing the button will insert the bot's username and
    the specified inline query in the current chat's input field. May be empty,
    in which case only the bot's username will be inserted. This offers a quick
    way for the user to open your bot in inline mode in the same chat - good for selecting
    something from multiple options. Not supported in channels and for messages
    sent on behalf of a Telegram Business account."""

    switch_inline_query_chosen_chat: Option["SwitchInlineQueryChosenChat"] = Nothing
    """Optional. If set, pressing the button will prompt the user to select one
    of their chats of the specified type, open that chat and insert the bot's
    username and the specified inline query in the input field. Not supported
    for messages sent on behalf of a Telegram Business account."""

    callback_game: Option["CallbackGame"] = Nothing
    """Optional. Description of the game that will be launched when the user presses
    the button. NOTE: This type of button must always be the first button in the
    first row."""

    pay: Option[bool] = Nothing
    """Optional. Specify True, to send a Pay button. Substrings `⭐` and `XTR` in
    the buttons's text will be replaced with a Telegram Star icon. NOTE: This
    type of button must always be the first button in the first row and can only
    be used in invoice messages."""


class LoginUrl(Model):
    """Object `LoginUrl`, see the [documentation](https://core.telegram.org/bots/api#loginurl).

    This object represents a parameter of the inline keyboard button used to automatically authorize a user. Serves as a great replacement for the Telegram Login Widget when the user is coming from Telegram. All the user needs to do is tap/click a button and confirm that they want to log in:
    Telegram apps support these buttons as of version 5.7.
    """

    url: str
    """An HTTPS URL to be opened with user authorization data added to the query
    string when the button is pressed. If the user refuses to provide authorization
    data, the original URL without information about the user will be opened.
    The data added is the same as described in Receiving authorization data.
    NOTE: You must always check the hash of the received data to verify the authentication
    and the integrity of the data as described in Checking authorization."""

    forward_text: Option[str] = Nothing
    """Optional. New text of the button in forwarded messages."""

    bot_username: Option[str] = Nothing
    """Optional. Username of a bot, which will be used for user authorization.
    See Setting up a bot for more details. If not specified, the current bot's
    username will be assumed. The url's domain must be the same as the domain
    linked with the bot. See Linking your domain to the bot for more details."""

    request_write_access: Option[bool] = Nothing
    """Optional. Pass True to request the permission for your bot to send messages
    to the user."""


class SwitchInlineQueryChosenChat(Model):
    """Object `SwitchInlineQueryChosenChat`, see the [documentation](https://core.telegram.org/bots/api#switchinlinequerychosenchat).

    This object represents an inline button that switches the current user to inline mode in a chosen chat, with an optional default inline query.
    """

    query: Option[str] = Nothing
    """Optional. The default inline query to be inserted in the input field. If
    left empty, only the bot's username will be inserted."""

    allow_user_chats: Option[bool] = Nothing
    """Optional. True, if private chats with users can be chosen."""

    allow_bot_chats: Option[bool] = Nothing
    """Optional. True, if private chats with bots can be chosen."""

    allow_group_chats: Option[bool] = Nothing
    """Optional. True, if group and supergroup chats can be chosen."""

    allow_channel_chats: Option[bool] = Nothing
    """Optional. True, if channel chats can be chosen."""


class CallbackQuery(Model):
    """Object `CallbackQuery`, see the [documentation](https://core.telegram.org/bots/api#callbackquery).

    This object represents an incoming callback query from a callback button in an inline keyboard. If the button that originated the query was attached to a message sent by the bot, the field message will be present. If the button was attached to a message sent via the bot (in inline mode), the field inline_message_id will be present. Exactly one of the fields data or game_short_name will be present.
    """

    id: str
    """Unique identifier for this query."""

    from_: "User"
    """Sender."""

    chat_instance: str
    """Global identifier, uniquely corresponding to the chat to which the message
    with the callback button was sent. Useful for high scores in games."""

    message: Option[Variative["Message", "InaccessibleMessage"]] = Nothing
    """Optional. Message sent by the bot with the callback button that originated
    the query."""

    inline_message_id: Option[str] = Nothing
    """Optional. Identifier of the message sent via the bot in inline mode, that
    originated the query."""

    data: Option[str] = Nothing
    """Optional. Data associated with the callback button. Be aware that the message
    originated the query can contain no callback buttons with this data."""

    game_short_name: Option[str] = Nothing
    """Optional. Short name of a Game to be returned, serves as the unique identifier
    for the game."""


class ForceReply(Model):
    """Object `ForceReply`, see the [documentation](https://core.telegram.org/bots/api#forcereply).

    Upon receiving a message with this object, Telegram clients will display a reply interface to the user (act as if the user has selected the bot's message and tapped 'Reply'). This can be extremely useful if you want to create user-friendly step-by-step interfaces without having to sacrifice privacy mode. Not supported in channels and for messages sent on behalf of a Telegram Business account.
    """

    force_reply: bool
    """Shows reply interface to the user, as if they manually selected the bot's
    message and tapped 'Reply'."""

    input_field_placeholder: Option[str] = Nothing
    """Optional. The placeholder to be shown in the input field when the reply is
    active; 1-64 characters."""

    selective: Option[bool] = Nothing
    """Optional. Use this parameter if you want to force reply from specific users
    only. Targets: 1) users that are @mentioned in the text of the Message object;
    2) if the bot's message is a reply to a message in the same chat and forum topic,
    sender of the original message."""


class ChatPhoto(Model):
    """Object `ChatPhoto`, see the [documentation](https://core.telegram.org/bots/api#chatphoto).

    This object represents a chat photo.
    """

    small_file_id: str
    """File identifier of small (160x160) chat photo. This file_id can be used
    only for photo download and only for as long as the photo is not changed."""

    small_file_unique_id: str
    """Unique file identifier of small (160x160) chat photo, which is supposed
    to be the same over time and for different bots. Can't be used to download
    or reuse the file."""

    big_file_id: str
    """File identifier of big (640x640) chat photo. This file_id can be used only
    for photo download and only for as long as the photo is not changed."""

    big_file_unique_id: str
    """Unique file identifier of big (640x640) chat photo, which is supposed to
    be the same over time and for different bots. Can't be used to download or
    reuse the file."""


class ChatInviteLink(Model):
    """Object `ChatInviteLink`, see the [documentation](https://core.telegram.org/bots/api#chatinvitelink).

    Represents an invite link for a chat.
    """

    invite_link: str
    """The invite link. If the link was created by another chat administrator,
    then the second part of the link will be replaced with `...`."""

    creator: "User"
    """Creator of the link."""

    creates_join_request: bool
    """True, if users joining the chat via the link need to be approved by chat administrators."""

    is_primary: bool
    """True, if the link is primary."""

    is_revoked: bool
    """True, if the link is revoked."""

    name: Option[str] = Nothing
    """Optional. Invite link name."""

    expire_date: Option[datetime] = Nothing
    """Optional. Point in time (Unix timestamp) when the link will expire or has
    been expired."""

    member_limit: Option[int] = Nothing
    """Optional. The maximum number of users that can be members of the chat simultaneously
    after joining the chat via this invite link; 1-99999."""

    pending_join_request_count: Option[int] = Nothing
    """Optional. Number of pending join requests created using this link."""


class ChatAdministratorRights(Model):
    """Object `ChatAdministratorRights`, see the [documentation](https://core.telegram.org/bots/api#chatadministratorrights).

    Represents the rights of an administrator in a chat.
    """

    is_anonymous: bool
    """True, if the user's presence in the chat is hidden."""

    can_manage_chat: bool
    """True, if the administrator can access the chat event log, get boost list,
    see hidden supergroup and channel members, report spam messages and ignore
    slow mode. Implied by any other administrator privilege."""

    can_delete_messages: bool
    """True, if the administrator can delete messages of other users."""

    can_manage_video_chats: bool
    """True, if the administrator can manage video chats."""

    can_restrict_members: bool
    """True, if the administrator can restrict, ban or unban chat members, or access
    supergroup statistics."""

    can_promote_members: bool
    """True, if the administrator can add new administrators with a subset of their
    own privileges or demote administrators that they have promoted, directly
    or indirectly (promoted by administrators that were appointed by the user)."""

    can_change_info: bool
    """True, if the user is allowed to change the chat title, photo and other settings."""

    can_invite_users: bool
    """True, if the user is allowed to invite new users to the chat."""

    can_post_stories: bool
    """True, if the administrator can post stories to the chat."""

    can_edit_stories: bool
    """True, if the administrator can edit stories posted by other users, post
    stories to the chat page, pin chat stories, and access the chat's story archive."""

    can_delete_stories: bool
    """True, if the administrator can delete stories posted by other users."""

    can_post_messages: Option[bool] = Nothing
    """Optional. True, if the administrator can post messages in the channel,
    or access channel statistics; for channels only."""

    can_edit_messages: Option[bool] = Nothing
    """Optional. True, if the administrator can edit messages of other users and
    can pin messages; for channels only."""

    can_pin_messages: Option[bool] = Nothing
    """Optional. True, if the user is allowed to pin messages; for groups and supergroups
    only."""

    can_manage_topics: Option[bool] = Nothing
    """Optional. True, if the user is allowed to create, rename, close, and reopen
    forum topics; for supergroups only."""


class ChatMemberUpdated(Model):
    """Object `ChatMemberUpdated`, see the [documentation](https://core.telegram.org/bots/api#chatmemberupdated).

    This object represents changes in the status of a chat member.
    """

    chat: "Chat"
    """Chat the user belongs to."""

    from_: "User"
    """Performer of the action, which resulted in the change."""

    date: datetime
    """Date the change was done in Unix time."""

    old_chat_member: Variative[
        "ChatMemberOwner",
        "ChatMemberAdministrator",
        "ChatMemberMember",
        "ChatMemberRestricted",
        "ChatMemberLeft",
        "ChatMemberBanned",
    ]
    """Previous information about the chat member."""

    new_chat_member: Variative[
        "ChatMemberOwner",
        "ChatMemberAdministrator",
        "ChatMemberMember",
        "ChatMemberRestricted",
        "ChatMemberLeft",
        "ChatMemberBanned",
    ]
    """New information about the chat member."""

    invite_link: Option["ChatInviteLink"] = Nothing
    """Optional. Chat invite link, which was used by the user to join the chat; for
    joining by invite link events only."""

    via_join_request: Option[bool] = Nothing
    """Optional. True, if the user joined the chat after sending a direct join request
    without using an invite link and being approved by an administrator."""

    via_chat_folder_invite_link: Option[bool] = Nothing
    """Optional. True, if the user joined the chat via a chat folder invite link."""

    @property
    def chat_id(self) -> int:
        """Alias `.chat_id` instead of `.chat.id`"""

        return self.chat.id


class ChatMemberOwner(ChatMember):
    """Object `ChatMemberOwner`, see the [documentation](https://core.telegram.org/bots/api#chatmemberowner).

    Represents a chat member that owns the chat and has all administrator privileges.
    """

    status: typing.Literal["creator"]
    """The member's status in the chat, always `creator`."""

    user: "User"
    """Information about the user."""

    is_anonymous: bool
    """True, if the user's presence in the chat is hidden."""

    custom_title: Option[str] = Nothing
    """Optional. Custom title for this user."""


class ChatMemberAdministrator(ChatMember):
    """Object `ChatMemberAdministrator`, see the [documentation](https://core.telegram.org/bots/api#chatmemberadministrator).

    Represents a chat member that has some additional privileges.
    """

    status: typing.Literal["administrator"]
    """The member's status in the chat, always `administrator`."""

    user: "User"
    """Information about the user."""

    can_be_edited: bool
    """True, if the bot is allowed to edit administrator privileges of that user."""

    is_anonymous: bool
    """True, if the user's presence in the chat is hidden."""

    can_manage_chat: bool
    """True, if the administrator can access the chat event log, get boost list,
    see hidden supergroup and channel members, report spam messages and ignore
    slow mode. Implied by any other administrator privilege."""

    can_delete_messages: bool
    """True, if the administrator can delete messages of other users."""

    can_manage_video_chats: bool
    """True, if the administrator can manage video chats."""

    can_restrict_members: bool
    """True, if the administrator can restrict, ban or unban chat members, or access
    supergroup statistics."""

    can_promote_members: bool
    """True, if the administrator can add new administrators with a subset of their
    own privileges or demote administrators that they have promoted, directly
    or indirectly (promoted by administrators that were appointed by the user)."""

    can_change_info: bool
    """True, if the user is allowed to change the chat title, photo and other settings."""

    can_invite_users: bool
    """True, if the user is allowed to invite new users to the chat."""

    can_post_stories: bool
    """True, if the administrator can post stories to the chat."""

    can_edit_stories: bool
    """True, if the administrator can edit stories posted by other users, post
    stories to the chat page, pin chat stories, and access the chat's story archive."""

    can_delete_stories: bool
    """True, if the administrator can delete stories posted by other users."""

    can_post_messages: Option[bool] = Nothing
    """Optional. True, if the administrator can post messages in the channel,
    or access channel statistics; for channels only."""

    can_edit_messages: Option[bool] = Nothing
    """Optional. True, if the administrator can edit messages of other users and
    can pin messages; for channels only."""

    can_pin_messages: Option[bool] = Nothing
    """Optional. True, if the user is allowed to pin messages; for groups and supergroups
    only."""

    can_manage_topics: Option[bool] = Nothing
    """Optional. True, if the user is allowed to create, rename, close, and reopen
    forum topics; for supergroups only."""

    custom_title: Option[str] = Nothing
    """Optional. Custom title for this user."""


class ChatMemberMember(ChatMember):
    """Object `ChatMemberMember`, see the [documentation](https://core.telegram.org/bots/api#chatmembermember).

    Represents a chat member that has no additional privileges or restrictions.
    """

    status: typing.Literal["member"]
    """The member's status in the chat, always `member`."""

    user: "User"
    """Information about the user."""

    until_date: Option[datetime] = Nothing
    """Optional. Date when the user's subscription will expire; Unix time."""


class ChatMemberRestricted(ChatMember):
    """Object `ChatMemberRestricted`, see the [documentation](https://core.telegram.org/bots/api#chatmemberrestricted).

    Represents a chat member that is under certain restrictions in the chat. Supergroups only.
    """

    status: typing.Literal["restricted"]
    """The member's status in the chat, always `restricted`."""

    user: "User"
    """Information about the user."""

    is_member: bool
    """True, if the user is a member of the chat at the moment of the request."""

    can_send_messages: bool
    """True, if the user is allowed to send text messages, contacts, giveaways,
    giveaway winners, invoices, locations and venues."""

    can_send_audios: bool
    """True, if the user is allowed to send audios."""

    can_send_documents: bool
    """True, if the user is allowed to send documents."""

    can_send_photos: bool
    """True, if the user is allowed to send photos."""

    can_send_videos: bool
    """True, if the user is allowed to send videos."""

    can_send_video_notes: bool
    """True, if the user is allowed to send video notes."""

    can_send_voice_notes: bool
    """True, if the user is allowed to send voice notes."""

    can_send_polls: bool
    """True, if the user is allowed to send polls."""

    can_send_other_messages: bool
    """True, if the user is allowed to send animations, games, stickers and use
    inline bots."""

    can_add_web_page_previews: bool
    """True, if the user is allowed to add web page previews to their messages."""

    can_change_info: bool
    """True, if the user is allowed to change the chat title, photo and other settings."""

    can_invite_users: bool
    """True, if the user is allowed to invite new users to the chat."""

    can_pin_messages: bool
    """True, if the user is allowed to pin messages."""

    can_manage_topics: bool
    """True, if the user is allowed to create forum topics."""

    until_date: datetime
    """Date when restrictions will be lifted for this user; Unix time. If 0, then
    the user is restricted forever."""


class ChatMemberLeft(ChatMember):
    """Object `ChatMemberLeft`, see the [documentation](https://core.telegram.org/bots/api#chatmemberleft).

    Represents a chat member that isn't currently a member of the chat, but may join it themselves.
    """

    status: typing.Literal["left"]
    """The member's status in the chat, always `left`."""

    user: "User"
    """Information about the user."""


class ChatMemberBanned(ChatMember):
    """Object `ChatMemberBanned`, see the [documentation](https://core.telegram.org/bots/api#chatmemberbanned).

    Represents a chat member that was banned in the chat and can't return to the chat or view chat messages.
    """

    status: typing.Literal["kicked"]
    """The member's status in the chat, always `kicked`."""

    user: "User"
    """Information about the user."""

    until_date: datetime
    """Date when restrictions will be lifted for this user; Unix time. If 0, then
    the user is banned forever."""


class ChatJoinRequest(Model):
    """Object `ChatJoinRequest`, see the [documentation](https://core.telegram.org/bots/api#chatjoinrequest).

    Represents a join request sent to a chat.
    """

    chat: "Chat"
    """Chat to which the request was sent."""

    from_: "User"
    """User that sent the join request."""

    user_chat_id: int
    """Identifier of a private chat with the user who sent the join request. This
    number may have more than 32 significant bits and some programming languages
    may have difficulty/silent defects in interpreting it. But it has at most
    52 significant bits, so a 64-bit integer or double-precision float type
    are safe for storing this identifier. The bot can use this identifier for
    5 minutes to send messages until the join request is processed, assuming
    no other administrator contacted the user."""

    date: datetime
    """Date the request was sent in Unix time."""

    bio: Option[str] = Nothing
    """Optional. Bio of the user."""

    invite_link: Option["ChatInviteLink"] = Nothing
    """Optional. Chat invite link that was used by the user to send the join request."""

    @property
    def chat_id(self) -> int:
        """`chat_id` instead of `chat.id`."""

        return self.chat.id


class ChatPermissions(Model):
    """Object `ChatPermissions`, see the [documentation](https://core.telegram.org/bots/api#chatpermissions).

    Describes actions that a non-administrator user is allowed to take in a chat.
    """

    can_send_messages: Option[bool] = Nothing
    """Optional. True, if the user is allowed to send text messages, contacts,
    giveaways, giveaway winners, invoices, locations and venues."""

    can_send_audios: Option[bool] = Nothing
    """Optional. True, if the user is allowed to send audios."""

    can_send_documents: Option[bool] = Nothing
    """Optional. True, if the user is allowed to send documents."""

    can_send_photos: Option[bool] = Nothing
    """Optional. True, if the user is allowed to send photos."""

    can_send_videos: Option[bool] = Nothing
    """Optional. True, if the user is allowed to send videos."""

    can_send_video_notes: Option[bool] = Nothing
    """Optional. True, if the user is allowed to send video notes."""

    can_send_voice_notes: Option[bool] = Nothing
    """Optional. True, if the user is allowed to send voice notes."""

    can_send_polls: Option[bool] = Nothing
    """Optional. True, if the user is allowed to send polls."""

    can_send_other_messages: Option[bool] = Nothing
    """Optional. True, if the user is allowed to send animations, games, stickers
    and use inline bots."""

    can_add_web_page_previews: Option[bool] = Nothing
    """Optional. True, if the user is allowed to add web page previews to their messages."""

    can_change_info: Option[bool] = Nothing
    """Optional. True, if the user is allowed to change the chat title, photo and
    other settings. Ignored in public supergroups."""

    can_invite_users: Option[bool] = Nothing
    """Optional. True, if the user is allowed to invite new users to the chat."""

    can_pin_messages: Option[bool] = Nothing
    """Optional. True, if the user is allowed to pin messages. Ignored in public
    supergroups."""

    can_manage_topics: Option[bool] = Nothing
    """Optional. True, if the user is allowed to create forum topics. If omitted
    defaults to the value of can_pin_messages."""


class Birthdate(Model):
    """Object `Birthdate`, see the [documentation](https://core.telegram.org/bots/api#birthdate).

    Describes the birthdate of a user.
    """

    day: int
    """Day of the user's birth; 1-31."""

    month: int
    """Month of the user's birth; 1-12."""

    year: Option[int] = Nothing
    """Optional. Year of the user's birth."""

    @property
    def is_birthday(self) -> bool:
        """True, if today is a user's birthday."""

        now = datetime.now()
        return now.month == self.month and now.day == self.day

    @property
    def age(self) -> Option[int]:
        """Optional. Contains the user's age, if the user has a birth year specified."""

        return self.year.map(
            lambda year: ((datetime.now() - datetime(year, self.month, self.day)) // 365).days
        )


class BusinessIntro(Model):
    """Object `BusinessIntro`, see the [documentation](https://core.telegram.org/bots/api#businessintro).

    Contains information about the start page settings of a Telegram Business account.
    """

    title: Option[str] = Nothing
    """Optional. Title text of the business intro."""

    message: Option[str] = Nothing
    """Optional. Message text of the business intro."""

    sticker: Option["Sticker"] = Nothing
    """Optional. Sticker of the business intro."""


class BusinessLocation(Model):
    """Object `BusinessLocation`, see the [documentation](https://core.telegram.org/bots/api#businesslocation).

    Contains information about the location of a Telegram Business account.
    """

    address: str
    """Address of the business."""

    location: Option["Location"] = Nothing
    """Optional. Location of the business."""


class BusinessOpeningHoursInterval(Model):
    """Object `BusinessOpeningHoursInterval`, see the [documentation](https://core.telegram.org/bots/api#businessopeninghoursinterval).

    Describes an interval of time during which a business is open.
    """

    opening_minute: int
    """The minute's sequence number in a week, starting on Monday, marking the
    start of the time interval during which the business is open; 0 - 7 * 24 * 60."""

    closing_minute: int
    """The minute's sequence number in a week, starting on Monday, marking the
    end of the time interval during which the business is open; 0 - 8 * 24 * 60."""


class BusinessOpeningHours(Model):
    """Object `BusinessOpeningHours`, see the [documentation](https://core.telegram.org/bots/api#businessopeninghours).

    Describes the opening hours of a business.
    """

    time_zone_name: str
    """Unique name of the time zone for which the opening hours are defined."""

    opening_hours: list["BusinessOpeningHoursInterval"]
    """List of time intervals describing business opening hours."""


class ChatLocation(Model):
    """Object `ChatLocation`, see the [documentation](https://core.telegram.org/bots/api#chatlocation).

    Represents a location to which a chat is connected.
    """

    location: "Location"
    """The location to which the supergroup is connected. Can't be a live location."""

    address: str
    """Location address; 1-64 characters, as defined by the chat owner."""


class ReactionTypeEmoji(ReactionType):
    """Object `ReactionTypeEmoji`, see the [documentation](https://core.telegram.org/bots/api#reactiontypeemoji).

    The reaction is based on an emoji.
    """

    type: typing.Literal["emoji"]
    """Type of the reaction, always `emoji`."""

    emoji: ReactionEmoji
    """Reaction emoji. Currently, it can be one of `👍`, `👎`, `❤`, `🔥`, `🥰`, `👏`,
    `😁`, `🤔`, `🤯`, `😱`, `🤬`, `😢`, `🎉`, `🤩`, `🤮`, `💩`, `🙏`, `👌`, `🕊`, `🤡`, `🥱`,
    `🥴`, `😍`, `🐳`, `❤‍🔥`, `🌚`, `🌭`, `💯`, `🤣`, `⚡`, `🍌`, `🏆`, `💔`, `🤨`, `😐`, `🍓`,
    `🍾`, `💋`, `🖕`, `😈`, `😴`, `😭`, `🤓`, `👻`, `👨‍💻`, `👀`, `🎃`, `🙈`, `😇`, `😨`, `🤝`,
    `✍`, `🤗`, `🫡`, `🎅`, `🎄`, `☃`, `💅`, `🤪`, `🗿`, `🆒`, `💘`, `🙉`, `🦄`, `😘`, `💊`,
    `🙊`, `😎`, `👾`, `🤷‍♂`, `🤷`, `🤷‍♀`, `😡`."""


class ReactionTypeCustomEmoji(ReactionType):
    """Object `ReactionTypeCustomEmoji`, see the [documentation](https://core.telegram.org/bots/api#reactiontypecustomemoji).

    The reaction is based on a custom emoji.
    """

    type: typing.Literal["custom_emoji"]
    """Type of the reaction, always `custom_emoji`."""

    custom_emoji_id: str
    """Custom emoji identifier."""


class ReactionTypePaid(ReactionType):
    """Object `ReactionTypePaid`, see the [documentation](https://core.telegram.org/bots/api#reactiontypepaid).

    The reaction is paid.
    """

    type: typing.Literal["paid"]
    """Type of the reaction, always `paid`."""


class ReactionCount(Model):
    """Object `ReactionCount`, see the [documentation](https://core.telegram.org/bots/api#reactioncount).

    Represents a reaction added to a message along with the number of times it was added.
    """

    type: Variative["ReactionTypeEmoji", "ReactionTypeCustomEmoji", "ReactionTypePaid"]
    """Type of the reaction."""

    total_count: int
    """Number of times the reaction was added."""


class MessageReactionUpdated(Model):
    """Object `MessageReactionUpdated`, see the [documentation](https://core.telegram.org/bots/api#messagereactionupdated).

    This object represents a change of a reaction on a message performed by a user.
    """

    chat: "Chat"
    """The chat containing the message the user reacted to."""

    message_id: int
    """Unique identifier of the message inside the chat."""

    date: datetime
    """Date of the change in Unix time."""

    old_reaction: list[Variative["ReactionTypeEmoji", "ReactionTypeCustomEmoji", "ReactionTypePaid"]]
    """Previous list of reaction types that were set by the user."""

    new_reaction: list[Variative["ReactionTypeEmoji", "ReactionTypeCustomEmoji", "ReactionTypePaid"]]
    """New list of reaction types that have been set by the user."""

    user: Option["User"] = Nothing
    """Optional. The user that changed the reaction, if the user isn't anonymous."""

    actor_chat: Option["Chat"] = Nothing
    """Optional. The chat on behalf of which the reaction was changed, if the user
    is anonymous."""


class MessageReactionCountUpdated(Model):
    """Object `MessageReactionCountUpdated`, see the [documentation](https://core.telegram.org/bots/api#messagereactioncountupdated).

    This object represents reaction changes on a message with anonymous reactions.
    """

    chat: "Chat"
    """The chat containing the message."""

    message_id: int
    """Unique message identifier inside the chat."""

    date: datetime
    """Date of the change in Unix time."""

    reactions: list["ReactionCount"]
    """List of reactions that are present on the message."""


class ForumTopic(Model):
    """Object `ForumTopic`, see the [documentation](https://core.telegram.org/bots/api#forumtopic).

    This object represents a forum topic.
    """

    message_thread_id: int
    """Unique identifier of the forum topic."""

    name: str
    """Name of the topic."""

    icon_color: TopicIconColor
    """Color of the topic icon in RGB format."""

    icon_custom_emoji_id: Option[str] = Nothing
    """Optional. Unique identifier of the custom emoji shown as the topic icon."""


class BotCommand(Model):
    """Object `BotCommand`, see the [documentation](https://core.telegram.org/bots/api#botcommand).

    This object represents a bot command.
    """

    command: str
    """Text of the command; 1-32 characters. Can contain only lowercase English
    letters, digits and underscores."""

    description: str
    """Description of the command; 1-256 characters."""


class BotCommandScopeDefault(BotCommandScope):
    """Object `BotCommandScopeDefault`, see the [documentation](https://core.telegram.org/bots/api#botcommandscopedefault).

    Represents the default scope of bot commands. Default commands are used if no commands with a narrower scope are specified for the user.
    """

    type: typing.Literal["default"]
    """Scope type, must be default."""


class BotCommandScopeAllPrivateChats(BotCommandScope):
    """Object `BotCommandScopeAllPrivateChats`, see the [documentation](https://core.telegram.org/bots/api#botcommandscopeallprivatechats).

    Represents the scope of bot commands, covering all private chats.
    """

    type: typing.Literal["all_private_chats"]
    """Scope type, must be all_private_chats."""


class BotCommandScopeAllGroupChats(BotCommandScope):
    """Object `BotCommandScopeAllGroupChats`, see the [documentation](https://core.telegram.org/bots/api#botcommandscopeallgroupchats).

    Represents the scope of bot commands, covering all group and supergroup chats.
    """

    type: typing.Literal["all_group_chats"]
    """Scope type, must be all_group_chats."""


class BotCommandScopeAllChatAdministrators(BotCommandScope):
    """Object `BotCommandScopeAllChatAdministrators`, see the [documentation](https://core.telegram.org/bots/api#botcommandscopeallchatadministrators).

    Represents the scope of bot commands, covering all group and supergroup chat administrators.
    """

    type: typing.Literal["all_chat_administrators"]
    """Scope type, must be all_chat_administrators."""


class BotCommandScopeChat(BotCommandScope):
    """Object `BotCommandScopeChat`, see the [documentation](https://core.telegram.org/bots/api#botcommandscopechat).

    Represents the scope of bot commands, covering a specific chat.
    """

    type: typing.Literal["chat"]
    """Scope type, must be chat."""

    chat_id: Variative[int, str]
    """Unique identifier for the target chat or username of the target supergroup
    (in the format @supergroupusername)."""


class BotCommandScopeChatAdministrators(BotCommandScope):
    """Object `BotCommandScopeChatAdministrators`, see the [documentation](https://core.telegram.org/bots/api#botcommandscopechatadministrators).

    Represents the scope of bot commands, covering all administrators of a specific group or supergroup chat.
    """

    type: typing.Literal["chat_administrators"]
    """Scope type, must be chat_administrators."""

    chat_id: Variative[int, str]
    """Unique identifier for the target chat or username of the target supergroup
    (in the format @supergroupusername)."""


class BotCommandScopeChatMember(BotCommandScope):
    """Object `BotCommandScopeChatMember`, see the [documentation](https://core.telegram.org/bots/api#botcommandscopechatmember).

    Represents the scope of bot commands, covering a specific member of a group or supergroup chat.
    """

    type: typing.Literal["chat_member"]
    """Scope type, must be chat_member."""

    chat_id: Variative[int, str]
    """Unique identifier for the target chat or username of the target supergroup
    (in the format @supergroupusername)."""

    user_id: int
    """Unique identifier of the target user."""


class BotName(Model):
    """Object `BotName`, see the [documentation](https://core.telegram.org/bots/api#botname).

    This object represents the bot's name.
    """

    name: str
    """The bot's name."""


class BotDescription(Model):
    """Object `BotDescription`, see the [documentation](https://core.telegram.org/bots/api#botdescription).

    This object represents the bot's description.
    """

    description: str
    """The bot's description."""


class BotShortDescription(Model):
    """Object `BotShortDescription`, see the [documentation](https://core.telegram.org/bots/api#botshortdescription).

    This object represents the bot's short description.
    """

    short_description: str
    """The bot's short description."""


class MenuButtonCommands(MenuButton):
    """Object `MenuButtonCommands`, see the [documentation](https://core.telegram.org/bots/api#menubuttoncommands).

    Represents a menu button, which opens the bot's list of commands.
    """

    type: typing.Literal["commands"]
    """Type of the button, must be commands."""


class MenuButtonWebApp(MenuButton):
    """Object `MenuButtonWebApp`, see the [documentation](https://core.telegram.org/bots/api#menubuttonwebapp).

    Represents a menu button, which launches a Web App.
    """

    type: typing.Literal["web_app"]
    """Type of the button, must be web_app."""

    text: str
    """Text on the button."""

    web_app: "WebAppInfo"
    """Description of the Web App that will be launched when the user presses the
    button. The Web App will be able to send an arbitrary message on behalf of
    the user using the method answerWebAppQuery. Alternatively, a t.me link
    to a Web App of the bot can be specified in the object instead of the Web App's
    URL, in which case the Web App will be opened as if the user pressed the link."""


class MenuButtonDefault(MenuButton):
    """Object `MenuButtonDefault`, see the [documentation](https://core.telegram.org/bots/api#menubuttondefault).

    Describes that no specific value for the menu button was set.
    """

    type: typing.Literal["default"]
    """Type of the button, must be default."""


class ChatBoostSourcePremium(ChatBoostSource):
    """Object `ChatBoostSourcePremium`, see the [documentation](https://core.telegram.org/bots/api#chatboostsourcepremium).

    The boost was obtained by subscribing to Telegram Premium or by gifting a Telegram Premium subscription to another user.
    """

    source: typing.Literal["premium"]
    """Source of the boost, always `premium`."""

    user: "User"
    """User that boosted the chat."""


class ChatBoostSourceGiftCode(ChatBoostSource):
    """Object `ChatBoostSourceGiftCode`, see the [documentation](https://core.telegram.org/bots/api#chatboostsourcegiftcode).

    The boost was obtained by the creation of Telegram Premium gift codes to boost a chat. Each such code boosts the chat 4 times for the duration of the corresponding Telegram Premium subscription.
    """

    source: typing.Literal["gift_code"]
    """Source of the boost, always `gift_code`."""

    user: "User"
    """User for which the gift code was created."""


class ChatBoostSourceGiveaway(ChatBoostSource):
    """Object `ChatBoostSourceGiveaway`, see the [documentation](https://core.telegram.org/bots/api#chatboostsourcegiveaway).

    The boost was obtained by the creation of a Telegram Premium giveaway. This boosts the chat 4 times for the duration of the corresponding Telegram Premium subscription.
    """

    source: typing.Literal["giveaway"]
    """Source of the boost, always `giveaway`."""

    giveaway_message_id: int
    """Identifier of a message in the chat with the giveaway; the message could
    have been deleted already. May be 0 if the message isn't sent yet."""

    user: Option["User"] = Nothing
    """Optional. User that won the prize in the giveaway if any."""

    is_unclaimed: Option[bool] = Nothing
    """Optional. True, if the giveaway was completed, but there was no user to win
    the prize."""


class ChatBoost(Model):
    """Object `ChatBoost`, see the [documentation](https://core.telegram.org/bots/api#chatboost).

    This object contains information about a chat boost.
    """

    boost_id: str
    """Unique identifier of the boost."""

    add_date: datetime
    """Point in time (Unix timestamp) when the chat was boosted."""

    expiration_date: datetime
    """Point in time (Unix timestamp) when the boost will automatically expire,
    unless the booster's Telegram Premium subscription is prolonged."""

    source: Variative["ChatBoostSourcePremium", "ChatBoostSourceGiftCode", "ChatBoostSourceGiveaway"]
    """Source of the added boost."""


class ChatBoostUpdated(Model):
    """Object `ChatBoostUpdated`, see the [documentation](https://core.telegram.org/bots/api#chatboostupdated).

    This object represents a boost added to a chat or changed.
    """

    chat: "Chat"
    """Chat which was boosted."""

    boost: "ChatBoost"
    """Information about the chat boost."""


class ChatBoostRemoved(Model):
    """Object `ChatBoostRemoved`, see the [documentation](https://core.telegram.org/bots/api#chatboostremoved).

    This object represents a boost removed from a chat.
    """

    chat: "Chat"
    """Chat which was boosted."""

    boost_id: str
    """Unique identifier of the boost."""

    remove_date: datetime
    """Point in time (Unix timestamp) when the boost was removed."""

    source: Variative["ChatBoostSourcePremium", "ChatBoostSourceGiftCode", "ChatBoostSourceGiveaway"]
    """Source of the removed boost."""


class UserChatBoosts(Model):
    """Object `UserChatBoosts`, see the [documentation](https://core.telegram.org/bots/api#userchatboosts).

    This object represents a list of boosts added to a chat by a user.
    """

    boosts: list["ChatBoost"]
    """The list of boosts added to the chat by the user."""


class BusinessConnection(Model):
    """Object `BusinessConnection`, see the [documentation](https://core.telegram.org/bots/api#businessconnection).

    Describes the connection of the bot with a business account.
    """

    id: str
    """Unique identifier of the business connection."""

    user: "User"
    """Business account user that created the business connection."""

    user_chat_id: int
    """Identifier of a private chat with the user who created the business connection.
    This number may have more than 32 significant bits and some programming
    languages may have difficulty/silent defects in interpreting it. But
    it has at most 52 significant bits, so a 64-bit integer or double-precision
    float type are safe for storing this identifier."""

    date: datetime
    """Date the connection was established in Unix time."""

    can_reply: bool
    """True, if the bot can act on behalf of the business account in chats that were
    active in the last 24 hours."""

    is_enabled: bool
    """True, if the connection is active."""


class BusinessMessagesDeleted(Model):
    """Object `BusinessMessagesDeleted`, see the [documentation](https://core.telegram.org/bots/api#businessmessagesdeleted).

    This object is received when messages are deleted from a connected business account.
    """

    business_connection_id: str
    """Unique identifier of the business connection."""

    chat: "Chat"
    """Information about a chat in the business account. The bot may not have access
    to the chat or the corresponding user."""

    message_ids: list[int]
    """The list of identifiers of deleted messages in the chat of the business account."""


class ResponseParameters(Model):
    """Object `ResponseParameters`, see the [documentation](https://core.telegram.org/bots/api#responseparameters).

    Describes why a request was unsuccessful.
    """

    migrate_to_chat_id: Option[int] = Nothing
    """Optional. The group has been migrated to a supergroup with the specified
    identifier. This number may have more than 32 significant bits and some
    programming languages may have difficulty/silent defects in interpreting
    it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision
    float type are safe for storing this identifier."""

    retry_after: Option[int] = Nothing
    """Optional. In case of exceeding flood control, the number of seconds left
    to wait before the request can be repeated."""


class InputMediaPhoto(InputMedia):
    """Object `InputMediaPhoto`, see the [documentation](https://core.telegram.org/bots/api#inputmediaphoto).

    Represents a photo to be sent.
    """

    type: typing.Literal["photo"]
    """Type of the result, must be photo."""

    media: Variative["InputFile", str]
    """File to send. Pass a file_id to send a file that exists on the Telegram servers
    (recommended), pass an HTTP URL for Telegram to get a file from the Internet,
    or pass `attach://<file_attach_name>` to upload a new one using multipart/form-data
    under <file_attach_name> name. More information on Sending Files: https://core.telegram.org/bots/api#sending-files."""

    caption: Option[str] = Nothing
    """Optional. Caption of the photo to be sent, 0-1024 characters after entities
    parsing."""

    parse_mode: Option[str] = Nothing
    """Optional. Mode for parsing entities in the photo caption. See formatting
    options for more details."""

    caption_entities: Option[list["MessageEntity"]] = Nothing
    """Optional. List of special entities that appear in the caption, which can
    be specified instead of parse_mode."""

    show_caption_above_media: Option[bool] = Nothing
    """Optional. Pass True, if the caption must be shown above the message media."""

    has_spoiler: Option[bool] = Nothing
    """Optional. Pass True if the photo needs to be covered with a spoiler animation."""


class InputMediaVideo(InputMedia):
    """Object `InputMediaVideo`, see the [documentation](https://core.telegram.org/bots/api#inputmediavideo).

    Represents a video to be sent.
    """

    type: typing.Literal["video"]
    """Type of the result, must be video."""

    media: Variative["InputFile", str]
    """File to send. Pass a file_id to send a file that exists on the Telegram servers
    (recommended), pass an HTTP URL for Telegram to get a file from the Internet,
    or pass `attach://<file_attach_name>` to upload a new one using multipart/form-data
    under <file_attach_name> name. More information on Sending Files: https://core.telegram.org/bots/api#sending-files."""

    thumbnail: Option[Variative["InputFile", str]] = Nothing
    """Optional. Thumbnail of the file sent; can be ignored if thumbnail generation
    for the file is supported server-side. The thumbnail should be in JPEG format
    and less than 200 kB in size. A thumbnail's width and height should not exceed
    320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails
    can't be reused and can be only uploaded as a new file, so you can pass `attach://<file_attach_name>`
    if the thumbnail was uploaded using multipart/form-data under <file_attach_name>.
    More information on Sending Files: https://core.telegram.org/bots/api#sending-files."""

    caption: Option[str] = Nothing
    """Optional. Caption of the video to be sent, 0-1024 characters after entities
    parsing."""

    parse_mode: Option[str] = Nothing
    """Optional. Mode for parsing entities in the video caption. See formatting
    options for more details."""

    caption_entities: Option[list["MessageEntity"]] = Nothing
    """Optional. List of special entities that appear in the caption, which can
    be specified instead of parse_mode."""

    show_caption_above_media: Option[bool] = Nothing
    """Optional. Pass True, if the caption must be shown above the message media."""

    width: Option[int] = Nothing
    """Optional. Video width."""

    height: Option[int] = Nothing
    """Optional. Video height."""

    duration: Option[int] = Nothing
    """Optional. Video duration in seconds."""

    supports_streaming: Option[bool] = Nothing
    """Optional. Pass True if the uploaded video is suitable for streaming."""

    has_spoiler: Option[bool] = Nothing
    """Optional. Pass True if the video needs to be covered with a spoiler animation."""


class InputMediaAnimation(InputMedia):
    """Object `InputMediaAnimation`, see the [documentation](https://core.telegram.org/bots/api#inputmediaanimation).

    Represents an animation file (GIF or H.264/MPEG-4 AVC video without sound) to be sent.
    """

    type: typing.Literal["animation"]
    """Type of the result, must be animation."""

    media: Variative["InputFile", str]
    """File to send. Pass a file_id to send a file that exists on the Telegram servers
    (recommended), pass an HTTP URL for Telegram to get a file from the Internet,
    or pass `attach://<file_attach_name>` to upload a new one using multipart/form-data
    under <file_attach_name> name. More information on Sending Files: https://core.telegram.org/bots/api#sending-files."""

    thumbnail: Option[Variative["InputFile", str]] = Nothing
    """Optional. Thumbnail of the file sent; can be ignored if thumbnail generation
    for the file is supported server-side. The thumbnail should be in JPEG format
    and less than 200 kB in size. A thumbnail's width and height should not exceed
    320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails
    can't be reused and can be only uploaded as a new file, so you can pass `attach://<file_attach_name>`
    if the thumbnail was uploaded using multipart/form-data under <file_attach_name>.
    More information on Sending Files: https://core.telegram.org/bots/api#sending-files."""

    caption: Option[str] = Nothing
    """Optional. Caption of the animation to be sent, 0-1024 characters after
    entities parsing."""

    parse_mode: Option[str] = Nothing
    """Optional. Mode for parsing entities in the animation caption. See formatting
    options for more details."""

    caption_entities: Option[list["MessageEntity"]] = Nothing
    """Optional. List of special entities that appear in the caption, which can
    be specified instead of parse_mode."""

    show_caption_above_media: Option[bool] = Nothing
    """Optional. Pass True, if the caption must be shown above the message media."""

    width: Option[int] = Nothing
    """Optional. Animation width."""

    height: Option[int] = Nothing
    """Optional. Animation height."""

    duration: Option[int] = Nothing
    """Optional. Animation duration in seconds."""

    has_spoiler: Option[bool] = Nothing
    """Optional. Pass True if the animation needs to be covered with a spoiler animation."""


class InputMediaAudio(InputMedia):
    """Object `InputMediaAudio`, see the [documentation](https://core.telegram.org/bots/api#inputmediaaudio).

    Represents an audio file to be treated as music to be sent.
    """

    type: typing.Literal["audio"]
    """Type of the result, must be audio."""

    media: Variative["InputFile", str]
    """File to send. Pass a file_id to send a file that exists on the Telegram servers
    (recommended), pass an HTTP URL for Telegram to get a file from the Internet,
    or pass `attach://<file_attach_name>` to upload a new one using multipart/form-data
    under <file_attach_name> name. More information on Sending Files: https://core.telegram.org/bots/api#sending-files."""

    thumbnail: Option[Variative["InputFile", str]] = Nothing
    """Optional. Thumbnail of the file sent; can be ignored if thumbnail generation
    for the file is supported server-side. The thumbnail should be in JPEG format
    and less than 200 kB in size. A thumbnail's width and height should not exceed
    320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails
    can't be reused and can be only uploaded as a new file, so you can pass `attach://<file_attach_name>`
    if the thumbnail was uploaded using multipart/form-data under <file_attach_name>.
    More information on Sending Files: https://core.telegram.org/bots/api#sending-files."""

    caption: Option[str] = Nothing
    """Optional. Caption of the audio to be sent, 0-1024 characters after entities
    parsing."""

    parse_mode: Option[str] = Nothing
    """Optional. Mode for parsing entities in the audio caption. See formatting
    options for more details."""

    caption_entities: Option[list["MessageEntity"]] = Nothing
    """Optional. List of special entities that appear in the caption, which can
    be specified instead of parse_mode."""

    duration: Option[int] = Nothing
    """Optional. Duration of the audio in seconds."""

    performer: Option[str] = Nothing
    """Optional. Performer of the audio."""

    title: Option[str] = Nothing
    """Optional. Title of the audio."""


class InputMediaDocument(InputMedia):
    """Object `InputMediaDocument`, see the [documentation](https://core.telegram.org/bots/api#inputmediadocument).

    Represents a general file to be sent.
    """

    type: typing.Literal["document"]
    """Type of the result, must be document."""

    media: Variative["InputFile", str]
    """File to send. Pass a file_id to send a file that exists on the Telegram servers
    (recommended), pass an HTTP URL for Telegram to get a file from the Internet,
    or pass `attach://<file_attach_name>` to upload a new one using multipart/form-data
    under <file_attach_name> name. More information on Sending Files: https://core.telegram.org/bots/api#sending-files."""

    thumbnail: Option[Variative["InputFile", str]] = Nothing
    """Optional. Thumbnail of the file sent; can be ignored if thumbnail generation
    for the file is supported server-side. The thumbnail should be in JPEG format
    and less than 200 kB in size. A thumbnail's width and height should not exceed
    320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails
    can't be reused and can be only uploaded as a new file, so you can pass `attach://<file_attach_name>`
    if the thumbnail was uploaded using multipart/form-data under <file_attach_name>.
    More information on Sending Files: https://core.telegram.org/bots/api#sending-files."""

    caption: Option[str] = Nothing
    """Optional. Caption of the document to be sent, 0-1024 characters after entities
    parsing."""

    parse_mode: Option[str] = Nothing
    """Optional. Mode for parsing entities in the document caption. See formatting
    options for more details."""

    caption_entities: Option[list["MessageEntity"]] = Nothing
    """Optional. List of special entities that appear in the caption, which can
    be specified instead of parse_mode."""

    disable_content_type_detection: Option[bool] = Nothing
    """Optional. Disables automatic server-side content type detection for
    files uploaded using multipart/form-data. Always True, if the document
    is sent as part of an album."""


class InputFile(typing.NamedTuple):
    """NamedTuple object `InputFile`, see the [documentation](https://core.telegram.org/bots/api#inputfile).

    This object represents the contents of a file to be uploaded. Must be posted using multipart/form-data in the usual way that files are uploaded via the browser.
    """

    filename: str
    """File name."""

    data: bytes
    """Bytes of file."""

    @classmethod
    def from_file(cls, path: str | pathlib.Path) -> typing.Self:
        path = pathlib.Path(path)
        return cls(
            filename=path.name,
            data=path.read_bytes(),
        )


class InputPaidMediaPhoto(InputPaidMedia):
    """Object `InputPaidMediaPhoto`, see the [documentation](https://core.telegram.org/bots/api#inputpaidmediaphoto).

    The paid media to send is a photo.
    """

    type: typing.Literal["photo"]
    """Type of the media, must be photo."""

    media: Variative["InputFile", str]
    """File to send. Pass a file_id to send a file that exists on the Telegram servers
    (recommended), pass an HTTP URL for Telegram to get a file from the Internet,
    or pass `attach://<file_attach_name>` to upload a new one using multipart/form-data
    under <file_attach_name> name. More information on Sending Files: https://core.telegram.org/bots/api#sending-files."""


class InputPaidMediaVideo(InputPaidMedia):
    """Object `InputPaidMediaVideo`, see the [documentation](https://core.telegram.org/bots/api#inputpaidmediavideo).

    The paid media to send is a video.
    """

    type: typing.Literal["video"]
    """Type of the media, must be video."""

    media: Variative["InputFile", str]
    """File to send. Pass a file_id to send a file that exists on the Telegram servers
    (recommended), pass an HTTP URL for Telegram to get a file from the Internet,
    or pass `attach://<file_attach_name>` to upload a new one using multipart/form-data
    under <file_attach_name> name. More information on Sending Files: https://core.telegram.org/bots/api#sending-files."""

    thumbnail: Option[Variative["InputFile", str]] = Nothing
    """Optional. Thumbnail of the file sent; can be ignored if thumbnail generation
    for the file is supported server-side. The thumbnail should be in JPEG format
    and less than 200 kB in size. A thumbnail's width and height should not exceed
    320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails
    can't be reused and can be only uploaded as a new file, so you can pass `attach://<file_attach_name>`
    if the thumbnail was uploaded using multipart/form-data under <file_attach_name>.
    More information on Sending Files: https://core.telegram.org/bots/api#sending-files."""

    width: Option[int] = Nothing
    """Optional. Video width."""

    height: Option[int] = Nothing
    """Optional. Video height."""

    duration: Option[int] = Nothing
    """Optional. Video duration in seconds."""

    supports_streaming: Option[bool] = Nothing
    """Optional. Pass True if the uploaded video is suitable for streaming."""


class Sticker(Model):
    """Object `Sticker`, see the [documentation](https://core.telegram.org/bots/api#sticker).

    This object represents a sticker.
    """

    file_id: str
    """Identifier for this file, which can be used to download or reuse the file."""

    file_unique_id: str
    """Unique identifier for this file, which is supposed to be the same over time
    and for different bots. Can't be used to download or reuse the file."""

    type: typing.Literal["regular", "mask", "custom_emoji"]
    """Type of the sticker, currently one of `regular`, `mask`, `custom_emoji`.
    The type of the sticker is independent from its format, which is determined
    by the fields is_animated and is_video."""

    width: int
    """Sticker width."""

    height: int
    """Sticker height."""

    is_animated: bool
    """True, if the sticker is animated."""

    is_video: bool
    """True, if the sticker is a video sticker."""

    thumbnail: Option["PhotoSize"] = Nothing
    """Optional. Sticker thumbnail in the .WEBP or .JPG format."""

    emoji: Option[str] = Nothing
    """Optional. Emoji associated with the sticker."""

    set_name: Option[str] = Nothing
    """Optional. Name of the sticker set to which the sticker belongs."""

    premium_animation: Option["File"] = Nothing
    """Optional. For premium regular stickers, premium animation for the sticker."""

    mask_position: Option["MaskPosition"] = Nothing
    """Optional. For mask stickers, the position where the mask should be placed."""

    custom_emoji_id: Option[str] = Nothing
    """Optional. For custom emoji stickers, unique identifier of the custom emoji."""

    needs_repainting: Option[bool] = Nothing
    """Optional. True, if the sticker must be repainted to a text color in messages,
    the color of the Telegram Premium badge in emoji status, white color on chat
    photos, or another appropriate color in other places."""

    file_size: Option[int] = Nothing
    """Optional. File size in bytes."""


class StickerSet(Model):
    """Object `StickerSet`, see the [documentation](https://core.telegram.org/bots/api#stickerset).

    This object represents a sticker set.
    """

    name: str
    """Sticker set name."""

    title: str
    """Sticker set title."""

    sticker_type: typing.Literal["regular", "mask", "custom_emoji"]
    """Type of stickers in the set, currently one of `regular`, `mask`, `custom_emoji`."""

    stickers: list["Sticker"]
    """List of all set stickers."""

    thumbnail: Option["PhotoSize"] = Nothing
    """Optional. Sticker set thumbnail in the .WEBP, .TGS, or .WEBM format."""


class MaskPosition(Model):
    """Object `MaskPosition`, see the [documentation](https://core.telegram.org/bots/api#maskposition).

    This object describes the position on faces where a mask should be placed by default.
    """

    point: str
    """The part of the face relative to which the mask should be placed. One of `forehead`,
    `eyes`, `mouth`, or `chin`."""

    x_shift: float
    """Shift by X-axis measured in widths of the mask scaled to the face size, from
    left to right. For example, choosing -1.0 will place mask just to the left
    of the default mask position."""

    y_shift: float
    """Shift by Y-axis measured in heights of the mask scaled to the face size, from
    top to bottom. For example, 1.0 will place the mask just below the default
    mask position."""

    scale: float
    """Mask scaling coefficient. For example, 2.0 means double size."""


class InputSticker(Model):
    """Object `InputSticker`, see the [documentation](https://core.telegram.org/bots/api#inputsticker).

    This object describes a sticker to be added to a sticker set.
    """

    sticker: Variative["InputFile", str]
    """The added sticker. Pass a file_id as a String to send a file that already exists
    on the Telegram servers, pass an HTTP URL as a String for Telegram to get a
    file from the Internet, upload a new one using multipart/form-data, or
    pass `attach://<file_attach_name>` to upload a new one using multipart/form-data
    under <file_attach_name> name. Animated and video stickers can't be uploaded
    via HTTP URL. More information on Sending Files: https://core.telegram.org/bots/api#sending-files."""

    format: str
    """Format of the added sticker, must be one of `static` for a .WEBP or .PNG image,
    `animated` for a .TGS animation, `video` for a WEBM video."""

    emoji_list: list[str]
    """List of 1-20 emoji associated with the sticker."""

    mask_position: Option["MaskPosition"] = Nothing
    """Optional. Position where the mask should be placed on faces. For `mask`
    stickers only."""

    keywords: Option[list[str]] = Nothing
    """Optional. List of 0-20 search keywords for the sticker with total length
    of up to 64 characters. For `regular` and `custom_emoji` stickers only."""


class InlineQuery(Model):
    """Object `InlineQuery`, see the [documentation](https://core.telegram.org/bots/api#inlinequery).

    This object represents an incoming inline query. When the user sends an empty query, your bot could return some default or trending results.
    """

    id: str
    """Unique identifier for this query."""

    from_: "User"
    """Sender."""

    query: str
    """Text of the query (up to 256 characters)."""

    offset: str
    """Offset of the results to be returned, can be controlled by the bot."""

    chat_type: Option[ChatType] = Nothing
    """Optional. Type of the chat from which the inline query was sent. Can be either
    `sender` for a private chat with the inline query sender, `private`, `group`,
    `supergroup`, or `channel`. The chat type should be always known for requests
    sent from official clients and most third-party clients, unless the request
    was sent from a secret chat."""

    location: Option["Location"] = Nothing
    """Optional. Sender location, only for bots that request user location."""


class InlineQueryResultsButton(Model):
    """Object `InlineQueryResultsButton`, see the [documentation](https://core.telegram.org/bots/api#inlinequeryresultsbutton).

    This object represents a button to be shown above inline query results. You must use exactly one of the optional fields.
    """

    text: str
    """Label text on the button."""

    web_app: Option["WebAppInfo"] = Nothing
    """Optional. Description of the Web App that will be launched when the user
    presses the button. The Web App will be able to switch back to the inline mode
    using the method switchInlineQuery inside the Web App."""

    start_parameter: Option[str] = Nothing
    """Optional. Deep-linking parameter for the /start message sent to the bot
    when a user presses the button. 1-64 characters, only A-Z, a-z, 0-9, _ and
    - are allowed. Example: An inline bot that sends YouTube videos can ask the
    user to connect the bot to their YouTube account to adapt search results
    accordingly. To do this, it displays a 'Connect your YouTube account' button
    above the results, or even before showing any. The user presses the button,
    switches to a private chat with the bot and, in doing so, passes a start parameter
    that instructs the bot to return an OAuth link. Once done, the bot can offer
    a switch_inline button so that the user can easily return to the chat where
    they wanted to use the bot's inline capabilities."""


class InlineQueryResultArticle(InlineQueryResult):
    """Object `InlineQueryResultArticle`, see the [documentation](https://core.telegram.org/bots/api#inlinequeryresultarticle).

    Represents a link to an article or web page.
    """

    type: typing.Literal["article"]
    """Type of the result, must be article."""

    id: str
    """Unique identifier for this result, 1-64 Bytes."""

    title: str
    """Title of the result."""

    input_message_content: Variative[
        "InputTextMessageContent",
        "InputLocationMessageContent",
        "InputVenueMessageContent",
        "InputContactMessageContent",
        "InputInvoiceMessageContent",
    ]
    """Content of the message to be sent."""

    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    """Optional. Inline keyboard attached to the message."""

    url: Option[str] = Nothing
    """Optional. URL of the result."""

    hide_url: Option[bool] = Nothing
    """Optional. Pass True if you don't want the URL to be shown in the message."""

    description: Option[str] = Nothing
    """Optional. Short description of the result."""

    thumbnail_url: Option[str] = Nothing
    """Optional. Url of the thumbnail for the result."""

    thumbnail_width: Option[int] = Nothing
    """Optional. Thumbnail width."""

    thumbnail_height: Option[int] = Nothing
    """Optional. Thumbnail height."""


class InlineQueryResultPhoto(InlineQueryResult):
    """Object `InlineQueryResultPhoto`, see the [documentation](https://core.telegram.org/bots/api#inlinequeryresultphoto).

    Represents a link to a photo. By default, this photo will be sent by the user with optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the photo.
    """

    type: typing.Literal["photo"]
    """Type of the result, must be photo."""

    id: str
    """Unique identifier for this result, 1-64 bytes."""

    photo_url: str
    """A valid URL of the photo. Photo must be in JPEG format. Photo size must not
    exceed 5MB."""

    thumbnail_url: str
    """URL of the thumbnail for the photo."""

    photo_width: Option[int] = Nothing
    """Optional. Width of the photo."""

    photo_height: Option[int] = Nothing
    """Optional. Height of the photo."""

    title: Option[str] = Nothing
    """Optional. Title for the result."""

    description: Option[str] = Nothing
    """Optional. Short description of the result."""

    caption: Option[str] = Nothing
    """Optional. Caption of the photo to be sent, 0-1024 characters after entities
    parsing."""

    parse_mode: Option[str] = Nothing
    """Optional. Mode for parsing entities in the photo caption. See formatting
    options for more details."""

    caption_entities: Option[list["MessageEntity"]] = Nothing
    """Optional. List of special entities that appear in the caption, which can
    be specified instead of parse_mode."""

    show_caption_above_media: Option[bool] = Nothing
    """Optional. Pass True, if the caption must be shown above the message media."""

    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    """Optional. Inline keyboard attached to the message."""

    input_message_content: Option[
        Variative[
            "InputTextMessageContent",
            "InputLocationMessageContent",
            "InputVenueMessageContent",
            "InputContactMessageContent",
            "InputInvoiceMessageContent",
        ]
    ] = Nothing
    """Optional. Content of the message to be sent instead of the photo."""


class InlineQueryResultGif(InlineQueryResult):
    """Object `InlineQueryResultGif`, see the [documentation](https://core.telegram.org/bots/api#inlinequeryresultgif).

    Represents a link to an animated GIF file. By default, this animated GIF file will be sent by the user with optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the animation.
    """

    type: typing.Literal["gif"]
    """Type of the result, must be gif."""

    id: str
    """Unique identifier for this result, 1-64 bytes."""

    gif_url: str
    """A valid URL for the GIF file. File size must not exceed 1MB."""

    thumbnail_url: str
    """URL of the static (JPEG or GIF) or animated (MPEG4) thumbnail for the result."""

    gif_width: Option[int] = Nothing
    """Optional. Width of the GIF."""

    gif_height: Option[int] = Nothing
    """Optional. Height of the GIF."""

    gif_duration: Option[int] = Nothing
    """Optional. Duration of the GIF in seconds."""

    thumbnail_mime_type: Option[typing.Literal["image/jpeg", "image/gif", "video/mp4"]] = Nothing
    """Optional. MIME type of the thumbnail, must be one of `image/jpeg`, `image/gif`,
    or `video/mp4`. Defaults to `image/jpeg`."""

    title: Option[str] = Nothing
    """Optional. Title for the result."""

    caption: Option[str] = Nothing
    """Optional. Caption of the GIF file to be sent, 0-1024 characters after entities
    parsing."""

    parse_mode: Option[str] = Nothing
    """Optional. Mode for parsing entities in the caption. See formatting options
    for more details."""

    caption_entities: Option[list["MessageEntity"]] = Nothing
    """Optional. List of special entities that appear in the caption, which can
    be specified instead of parse_mode."""

    show_caption_above_media: Option[bool] = Nothing
    """Optional. Pass True, if the caption must be shown above the message media."""

    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    """Optional. Inline keyboard attached to the message."""

    input_message_content: Option[
        Variative[
            "InputTextMessageContent",
            "InputLocationMessageContent",
            "InputVenueMessageContent",
            "InputContactMessageContent",
            "InputInvoiceMessageContent",
        ]
    ] = Nothing
    """Optional. Content of the message to be sent instead of the GIF animation."""


class InlineQueryResultMpeg4Gif(InlineQueryResult):
    """Object `InlineQueryResultMpeg4Gif`, see the [documentation](https://core.telegram.org/bots/api#inlinequeryresultmpeg4gif).

    Represents a link to a video animation (H.264/MPEG-4 AVC video without sound). By default, this animated MPEG-4 file will be sent by the user with optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the animation.
    """

    type: typing.Literal["mpeg4_gif"]
    """Type of the result, must be mpeg4_gif."""

    id: str
    """Unique identifier for this result, 1-64 bytes."""

    mpeg4_url: str
    """A valid URL for the MPEG4 file. File size must not exceed 1MB."""

    thumbnail_url: str
    """URL of the static (JPEG or GIF) or animated (MPEG4) thumbnail for the result."""

    mpeg4_width: Option[int] = Nothing
    """Optional. Video width."""

    mpeg4_height: Option[int] = Nothing
    """Optional. Video height."""

    mpeg4_duration: Option[int] = Nothing
    """Optional. Video duration in seconds."""

    thumbnail_mime_type: Option[typing.Literal["image/jpeg", "image/gif", "video/mp4"]] = Nothing
    """Optional. MIME type of the thumbnail, must be one of `image/jpeg`, `image/gif`,
    or `video/mp4`. Defaults to `image/jpeg`."""

    title: Option[str] = Nothing
    """Optional. Title for the result."""

    caption: Option[str] = Nothing
    """Optional. Caption of the MPEG-4 file to be sent, 0-1024 characters after
    entities parsing."""

    parse_mode: Option[str] = Nothing
    """Optional. Mode for parsing entities in the caption. See formatting options
    for more details."""

    caption_entities: Option[list["MessageEntity"]] = Nothing
    """Optional. List of special entities that appear in the caption, which can
    be specified instead of parse_mode."""

    show_caption_above_media: Option[bool] = Nothing
    """Optional. Pass True, if the caption must be shown above the message media."""

    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    """Optional. Inline keyboard attached to the message."""

    input_message_content: Option[
        Variative[
            "InputTextMessageContent",
            "InputLocationMessageContent",
            "InputVenueMessageContent",
            "InputContactMessageContent",
            "InputInvoiceMessageContent",
        ]
    ] = Nothing
    """Optional. Content of the message to be sent instead of the video animation."""


class InlineQueryResultVideo(InlineQueryResult):
    """Object `InlineQueryResultVideo`, see the [documentation](https://core.telegram.org/bots/api#inlinequeryresultvideo).

    Represents a link to a page containing an embedded video player or a video file. By default, this video file will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the video.
    """

    type: typing.Literal["video"]
    """Type of the result, must be video."""

    id: str
    """Unique identifier for this result, 1-64 bytes."""

    video_url: str
    """A valid URL for the embedded video player or video file."""

    mime_type: str
    """MIME type of the content of the video URL, `text/html` or `video/mp4`."""

    thumbnail_url: str
    """URL of the thumbnail (JPEG only) for the video."""

    title: str
    """Title for the result."""

    caption: Option[str] = Nothing
    """Optional. Caption of the video to be sent, 0-1024 characters after entities
    parsing."""

    parse_mode: Option[str] = Nothing
    """Optional. Mode for parsing entities in the video caption. See formatting
    options for more details."""

    caption_entities: Option[list["MessageEntity"]] = Nothing
    """Optional. List of special entities that appear in the caption, which can
    be specified instead of parse_mode."""

    show_caption_above_media: Option[bool] = Nothing
    """Optional. Pass True, if the caption must be shown above the message media."""

    video_width: Option[int] = Nothing
    """Optional. Video width."""

    video_height: Option[int] = Nothing
    """Optional. Video height."""

    video_duration: Option[int] = Nothing
    """Optional. Video duration in seconds."""

    description: Option[str] = Nothing
    """Optional. Short description of the result."""

    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    """Optional. Inline keyboard attached to the message."""

    input_message_content: Option[
        Variative[
            "InputTextMessageContent",
            "InputLocationMessageContent",
            "InputVenueMessageContent",
            "InputContactMessageContent",
            "InputInvoiceMessageContent",
        ]
    ] = Nothing
    """Optional. Content of the message to be sent instead of the video. This field
    is required if InlineQueryResultVideo is used to send an HTML-page as a
    result (e.g., a YouTube video)."""


class InlineQueryResultAudio(InlineQueryResult):
    """Object `InlineQueryResultAudio`, see the [documentation](https://core.telegram.org/bots/api#inlinequeryresultaudio).

    Represents a link to an MP3 audio file. By default, this audio file will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the audio.
    """

    type: typing.Literal["audio"]
    """Type of the result, must be audio."""

    id: str
    """Unique identifier for this result, 1-64 bytes."""

    audio_url: str
    """A valid URL for the audio file."""

    title: str
    """Title."""

    caption: Option[str] = Nothing
    """Optional. Caption, 0-1024 characters after entities parsing."""

    parse_mode: Option[str] = Nothing
    """Optional. Mode for parsing entities in the audio caption. See formatting
    options for more details."""

    caption_entities: Option[list["MessageEntity"]] = Nothing
    """Optional. List of special entities that appear in the caption, which can
    be specified instead of parse_mode."""

    performer: Option[str] = Nothing
    """Optional. Performer."""

    audio_duration: Option[int] = Nothing
    """Optional. Audio duration in seconds."""

    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    """Optional. Inline keyboard attached to the message."""

    input_message_content: Option[
        Variative[
            "InputTextMessageContent",
            "InputLocationMessageContent",
            "InputVenueMessageContent",
            "InputContactMessageContent",
            "InputInvoiceMessageContent",
        ]
    ] = Nothing
    """Optional. Content of the message to be sent instead of the audio."""


class InlineQueryResultVoice(InlineQueryResult):
    """Object `InlineQueryResultVoice`, see the [documentation](https://core.telegram.org/bots/api#inlinequeryresultvoice).

    Represents a link to a voice recording in an .OGG container encoded with OPUS. By default, this voice recording will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the the voice message.
    """

    type: typing.Literal["voice"]
    """Type of the result, must be voice."""

    id: str
    """Unique identifier for this result, 1-64 bytes."""

    voice_url: str
    """A valid URL for the voice recording."""

    title: str
    """Recording title."""

    caption: Option[str] = Nothing
    """Optional. Caption, 0-1024 characters after entities parsing."""

    parse_mode: Option[str] = Nothing
    """Optional. Mode for parsing entities in the voice message caption. See formatting
    options for more details."""

    caption_entities: Option[list["MessageEntity"]] = Nothing
    """Optional. List of special entities that appear in the caption, which can
    be specified instead of parse_mode."""

    voice_duration: Option[int] = Nothing
    """Optional. Recording duration in seconds."""

    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    """Optional. Inline keyboard attached to the message."""

    input_message_content: Option[
        Variative[
            "InputTextMessageContent",
            "InputLocationMessageContent",
            "InputVenueMessageContent",
            "InputContactMessageContent",
            "InputInvoiceMessageContent",
        ]
    ] = Nothing
    """Optional. Content of the message to be sent instead of the voice recording."""


class InlineQueryResultDocument(InlineQueryResult):
    """Object `InlineQueryResultDocument`, see the [documentation](https://core.telegram.org/bots/api#inlinequeryresultdocument).

    Represents a link to a file. By default, this file will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the file. Currently, only .PDF and .ZIP files can be sent using this method.
    """

    type: typing.Literal["document"]
    """Type of the result, must be document."""

    id: str
    """Unique identifier for this result, 1-64 bytes."""

    title: str
    """Title for the result."""

    document_url: str
    """A valid URL for the file."""

    mime_type: typing.Literal["application/pdf", "application/zip"]
    """MIME type of the content of the file, either `application/pdf` or `application/zip`."""

    caption: Option[str] = Nothing
    """Optional. Caption of the document to be sent, 0-1024 characters after entities
    parsing."""

    parse_mode: Option[str] = Nothing
    """Optional. Mode for parsing entities in the document caption. See formatting
    options for more details."""

    caption_entities: Option[list["MessageEntity"]] = Nothing
    """Optional. List of special entities that appear in the caption, which can
    be specified instead of parse_mode."""

    description: Option[str] = Nothing
    """Optional. Short description of the result."""

    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    """Optional. Inline keyboard attached to the message."""

    input_message_content: Option[
        Variative[
            "InputTextMessageContent",
            "InputLocationMessageContent",
            "InputVenueMessageContent",
            "InputContactMessageContent",
            "InputInvoiceMessageContent",
        ]
    ] = Nothing
    """Optional. Content of the message to be sent instead of the file."""

    thumbnail_url: Option[str] = Nothing
    """Optional. URL of the thumbnail (JPEG only) for the file."""

    thumbnail_width: Option[int] = Nothing
    """Optional. Thumbnail width."""

    thumbnail_height: Option[int] = Nothing
    """Optional. Thumbnail height."""


class InlineQueryResultLocation(InlineQueryResult):
    """Object `InlineQueryResultLocation`, see the [documentation](https://core.telegram.org/bots/api#inlinequeryresultlocation).

    Represents a location on a map. By default, the location will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the location.
    """

    type: typing.Literal["location"]
    """Type of the result, must be location."""

    id: str
    """Unique identifier for this result, 1-64 Bytes."""

    latitude: float
    """Location latitude in degrees."""

    longitude: float
    """Location longitude in degrees."""

    title: str
    """Location title."""

    horizontal_accuracy: Option[float] = Nothing
    """Optional. The radius of uncertainty for the location, measured in meters;
    0-1500."""

    live_period: Option[int] = Nothing
    """Optional. Period in seconds during which the location can be updated, should
    be between 60 and 86400, or 0x7FFFFFFF for live locations that can be edited
    indefinitely."""

    heading: Option[int] = Nothing
    """Optional. For live locations, a direction in which the user is moving, in
    degrees. Must be between 1 and 360 if specified."""

    proximity_alert_radius: Option[int] = Nothing
    """Optional. For live locations, a maximum distance for proximity alerts
    about approaching another chat member, in meters. Must be between 1 and
    100000 if specified."""

    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    """Optional. Inline keyboard attached to the message."""

    input_message_content: Option[
        Variative[
            "InputTextMessageContent",
            "InputLocationMessageContent",
            "InputVenueMessageContent",
            "InputContactMessageContent",
            "InputInvoiceMessageContent",
        ]
    ] = Nothing
    """Optional. Content of the message to be sent instead of the location."""

    thumbnail_url: Option[str] = Nothing
    """Optional. Url of the thumbnail for the result."""

    thumbnail_width: Option[int] = Nothing
    """Optional. Thumbnail width."""

    thumbnail_height: Option[int] = Nothing
    """Optional. Thumbnail height."""


class InlineQueryResultVenue(InlineQueryResult):
    """Object `InlineQueryResultVenue`, see the [documentation](https://core.telegram.org/bots/api#inlinequeryresultvenue).

    Represents a venue. By default, the venue will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the venue.
    """

    type: typing.Literal["venue"]
    """Type of the result, must be venue."""

    id: str
    """Unique identifier for this result, 1-64 Bytes."""

    latitude: float
    """Latitude of the venue location in degrees."""

    longitude: float
    """Longitude of the venue location in degrees."""

    title: str
    """Title of the venue."""

    address: str
    """Address of the venue."""

    foursquare_id: Option[str] = Nothing
    """Optional. Foursquare identifier of the venue if known."""

    foursquare_type: Option[str] = Nothing
    """Optional. Foursquare type of the venue, if known. (For example, `arts_entertainment/default`,
    `arts_entertainment/aquarium` or `food/icecream`.)."""

    google_place_id: Option[str] = Nothing
    """Optional. Google Places identifier of the venue."""

    google_place_type: Option[str] = Nothing
    """Optional. Google Places type of the venue. (See supported types.)."""

    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    """Optional. Inline keyboard attached to the message."""

    input_message_content: Option[
        Variative[
            "InputTextMessageContent",
            "InputLocationMessageContent",
            "InputVenueMessageContent",
            "InputContactMessageContent",
            "InputInvoiceMessageContent",
        ]
    ] = Nothing
    """Optional. Content of the message to be sent instead of the venue."""

    thumbnail_url: Option[str] = Nothing
    """Optional. Url of the thumbnail for the result."""

    thumbnail_width: Option[int] = Nothing
    """Optional. Thumbnail width."""

    thumbnail_height: Option[int] = Nothing
    """Optional. Thumbnail height."""


class InlineQueryResultContact(InlineQueryResult):
    """Object `InlineQueryResultContact`, see the [documentation](https://core.telegram.org/bots/api#inlinequeryresultcontact).

    Represents a contact with a phone number. By default, this contact will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the contact.
    """

    type: typing.Literal["contact"]
    """Type of the result, must be contact."""

    id: str
    """Unique identifier for this result, 1-64 Bytes."""

    phone_number: str
    """Contact's phone number."""

    first_name: str
    """Contact's first name."""

    last_name: Option[str] = Nothing
    """Optional. Contact's last name."""

    vcard: Option[str] = Nothing
    """Optional. Additional data about the contact in the form of a vCard, 0-2048
    bytes."""

    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    """Optional. Inline keyboard attached to the message."""

    input_message_content: Option[
        Variative[
            "InputTextMessageContent",
            "InputLocationMessageContent",
            "InputVenueMessageContent",
            "InputContactMessageContent",
            "InputInvoiceMessageContent",
        ]
    ] = Nothing
    """Optional. Content of the message to be sent instead of the contact."""

    thumbnail_url: Option[str] = Nothing
    """Optional. Url of the thumbnail for the result."""

    thumbnail_width: Option[int] = Nothing
    """Optional. Thumbnail width."""

    thumbnail_height: Option[int] = Nothing
    """Optional. Thumbnail height."""


class InlineQueryResultGame(InlineQueryResult):
    """Object `InlineQueryResultGame`, see the [documentation](https://core.telegram.org/bots/api#inlinequeryresultgame).

    Represents a Game.
    """

    type: typing.Literal["game"]
    """Type of the result, must be game."""

    id: str
    """Unique identifier for this result, 1-64 bytes."""

    game_short_name: str
    """Short name of the game."""

    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    """Optional. Inline keyboard attached to the message."""


class InlineQueryResultCachedPhoto(InlineQueryResult):
    """Object `InlineQueryResultCachedPhoto`, see the [documentation](https://core.telegram.org/bots/api#inlinequeryresultcachedphoto).

    Represents a link to a photo stored on the Telegram servers. By default, this photo will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the photo.
    """

    type: typing.Literal["photo"]
    """Type of the result, must be photo."""

    id: str
    """Unique identifier for this result, 1-64 bytes."""

    photo_file_id: str
    """A valid file identifier of the photo."""

    title: Option[str] = Nothing
    """Optional. Title for the result."""

    description: Option[str] = Nothing
    """Optional. Short description of the result."""

    caption: Option[str] = Nothing
    """Optional. Caption of the photo to be sent, 0-1024 characters after entities
    parsing."""

    parse_mode: Option[str] = Nothing
    """Optional. Mode for parsing entities in the photo caption. See formatting
    options for more details."""

    caption_entities: Option[list["MessageEntity"]] = Nothing
    """Optional. List of special entities that appear in the caption, which can
    be specified instead of parse_mode."""

    show_caption_above_media: Option[bool] = Nothing
    """Optional. Pass True, if the caption must be shown above the message media."""

    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    """Optional. Inline keyboard attached to the message."""

    input_message_content: Option[
        Variative[
            "InputTextMessageContent",
            "InputLocationMessageContent",
            "InputVenueMessageContent",
            "InputContactMessageContent",
            "InputInvoiceMessageContent",
        ]
    ] = Nothing
    """Optional. Content of the message to be sent instead of the photo."""


class InlineQueryResultCachedGif(InlineQueryResult):
    """Object `InlineQueryResultCachedGif`, see the [documentation](https://core.telegram.org/bots/api#inlinequeryresultcachedgif).

    Represents a link to an animated GIF file stored on the Telegram servers. By default, this animated GIF file will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with specified content instead of the animation.
    """

    type: typing.Literal["gif"]
    """Type of the result, must be gif."""

    id: str
    """Unique identifier for this result, 1-64 bytes."""

    gif_file_id: str
    """A valid file identifier for the GIF file."""

    title: Option[str] = Nothing
    """Optional. Title for the result."""

    caption: Option[str] = Nothing
    """Optional. Caption of the GIF file to be sent, 0-1024 characters after entities
    parsing."""

    parse_mode: Option[str] = Nothing
    """Optional. Mode for parsing entities in the caption. See formatting options
    for more details."""

    caption_entities: Option[list["MessageEntity"]] = Nothing
    """Optional. List of special entities that appear in the caption, which can
    be specified instead of parse_mode."""

    show_caption_above_media: Option[bool] = Nothing
    """Optional. Pass True, if the caption must be shown above the message media."""

    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    """Optional. Inline keyboard attached to the message."""

    input_message_content: Option[
        Variative[
            "InputTextMessageContent",
            "InputLocationMessageContent",
            "InputVenueMessageContent",
            "InputContactMessageContent",
            "InputInvoiceMessageContent",
        ]
    ] = Nothing
    """Optional. Content of the message to be sent instead of the GIF animation."""


class InlineQueryResultCachedMpeg4Gif(InlineQueryResult):
    """Object `InlineQueryResultCachedMpeg4Gif`, see the [documentation](https://core.telegram.org/bots/api#inlinequeryresultcachedmpeg4gif).

    Represents a link to a video animation (H.264/MPEG-4 AVC video without sound) stored on the Telegram servers. By default, this animated MPEG-4 file will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the animation.
    """

    type: typing.Literal["mpeg4_gif"]
    """Type of the result, must be mpeg4_gif."""

    id: str
    """Unique identifier for this result, 1-64 bytes."""

    mpeg4_file_id: str
    """A valid file identifier for the MPEG4 file."""

    title: Option[str] = Nothing
    """Optional. Title for the result."""

    caption: Option[str] = Nothing
    """Optional. Caption of the MPEG-4 file to be sent, 0-1024 characters after
    entities parsing."""

    parse_mode: Option[str] = Nothing
    """Optional. Mode for parsing entities in the caption. See formatting options
    for more details."""

    caption_entities: Option[list["MessageEntity"]] = Nothing
    """Optional. List of special entities that appear in the caption, which can
    be specified instead of parse_mode."""

    show_caption_above_media: Option[bool] = Nothing
    """Optional. Pass True, if the caption must be shown above the message media."""

    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    """Optional. Inline keyboard attached to the message."""

    input_message_content: Option[
        Variative[
            "InputTextMessageContent",
            "InputLocationMessageContent",
            "InputVenueMessageContent",
            "InputContactMessageContent",
            "InputInvoiceMessageContent",
        ]
    ] = Nothing
    """Optional. Content of the message to be sent instead of the video animation."""


class InlineQueryResultCachedSticker(InlineQueryResult):
    """Object `InlineQueryResultCachedSticker`, see the [documentation](https://core.telegram.org/bots/api#inlinequeryresultcachedsticker).

    Represents a link to a sticker stored on the Telegram servers. By default, this sticker will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the sticker.
    """

    type: typing.Literal["sticker"]
    """Type of the result, must be sticker."""

    id: str
    """Unique identifier for this result, 1-64 bytes."""

    sticker_file_id: str
    """A valid file identifier of the sticker."""

    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    """Optional. Inline keyboard attached to the message."""

    input_message_content: Option[
        Variative[
            "InputTextMessageContent",
            "InputLocationMessageContent",
            "InputVenueMessageContent",
            "InputContactMessageContent",
            "InputInvoiceMessageContent",
        ]
    ] = Nothing
    """Optional. Content of the message to be sent instead of the sticker."""


class InlineQueryResultCachedDocument(InlineQueryResult):
    """Object `InlineQueryResultCachedDocument`, see the [documentation](https://core.telegram.org/bots/api#inlinequeryresultcacheddocument).

    Represents a link to a file stored on the Telegram servers. By default, this file will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the file.
    """

    type: typing.Literal["document"]
    """Type of the result, must be document."""

    id: str
    """Unique identifier for this result, 1-64 bytes."""

    title: str
    """Title for the result."""

    document_file_id: str
    """A valid file identifier for the file."""

    description: Option[str] = Nothing
    """Optional. Short description of the result."""

    caption: Option[str] = Nothing
    """Optional. Caption of the document to be sent, 0-1024 characters after entities
    parsing."""

    parse_mode: Option[str] = Nothing
    """Optional. Mode for parsing entities in the document caption. See formatting
    options for more details."""

    caption_entities: Option[list["MessageEntity"]] = Nothing
    """Optional. List of special entities that appear in the caption, which can
    be specified instead of parse_mode."""

    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    """Optional. Inline keyboard attached to the message."""

    input_message_content: Option[
        Variative[
            "InputTextMessageContent",
            "InputLocationMessageContent",
            "InputVenueMessageContent",
            "InputContactMessageContent",
            "InputInvoiceMessageContent",
        ]
    ] = Nothing
    """Optional. Content of the message to be sent instead of the file."""


class InlineQueryResultCachedVideo(InlineQueryResult):
    """Object `InlineQueryResultCachedVideo`, see the [documentation](https://core.telegram.org/bots/api#inlinequeryresultcachedvideo).

    Represents a link to a video file stored on the Telegram servers. By default, this video file will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the video.
    """

    type: typing.Literal["video"]
    """Type of the result, must be video."""

    id: str
    """Unique identifier for this result, 1-64 bytes."""

    video_file_id: str
    """A valid file identifier for the video file."""

    title: str
    """Title for the result."""

    description: Option[str] = Nothing
    """Optional. Short description of the result."""

    caption: Option[str] = Nothing
    """Optional. Caption of the video to be sent, 0-1024 characters after entities
    parsing."""

    parse_mode: Option[str] = Nothing
    """Optional. Mode for parsing entities in the video caption. See formatting
    options for more details."""

    caption_entities: Option[list["MessageEntity"]] = Nothing
    """Optional. List of special entities that appear in the caption, which can
    be specified instead of parse_mode."""

    show_caption_above_media: Option[bool] = Nothing
    """Optional. Pass True, if the caption must be shown above the message media."""

    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    """Optional. Inline keyboard attached to the message."""

    input_message_content: Option[
        Variative[
            "InputTextMessageContent",
            "InputLocationMessageContent",
            "InputVenueMessageContent",
            "InputContactMessageContent",
            "InputInvoiceMessageContent",
        ]
    ] = Nothing
    """Optional. Content of the message to be sent instead of the video."""


class InlineQueryResultCachedVoice(InlineQueryResult):
    """Object `InlineQueryResultCachedVoice`, see the [documentation](https://core.telegram.org/bots/api#inlinequeryresultcachedvoice).

    Represents a link to a voice message stored on the Telegram servers. By default, this voice message will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the voice message.
    """

    type: typing.Literal["voice"]
    """Type of the result, must be voice."""

    id: str
    """Unique identifier for this result, 1-64 bytes."""

    voice_file_id: str
    """A valid file identifier for the voice message."""

    title: str
    """Voice message title."""

    caption: Option[str] = Nothing
    """Optional. Caption, 0-1024 characters after entities parsing."""

    parse_mode: Option[str] = Nothing
    """Optional. Mode for parsing entities in the voice message caption. See formatting
    options for more details."""

    caption_entities: Option[list["MessageEntity"]] = Nothing
    """Optional. List of special entities that appear in the caption, which can
    be specified instead of parse_mode."""

    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    """Optional. Inline keyboard attached to the message."""

    input_message_content: Option[
        Variative[
            "InputTextMessageContent",
            "InputLocationMessageContent",
            "InputVenueMessageContent",
            "InputContactMessageContent",
            "InputInvoiceMessageContent",
        ]
    ] = Nothing
    """Optional. Content of the message to be sent instead of the voice message."""


class InlineQueryResultCachedAudio(InlineQueryResult):
    """Object `InlineQueryResultCachedAudio`, see the [documentation](https://core.telegram.org/bots/api#inlinequeryresultcachedaudio).

    Represents a link to an MP3 audio file stored on the Telegram servers. By default, this audio file will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the audio.
    """

    type: typing.Literal["audio"]
    """Type of the result, must be audio."""

    id: str
    """Unique identifier for this result, 1-64 bytes."""

    audio_file_id: str
    """A valid file identifier for the audio file."""

    caption: Option[str] = Nothing
    """Optional. Caption, 0-1024 characters after entities parsing."""

    parse_mode: Option[str] = Nothing
    """Optional. Mode for parsing entities in the audio caption. See formatting
    options for more details."""

    caption_entities: Option[list["MessageEntity"]] = Nothing
    """Optional. List of special entities that appear in the caption, which can
    be specified instead of parse_mode."""

    reply_markup: Option["InlineKeyboardMarkup"] = Nothing
    """Optional. Inline keyboard attached to the message."""

    input_message_content: Option[
        Variative[
            "InputTextMessageContent",
            "InputLocationMessageContent",
            "InputVenueMessageContent",
            "InputContactMessageContent",
            "InputInvoiceMessageContent",
        ]
    ] = Nothing
    """Optional. Content of the message to be sent instead of the audio."""


class InputTextMessageContent(InputMessageContent):
    """Object `InputTextMessageContent`, see the [documentation](https://core.telegram.org/bots/api#inputtextmessagecontent).

    Represents the content of a text message to be sent as the result of an inline query.
    """

    message_text: str
    """Text of the message to be sent, 1-4096 characters."""

    parse_mode: Option[str] = Nothing
    """Optional. Mode for parsing entities in the message text. See formatting
    options for more details."""

    entities: Option[list["MessageEntity"]] = Nothing
    """Optional. List of special entities that appear in message text, which can
    be specified instead of parse_mode."""

    link_preview_options: Option["LinkPreviewOptions"] = Nothing
    """Optional. Link preview generation options for the message."""


class InputLocationMessageContent(InputMessageContent):
    """Object `InputLocationMessageContent`, see the [documentation](https://core.telegram.org/bots/api#inputlocationmessagecontent).

    Represents the content of a location message to be sent as the result of an inline query.
    """

    latitude: float
    """Latitude of the location in degrees."""

    longitude: float
    """Longitude of the location in degrees."""

    horizontal_accuracy: Option[float] = Nothing
    """Optional. The radius of uncertainty for the location, measured in meters;
    0-1500."""

    live_period: Option[int] = Nothing
    """Optional. Period in seconds during which the location can be updated, should
    be between 60 and 86400, or 0x7FFFFFFF for live locations that can be edited
    indefinitely."""

    heading: Option[int] = Nothing
    """Optional. For live locations, a direction in which the user is moving, in
    degrees. Must be between 1 and 360 if specified."""

    proximity_alert_radius: Option[int] = Nothing
    """Optional. For live locations, a maximum distance for proximity alerts
    about approaching another chat member, in meters. Must be between 1 and
    100000 if specified."""


class InputVenueMessageContent(InputMessageContent):
    """Object `InputVenueMessageContent`, see the [documentation](https://core.telegram.org/bots/api#inputvenuemessagecontent).

    Represents the content of a venue message to be sent as the result of an inline query.
    """

    latitude: float
    """Latitude of the venue in degrees."""

    longitude: float
    """Longitude of the venue in degrees."""

    title: str
    """Name of the venue."""

    address: str
    """Address of the venue."""

    foursquare_id: Option[str] = Nothing
    """Optional. Foursquare identifier of the venue, if known."""

    foursquare_type: Option[str] = Nothing
    """Optional. Foursquare type of the venue, if known. (For example, `arts_entertainment/default`,
    `arts_entertainment/aquarium` or `food/icecream`.)."""

    google_place_id: Option[str] = Nothing
    """Optional. Google Places identifier of the venue."""

    google_place_type: Option[str] = Nothing
    """Optional. Google Places type of the venue. (See supported types.)."""


class InputContactMessageContent(InputMessageContent):
    """Object `InputContactMessageContent`, see the [documentation](https://core.telegram.org/bots/api#inputcontactmessagecontent).

    Represents the content of a contact message to be sent as the result of an inline query.
    """

    phone_number: str
    """Contact's phone number."""

    first_name: str
    """Contact's first name."""

    last_name: Option[str] = Nothing
    """Optional. Contact's last name."""

    vcard: Option[str] = Nothing
    """Optional. Additional data about the contact in the form of a vCard, 0-2048
    bytes."""


class InputInvoiceMessageContent(InputMessageContent):
    """Object `InputInvoiceMessageContent`, see the [documentation](https://core.telegram.org/bots/api#inputinvoicemessagecontent).

    Represents the content of an invoice message to be sent as the result of an inline query.
    """

    title: str
    """Product name, 1-32 characters."""

    description: str
    """Product description, 1-255 characters."""

    payload: str
    """Bot-defined invoice payload, 1-128 bytes. This will not be displayed to
    the user, use for your internal processes."""

    currency: Currency
    """Three-letter ISO 4217 currency code, see more on currencies. Pass `XTR`
    for payments in Telegram Stars."""

    prices: list["LabeledPrice"]
    """Price breakdown, a JSON-serialized list of components (e.g. product price,
    tax, discount, delivery cost, delivery tax, bonus, etc.). Must contain
    exactly one item for payments in Telegram Stars."""

    provider_token: Option[str] = Nothing
    """Optional. Payment provider token, obtained via @BotFather. Pass an empty
    string for payments in Telegram Stars."""

    max_tip_amount: Option[int] = Nothing
    """Optional. The maximum accepted amount for tips in the smallest units of
    the currency (integer, not float/double). For example, for a maximum tip
    of US$ 1.45 pass max_tip_amount = 145. See the exp parameter in currencies.json,
    it shows the number of digits past the decimal point for each currency (2
    for the majority of currencies). Defaults to 0. Not supported for payments
    in Telegram Stars."""

    suggested_tip_amounts: Option[list[int]] = Nothing
    """Optional. A JSON-serialized array of suggested amounts of tip in the smallest
    units of the currency (integer, not float/double). At most 4 suggested
    tip amounts can be specified. The suggested tip amounts must be positive,
    passed in a strictly increased order and must not exceed max_tip_amount."""

    provider_data: Option[str] = Nothing
    """Optional. A JSON-serialized object for data about the invoice, which will
    be shared with the payment provider. A detailed description of the required
    fields should be provided by the payment provider."""

    photo_url: Option[str] = Nothing
    """Optional. URL of the product photo for the invoice. Can be a photo of the goods
    or a marketing image for a service."""

    photo_size: Option[int] = Nothing
    """Optional. Photo size in bytes."""

    photo_width: Option[int] = Nothing
    """Optional. Photo width."""

    photo_height: Option[int] = Nothing
    """Optional. Photo height."""

    need_name: Option[bool] = Nothing
    """Optional. Pass True if you require the user's full name to complete the order.
    Ignored for payments in Telegram Stars."""

    need_phone_number: Option[bool] = Nothing
    """Optional. Pass True if you require the user's phone number to complete the
    order. Ignored for payments in Telegram Stars."""

    need_email: Option[bool] = Nothing
    """Optional. Pass True if you require the user's email address to complete
    the order. Ignored for payments in Telegram Stars."""

    need_shipping_address: Option[bool] = Nothing
    """Optional. Pass True if you require the user's shipping address to complete
    the order. Ignored for payments in Telegram Stars."""

    send_phone_number_to_provider: Option[bool] = Nothing
    """Optional. Pass True if the user's phone number should be sent to the provider.
    Ignored for payments in Telegram Stars."""

    send_email_to_provider: Option[bool] = Nothing
    """Optional. Pass True if the user's email address should be sent to the provider.
    Ignored for payments in Telegram Stars."""

    is_flexible: Option[bool] = Nothing
    """Optional. Pass True if the final price depends on the shipping method. Ignored
    for payments in Telegram Stars."""


class ChosenInlineResult(Model):
    """Object `ChosenInlineResult`, see the [documentation](https://core.telegram.org/bots/api#choseninlineresult).

    Represents a result of an inline query that was chosen by the user and sent to their chat partner.
    Note: It is necessary to enable inline feedback via @BotFather in order to receive these objects in updates.
    """

    result_id: str
    """The unique identifier for the result that was chosen."""

    from_: "User"
    """The user that chose the result."""

    query: str
    """The query that was used to obtain the result."""

    location: Option["Location"] = Nothing
    """Optional. Sender location, only for bots that require user location."""

    inline_message_id: Option[str] = Nothing
    """Optional. Identifier of the sent inline message. Available only if there
    is an inline keyboard attached to the message. Will be also received in callback
    queries and can be used to edit the message."""


class SentWebAppMessage(Model):
    """Object `SentWebAppMessage`, see the [documentation](https://core.telegram.org/bots/api#sentwebappmessage).

    Describes an inline message sent by a Web App on behalf of a user.
    """

    inline_message_id: Option[str] = Nothing
    """Optional. Identifier of the sent inline message. Available only if there
    is an inline keyboard attached to the message."""


class LabeledPrice(Model):
    """Object `LabeledPrice`, see the [documentation](https://core.telegram.org/bots/api#labeledprice).

    This object represents a portion of the price for goods or services.
    """

    label: str
    """Portion label."""

    amount: int
    """Price of the product in the smallest units of the currency (integer, not
    float/double). For example, for a price of US$ 1.45 pass amount = 145. See
    the exp parameter in currencies.json, it shows the number of digits past
    the decimal point for each currency (2 for the majority of currencies)."""


class Invoice(Model):
    """Object `Invoice`, see the [documentation](https://core.telegram.org/bots/api#invoice).

    This object contains basic information about an invoice.
    """

    title: str
    """Product name."""

    description: str
    """Product description."""

    start_parameter: str
    """Unique bot deep-linking parameter that can be used to generate this invoice."""

    currency: Currency
    """Three-letter ISO 4217 currency code, or `XTR` for payments in Telegram
    Stars."""

    total_amount: int
    """Total price in the smallest units of the currency (integer, not float/double).
    For example, for a price of US$ 1.45 pass amount = 145. See the exp parameter
    in currencies.json, it shows the number of digits past the decimal point
    for each currency (2 for the majority of currencies)."""


class ShippingAddress(Model):
    """Object `ShippingAddress`, see the [documentation](https://core.telegram.org/bots/api#shippingaddress).

    This object represents a shipping address.
    """

    country_code: str
    """Two-letter ISO 3166-1 alpha-2 country code."""

    state: str
    """State, if applicable."""

    city: str
    """City."""

    street_line1: str
    """First line for the address."""

    street_line2: str
    """Second line for the address."""

    post_code: str
    """Address post code."""


class OrderInfo(Model):
    """Object `OrderInfo`, see the [documentation](https://core.telegram.org/bots/api#orderinfo).

    This object represents information about an order.
    """

    name: Option[str] = Nothing
    """Optional. User name."""

    phone_number: Option[str] = Nothing
    """Optional. User's phone number."""

    email: Option[str] = Nothing
    """Optional. User email."""

    shipping_address: Option["ShippingAddress"] = Nothing
    """Optional. User shipping address."""


class ShippingOption(Model):
    """Object `ShippingOption`, see the [documentation](https://core.telegram.org/bots/api#shippingoption).

    This object represents one shipping option.
    """

    id: str
    """Shipping option identifier."""

    title: str
    """Option title."""

    prices: list["LabeledPrice"]
    """List of price portions."""


class SuccessfulPayment(Model):
    """Object `SuccessfulPayment`, see the [documentation](https://core.telegram.org/bots/api#successfulpayment).

    This object contains basic information about a successful payment.
    """

    currency: Currency
    """Three-letter ISO 4217 currency code, or `XTR` for payments in Telegram
    Stars."""

    total_amount: int
    """Total price in the smallest units of the currency (integer, not float/double).
    For example, for a price of US$ 1.45 pass amount = 145. See the exp parameter
    in currencies.json, it shows the number of digits past the decimal point
    for each currency (2 for the majority of currencies)."""

    invoice_payload: str
    """Bot-specified invoice payload."""

    telegram_payment_charge_id: str
    """Telegram payment identifier."""

    provider_payment_charge_id: str
    """Provider payment identifier."""

    shipping_option_id: Option[str] = Nothing
    """Optional. Identifier of the shipping option chosen by the user."""

    order_info: Option["OrderInfo"] = Nothing
    """Optional. Order information provided by the user."""


class RefundedPayment(Model):
    """Object `RefundedPayment`, see the [documentation](https://core.telegram.org/bots/api#refundedpayment).

    This object contains basic information about a refunded payment.
    """

    currency: typing.Literal["XTR"]
    """Three-letter ISO 4217 currency code, or `XTR` for payments in Telegram
    Stars. Currently, always `XTR`."""

    total_amount: int
    """Total refunded price in the smallest units of the currency (integer, not
    float/double). For example, for a price of US$ 1.45, total_amount = 145.
    See the exp parameter in currencies.json, it shows the number of digits
    past the decimal point for each currency (2 for the majority of currencies)."""

    invoice_payload: str
    """Bot-specified invoice payload."""

    telegram_payment_charge_id: str
    """Telegram payment identifier."""

    provider_payment_charge_id: Option[str] = Nothing
    """Optional. Provider payment identifier."""


class ShippingQuery(Model):
    """Object `ShippingQuery`, see the [documentation](https://core.telegram.org/bots/api#shippingquery).

    This object contains information about an incoming shipping query.
    """

    id: str
    """Unique query identifier."""

    from_: "User"
    """User who sent the query."""

    invoice_payload: str
    """Bot-specified invoice payload."""

    shipping_address: "ShippingAddress"
    """User specified shipping address."""


class PreCheckoutQuery(Model):
    """Object `PreCheckoutQuery`, see the [documentation](https://core.telegram.org/bots/api#precheckoutquery).

    This object contains information about an incoming pre-checkout query.
    """

    id: str
    """Unique query identifier."""

    from_: "User"
    """User who sent the query."""

    currency: Currency
    """Three-letter ISO 4217 currency code, or `XTR` for payments in Telegram
    Stars."""

    total_amount: int
    """Total price in the smallest units of the currency (integer, not float/double).
    For example, for a price of US$ 1.45 pass amount = 145. See the exp parameter
    in currencies.json, it shows the number of digits past the decimal point
    for each currency (2 for the majority of currencies)."""

    invoice_payload: str
    """Bot-specified invoice payload."""

    shipping_option_id: Option[str] = Nothing
    """Optional. Identifier of the shipping option chosen by the user."""

    order_info: Option["OrderInfo"] = Nothing
    """Optional. Order information provided by the user."""


class RevenueWithdrawalStatePending(RevenueWithdrawalState):
    """Object `RevenueWithdrawalStatePending`, see the [documentation](https://core.telegram.org/bots/api#revenuewithdrawalstatepending).

    The withdrawal is in progress.
    """

    type: typing.Literal["pending"]
    """Type of the state, always `pending`."""


class RevenueWithdrawalStateSucceeded(RevenueWithdrawalState):
    """Object `RevenueWithdrawalStateSucceeded`, see the [documentation](https://core.telegram.org/bots/api#revenuewithdrawalstatesucceeded).

    The withdrawal succeeded.
    """

    type: typing.Literal["succeeded"]
    """Type of the state, always `succeeded`."""

    date: datetime
    """Date the withdrawal was completed in Unix time."""

    url: str
    """An HTTPS URL that can be used to see transaction details."""


class RevenueWithdrawalStateFailed(RevenueWithdrawalState):
    """Object `RevenueWithdrawalStateFailed`, see the [documentation](https://core.telegram.org/bots/api#revenuewithdrawalstatefailed).

    The withdrawal failed and the transaction was refunded.
    """

    type: typing.Literal["failed"]
    """Type of the state, always `failed`."""


class TransactionPartnerUser(TransactionPartner):
    """Object `TransactionPartnerUser`, see the [documentation](https://core.telegram.org/bots/api#transactionpartneruser).

    Describes a transaction with a user.
    """

    type: typing.Literal["user"]
    """Type of the transaction partner, always `user`."""

    user: "User"
    """Information about the user."""

    invoice_payload: Option[str] = Nothing
    """Optional. Bot-specified invoice payload."""

    paid_media: Option[list[Variative["PaidMediaPreview", "PaidMediaPhoto", "PaidMediaVideo"]]] = Nothing
    """Optional. Information about the paid media bought by the user."""


class TransactionPartnerFragment(TransactionPartner):
    """Object `TransactionPartnerFragment`, see the [documentation](https://core.telegram.org/bots/api#transactionpartnerfragment).

    Describes a withdrawal transaction with Fragment.
    """

    type: typing.Literal["fragment"]
    """Type of the transaction partner, always `fragment`."""

    withdrawal_state: Option[
        Variative[
            "RevenueWithdrawalStatePending", "RevenueWithdrawalStateSucceeded", "RevenueWithdrawalStateFailed"
        ]
    ] = Nothing
    """Optional. State of the transaction if the transaction is outgoing."""


class TransactionPartnerTelegramAds(TransactionPartner):
    """Object `TransactionPartnerTelegramAds`, see the [documentation](https://core.telegram.org/bots/api#transactionpartnertelegramads).

    Describes a withdrawal transaction to the Telegram Ads platform.
    """

    type: typing.Literal["telegram_ads"]
    """Type of the transaction partner, always `telegram_ads`."""


class TransactionPartnerOther(TransactionPartner):
    """Object `TransactionPartnerOther`, see the [documentation](https://core.telegram.org/bots/api#transactionpartnerother).

    Describes a transaction with an unknown source or recipient.
    """

    type: typing.Literal["other"]
    """Type of the transaction partner, always `other`."""


class StarTransaction(Model):
    """Object `StarTransaction`, see the [documentation](https://core.telegram.org/bots/api#startransaction).

    Describes a Telegram Star transaction.
    """

    id: str
    """Unique identifier of the transaction. Coincides with the identifer of
    the original transaction for refund transactions. Coincides with SuccessfulPayment.telegram_payment_charge_id
    for successful incoming payments from users."""

    amount: int
    """Number of Telegram Stars transferred by the transaction."""

    date: datetime
    """Date the transaction was created in Unix time."""

    source: Option[
        Variative[
            "TransactionPartnerUser",
            "TransactionPartnerFragment",
            "TransactionPartnerTelegramAds",
            "TransactionPartnerOther",
        ]
    ] = Nothing
    """Optional. Source of an incoming transaction (e.g., a user purchasing goods
    or services, Fragment refunding a failed withdrawal). Only for incoming
    transactions."""

    receiver: Option[
        Variative[
            "TransactionPartnerUser",
            "TransactionPartnerFragment",
            "TransactionPartnerTelegramAds",
            "TransactionPartnerOther",
        ]
    ] = Nothing
    """Optional. Receiver of an outgoing transaction (e.g., a user for a purchase
    refund, Fragment for a withdrawal). Only for outgoing transactions."""


class StarTransactions(Model):
    """Object `StarTransactions`, see the [documentation](https://core.telegram.org/bots/api#startransactions).

    Contains a list of Telegram Star transactions.
    """

    transactions: list["StarTransaction"]
    """The list of transactions."""


class PassportData(Model):
    """Object `PassportData`, see the [documentation](https://core.telegram.org/bots/api#passportdata).

    Describes Telegram Passport data shared with the bot by the user.
    """

    data: list["EncryptedPassportElement"]
    """Array with information about documents and other Telegram Passport elements
    that was shared with the bot."""

    credentials: "EncryptedCredentials"
    """Encrypted credentials required to decrypt the data."""


class PassportFile(Model):
    """Object `PassportFile`, see the [documentation](https://core.telegram.org/bots/api#passportfile).

    This object represents a file uploaded to Telegram Passport. Currently all Telegram Passport files are in JPEG format when decrypted and don't exceed 10MB.
    """

    file_id: str
    """Identifier for this file, which can be used to download or reuse the file."""

    file_unique_id: str
    """Unique identifier for this file, which is supposed to be the same over time
    and for different bots. Can't be used to download or reuse the file."""

    file_size: int
    """File size in bytes."""

    file_date: datetime
    """Unix time when the file was uploaded."""


class EncryptedPassportElement(Model):
    """Object `EncryptedPassportElement`, see the [documentation](https://core.telegram.org/bots/api#encryptedpassportelement).

    Describes documents or other Telegram Passport elements shared with the bot by the user.
    """

    type: EncryptedPassportElementType
    """Element type. One of `personal_details`, `passport`, `driver_license`,
    `identity_card`, `internal_passport`, `address`, `utility_bill`,
    `bank_statement`, `rental_agreement`, `passport_registration`,
    `temporary_registration`, `phone_number`, `email`."""

    hash: str
    """Base64-encoded element hash for using in PassportElementErrorUnspecified."""

    data: Option[str] = Nothing
    """Optional. Base64-encoded encrypted Telegram Passport element data provided
    by the user; available only for `personal_details`, `passport`, `driver_license`,
    `identity_card`, `internal_passport` and `address` types. Can be decrypted
    and verified using the accompanying EncryptedCredentials."""

    phone_number: Option[str] = Nothing
    """Optional. User's verified phone number; available only for `phone_number`
    type."""

    email: Option[str] = Nothing
    """Optional. User's verified email address; available only for `email` type."""

    files: Option[list["PassportFile"]] = Nothing
    """Optional. Array of encrypted files with documents provided by the user;
    available only for `utility_bill`, `bank_statement`, `rental_agreement`,
    `passport_registration` and `temporary_registration` types. Files
    can be decrypted and verified using the accompanying EncryptedCredentials."""

    front_side: Option["PassportFile"] = Nothing
    """Optional. Encrypted file with the front side of the document, provided
    by the user; available only for `passport`, `driver_license`, `identity_card`
    and `internal_passport`. The file can be decrypted and verified using
    the accompanying EncryptedCredentials."""

    reverse_side: Option["PassportFile"] = Nothing
    """Optional. Encrypted file with the reverse side of the document, provided
    by the user; available only for `driver_license` and `identity_card`.
    The file can be decrypted and verified using the accompanying EncryptedCredentials."""

    selfie: Option["PassportFile"] = Nothing
    """Optional. Encrypted file with the selfie of the user holding a document,
    provided by the user; available if requested for `passport`, `driver_license`,
    `identity_card` and `internal_passport`. The file can be decrypted and
    verified using the accompanying EncryptedCredentials."""

    translation: Option[list["PassportFile"]] = Nothing
    """Optional. Array of encrypted files with translated versions of documents
    provided by the user; available if requested for `passport`, `driver_license`,
    `identity_card`, `internal_passport`, `utility_bill`, `bank_statement`,
    `rental_agreement`, `passport_registration` and `temporary_registration`
    types. Files can be decrypted and verified using the accompanying EncryptedCredentials."""


class EncryptedCredentials(Model):
    """Object `EncryptedCredentials`, see the [documentation](https://core.telegram.org/bots/api#encryptedcredentials).

    Describes data required for decrypting and authenticating EncryptedPassportElement. See the Telegram Passport Documentation for a complete description of the data decryption and authentication processes.
    """

    data: str
    """Base64-encoded encrypted JSON-serialized data with unique user's payload,
    data hashes and secrets required for EncryptedPassportElement decryption
    and authentication."""

    hash: str
    """Base64-encoded data hash for data authentication."""

    secret: str
    """Base64-encoded secret, encrypted with the bot's public RSA key, required
    for data decryption."""


class PassportElementErrorDataField(PassportElementError):
    """Object `PassportElementErrorDataField`, see the [documentation](https://core.telegram.org/bots/api#passportelementerrordatafield).

    Represents an issue in one of the data fields that was provided by the user. The error is considered resolved when the field's value changes.
    """

    source: typing.Literal["data"]
    """Error source, must be data."""

    type: typing.Literal[
        "personal_details",
        "passport",
        "driver_license",
        "identity_card",
        "internal_passport",
        "address",
    ]
    """The section of the user's Telegram Passport which has the error, one of `personal_details`,
    `passport`, `driver_license`, `identity_card`, `internal_passport`,
    `address`."""

    field_name: str
    """Name of the data field which has the error."""

    data_hash: str
    """Base64-encoded data hash."""

    message: str
    """Error message."""


class PassportElementErrorFrontSide(PassportElementError):
    """Object `PassportElementErrorFrontSide`, see the [documentation](https://core.telegram.org/bots/api#passportelementerrorfrontside).

    Represents an issue with the front side of a document. The error is considered resolved when the file with the front side of the document changes.
    """

    source: typing.Literal["front_side"]
    """Error source, must be front_side."""

    type: typing.Literal[
        "passport",
        "driver_license",
        "identity_card",
        "internal_passport",
    ]
    """The section of the user's Telegram Passport which has the issue, one of `passport`,
    `driver_license`, `identity_card`, `internal_passport`."""

    file_hash: str
    """Base64-encoded hash of the file with the front side of the document."""

    message: str
    """Error message."""


class PassportElementErrorReverseSide(PassportElementError):
    """Object `PassportElementErrorReverseSide`, see the [documentation](https://core.telegram.org/bots/api#passportelementerrorreverseside).

    Represents an issue with the reverse side of a document. The error is considered resolved when the file with reverse side of the document changes.
    """

    source: typing.Literal["reverse_side"]
    """Error source, must be reverse_side."""

    type: typing.Literal["driver_license", "identity_card"]
    """The section of the user's Telegram Passport which has the issue, one of `driver_license`,
    `identity_card`."""

    file_hash: str
    """Base64-encoded hash of the file with the reverse side of the document."""

    message: str
    """Error message."""


class PassportElementErrorSelfie(PassportElementError):
    """Object `PassportElementErrorSelfie`, see the [documentation](https://core.telegram.org/bots/api#passportelementerrorselfie).

    Represents an issue with the selfie with a document. The error is considered resolved when the file with the selfie changes.
    """

    source: typing.Literal["selfie"]
    """Error source, must be selfie."""

    type: typing.Literal[
        "passport",
        "driver_license",
        "identity_card",
        "internal_passport",
    ]
    """The section of the user's Telegram Passport which has the issue, one of `passport`,
    `driver_license`, `identity_card`, `internal_passport`."""

    file_hash: str
    """Base64-encoded hash of the file with the selfie."""

    message: str
    """Error message."""


class PassportElementErrorFile(PassportElementError):
    """Object `PassportElementErrorFile`, see the [documentation](https://core.telegram.org/bots/api#passportelementerrorfile).

    Represents an issue with a document scan. The error is considered resolved when the file with the document scan changes.
    """

    source: typing.Literal["file"]
    """Error source, must be file."""

    type: typing.Literal[
        "utility_bill",
        "bank_statement",
        "rental_agreement",
        "passport_registration",
        "temporary_registration",
    ]
    """The section of the user's Telegram Passport which has the issue, one of `utility_bill`,
    `bank_statement`, `rental_agreement`, `passport_registration`,
    `temporary_registration`."""

    file_hash: str
    """Base64-encoded file hash."""

    message: str
    """Error message."""


class PassportElementErrorFiles(PassportElementError):
    """Object `PassportElementErrorFiles`, see the [documentation](https://core.telegram.org/bots/api#passportelementerrorfiles).

    Represents an issue with a list of scans. The error is considered resolved when the list of files containing the scans changes.
    """

    source: typing.Literal["files"]
    """Error source, must be files."""

    type: typing.Literal[
        "utility_bill",
        "bank_statement",
        "rental_agreement",
        "passport_registration",
        "temporary_registration",
    ]
    """The section of the user's Telegram Passport which has the issue, one of `utility_bill`,
    `bank_statement`, `rental_agreement`, `passport_registration`,
    `temporary_registration`."""

    file_hashes: list[str]
    """List of base64-encoded file hashes."""

    message: str
    """Error message."""


class PassportElementErrorTranslationFile(PassportElementError):
    """Object `PassportElementErrorTranslationFile`, see the [documentation](https://core.telegram.org/bots/api#passportelementerrortranslationfile).

    Represents an issue with one of the files that constitute the translation of a document. The error is considered resolved when the file changes.
    """

    source: typing.Literal["translation_file"]
    """Error source, must be translation_file."""

    type: typing.Literal[
        "passport",
        "driver_license",
        "identity_card",
        "internal_passport",
        "utility_bill",
        "bank_statement",
        "rental_agreement",
        "passport_registration",
        "temporary_registration",
    ]
    """Type of element of the user's Telegram Passport which has the issue, one
    of `passport`, `driver_license`, `identity_card`, `internal_passport`,
    `utility_bill`, `bank_statement`, `rental_agreement`, `passport_registration`,
    `temporary_registration`."""

    file_hash: str
    """Base64-encoded file hash."""

    message: str
    """Error message."""


class PassportElementErrorTranslationFiles(PassportElementError):
    """Object `PassportElementErrorTranslationFiles`, see the [documentation](https://core.telegram.org/bots/api#passportelementerrortranslationfiles).

    Represents an issue with the translated version of a document. The error is considered resolved when a file with the document translation change.
    """

    source: typing.Literal["translation_files"]
    """Error source, must be translation_files."""

    type: typing.Literal[
        "passport",
        "driver_license",
        "identity_card",
        "internal_passport",
        "utility_bill",
        "bank_statement",
        "rental_agreement",
        "passport_registration",
        "temporary_registration",
    ]
    """Type of element of the user's Telegram Passport which has the issue, one
    of `passport`, `driver_license`, `identity_card`, `internal_passport`,
    `utility_bill`, `bank_statement`, `rental_agreement`, `passport_registration`,
    `temporary_registration`."""

    file_hashes: list[str]
    """List of base64-encoded file hashes."""

    message: str
    """Error message."""


class PassportElementErrorUnspecified(PassportElementError):
    """Object `PassportElementErrorUnspecified`, see the [documentation](https://core.telegram.org/bots/api#passportelementerrorunspecified).

    Represents an issue in an unspecified place. The error is considered resolved when new data is added.
    """

    source: typing.Literal["unspecified"]
    """Error source, must be unspecified."""

    type: EncryptedPassportElementType
    """Type of element of the user's Telegram Passport which has the issue."""

    element_hash: str
    """Base64-encoded element hash."""

    message: str
    """Error message."""


class Game(Model):
    """Object `Game`, see the [documentation](https://core.telegram.org/bots/api#game).

    This object represents a game. Use BotFather to create and edit games, their short names will act as unique identifiers.
    """

    title: str
    """Title of the game."""

    description: str
    """Description of the game."""

    photo: list["PhotoSize"]
    """Photo that will be displayed in the game message in chats."""

    text: Option[str] = Nothing
    """Optional. Brief description of the game or high scores included in the game
    message. Can be automatically edited to include current high scores for
    the game when the bot calls setGameScore, or manually edited using editMessageText.
    0-4096 characters."""

    text_entities: Option[list["MessageEntity"]] = Nothing
    """Optional. Special entities that appear in text, such as usernames, URLs,
    bot commands, etc."""

    animation: Option["Animation"] = Nothing
    """Optional. Animation that will be displayed in the game message in chats.
    Upload via BotFather."""


class CallbackGame(Model):
    """Object `CallbackGame`, see the [documentation](https://core.telegram.org/bots/api#callbackgame).

    A placeholder, currently holds no information. Use BotFather to set up your game.
    """


class GameHighScore(Model):
    """Object `GameHighScore`, see the [documentation](https://core.telegram.org/bots/api#gamehighscore).

    This object represents one row of the high scores table for a game.
    """

    position: int
    """Position in high score table for the game."""

    user: "User"
    """User."""

    score: int
    """Score."""


__all__ = (
    "Animation",
    "Audio",
    "BackgroundFill",
    "BackgroundFillFreeformGradient",
    "BackgroundFillGradient",
    "BackgroundFillSolid",
    "BackgroundType",
    "BackgroundTypeChatTheme",
    "BackgroundTypeFill",
    "BackgroundTypePattern",
    "BackgroundTypeWallpaper",
    "Birthdate",
    "BotCommand",
    "BotCommandScope",
    "BotCommandScopeAllChatAdministrators",
    "BotCommandScopeAllGroupChats",
    "BotCommandScopeAllPrivateChats",
    "BotCommandScopeChat",
    "BotCommandScopeChatAdministrators",
    "BotCommandScopeChatMember",
    "BotCommandScopeDefault",
    "BotDescription",
    "BotName",
    "BotShortDescription",
    "BusinessConnection",
    "BusinessIntro",
    "BusinessLocation",
    "BusinessMessagesDeleted",
    "BusinessOpeningHours",
    "BusinessOpeningHoursInterval",
    "CallbackGame",
    "CallbackQuery",
    "Chat",
    "ChatAdministratorRights",
    "ChatBackground",
    "ChatBoost",
    "ChatBoostAdded",
    "ChatBoostRemoved",
    "ChatBoostSource",
    "ChatBoostSourceGiftCode",
    "ChatBoostSourceGiveaway",
    "ChatBoostSourcePremium",
    "ChatBoostUpdated",
    "ChatFullInfo",
    "ChatInviteLink",
    "ChatJoinRequest",
    "ChatLocation",
    "ChatMember",
    "ChatMemberAdministrator",
    "ChatMemberBanned",
    "ChatMemberLeft",
    "ChatMemberMember",
    "ChatMemberOwner",
    "ChatMemberRestricted",
    "ChatMemberUpdated",
    "ChatPermissions",
    "ChatPhoto",
    "ChatShared",
    "ChosenInlineResult",
    "Contact",
    "Dice",
    "Document",
    "EncryptedCredentials",
    "EncryptedPassportElement",
    "ExternalReplyInfo",
    "File",
    "ForceReply",
    "ForumTopic",
    "ForumTopicClosed",
    "ForumTopicCreated",
    "ForumTopicEdited",
    "ForumTopicReopened",
    "Game",
    "GameHighScore",
    "GeneralForumTopicHidden",
    "GeneralForumTopicUnhidden",
    "Giveaway",
    "GiveawayCompleted",
    "GiveawayCreated",
    "GiveawayWinners",
    "InaccessibleMessage",
    "InlineKeyboardButton",
    "InlineKeyboardMarkup",
    "InlineQuery",
    "InlineQueryResult",
    "InlineQueryResultArticle",
    "InlineQueryResultAudio",
    "InlineQueryResultCachedAudio",
    "InlineQueryResultCachedDocument",
    "InlineQueryResultCachedGif",
    "InlineQueryResultCachedMpeg4Gif",
    "InlineQueryResultCachedPhoto",
    "InlineQueryResultCachedSticker",
    "InlineQueryResultCachedVideo",
    "InlineQueryResultCachedVoice",
    "InlineQueryResultContact",
    "InlineQueryResultDocument",
    "InlineQueryResultGame",
    "InlineQueryResultGif",
    "InlineQueryResultLocation",
    "InlineQueryResultMpeg4Gif",
    "InlineQueryResultPhoto",
    "InlineQueryResultVenue",
    "InlineQueryResultVideo",
    "InlineQueryResultVoice",
    "InlineQueryResultsButton",
    "InputContactMessageContent",
    "InputFile",
    "InputInvoiceMessageContent",
    "InputLocationMessageContent",
    "InputMedia",
    "InputMediaAnimation",
    "InputMediaAudio",
    "InputMediaDocument",
    "InputMediaPhoto",
    "InputMediaVideo",
    "InputMessageContent",
    "InputPaidMedia",
    "InputPaidMediaPhoto",
    "InputPaidMediaVideo",
    "InputPollOption",
    "InputSticker",
    "InputTextMessageContent",
    "InputVenueMessageContent",
    "Invoice",
    "KeyboardButton",
    "KeyboardButtonPollType",
    "KeyboardButtonRequestChat",
    "KeyboardButtonRequestUsers",
    "LabeledPrice",
    "LinkPreviewOptions",
    "Location",
    "LoginUrl",
    "MaskPosition",
    "MaybeInaccessibleMessage",
    "MenuButton",
    "MenuButtonCommands",
    "MenuButtonDefault",
    "MenuButtonWebApp",
    "Message",
    "MessageAutoDeleteTimerChanged",
    "MessageEntity",
    "MessageId",
    "MessageOrigin",
    "MessageOriginChannel",
    "MessageOriginChat",
    "MessageOriginHiddenUser",
    "MessageOriginUser",
    "MessageReactionCountUpdated",
    "MessageReactionUpdated",
    "Model",
    "OrderInfo",
    "PaidMedia",
    "PaidMediaInfo",
    "PaidMediaPhoto",
    "PaidMediaPreview",
    "PaidMediaVideo",
    "PassportData",
    "PassportElementError",
    "PassportElementErrorDataField",
    "PassportElementErrorFile",
    "PassportElementErrorFiles",
    "PassportElementErrorFrontSide",
    "PassportElementErrorReverseSide",
    "PassportElementErrorSelfie",
    "PassportElementErrorTranslationFile",
    "PassportElementErrorTranslationFiles",
    "PassportElementErrorUnspecified",
    "PassportFile",
    "PhotoSize",
    "Poll",
    "PollAnswer",
    "PollOption",
    "PreCheckoutQuery",
    "ProximityAlertTriggered",
    "ReactionCount",
    "ReactionType",
    "ReactionTypeCustomEmoji",
    "ReactionTypeEmoji",
    "ReactionTypePaid",
    "RefundedPayment",
    "ReplyKeyboardMarkup",
    "ReplyKeyboardRemove",
    "ReplyParameters",
    "ResponseParameters",
    "RevenueWithdrawalState",
    "RevenueWithdrawalStateFailed",
    "RevenueWithdrawalStatePending",
    "RevenueWithdrawalStateSucceeded",
    "SentWebAppMessage",
    "SharedUser",
    "ShippingAddress",
    "ShippingOption",
    "ShippingQuery",
    "StarTransaction",
    "StarTransactions",
    "Sticker",
    "StickerSet",
    "Story",
    "SuccessfulPayment",
    "SwitchInlineQueryChosenChat",
    "TextQuote",
    "TransactionPartner",
    "TransactionPartnerFragment",
    "TransactionPartnerOther",
    "TransactionPartnerTelegramAds",
    "TransactionPartnerUser",
    "Update",
    "User",
    "UserChatBoosts",
    "UserProfilePhotos",
    "UsersShared",
    "Venue",
    "Video",
    "VideoChatEnded",
    "VideoChatParticipantsInvited",
    "VideoChatScheduled",
    "VideoChatStarted",
    "VideoNote",
    "Voice",
    "WebAppData",
    "WebAppInfo",
    "WebhookInfo",
    "WriteAccessAllowed",
)
