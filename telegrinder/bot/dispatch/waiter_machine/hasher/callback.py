from fntypes import Some

from telegrinder.bot.cute_types import CallbackQueryCute as CallbackQuery
from telegrinder.bot.dispatch.view import CallbackQueryView

from .hasher import Hasher


def from_chat_hash(chat_id: int) -> int:
    return chat_id


def get_chat_from_event(event: CallbackQuery) -> int | None:
    return event.chat.and_then(lambda chat: Some(chat.id)).unwrap_or_none()


CALLBACK_QUERY_FROM_CHAT = Hasher(
    view=CallbackQueryView,
    get_hash_from_data=from_chat_hash,
    get_data_from_event=get_chat_from_event,
)


def for_message_hash(message_id: int) -> int:
    return message_id


def get_message_for_event(event: CallbackQuery) -> int | None:
    return event.message_id.unwrap_or_none()


CALLBACK_QUERY_FOR_MESSAGE = Hasher(
    view=CallbackQueryView,
    get_hash_from_data=for_message_hash,
    get_data_from_event=get_message_for_event,
)


def for_message_in_chat(chat_and_message: tuple[int, int]) -> str:
    return f"{chat_and_message[0]}_{chat_and_message[1]}"


def get_chat_and_message_for_event(event: CallbackQuery) -> tuple[int, int] | None:
    if not event.message_id or not event.chat:
        return None
    return event.chat.unwrap().id, event.message_id.unwrap()


CALLBACK_QUERY_IN_CHAT_FOR_MESSAGE = Hasher(
    view=CallbackQueryView,
    get_hash_from_data=for_message_in_chat,
    get_data_from_event=get_chat_and_message_for_event,
)
