import typing

from telegrinder.tools.waiter_machine.hasher.hasher import Hasher, hash_data, identity_hash
from telegrinder.types.enums import UpdateType

if typing.TYPE_CHECKING:
    from telegrinder.bot.cute_types.callback_query import CallbackQueryCute as CallbackQuery

    type ChatId = int
    type MessageId = int
    type MessageThreadId = int
    type CallbackActorUserId = int
    type CallbackQueryId = str
    type InlineMessageId = str
    type ChatInstanceId = str
    type CallbackData = str
    type ReceiverUserId = int
    type EphemeralMessageId = int

CALLBACK_QUERY_UPDATE_TYPES: typing.Final = frozenset((UpdateType.CALLBACK_QUERY,))


def get_chat_for_event(event: CallbackQuery) -> ChatId | None:
    return event.chat.map(lambda chat: chat.id).unwrap_or_none()


def get_chat_thread_event(event: CallbackQuery) -> tuple[MessageThreadId, ChatId] | None:
    chat_id = get_chat_for_event(event)

    if chat_id is None:
        return None

    thread_id = event.message_thread_id.unwrap_or_none()

    if thread_id is None:
        return None

    return thread_id, chat_id


def get_for_message_in_chat_thread_event(event: CallbackQuery) -> tuple[MessageId, MessageThreadId, ChatId] | None:
    data = get_chat_thread_event(event)
    if data is None:
        return None

    message_id = get_message_for_event(event)
    if message_id is None:
        return None

    thread_id, chat_id = data
    return message_id, thread_id, chat_id


def get_message_for_event(event: CallbackQuery) -> MessageId | None:
    return event.message_id.unwrap_or_none()


def get_chat_and_message_for_event(event: CallbackQuery) -> tuple[ChatId, MessageId] | None:
    chat_id = get_chat_for_event(event)

    if chat_id is None:
        return None

    message_id = get_message_for_event(event)

    if message_id is None:
        return None

    return chat_id, message_id


def get_query_id_from_event(event: CallbackQuery) -> CallbackQueryId:
    return event.id


def get_user_from_event(event: CallbackQuery) -> CallbackActorUserId:
    return event.from_user.id


def get_user_in_chat_from_event(event: CallbackQuery) -> tuple[ChatId, CallbackActorUserId] | None:
    chat_id = get_chat_for_event(event)
    return None if chat_id is None else (chat_id, event.from_user.id)


def get_user_in_chat_thread_from_event(
    event: CallbackQuery,
) -> tuple[MessageThreadId, ChatId, CallbackActorUserId] | None:
    data = get_chat_thread_event(event)
    return None if data is None else (*data, event.from_user.id)


def get_message_and_user_in_chat_from_event(
    event: CallbackQuery,
) -> tuple[ChatId, MessageId, CallbackActorUserId] | None:
    data = get_chat_and_message_for_event(event)
    return None if data is None else (*data, event.from_user.id)


def get_message_and_user_in_chat_thread_from_event(
    event: CallbackQuery,
) -> tuple[MessageId, MessageThreadId, ChatId, CallbackActorUserId] | None:
    data = get_for_message_in_chat_thread_event(event)
    return None if data is None else (*data, event.from_user.id)


def get_inline_message_from_event(event: CallbackQuery) -> InlineMessageId | None:
    return event.inline_message_id.unwrap_or_none()


def get_inline_message_and_user_from_event(event: CallbackQuery) -> tuple[InlineMessageId, CallbackActorUserId] | None:
    message_id = get_inline_message_from_event(event)
    return None if message_id is None else (message_id, event.from_user.id)


def get_chat_instance_from_event(event: CallbackQuery) -> ChatInstanceId:
    return event.chat_instance


def get_chat_instance_and_user_from_event(event: CallbackQuery) -> tuple[ChatInstanceId, CallbackActorUserId]:
    return event.chat_instance, event.from_user.id


def get_receiver_user_from_event(event: CallbackQuery) -> ReceiverUserId | None:
    return event.receiver_user_id.unwrap_or_none()


def get_ephemeral_message_in_chat_from_event(event: CallbackQuery) -> tuple[ChatId, EphemeralMessageId] | None:
    chat_id = get_chat_for_event(event)
    message_id = event.ephemeral_message_id.unwrap_or_none()
    return None if chat_id is None or message_id is None else (chat_id, message_id)


def get_ephemeral_message_and_user_in_chat_from_event(
    event: CallbackQuery,
) -> tuple[ChatId, EphemeralMessageId, CallbackActorUserId] | None:
    data = get_ephemeral_message_in_chat_from_event(event)
    return None if data is None else (*data, event.from_user.id)


def get_data_from_event(event: CallbackQuery) -> CallbackData | None:
    return event.data.unwrap_or_none()


def get_data_and_user_from_event(event: CallbackQuery) -> tuple[CallbackData, CallbackActorUserId] | None:
    data = get_data_from_event(event)
    return None if data is None else (data, event.from_user.id)


