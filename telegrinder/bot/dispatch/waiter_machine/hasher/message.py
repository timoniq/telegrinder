from telegrinder.bot.cute_types import MessageCute as Message
from telegrinder.bot.dispatch.view import MessageView

from .hasher import Hasher


def from_chat_hash(chat_id: int) -> int:
    return chat_id


def get_chat_from_event(event: Message) -> int:
    return event.chat.id


MESSAGE_IN_CHAT = Hasher(
    view=MessageView, create_hash=from_chat_hash, get_data_from_event=get_chat_from_event
)


def from_user_hash(from_id: int) -> int:
    return from_id


def get_user_from_event(event: Message) -> int:
    return event.from_user.id


MESSAGE_FROM_USER = Hasher(
    view=MessageView,
    create_hash=from_user_hash,
    get_data_from_event=get_user_from_event,
)


def from_user_in_chat_hash(chat_and_user: tuple[int, int]) -> str:
    return f"{chat_and_user[0]}_{chat_and_user[1]}"


def get_user_in_chat_from_event(event: Message) -> tuple[int, int]:
    return event.chat.id, event.from_user.id


MESSAGE_FROM_USER_IN_CHAT = Hasher(
    view=MessageView,
    create_hash=from_user_in_chat_hash,
    get_data_from_event=get_user_in_chat_from_event,
)
