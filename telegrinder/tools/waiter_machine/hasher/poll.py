import typing

from telegrinder.tools.waiter_machine.hasher.hasher import Hasher, hash_data, identity_hash
from telegrinder.types.enums import UpdateType

if typing.TYPE_CHECKING:
    from telegrinder.bot.cute_types.poll import PollCute as Poll
    from telegrinder.bot.cute_types.poll_answer import PollAnswerCute as PollAnswer

    type VoterChatId = int
    type PollId = str
    type VoterUserId = int


def get_poll_id(event: Poll) -> PollId:
    return event.id


def get_answer_poll(event: PollAnswer) -> PollId:
    return event.poll_id


def get_answer_user(event: PollAnswer) -> VoterUserId | None:
    return event.user.map(lambda user: user.id).unwrap_or_none()


def get_answer_user_in_poll(event: PollAnswer) -> tuple[PollId, VoterUserId] | None:
    user_id = get_answer_user(event)
    return None if user_id is None else (event.poll_id, user_id)


def get_answer_chat(event: PollAnswer) -> VoterChatId | None:
    return event.voter_chat.map(lambda chat: chat.id).unwrap_or_none()


def get_answer_chat_in_poll(event: PollAnswer) -> tuple[PollId, VoterChatId] | None:
    chat_id = get_answer_chat(event)
    return None if chat_id is None else (event.poll_id, chat_id)


POLL: typing.Final = Hasher(
    update_types=frozenset((UpdateType.POLL,)),
    hash_from_data=identity_hash,
    data_from_event=get_poll_id,
)
POLL_ANSWER: typing.Final = Hasher(
    update_types=frozenset((UpdateType.POLL_ANSWER,)),
    hash_from_data=identity_hash,
    data_from_event=get_answer_poll,
)
POLL_ANSWER_FROM_USER: typing.Final = Hasher(
    update_types=frozenset((UpdateType.POLL_ANSWER,)),
    hash_from_data=identity_hash,
    data_from_event=get_answer_user,
)
POLL_ANSWER_IN_POLL_FROM_USER: typing.Final = Hasher(
    update_types=frozenset((UpdateType.POLL_ANSWER,)),
    hash_from_data=hash_data,
    data_from_event=get_answer_user_in_poll,
)
POLL_ANSWER_FROM_CHAT: typing.Final = Hasher(
    update_types=frozenset((UpdateType.POLL_ANSWER,)),
    hash_from_data=identity_hash,
    data_from_event=get_answer_chat,
)
POLL_ANSWER_IN_POLL_FROM_CHAT: typing.Final = Hasher(
    update_types=frozenset((UpdateType.POLL_ANSWER,)),
    hash_from_data=hash_data,
    data_from_event=get_answer_chat_in_poll,
)


__all__ = (
    "POLL",
    "POLL_ANSWER",
    "POLL_ANSWER_FROM_CHAT",
    "POLL_ANSWER_FROM_USER",
    "POLL_ANSWER_IN_POLL_FROM_CHAT",
    "POLL_ANSWER_IN_POLL_FROM_USER",
)