CALLBACK_QUERY_FROM_CHAT: typing.Final = Hasher(
    update_types=CALLBACK_QUERY_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_chat_for_event,
)
CALLBACK_QUERY_FROM_CHAT_THREAD: typing.Final = Hasher(
    update_types=CALLBACK_QUERY_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_chat_thread_event,
)
CALLBACK_QUERY_FOR_MESSAGE: typing.Final = Hasher(
    update_types=CALLBACK_QUERY_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_message_for_event,
)
CALLBACK_QUERY_IN_CHAT_FOR_MESSAGE: typing.Final = Hasher(
    update_types=CALLBACK_QUERY_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_chat_and_message_for_event,
)
CALLBACK_QUERY_IN_CHAT_THREAD_FOR_MESSAGE: typing.Final = Hasher(
    update_types=CALLBACK_QUERY_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_for_message_in_chat_thread_event,
)

CALLBACK_QUERY: typing.Final = Hasher(
    update_types=CALLBACK_QUERY_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_query_id_from_event,
)

CALLBACK_QUERY_FROM_USER: typing.Final = Hasher(
    update_types=CALLBACK_QUERY_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_user_from_event,
)

CALLBACK_QUERY_FROM_USER_IN_CHAT: typing.Final = Hasher(
    update_types=CALLBACK_QUERY_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_user_in_chat_from_event,
)

CALLBACK_QUERY_FROM_USER_IN_CHAT_THREAD: typing.Final = Hasher(
    update_types=CALLBACK_QUERY_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_user_in_chat_thread_from_event,
)

CALLBACK_QUERY_IN_CHAT_FOR_MESSAGE_FROM_USER: typing.Final = Hasher(
    update_types=CALLBACK_QUERY_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_message_and_user_in_chat_from_event,
)

CALLBACK_QUERY_IN_CHAT_THREAD_FOR_MESSAGE_FROM_USER: typing.Final = Hasher(
    update_types=CALLBACK_QUERY_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_message_and_user_in_chat_thread_from_event,
)

CALLBACK_QUERY_FOR_INLINE_MESSAGE: typing.Final = Hasher(
    update_types=CALLBACK_QUERY_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_inline_message_from_event,
)

CALLBACK_QUERY_FOR_INLINE_MESSAGE_FROM_USER: typing.Final = Hasher(
    update_types=CALLBACK_QUERY_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_inline_message_and_user_from_event,
)

CALLBACK_QUERY_FROM_CHAT_INSTANCE: typing.Final = Hasher(
    update_types=CALLBACK_QUERY_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_chat_instance_from_event,
)

CALLBACK_QUERY_FROM_USER_IN_CHAT_INSTANCE: typing.Final = Hasher(
    update_types=CALLBACK_QUERY_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_chat_instance_and_user_from_event,
)

CALLBACK_QUERY_FOR_RECEIVER_USER: typing.Final = Hasher(
    update_types=CALLBACK_QUERY_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_receiver_user_from_event,
)

CALLBACK_QUERY_IN_CHAT_FOR_EPHEMERAL_MESSAGE: typing.Final = Hasher(
    update_types=CALLBACK_QUERY_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_ephemeral_message_in_chat_from_event,
)

CALLBACK_QUERY_IN_CHAT_FOR_EPHEMERAL_MESSAGE_FROM_USER: typing.Final = Hasher(
    update_types=CALLBACK_QUERY_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_ephemeral_message_and_user_in_chat_from_event,
)

CALLBACK_QUERY_FOR_DATA: typing.Final = Hasher(
    update_types=CALLBACK_QUERY_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_data_from_event,
)

CALLBACK_QUERY_FOR_DATA_FROM_USER: typing.Final = Hasher(
    update_types=CALLBACK_QUERY_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_data_and_user_from_event,
)


__all__ = (
    "CALLBACK_QUERY",
    "CALLBACK_QUERY_FOR_DATA",
    "CALLBACK_QUERY_FOR_DATA_FROM_USER",
    "CALLBACK_QUERY_FOR_INLINE_MESSAGE",
    "CALLBACK_QUERY_FOR_INLINE_MESSAGE_FROM_USER",
    "CALLBACK_QUERY_FOR_MESSAGE",
    "CALLBACK_QUERY_FOR_RECEIVER_USER",
    "CALLBACK_QUERY_FROM_CHAT",
    "CALLBACK_QUERY_FROM_CHAT_INSTANCE",
    "CALLBACK_QUERY_FROM_CHAT_THREAD",
    "CALLBACK_QUERY_FROM_USER",
    "CALLBACK_QUERY_FROM_USER_IN_CHAT",
    "CALLBACK_QUERY_FROM_USER_IN_CHAT_INSTANCE",
    "CALLBACK_QUERY_FROM_USER_IN_CHAT_THREAD",
    "CALLBACK_QUERY_IN_CHAT_FOR_EPHEMERAL_MESSAGE",
    "CALLBACK_QUERY_IN_CHAT_FOR_EPHEMERAL_MESSAGE_FROM_USER",
    "CALLBACK_QUERY_IN_CHAT_FOR_MESSAGE",
    "CALLBACK_QUERY_IN_CHAT_FOR_MESSAGE_FROM_USER",
    "CALLBACK_QUERY_IN_CHAT_THREAD_FOR_MESSAGE",
    "CALLBACK_QUERY_IN_CHAT_THREAD_FOR_MESSAGE_FROM_USER",
)
