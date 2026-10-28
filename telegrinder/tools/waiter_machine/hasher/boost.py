import typing

from telegrinder.tools.waiter_machine.hasher.hasher import Hasher, hash_data, identity_hash
from telegrinder.types.enums import UpdateType
from telegrinder.types.objects import ChatBoostSourceGiveaway

if typing.TYPE_CHECKING:
    from telegrinder.bot.cute_types.chat_boost_removed import ChatBoostRemovedCute as ChatBoostRemoved
    from telegrinder.bot.cute_types.chat_boost_updated import ChatBoostUpdatedCute as ChatBoostUpdated
    from telegrinder.types.objects import ChatBoostSourceGiftCode, ChatBoostSourcePremium

    type BoostId = str
    type ChatId = int
    type BoostSourceUserId = int
    type GiveawayMessageId = int


def get_source_user(
    source: ChatBoostSourcePremium | ChatBoostSourceGiftCode | ChatBoostSourceGiveaway,
) -> BoostSourceUserId | None:
    if isinstance(source, ChatBoostSourceGiveaway):
        return source.user.map(lambda user: user.id).unwrap_or_none()

    return source.user.id


def get_boost_id(event: ChatBoostUpdated) -> BoostId:
    return event.boost.boost_id


def get_boost_chat(event: ChatBoostUpdated) -> ChatId:
    return event.chat.id


def get_boost_in_chat(event: ChatBoostUpdated) -> tuple[ChatId, BoostId]:
    return event.chat.id, event.boost.boost_id


def get_boost_user(event: ChatBoostUpdated) -> BoostSourceUserId | None:
    return get_source_user(event.boost.source.v)


def get_boost_user_in_chat(event: ChatBoostUpdated) -> tuple[ChatId, BoostSourceUserId] | None:
    user_id = get_boost_user(event)
    return None if user_id is None else (event.chat.id, user_id)


def get_boost_giveaway_in_chat(event: ChatBoostUpdated) -> tuple[ChatId, GiveawayMessageId] | None:
    source = event.boost.source.v

    if not isinstance(source, ChatBoostSourceGiveaway):
        return None
    return event.chat.id, source.giveaway_message_id


def get_removed_boost_id(event: ChatBoostRemoved) -> BoostId:
    return event.boost_id


def get_removed_boost_chat(event: ChatBoostRemoved) -> ChatId:
    return event.chat.id


def get_removed_boost_in_chat(event: ChatBoostRemoved) -> tuple[ChatId, BoostId]:
    return event.chat.id, event.boost_id


def get_removed_boost_user(event: ChatBoostRemoved) -> BoostSourceUserId | None:
    return get_source_user(event.source.v)


def get_removed_boost_user_in_chat(event: ChatBoostRemoved) -> tuple[ChatId, BoostSourceUserId] | None:
    user_id = get_removed_boost_user(event)
    return None if user_id is None else (event.chat.id, user_id)


def get_removed_boost_giveaway_in_chat(event: ChatBoostRemoved) -> tuple[ChatId, GiveawayMessageId] | None:
    source = event.source.v

    if not isinstance(source, ChatBoostSourceGiveaway):
        return None
    return event.chat.id, source.giveaway_message_id


CHAT_BOOST: typing.Final = Hasher(
    update_types=frozenset((UpdateType.CHAT_BOOST,)),
    hash_from_data=identity_hash,
    data_from_event=get_boost_id,
)
CHAT_BOOST_IN_CHAT: typing.Final = Hasher(
    update_types=frozenset((UpdateType.CHAT_BOOST,)),
    hash_from_data=identity_hash,
    data_from_event=get_boost_chat,
)
CHAT_BOOST_IN_CHAT_FOR_BOOST: typing.Final = Hasher(
    update_types=frozenset((UpdateType.CHAT_BOOST,)),
    hash_from_data=hash_data,
    data_from_event=get_boost_in_chat,
)
CHAT_BOOST_FROM_USER: typing.Final = Hasher(
    update_types=frozenset((UpdateType.CHAT_BOOST,)),
    hash_from_data=identity_hash,
    data_from_event=get_boost_user,
)
CHAT_BOOST_FROM_USER_IN_CHAT: typing.Final = Hasher(
    update_types=frozenset((UpdateType.CHAT_BOOST,)),
    hash_from_data=hash_data,
    data_from_event=get_boost_user_in_chat,
)
CHAT_BOOST_IN_CHAT_FOR_GIVEAWAY: typing.Final = Hasher(
    update_types=frozenset((UpdateType.CHAT_BOOST,)),
    hash_from_data=hash_data,
    data_from_event=get_boost_giveaway_in_chat,
)
REMOVED_CHAT_BOOST: typing.Final = Hasher(
    update_types=frozenset((UpdateType.REMOVED_CHAT_BOOST,)),
    hash_from_data=identity_hash,
    data_from_event=get_removed_boost_id,
)
REMOVED_CHAT_BOOST_IN_CHAT: typing.Final = Hasher(
    update_types=frozenset((UpdateType.REMOVED_CHAT_BOOST,)),
    hash_from_data=identity_hash,
    data_from_event=get_removed_boost_chat,
)
REMOVED_CHAT_BOOST_IN_CHAT_FOR_BOOST: typing.Final = Hasher(
    update_types=frozenset((UpdateType.REMOVED_CHAT_BOOST,)),
    hash_from_data=hash_data,
    data_from_event=get_removed_boost_in_chat,
)
REMOVED_CHAT_BOOST_FROM_USER: typing.Final = Hasher(
    update_types=frozenset((UpdateType.REMOVED_CHAT_BOOST,)),
    hash_from_data=identity_hash,
    data_from_event=get_removed_boost_user,
)
REMOVED_CHAT_BOOST_FROM_USER_IN_CHAT: typing.Final = Hasher(
    update_types=frozenset((UpdateType.REMOVED_CHAT_BOOST,)),
    hash_from_data=hash_data,
    data_from_event=get_removed_boost_user_in_chat,
)
REMOVED_CHAT_BOOST_IN_CHAT_FOR_GIVEAWAY: typing.Final = Hasher(
    update_types=frozenset((UpdateType.REMOVED_CHAT_BOOST,)),
    hash_from_data=hash_data,
    data_from_event=get_removed_boost_giveaway_in_chat,
)


__all__ = (
    "CHAT_BOOST",
    "CHAT_BOOST_FROM_USER",
    "CHAT_BOOST_FROM_USER_IN_CHAT",
    "CHAT_BOOST_IN_CHAT",
    "CHAT_BOOST_IN_CHAT_FOR_BOOST",
    "CHAT_BOOST_IN_CHAT_FOR_GIVEAWAY",
    "REMOVED_CHAT_BOOST",
    "REMOVED_CHAT_BOOST_FROM_USER",
    "REMOVED_CHAT_BOOST_FROM_USER_IN_CHAT",
    "REMOVED_CHAT_BOOST_IN_CHAT",
    "REMOVED_CHAT_BOOST_IN_CHAT_FOR_BOOST",
    "REMOVED_CHAT_BOOST_IN_CHAT_FOR_GIVEAWAY",
)
