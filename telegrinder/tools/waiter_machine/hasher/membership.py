import typing

from telegrinder.tools.waiter_machine.hasher.hasher import Hasher, hash_data, identity_hash
from telegrinder.types.enums import UpdateType

if typing.TYPE_CHECKING:
    from telegrinder.bot.cute_types.chat_join_request import ChatJoinRequestCute as ChatJoinRequest
    from telegrinder.bot.cute_types.chat_member_updated import ChatMemberUpdatedCute as ChatMemberUpdated

    type ChatId = int
    type JoinRequesterUserId = int
    type ActorUserId = int
    type TargetMemberUserId = int
    type JoinRequestUserChatId = int
    type JoinRequestQueryId = str


def get_member_chat(event: ChatMemberUpdated) -> ChatId:
    return event.chat.id


def get_member_actor(event: ChatMemberUpdated) -> ActorUserId:
    return event.from_.id


def get_member_actor_in_chat(event: ChatMemberUpdated) -> tuple[ChatId, ActorUserId]:
    return event.chat.id, event.from_.id


def get_member_target(event: ChatMemberUpdated) -> TargetMemberUserId:
    return event.new_chat_member.v.user.id


def get_member_target_in_chat(event: ChatMemberUpdated) -> tuple[ChatId, TargetMemberUserId]:
    return event.chat.id, event.new_chat_member.v.user.id


def get_join_chat(event: ChatJoinRequest) -> ChatId:
    return event.chat.id


def get_join_user(event: ChatJoinRequest) -> JoinRequesterUserId:
    return event.from_.id


def get_join_user_in_chat(event: ChatJoinRequest) -> tuple[ChatId, JoinRequesterUserId]:
    return event.chat.id, event.from_.id


def get_join_user_chat(event: ChatJoinRequest) -> JoinRequestUserChatId:
    return event.user_chat_id


def get_join_query(event: ChatJoinRequest) -> JoinRequestQueryId | None:
    return event.query_id.unwrap_or_none()


def get_join_user_in_user_chat(event: ChatJoinRequest) -> tuple[JoinRequestUserChatId, JoinRequesterUserId]:
    return event.user_chat_id, event.from_.id


CHAT_MEMBER_IN_CHAT: typing.Final = Hasher(
    update_types=frozenset((UpdateType.CHAT_MEMBER,)),
    hash_from_data=identity_hash,
    data_from_event=get_member_chat,
)

CHAT_MEMBER_FROM_USER: typing.Final = Hasher(
    update_types=frozenset((UpdateType.CHAT_MEMBER,)),
    hash_from_data=identity_hash,
    data_from_event=get_member_actor,
)

CHAT_MEMBER_FROM_USER_IN_CHAT: typing.Final = Hasher(
    update_types=frozenset((UpdateType.CHAT_MEMBER,)),
    hash_from_data=hash_data,
    data_from_event=get_member_actor_in_chat,
)

CHAT_MEMBER_FOR_USER: typing.Final = Hasher(
    update_types=frozenset((UpdateType.CHAT_MEMBER,)),
    hash_from_data=identity_hash,
    data_from_event=get_member_target,
)

CHAT_MEMBER_FOR_USER_IN_CHAT: typing.Final = Hasher(
    update_types=frozenset((UpdateType.CHAT_MEMBER,)),
    hash_from_data=hash_data,
    data_from_event=get_member_target_in_chat,
)

MY_CHAT_MEMBER_IN_CHAT: typing.Final = Hasher(
    update_types=frozenset((UpdateType.MY_CHAT_MEMBER,)),
    hash_from_data=identity_hash,
    data_from_event=get_member_chat,
)

MY_CHAT_MEMBER_FROM_USER: typing.Final = Hasher(
    update_types=frozenset((UpdateType.MY_CHAT_MEMBER,)),
    hash_from_data=identity_hash,
    data_from_event=get_member_actor,
)

MY_CHAT_MEMBER_FROM_USER_IN_CHAT: typing.Final = Hasher(
    update_types=frozenset((UpdateType.MY_CHAT_MEMBER,)),
    hash_from_data=hash_data,
    data_from_event=get_member_actor_in_chat,
)

MY_CHAT_MEMBER_FOR_USER: typing.Final = Hasher(
    update_types=frozenset((UpdateType.MY_CHAT_MEMBER,)),
    hash_from_data=identity_hash,
    data_from_event=get_member_target,
)

MY_CHAT_MEMBER_FOR_USER_IN_CHAT: typing.Final = Hasher(
    update_types=frozenset((UpdateType.MY_CHAT_MEMBER,)),
    hash_from_data=hash_data,
    data_from_event=get_member_target_in_chat,
)

CHAT_JOIN_REQUEST: typing.Final = Hasher(
    update_types=frozenset((UpdateType.CHAT_JOIN_REQUEST,)),
    hash_from_data=identity_hash,
    data_from_event=get_join_query,
)

CHAT_JOIN_REQUEST_IN_CHAT: typing.Final = Hasher(
    update_types=frozenset((UpdateType.CHAT_JOIN_REQUEST,)),
    hash_from_data=identity_hash,
    data_from_event=get_join_chat,
)

CHAT_JOIN_REQUEST_FROM_USER: typing.Final = Hasher(
    update_types=frozenset((UpdateType.CHAT_JOIN_REQUEST,)),
    hash_from_data=identity_hash,
    data_from_event=get_join_user,
)

CHAT_JOIN_REQUEST_FROM_USER_IN_CHAT: typing.Final = Hasher(
    update_types=frozenset((UpdateType.CHAT_JOIN_REQUEST,)),
    hash_from_data=hash_data,
    data_from_event=get_join_user_in_chat,
)

CHAT_JOIN_REQUEST_IN_USER_CHAT: typing.Final = Hasher(
    update_types=frozenset((UpdateType.CHAT_JOIN_REQUEST,)),
    hash_from_data=identity_hash,
    data_from_event=get_join_user_chat,
)

CHAT_JOIN_REQUEST_FROM_USER_IN_USER_CHAT: typing.Final = Hasher(
    update_types=frozenset((UpdateType.CHAT_JOIN_REQUEST,)),
    hash_from_data=hash_data,
    data_from_event=get_join_user_in_user_chat,
)


__all__ = (
    "CHAT_JOIN_REQUEST",
    "CHAT_JOIN_REQUEST_FROM_USER",
    "CHAT_JOIN_REQUEST_FROM_USER_IN_CHAT",
    "CHAT_JOIN_REQUEST_FROM_USER_IN_USER_CHAT",
    "CHAT_JOIN_REQUEST_IN_CHAT",
    "CHAT_JOIN_REQUEST_IN_USER_CHAT",
    "CHAT_MEMBER_FOR_USER",
    "CHAT_MEMBER_FOR_USER_IN_CHAT",
    "CHAT_MEMBER_FROM_USER",
    "CHAT_MEMBER_FROM_USER_IN_CHAT",
    "CHAT_MEMBER_IN_CHAT",
    "MY_CHAT_MEMBER_FOR_USER",
    "MY_CHAT_MEMBER_FOR_USER_IN_CHAT",
    "MY_CHAT_MEMBER_FROM_USER",
    "MY_CHAT_MEMBER_FROM_USER_IN_CHAT",
    "MY_CHAT_MEMBER_IN_CHAT",
)
