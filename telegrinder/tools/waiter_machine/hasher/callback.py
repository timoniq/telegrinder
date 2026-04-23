import typing

from telegrinder.tools.waiter_machine.hasher.hasher import Hasher
from telegrinder.types.enums import UpdateType

if typing.TYPE_CHECKING:
    from telegrinder.bot.cute_types.callback_query import CallbackQueryCute as CallbackQuery

CALLBACK_QUERY_UPDATE_TYPES: typing.Final = frozenset((UpdateType.CALLBACK_QUERY,))


def from_chat_hash(chat_id: int) -> int:
    return chat_id


def get_chat_from_event(event: CallbackQuery) -> int | None:
    return event.chat.map(lambda chat: chat.id).unwrap_or_none()


def for_message_hash(message_id: int) -> int:
    return message_id


def get_message_for_event(event: CallbackQuery) -> int | None:
    return event.message_id.unwrap_or_none()


def for_message_in_chat(chat_and_message: tuple[int, int]) -> str:
    return f"{chat_and_message[0]}_{chat_and_message[1]}"


def get_chat_and_message_for_event(event: CallbackQuery) -> tuple[int, int] | None:
    if not event.message_id or not event.chat:
        return None
    return event.chat.unwrap().id, event.message_id.unwrap()


CALLBACK_QUERY_FROM_CHAT: typing.Final = Hasher(
    update_types=CALLBACK_QUERY_UPDATE_TYPES,
    hash_from_data=from_chat_hash,
    data_from_event=get_chat_from_event,
)
CALLBACK_QUERY_FOR_MESSAGE: typing.Final = Hasher(
    update_types=CALLBACK_QUERY_UPDATE_TYPES,
    hash_from_data=for_message_hash,
    data_from_event=get_message_for_event,
)
CALLBACK_QUERY_IN_CHAT_FOR_MESSAGE: typing.Final = Hasher(
    update_types=CALLBACK_QUERY_UPDATE_TYPES,
    hash_from_data=for_message_in_chat,
    data_from_event=get_chat_and_message_for_event,
)


__all__ = (
    "CALLBACK_QUERY_FOR_MESSAGE",
    "CALLBACK_QUERY_FROM_CHAT",
    "CALLBACK_QUERY_IN_CHAT_FOR_MESSAGE",
)
