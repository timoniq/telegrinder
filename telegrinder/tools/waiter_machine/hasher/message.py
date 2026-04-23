import typing

from telegrinder.tools.waiter_machine.hasher.hasher import Hasher
from telegrinder.types.enums import UpdateType

if typing.TYPE_CHECKING:
    from telegrinder.bot.cute_types.message import MessageCute as Message

MESSAGE_UPDATE_TYPES: typing.Final = frozenset(
    (
        UpdateType.MESSAGE,
        UpdateType.CHANNEL_POST,
        UpdateType.BUSINESS_MESSAGE,
        UpdateType.EDITED_MESSAGE,
        UpdateType.EDITED_CHANNEL_POST,
        UpdateType.EDITED_BUSINESS_MESSAGE,
    ),
)


def from_chat_hash(chat_id: int) -> int:
    return chat_id


def get_chat_from_event(event: Message) -> int:
    return event.chat.id


def from_user_in_chat_hash(chat_and_user: tuple[int, int]) -> str:
    return f"{chat_and_user[0]}_{chat_and_user[1]}"


def get_user_in_chat_from_event(event: Message) -> tuple[int, int]:
    return event.chat.id, event.from_user.id


def from_user_hash(from_id: int) -> int:
    return from_id


def get_user_from_event(event: Message) -> int:
    return event.from_user.id


MESSAGE_IN_CHAT: typing.Final = Hasher(
    update_types=MESSAGE_UPDATE_TYPES,
    hash_from_data=from_chat_hash,
    data_from_event=get_chat_from_event,
)

MESSAGE_FROM_USER: typing.Final = Hasher(
    update_types=MESSAGE_UPDATE_TYPES,
    hash_from_data=from_user_hash,
    data_from_event=get_user_from_event,
)

MESSAGE_FROM_USER_IN_CHAT: typing.Final = Hasher(
    update_types=MESSAGE_UPDATE_TYPES,
    hash_from_data=from_user_in_chat_hash,
    data_from_event=get_user_in_chat_from_event,
)


__all__ = (
    "MESSAGE_FROM_USER",
    "MESSAGE_FROM_USER_IN_CHAT",
    "MESSAGE_IN_CHAT",
)
