import typing

from telegrinder.tools.waiter_machine.hasher.hasher import Hasher, hash_data, identity_hash
from telegrinder.types.enums import UpdateType

if typing.TYPE_CHECKING:
    from telegrinder.bot.cute_types.chosen_inline_result import ChosenInlineResultCute as ChosenInlineResult
    from telegrinder.bot.cute_types.inline_query import InlineQueryCute as InlineQuery

type UserId = int
type ResultId = str
type QueryId = str
type InlineMessageId = str

INLINE_QUERY_UPDATE_TYPES: typing.Final = frozenset((UpdateType.INLINE_QUERY,))
CHOSEN_INLINE_RESULT_UPDATE_TYPES: typing.Final = frozenset((UpdateType.CHOSEN_INLINE_RESULT,))


def get_inline_query_id_from_event(event: InlineQuery) -> QueryId:
    return event.id


def get_chosen_inline_result_id_from_event(event: ChosenInlineResult) -> ResultId:
    return event.result_id


def get_user_id_from_inline_query_event(event: InlineQuery) -> UserId:
    return event.from_user.id


def get_user_id_from_chosen_inline_result_event(event: ChosenInlineResult) -> UserId:
    return event.from_user.id


def get_inline_message_id_from_chosen_inline_result_event(event: ChosenInlineResult) -> InlineMessageId | None:
    return event.inline_message_id.unwrap_or_none()


def get_inline_message_id_and_user_id_from_chosen_inline_result_event(
    event: ChosenInlineResult,
) -> tuple[InlineMessageId, UserId] | None:
    inline_message_id = get_inline_message_id_from_chosen_inline_result_event(event)

    if inline_message_id is None:
        return None

    return inline_message_id, event.from_user.id


INLINE_QUERY: typing.Final = Hasher(
    update_types=INLINE_QUERY_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_inline_query_id_from_event,
)
INLINE_QUERY_FROM_USER: typing.Final = Hasher(
    update_types=INLINE_QUERY_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_user_id_from_inline_query_event,
)
CHOSEN_INLINE_RESULT: typing.Final = Hasher(
    update_types=CHOSEN_INLINE_RESULT_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_chosen_inline_result_id_from_event,
)
CHOSEN_INLINE_RESULT_FROM_USER: typing.Final = Hasher(
    update_types=CHOSEN_INLINE_RESULT_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_user_id_from_chosen_inline_result_event,
)
CHOSEN_INLINE_RESULT_FOR_MESSAGE: typing.Final = Hasher(
    update_types=CHOSEN_INLINE_RESULT_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_inline_message_id_from_chosen_inline_result_event,
)
CHOSEN_INLINE_RESULT_FOR_MESSAGE_FROM_USER: typing.Final = Hasher(
    update_types=CHOSEN_INLINE_RESULT_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_inline_message_id_and_user_id_from_chosen_inline_result_event,
)


__all__ = (
    "CHOSEN_INLINE_RESULT",
    "CHOSEN_INLINE_RESULT_FOR_MESSAGE",
    "CHOSEN_INLINE_RESULT_FOR_MESSAGE_FROM_USER",
    "CHOSEN_INLINE_RESULT_FROM_USER",
    "INLINE_QUERY",
    "INLINE_QUERY_FROM_USER",
)
