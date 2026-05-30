import typing

from telegrinder.tools.waiter_machine.hasher.hasher import Hasher, hash_data, identity_hash
from telegrinder.types.enums import UpdateType

if typing.TYPE_CHECKING:
    from telegrinder.bot.cute_types.callback_query import CallbackQueryCute as CallbackQuery

type ChatId = int
type MessageId = int
type ThreadId = int

CALLBACK_QUERY_UPDATE_TYPES: typing.Final = frozenset((UpdateType.CALLBACK_QUERY,))


def get_chat_for_event(event: CallbackQuery) -> ChatId | None:
    return event.chat.map(lambda chat: chat.id).unwrap_or_none()


def get_chat_thread_event(event: CallbackQuery) -> tuple[ThreadId, ChatId] | None:
    chat_id = get_chat_for_event(event)

    if chat_id is None:
        return None

    thread_id = event.message_thread_id.unwrap_or_none()

    if thread_id is None:
        return None

    return thread_id, chat_id


def get_for_message_in_chat_thread_event(event: CallbackQuery) -> tuple[MessageId, ThreadId, ChatId] | None:
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


__all__ = (
    "CALLBACK_QUERY_FOR_MESSAGE",
    "CALLBACK_QUERY_FROM_CHAT",
    "CALLBACK_QUERY_FROM_CHAT_THREAD",
    "CALLBACK_QUERY_IN_CHAT_FOR_MESSAGE",
    "CALLBACK_QUERY_IN_CHAT_THREAD_FOR_MESSAGE",
)
