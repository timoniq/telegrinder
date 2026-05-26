import typing

from telegrinder.tools.waiter_machine.hasher.hasher import Hasher, hash_data, identity_hash
from telegrinder.types import ChatType
from telegrinder.types.enums import UpdateType

if typing.TYPE_CHECKING:
    from telegrinder.bot.cute_types.message import MessageCute as Message


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
        UpdateType.DELETED_BUSINESS_MESSAGES,
    ),
)
ANY_MESSAGE_UPDATE_TYPES: typing.Final = frozenset(
    (
        *MESSAGE_UPDATE_TYPES,
        *BUSINESS_MESSAGE_UPDATE_TYPES,
        *GUEST_MESSAGE_UPDATE_TYPES,
    ),
)


def get_chat_from_event(event: Message) -> int:
    return event.chat.id


def get_user_from_event(event: Message) -> int | None:
    return event.from_.map(lambda user: user.id).unwrap_or_none()


def get_thread_id_from_event(event: Message) -> int | None:
    return event.message_thread_id.unwrap_or_none()


def get_business_connection_id_from_event(event: Message) -> str | None:
    return event.business_connection_id.unwrap_or_none()


def get_user_in_chat_from_event(event: Message) -> tuple[int, int] | None:
    user_id = get_user_from_event(event)
    return None if user_id is None else (event.chat.id, user_id)


def get_user_in_thread_from_event(event: Message) -> tuple[int, int] | None:
    if event.chat.type != ChatType.PRIVATE:
        return None

    data = get_user_in_chat_thread_from_event(event)
    if data is None:
        return None

    return data[0], data[1]


def get_user_in_chat_thread_from_event(event: Message) -> tuple[int, int, int] | None:
    thread_id = event.message_thread_id.unwrap_or_none()

    if thread_id is None:
        return None

    data = get_user_in_chat_from_event(event)
    return None if data is None else (thread_id, *data)


def get_chat_and_thread_id_from_event(event: Message) -> tuple[int, int] | None:
    thread_id = get_thread_id_from_event(event)
    return None if thread_id is None else (thread_id, get_chat_from_event(event))


def get_guest_query_id_from_event(event: Message) -> str | None:
    return event.guest_query_id.unwrap_or_none()


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


__all__ = (
    "ANY_MESSAGE_FROM_USER",
    "ANY_MESSAGE_FROM_USER_IN_CHAT",
    "ANY_MESSAGE_IN_CHAT",
    "BUSINESS_MESSAGE",
    "GUEST_MESSAGE",
    "GUEST_MESSAGE_FROM_USER",
    "GUEST_MESSAGE_FROM_USER_IN_CHAT",
    "GUEST_MESSAGE_FROM_USER_IN_CHAT_THREAD",
    "GUEST_MESSAGE_FROM_USER_IN_THREAD",
    "GUEST_MESSAGE_IN_CHAT",
    "GUEST_MESSAGE_IN_CHAT_THREAD",
    "GUEST_MESSAGE_IN_THREAD",
    "MESSAGE_FROM_USER",
    "MESSAGE_FROM_USER_IN_CHAT",
    "MESSAGE_FROM_USER_IN_CHAT_THREAD",
    "MESSAGE_FROM_USER_IN_THREAD",
    "MESSAGE_IN_CHAT",
    "MESSAGE_IN_CHAT_THREAD",
    "MESSAGE_IN_TRHEAD",
    "MESSAGE_POST_IN_CHANNEL",
)
