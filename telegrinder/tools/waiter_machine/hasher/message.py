import typing

from telegrinder.tools.waiter_machine.hasher.hasher import Hasher, hash_data, identity_hash
from telegrinder.types import ChatType
from telegrinder.types.enums import UpdateType

if typing.TYPE_CHECKING:
    from telegrinder.bot.cute_types.message import MessageCute as Message

    type MessageThreadId = int
    type ChatId = int
    type ViaBotId = int
    type SenderUserId = int
    type BusinessConnectionId = str
    type MessageId = int
    type MediaGroupId = str
    type SenderBusinessBotId = int
    type DirectMessagesTopicId = int
    type GuestQueryId = str
    type SenderChatId = int
    type ReceiverUserId = int
    type EphemeralMessageId = int

GUEST_MESSAGE_UPDATE_TYPES: typing.Final = frozenset((UpdateType.GUEST_MESSAGE,))
MESSAGE_UPDATE_TYPES: typing.Final = frozenset(
    (
        UpdateType.MESSAGE,
        UpdateType.EDITED_MESSAGE,
    ),
)
MESSAGE_CHANNEL_POST_UPDATE_TYPES: typing.Final = frozenset(
    (
        UpdateType.CHANNEL_POST,
        UpdateType.EDITED_CHANNEL_POST,
    ),
)
BUSINESS_MESSAGE_UPDATE_TYPES: typing.Final = frozenset(
    (
        UpdateType.BUSINESS_MESSAGE,
        UpdateType.EDITED_BUSINESS_MESSAGE,
    ),
)
ANY_MESSAGE_UPDATE_TYPES: typing.Final = frozenset(
    (
        *MESSAGE_UPDATE_TYPES,
        *MESSAGE_CHANNEL_POST_UPDATE_TYPES,
        *BUSINESS_MESSAGE_UPDATE_TYPES,
        *GUEST_MESSAGE_UPDATE_TYPES,
    ),
)


def get_chat_from_event(event: Message) -> ChatId:
    return event.chat.id


def get_user_from_event(event: Message) -> SenderUserId | None:
    return event.from_.map(lambda user: user.id).unwrap_or_none()


def get_thread_id_from_event(event: Message) -> MessageThreadId | None:
    return event.message_thread_id.unwrap_or_none()


def get_business_connection_id_from_event(event: Message) -> BusinessConnectionId | None:
    return event.business_connection_id.unwrap_or_none()


def get_user_in_chat_from_event(event: Message) -> tuple[ChatId, SenderUserId] | None:
    user_id = get_user_from_event(event)
    return None if user_id is None else (event.chat.id, user_id)


def get_user_in_thread_from_event(event: Message) -> tuple[MessageThreadId, SenderUserId] | None:
    if event.chat.type != ChatType.PRIVATE:
        return None

    data = get_user_in_chat_thread_from_event(event)
    if data is None:
        return None

    return data[0], data[2]


def get_user_in_chat_thread_from_event(event: Message) -> tuple[MessageThreadId, ChatId, SenderUserId] | None:
    thread_id = event.message_thread_id.unwrap_or_none()

    if thread_id is None:
        return None

    data = get_user_in_chat_from_event(event)
    return None if data is None else (thread_id, *data)


def get_chat_and_thread_id_from_event(event: Message) -> tuple[MessageThreadId, ChatId] | None:
    thread_id = get_thread_id_from_event(event)
    return None if thread_id is None else (thread_id, get_chat_from_event(event))


def get_guest_query_id_from_event(event: Message) -> GuestQueryId | None:
    return event.guest_query_id.unwrap_or_none()


def get_message_in_chat_from_event(event: Message) -> tuple[ChatId, MessageId]:
    return event.chat.id, event.message_id


def get_sender_chat_from_event(event: Message) -> SenderChatId | None:
    return event.sender_chat.map(lambda chat: chat.id).unwrap_or_none()


def get_sender_chat_in_chat_from_event(event: Message) -> tuple[ChatId, SenderChatId] | None:
    sender_chat_id = get_sender_chat_from_event(event)
    return None if sender_chat_id is None else (event.chat.id, sender_chat_id)


def get_receiver_user_from_event(event: Message) -> ReceiverUserId | None:
    return event.receiver_user.map(lambda user: user.id).unwrap_or_none()


