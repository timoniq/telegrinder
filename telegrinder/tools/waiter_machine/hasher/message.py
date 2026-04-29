import typing

from telegrinder.tools.waiter_machine.hasher.hasher import Hasher, identity
from telegrinder.types import ChatType
from telegrinder.types.enums import UpdateType

if typing.TYPE_CHECKING:
    from telegrinder.bot.cute_types.message import MessageCute as Message


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
ANY_MESSAGE_UPDATE_TYPES: typing.Final = frozenset((*MESSAGE_UPDATE_TYPES, *BUSINESS_MESSAGE_UPDATE_TYPES))


def get_chat_from_event(event: Message) -> int:
    return event.chat.id


def get_user_from_event(event: Message) -> int:
    return event.from_user.id


def get_thread_id_from_event(event: Message) -> int | None:
    return event.message_thread_id.unwrap_or_none()


def get_business_connection_id_from_event(event: Message) -> str | None:
    return event.business_connection_id.unwrap_or_none()


def get_user_in_chat_from_event(event: Message) -> tuple[int, int]:
    return event.chat.id, event.from_user.id


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

    return thread_id, event.chat.id, event.from_user.id


def from_user_in_chat_hash(chat_and_user: tuple[int, int]) -> str:
    return f"{chat_and_user[0]}_{chat_and_user[1]}"


def from_user_in_thread_hash(thread_and_user: tuple[int, int]) -> str:
    return f"{thread_and_user[0]}_{thread_and_user[1]}"


def from_user_in_chat_thread_hash(data: tuple[int, int, int]) -> str:
    return f"{data[0]}_{data[1]}_{data[2]}"


BUSINESS_MESSAGE: typing.Final = Hasher(
    update_types=BUSINESS_MESSAGE_UPDATE_TYPES,
    hash_from_data=identity,
    data_from_event=get_business_connection_id_from_event,
)
MESSAGE_POST_IN_CHANNEL = Hasher(
    update_types=MESSAGE_CHANNEL_POST_UPDATE_TYPES,
    hash_from_data=identity,
    data_from_event=get_chat_from_event,
)
ANY_MESSAGE_FROM_USER: typing.Final = Hasher(
    update_types=ANY_MESSAGE_UPDATE_TYPES,
    hash_from_data=identity,
    data_from_event=get_user_from_event,
)
MESSAGE_FROM_USER: typing.Final = Hasher(
    update_types=MESSAGE_UPDATE_TYPES,
    hash_from_data=identity,
    data_from_event=get_user_from_event,
)
MESSAGE_IN_CHAT: typing.Final = Hasher(
    update_types=MESSAGE_UPDATE_TYPES,
    hash_from_data=identity,
    data_from_event=get_chat_from_event,
)
MESSAGE_FROM_USER_IN_CHAT: typing.Final = Hasher(
    update_types=MESSAGE_UPDATE_TYPES,
    hash_from_data=from_user_in_chat_hash,
    data_from_event=get_user_in_chat_from_event,
)
MESSAGE_FROM_USER_IN_THREAD: typing.Final = Hasher(
    update_types=MESSAGE_UPDATE_TYPES,
    hash_from_data=from_user_in_thread_hash,
    data_from_event=get_user_in_thread_from_event,
)
MESSAGE_FROM_USER_IN_CHAT_THREAD = Hasher(
    update_types=MESSAGE_UPDATE_TYPES,
    hash_from_data=from_user_in_chat_thread_hash,
    data_from_event=get_user_in_chat_thread_from_event,
)


__all__ = (
    "ANY_MESSAGE_FROM_USER",
    "BUSINESS_MESSAGE",
    "MESSAGE_FROM_USER",
    "MESSAGE_FROM_USER_IN_CHAT",
    "MESSAGE_FROM_USER_IN_CHAT_THREAD",
    "MESSAGE_FROM_USER_IN_THREAD",
    "MESSAGE_IN_CHAT",
    "MESSAGE_POST_IN_CHANNEL",
)
