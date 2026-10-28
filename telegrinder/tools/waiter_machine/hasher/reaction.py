import typing

from telegrinder.tools.waiter_machine.hasher.hasher import Hasher, hash_data, identity_hash
from telegrinder.types.enums import UpdateType

if typing.TYPE_CHECKING:
    from telegrinder.bot.cute_types.message_reaction_count_updated import (
        MessageReactionCountUpdatedCute as MessageReactionCountUpdated,
    )
    from telegrinder.bot.cute_types.message_reaction_updated import MessageReactionUpdatedCute as MessageReactionUpdated

    type ChatId = int
    type MessageId = int
    type ReactionUserId = int
    type ActorChatId = int


def get_reaction_chat(event: MessageReactionUpdated) -> ChatId:
    return event.chat.id


def get_reaction_message(event: MessageReactionUpdated) -> tuple[ChatId, MessageId]:
    return event.chat.id, event.message_id


def get_reaction_user(event: MessageReactionUpdated) -> ReactionUserId | None:
    return event.user.map(lambda user: user.id).unwrap_or_none()


def get_reaction_user_in_chat(event: MessageReactionUpdated) -> tuple[ChatId, ReactionUserId] | None:
    user_id = get_reaction_user(event)
    return None if user_id is None else (event.chat.id, user_id)


def get_reaction_message_from_user(event: MessageReactionUpdated) -> tuple[ChatId, MessageId, ReactionUserId] | None:
    user_id = get_reaction_user(event)
    return None if user_id is None else (event.chat.id, event.message_id, user_id)


def get_reaction_actor_chat(event: MessageReactionUpdated) -> ActorChatId | None:
    return event.actor_chat.map(lambda chat: chat.id).unwrap_or_none()


def get_reaction_message_from_actor_chat(event: MessageReactionUpdated) -> tuple[ChatId, MessageId, ActorChatId] | None:
    actor_chat_id = get_reaction_actor_chat(event)
    return None if actor_chat_id is None else (event.chat.id, event.message_id, actor_chat_id)


def get_reaction_count_chat(event: MessageReactionCountUpdated) -> ChatId:
    return event.chat.id


def get_reaction_count_message(event: MessageReactionCountUpdated) -> tuple[ChatId, MessageId]:
    return event.chat.id, event.message_id


MESSAGE_REACTION_IN_CHAT: typing.Final = Hasher(
    update_types=frozenset((UpdateType.MESSAGE_REACTION,)),
    hash_from_data=identity_hash,
    data_from_event=get_reaction_chat,
)

MESSAGE_REACTION_IN_CHAT_FOR_MESSAGE: typing.Final = Hasher(
    update_types=frozenset((UpdateType.MESSAGE_REACTION,)),
    hash_from_data=hash_data,
    data_from_event=get_reaction_message,
)

MESSAGE_REACTION_FROM_USER: typing.Final = Hasher(
    update_types=frozenset((UpdateType.MESSAGE_REACTION,)),
    hash_from_data=identity_hash,
    data_from_event=get_reaction_user,
)

MESSAGE_REACTION_FROM_USER_IN_CHAT: typing.Final = Hasher(
    update_types=frozenset((UpdateType.MESSAGE_REACTION,)),
    hash_from_data=hash_data,
    data_from_event=get_reaction_user_in_chat,
)

MESSAGE_REACTION_IN_CHAT_FOR_MESSAGE_FROM_USER: typing.Final = Hasher(
    update_types=frozenset((UpdateType.MESSAGE_REACTION,)),
    hash_from_data=hash_data,
    data_from_event=get_reaction_message_from_user,
)

MESSAGE_REACTION_FROM_ACTOR_CHAT: typing.Final = Hasher(
    update_types=frozenset((UpdateType.MESSAGE_REACTION,)),
    hash_from_data=identity_hash,
    data_from_event=get_reaction_actor_chat,
)

MESSAGE_REACTION_IN_CHAT_FOR_MESSAGE_FROM_ACTOR_CHAT: typing.Final = Hasher(
    update_types=frozenset((UpdateType.MESSAGE_REACTION,)),
    hash_from_data=hash_data,
    data_from_event=get_reaction_message_from_actor_chat,
)

MESSAGE_REACTION_COUNT_IN_CHAT: typing.Final = Hasher(
    update_types=frozenset((UpdateType.MESSAGE_REACTION_COUNT,)),
    hash_from_data=identity_hash,
    data_from_event=get_reaction_count_chat,
)

MESSAGE_REACTION_COUNT_IN_CHAT_FOR_MESSAGE: typing.Final = Hasher(
    update_types=frozenset((UpdateType.MESSAGE_REACTION_COUNT,)),
    hash_from_data=hash_data,
    data_from_event=get_reaction_count_message,
)


__all__ = (
    "MESSAGE_REACTION_COUNT_IN_CHAT",
    "MESSAGE_REACTION_COUNT_IN_CHAT_FOR_MESSAGE",
    "MESSAGE_REACTION_FROM_ACTOR_CHAT",
    "MESSAGE_REACTION_FROM_USER",
    "MESSAGE_REACTION_FROM_USER_IN_CHAT",
    "MESSAGE_REACTION_IN_CHAT",
    "MESSAGE_REACTION_IN_CHAT_FOR_MESSAGE",
    "MESSAGE_REACTION_IN_CHAT_FOR_MESSAGE_FROM_ACTOR_CHAT",
    "MESSAGE_REACTION_IN_CHAT_FOR_MESSAGE_FROM_USER",
)