def get_ephemeral_message_in_chat_from_event(event: Message) -> tuple[ChatId, EphemeralMessageId] | None:
    message_id = event.ephemeral_message_id.unwrap_or_none()
    return None if message_id is None else (event.chat.id, message_id)


def get_ephemeral_message_for_user_in_chat_from_event(
    event: Message,
) -> tuple[ChatId, EphemeralMessageId, ReceiverUserId] | None:
    data = get_ephemeral_message_in_chat_from_event(event)
    user_id = get_receiver_user_from_event(event)
    return None if data is None or user_id is None else (*data, user_id)


def get_media_group_in_chat_from_event(event: Message) -> tuple[MediaGroupId, ChatId] | None:
    group_id = event.media_group_id.unwrap_or_none()
    return None if group_id is None else (group_id, event.chat.id)


def get_direct_messages_topic_in_chat_from_event(event: Message) -> tuple[DirectMessagesTopicId, ChatId] | None:
    topic_id = event.direct_messages_topic.map(lambda topic: topic.topic_id).unwrap_or_none()
    return None if topic_id is None else (topic_id, event.chat.id)


def get_via_bot_from_event(event: Message) -> ViaBotId | None:
    return event.via_bot.map(lambda user: user.id).unwrap_or_none()


def get_connection_in_chat_from_event(event: Message) -> tuple[BusinessConnectionId, ChatId] | None:
    connection_id = get_business_connection_id_from_event(event)
    return None if connection_id is None else (connection_id, event.chat.id)


def get_connection_user_in_chat_from_event(event: Message) -> tuple[BusinessConnectionId, ChatId, SenderUserId] | None:
    data = get_connection_in_chat_from_event(event)
    user_id = get_user_from_event(event)
    return None if data is None or user_id is None else (*data, user_id)


def get_connection_message_in_chat_from_event(event: Message) -> tuple[BusinessConnectionId, ChatId, MessageId] | None:
    data = get_connection_in_chat_from_event(event)
    return None if data is None else (*data, event.message_id)


def get_connection_thread_in_chat_from_event(
    event: Message,
) -> tuple[BusinessConnectionId, MessageThreadId, ChatId] | None:
    connection_id = get_business_connection_id_from_event(event)
    data = get_chat_and_thread_id_from_event(event)
    return None if connection_id is None or data is None else (connection_id, *data)


def get_business_bot_from_event(event: Message) -> SenderBusinessBotId | None:
    return event.sender_business_bot.map(lambda user: user.id).unwrap_or_none()


def get_business_bot_for_connection_from_event(
    event: Message,
) -> tuple[BusinessConnectionId, SenderBusinessBotId] | None:
    connection_id = get_business_connection_id_from_event(event)
    user_id = get_business_bot_from_event(event)
    return None if connection_id is None or user_id is None else (connection_id, user_id)


def get_guest_query_in_chat_from_event(event: Message) -> tuple[GuestQueryId, ChatId] | None:
    query_id = get_guest_query_id_from_event(event)
    return None if query_id is None else (query_id, event.chat.id)


def get_guest_query_from_user_from_event(event: Message) -> tuple[GuestQueryId, SenderUserId] | None:
    query_id = get_guest_query_id_from_event(event)
    user_id = get_user_from_event(event)
    return None if query_id is None or user_id is None else (query_id, user_id)


