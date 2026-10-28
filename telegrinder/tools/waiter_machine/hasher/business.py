import typing

from telegrinder.tools.waiter_machine.hasher.hasher import Hasher, hash_data, identity_hash
from telegrinder.types.enums import UpdateType

if typing.TYPE_CHECKING:
    from telegrinder.bot.cute_types.business_connection import BusinessConnectionCute as BusinessConnection
    from telegrinder.bot.cute_types.business_messages_deleted import (
        BusinessMessagesDeletedCute as BusinessMessagesDeleted,
    )

    type BusinessConnectionId = str
    type ChatId = int
    type BusinessAccountUserChatId = int
    type BusinessAccountUserId = int


def get_connection_id(event: BusinessConnection) -> BusinessConnectionId:
    return event.id


def get_connection_user(event: BusinessConnection) -> BusinessAccountUserId:
    return event.user.id


def get_connection_user_chat(event: BusinessConnection) -> BusinessAccountUserChatId:
    return event.user_chat_id


def get_connection_user_in_chat(event: BusinessConnection) -> tuple[BusinessAccountUserChatId, BusinessAccountUserId]:
    return event.user_chat_id, event.user.id


def get_deleted_connection(event: BusinessMessagesDeleted) -> BusinessConnectionId:
    return event.business_connection_id


def get_deleted_chat(event: BusinessMessagesDeleted) -> ChatId:
    return event.chat.id


def get_deleted_connection_in_chat(event: BusinessMessagesDeleted) -> tuple[BusinessConnectionId, ChatId]:
    return event.business_connection_id, event.chat.id


BUSINESS_CONNECTION: typing.Final = Hasher(
    update_types=frozenset((UpdateType.BUSINESS_CONNECTION,)),
    hash_from_data=identity_hash,
    data_from_event=get_connection_id,
)

BUSINESS_CONNECTION_FROM_USER: typing.Final = Hasher(
    update_types=frozenset((UpdateType.BUSINESS_CONNECTION,)),
    hash_from_data=identity_hash,
    data_from_event=get_connection_user,
)

BUSINESS_CONNECTION_IN_USER_CHAT: typing.Final = Hasher(
    update_types=frozenset((UpdateType.BUSINESS_CONNECTION,)),
    hash_from_data=identity_hash,
    data_from_event=get_connection_user_chat,
)

BUSINESS_CONNECTION_FROM_USER_IN_USER_CHAT: typing.Final = Hasher(
    update_types=frozenset((UpdateType.BUSINESS_CONNECTION,)),
    hash_from_data=hash_data,
    data_from_event=get_connection_user_in_chat,
)

DELETED_BUSINESS_MESSAGES: typing.Final = Hasher(
    update_types=frozenset((UpdateType.DELETED_BUSINESS_MESSAGES,)),
    hash_from_data=identity_hash,
    data_from_event=get_deleted_connection,
)

DELETED_BUSINESS_MESSAGES_IN_CHAT: typing.Final = Hasher(
    update_types=frozenset((UpdateType.DELETED_BUSINESS_MESSAGES,)),
    hash_from_data=identity_hash,
    data_from_event=get_deleted_chat,
)

DELETED_BUSINESS_MESSAGES_IN_CHAT_FOR_CONNECTION: typing.Final = Hasher(
    update_types=frozenset((UpdateType.DELETED_BUSINESS_MESSAGES,)),
    hash_from_data=hash_data,
    data_from_event=get_deleted_connection_in_chat,
)


__all__ = (
    "BUSINESS_CONNECTION",
    "BUSINESS_CONNECTION_FROM_USER",
    "BUSINESS_CONNECTION_FROM_USER_IN_USER_CHAT",
    "BUSINESS_CONNECTION_IN_USER_CHAT",
    "DELETED_BUSINESS_MESSAGES",
    "DELETED_BUSINESS_MESSAGES_IN_CHAT",
    "DELETED_BUSINESS_MESSAGES_IN_CHAT_FOR_CONNECTION",
)