ANY_MESSAGE_FROM_USER: typing.Final = Hasher(
    update_types=ANY_MESSAGE_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_user_from_event,
)
ANY_MESSAGE_IN_CHAT: typing.Final = Hasher(
    update_types=ANY_MESSAGE_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_chat_from_event,
)
ANY_MESSAGE_FROM_USER_IN_CHAT: typing.Final = Hasher(
    update_types=ANY_MESSAGE_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_user_in_chat_from_event,
)
BUSINESS_MESSAGE: typing.Final = Hasher(
    update_types=BUSINESS_MESSAGE_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_business_connection_id_from_event,
)
GUEST_MESSAGE: typing.Final = Hasher(
    update_types=GUEST_MESSAGE_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_guest_query_id_from_event,
)
GUEST_MESSAGE_FROM_USER: typing.Final = Hasher(
    update_types=GUEST_MESSAGE_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_user_from_event,
)
GUEST_MESSAGE_IN_CHAT: typing.Final = Hasher(
    update_types=GUEST_MESSAGE_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_chat_from_event,
)
GUEST_MESSAGE_IN_THREAD: typing.Final = Hasher(
    update_types=GUEST_MESSAGE_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_thread_id_from_event,
)
GUEST_MESSAGE_IN_CHAT_THREAD: typing.Final = Hasher(
    update_types=GUEST_MESSAGE_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_chat_and_thread_id_from_event,
)
GUEST_MESSAGE_FROM_USER_IN_CHAT: typing.Final = Hasher(
    update_types=GUEST_MESSAGE_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_user_in_chat_from_event,
)
GUEST_MESSAGE_FROM_USER_IN_THREAD: typing.Final = Hasher(
    update_types=GUEST_MESSAGE_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_user_in_thread_from_event,
)
GUEST_MESSAGE_FROM_USER_IN_CHAT_THREAD = Hasher(
    update_types=GUEST_MESSAGE_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_user_in_chat_thread_from_event,
)
MESSAGE_POST_IN_CHANNEL = Hasher(
    update_types=MESSAGE_CHANNEL_POST_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_chat_from_event,
)
MESSAGE_FROM_USER: typing.Final = Hasher(
    update_types=MESSAGE_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_user_from_event,
)
MESSAGE_IN_CHAT: typing.Final = Hasher(
    update_types=MESSAGE_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_chat_from_event,
)
MESSAGE_IN_TRHEAD: typing.Final = Hasher(
    update_types=MESSAGE_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_thread_id_from_event,
)
MESSAGE_IN_CHAT_THREAD: typing.Final = Hasher(
    update_types=MESSAGE_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_chat_and_thread_id_from_event,
)
MESSAGE_FROM_USER_IN_CHAT: typing.Final = Hasher(
    update_types=MESSAGE_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_user_in_chat_from_event,
)
MESSAGE_FROM_USER_IN_THREAD: typing.Final = Hasher(
    update_types=MESSAGE_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_user_in_thread_from_event,
)
MESSAGE_FROM_USER_IN_CHAT_THREAD = Hasher(
    update_types=MESSAGE_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_user_in_chat_thread_from_event,
)
ANY_MESSAGE_IN_CHAT_THREAD: typing.Final = Hasher(
    update_types=ANY_MESSAGE_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_chat_and_thread_id_from_event,
)
ANY_MESSAGE_FROM_USER_IN_CHAT_THREAD: typing.Final = Hasher(
    update_types=ANY_MESSAGE_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_user_in_chat_thread_from_event,
)
ANY_MESSAGE_IN_CHAT_FOR_MESSAGE: typing.Final = Hasher(
    update_types=ANY_MESSAGE_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_message_in_chat_from_event,
)
ANY_MESSAGE_FROM_SENDER_CHAT: typing.Final = Hasher(
    update_types=ANY_MESSAGE_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_sender_chat_from_event,
)
ANY_MESSAGE_FROM_SENDER_CHAT_IN_CHAT: typing.Final = Hasher(
    update_types=ANY_MESSAGE_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_sender_chat_in_chat_from_event,
)
ANY_MESSAGE_FOR_RECEIVER_USER: typing.Final = Hasher(
    update_types=ANY_MESSAGE_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_receiver_user_from_event,
)
ANY_MESSAGE_IN_CHAT_FOR_EPHEMERAL_MESSAGE: typing.Final = Hasher(
    update_types=ANY_MESSAGE_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_ephemeral_message_in_chat_from_event,
)
ANY_MESSAGE_IN_CHAT_FOR_EPHEMERAL_MESSAGE_FOR_USER: typing.Final = Hasher(
    update_types=ANY_MESSAGE_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_ephemeral_message_for_user_in_chat_from_event,
)
ANY_MESSAGE_IN_CHAT_FOR_MEDIA_GROUP: typing.Final = Hasher(
    update_types=ANY_MESSAGE_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_media_group_in_chat_from_event,
)
ANY_MESSAGE_IN_CHAT_DIRECT_MESSAGES_TOPIC: typing.Final = Hasher(
    update_types=ANY_MESSAGE_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_direct_messages_topic_in_chat_from_event,
)
ANY_MESSAGE_FROM_VIA_BOT: typing.Final = Hasher(
    update_types=ANY_MESSAGE_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_via_bot_from_event,
)
MESSAGE_IN_CHAT_FOR_MESSAGE: typing.Final = Hasher(
    update_types=MESSAGE_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_message_in_chat_from_event,
)
MESSAGE_FROM_SENDER_CHAT: typing.Final = Hasher(
    update_types=MESSAGE_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_sender_chat_from_event,
)
MESSAGE_FROM_SENDER_CHAT_IN_CHAT: typing.Final = Hasher(
    update_types=MESSAGE_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_sender_chat_in_chat_from_event,
)
MESSAGE_FOR_RECEIVER_USER: typing.Final = Hasher(
    update_types=MESSAGE_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_receiver_user_from_event,
)
MESSAGE_IN_CHAT_FOR_EPHEMERAL_MESSAGE: typing.Final = Hasher(
    update_types=MESSAGE_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_ephemeral_message_in_chat_from_event,
)
MESSAGE_IN_CHAT_FOR_EPHEMERAL_MESSAGE_FOR_USER: typing.Final = Hasher(
    update_types=MESSAGE_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_ephemeral_message_for_user_in_chat_from_event,
)
MESSAGE_IN_CHAT_FOR_MEDIA_GROUP: typing.Final = Hasher(
    update_types=MESSAGE_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_media_group_in_chat_from_event,
)
MESSAGE_IN_CHAT_DIRECT_MESSAGES_TOPIC: typing.Final = Hasher(
    update_types=MESSAGE_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_direct_messages_topic_in_chat_from_event,
)
MESSAGE_FROM_VIA_BOT: typing.Final = Hasher(
    update_types=MESSAGE_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_via_bot_from_event,
)
BUSINESS_MESSAGE_IN_CHAT: typing.Final = Hasher(
    update_types=BUSINESS_MESSAGE_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_chat_from_event,
)
BUSINESS_MESSAGE_FROM_USER: typing.Final = Hasher(
    update_types=BUSINESS_MESSAGE_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_user_from_event,
)
BUSINESS_MESSAGE_FROM_USER_IN_CHAT: typing.Final = Hasher(
    update_types=BUSINESS_MESSAGE_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_user_in_chat_from_event,
)
BUSINESS_MESSAGE_IN_CHAT_FOR_CONNECTION: typing.Final = Hasher(
    update_types=BUSINESS_MESSAGE_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_connection_in_chat_from_event,
)
BUSINESS_MESSAGE_FROM_USER_IN_CHAT_FOR_CONNECTION: typing.Final = Hasher(
    update_types=BUSINESS_MESSAGE_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_connection_user_in_chat_from_event,
)
BUSINESS_MESSAGE_FOR_CONNECTION_IN_CHAT_FOR_MESSAGE: typing.Final = Hasher(
    update_types=BUSINESS_MESSAGE_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_connection_message_in_chat_from_event,
)
BUSINESS_MESSAGE_IN_CHAT_THREAD_FOR_CONNECTION: typing.Final = Hasher(
    update_types=BUSINESS_MESSAGE_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_connection_thread_in_chat_from_event,
)
BUSINESS_MESSAGE_FROM_BUSINESS_BOT: typing.Final = Hasher(
    update_types=BUSINESS_MESSAGE_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_business_bot_from_event,
)
BUSINESS_MESSAGE_FROM_BUSINESS_BOT_FOR_CONNECTION: typing.Final = Hasher(
    update_types=BUSINESS_MESSAGE_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_business_bot_for_connection_from_event,
)
GUEST_MESSAGE_IN_CHAT_FOR_MESSAGE: typing.Final = Hasher(
    update_types=GUEST_MESSAGE_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_message_in_chat_from_event,
)
GUEST_MESSAGE_IN_CHAT_FOR_QUERY: typing.Final = Hasher(
    update_types=GUEST_MESSAGE_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_guest_query_in_chat_from_event,
)
GUEST_MESSAGE_FOR_QUERY_FROM_USER: typing.Final = Hasher(
    update_types=GUEST_MESSAGE_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_guest_query_from_user_from_event,
)
MESSAGE_POST_IN_CHANNEL_FOR_MESSAGE: typing.Final = Hasher(
    update_types=MESSAGE_CHANNEL_POST_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_message_in_chat_from_event,
)
MESSAGE_POST_FROM_USER: typing.Final = Hasher(
    update_types=MESSAGE_CHANNEL_POST_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_user_from_event,
)
MESSAGE_POST_FROM_SENDER_CHAT: typing.Final = Hasher(
    update_types=MESSAGE_CHANNEL_POST_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_sender_chat_from_event,
)
MESSAGE_POST_IN_CHANNEL_FOR_MEDIA_GROUP: typing.Final = Hasher(
    update_types=MESSAGE_CHANNEL_POST_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_media_group_in_chat_from_event,
)


__all__ = (
    "ANY_MESSAGE_FOR_RECEIVER_USER",
    "ANY_MESSAGE_FROM_SENDER_CHAT",
    "ANY_MESSAGE_FROM_SENDER_CHAT_IN_CHAT",
    "ANY_MESSAGE_FROM_USER",
    "ANY_MESSAGE_FROM_USER_IN_CHAT",
    "ANY_MESSAGE_FROM_USER_IN_CHAT_THREAD",
    "ANY_MESSAGE_FROM_VIA_BOT",
    "ANY_MESSAGE_IN_CHAT",
    "ANY_MESSAGE_IN_CHAT_DIRECT_MESSAGES_TOPIC",
    "ANY_MESSAGE_IN_CHAT_FOR_EPHEMERAL_MESSAGE",
    "ANY_MESSAGE_IN_CHAT_FOR_EPHEMERAL_MESSAGE_FOR_USER",
    "ANY_MESSAGE_IN_CHAT_FOR_MEDIA_GROUP",
    "ANY_MESSAGE_IN_CHAT_FOR_MESSAGE",
    "ANY_MESSAGE_IN_CHAT_THREAD",
    "BUSINESS_MESSAGE",
    "BUSINESS_MESSAGE_FOR_CONNECTION_IN_CHAT_FOR_MESSAGE",
    "BUSINESS_MESSAGE_FROM_BUSINESS_BOT",
    "BUSINESS_MESSAGE_FROM_BUSINESS_BOT_FOR_CONNECTION",
    "BUSINESS_MESSAGE_FROM_USER",
    "BUSINESS_MESSAGE_FROM_USER_IN_CHAT",
    "BUSINESS_MESSAGE_FROM_USER_IN_CHAT_FOR_CONNECTION",
    "BUSINESS_MESSAGE_IN_CHAT",
    "BUSINESS_MESSAGE_IN_CHAT_FOR_CONNECTION",
    "BUSINESS_MESSAGE_IN_CHAT_THREAD_FOR_CONNECTION",
    "GUEST_MESSAGE",
    "GUEST_MESSAGE_FOR_QUERY_FROM_USER",
    "GUEST_MESSAGE_FROM_USER",
    "GUEST_MESSAGE_FROM_USER_IN_CHAT",
    "GUEST_MESSAGE_FROM_USER_IN_CHAT_THREAD",
    "GUEST_MESSAGE_FROM_USER_IN_THREAD",
    "GUEST_MESSAGE_IN_CHAT",
    "GUEST_MESSAGE_IN_CHAT_FOR_MESSAGE",
    "GUEST_MESSAGE_IN_CHAT_FOR_QUERY",
    "GUEST_MESSAGE_IN_CHAT_THREAD",
    "GUEST_MESSAGE_IN_THREAD",
    "MESSAGE_FOR_RECEIVER_USER",
    "MESSAGE_FROM_SENDER_CHAT",
    "MESSAGE_FROM_SENDER_CHAT_IN_CHAT",
    "MESSAGE_FROM_USER",
    "MESSAGE_FROM_USER_IN_CHAT",
    "MESSAGE_FROM_USER_IN_CHAT_THREAD",
    "MESSAGE_FROM_USER_IN_THREAD",
    "MESSAGE_FROM_VIA_BOT",
    "MESSAGE_IN_CHAT",
    "MESSAGE_IN_CHAT_DIRECT_MESSAGES_TOPIC",
    "MESSAGE_IN_CHAT_FOR_EPHEMERAL_MESSAGE",
    "MESSAGE_IN_CHAT_FOR_EPHEMERAL_MESSAGE_FOR_USER",
    "MESSAGE_IN_CHAT_FOR_MEDIA_GROUP",
    "MESSAGE_IN_CHAT_FOR_MESSAGE",
    "MESSAGE_IN_CHAT_THREAD",
    "MESSAGE_IN_TRHEAD",
    "MESSAGE_POST_FROM_SENDER_CHAT",
    "MESSAGE_POST_FROM_USER",
    "MESSAGE_POST_IN_CHANNEL",
    "MESSAGE_POST_IN_CHANNEL_FOR_MEDIA_GROUP",
    "MESSAGE_POST_IN_CHANNEL_FOR_MESSAGE",
)
