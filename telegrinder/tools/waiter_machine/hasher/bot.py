import typing

from telegrinder.tools.waiter_machine.hasher.hasher import Hasher, hash_data, identity_hash
from telegrinder.types.enums import UpdateType

if typing.TYPE_CHECKING:
    from telegrinder.bot.cute_types.managed_bot_updated import ManagedBotUpdatedCute as ManagedBotUpdated
    from telegrinder.bot.cute_types.stopped_message_generation import (
        MessageGenerationStoppedCute as MessageGenerationStopped,
    )
    from telegrinder.bot.cute_types.subscription import BotSubscriptionUpdatedCute as BotSubscriptionUpdated

    type ManagedBotId = int
    type ChatId = int
    type ManagedBotUserId = int
    type MessageThreadId = int
    type SubscriptionUserId = int
    type InvoicePayload = str
    type MessageDraftId = int


def get_managed_bot(event: ManagedBotUpdated) -> ManagedBotId:
    return event.bot.id


def get_managed_bot_user(event: ManagedBotUpdated) -> ManagedBotUserId:
    return event.user.id


def get_managed_bot_and_user(event: ManagedBotUpdated) -> tuple[ManagedBotId, ManagedBotUserId]:
    return event.bot.id, event.user.id


def get_subscription_payload(event: BotSubscriptionUpdated) -> InvoicePayload:
    return event.invoice_payload


def get_subscription_user(event: BotSubscriptionUpdated) -> SubscriptionUserId:
    return event.user.id


def get_subscription_payload_and_user(event: BotSubscriptionUpdated) -> tuple[InvoicePayload, SubscriptionUserId]:
    return event.invoice_payload, event.user.id


def get_stopped_draft(event: MessageGenerationStopped) -> MessageDraftId:
    return event.draft_id


def get_stopped_chat(event: MessageGenerationStopped) -> ChatId:
    return event.chat.id


def get_stopped_draft_in_chat(event: MessageGenerationStopped) -> tuple[ChatId, MessageDraftId]:
    return event.chat.id, event.draft_id


def get_stopped_thread_in_chat(event: MessageGenerationStopped) -> tuple[MessageThreadId, ChatId] | None:
    thread_id = event.message_thread_id.unwrap_or_none()
    return None if thread_id is None else (thread_id, event.chat.id)


def get_stopped_draft_in_chat_thread(
    event: MessageGenerationStopped,
) -> tuple[MessageDraftId, MessageThreadId, ChatId] | None:
    data = get_stopped_thread_in_chat(event)
    return None if data is None else (event.draft_id, *data)


MANAGED_BOT: typing.Final = Hasher(
    update_types=frozenset((UpdateType.MANAGED_BOT,)),
    hash_from_data=identity_hash,
    data_from_event=get_managed_bot,
)
MANAGED_BOT_FROM_USER: typing.Final = Hasher(
    update_types=frozenset((UpdateType.MANAGED_BOT,)),
    hash_from_data=identity_hash,
    data_from_event=get_managed_bot_user,
)
MANAGED_BOT_FROM_USER_FOR_BOT: typing.Final = Hasher(
    update_types=frozenset((UpdateType.MANAGED_BOT,)),
    hash_from_data=hash_data,
    data_from_event=get_managed_bot_and_user,
)
BOT_SUBSCRIPTION: typing.Final = Hasher(
    update_types=frozenset((UpdateType.SUBSCRIPTION,)),
    hash_from_data=identity_hash,
    data_from_event=get_subscription_payload,
)
BOT_SUBSCRIPTION_FROM_USER: typing.Final = Hasher(
    update_types=frozenset((UpdateType.SUBSCRIPTION,)),
    hash_from_data=identity_hash,
    data_from_event=get_subscription_user,
)
BOT_SUBSCRIPTION_FOR_PAYLOAD_FROM_USER: typing.Final = Hasher(
    update_types=frozenset((UpdateType.SUBSCRIPTION,)),
    hash_from_data=hash_data,
    data_from_event=get_subscription_payload_and_user,
)
MESSAGE_GENERATION_STOPPED: typing.Final = Hasher(
    update_types=frozenset((UpdateType.STOPPED_MESSAGE_GENERATION,)),
    hash_from_data=identity_hash,
    data_from_event=get_stopped_draft,
)
MESSAGE_GENERATION_STOPPED_IN_CHAT: typing.Final = Hasher(
    update_types=frozenset((UpdateType.STOPPED_MESSAGE_GENERATION,)),
    hash_from_data=identity_hash,
    data_from_event=get_stopped_chat,
)
MESSAGE_GENERATION_STOPPED_IN_CHAT_FOR_DRAFT: typing.Final = Hasher(
    update_types=frozenset((UpdateType.STOPPED_MESSAGE_GENERATION,)),
    hash_from_data=hash_data,
    data_from_event=get_stopped_draft_in_chat,
)
MESSAGE_GENERATION_STOPPED_IN_CHAT_THREAD: typing.Final = Hasher(
    update_types=frozenset((UpdateType.STOPPED_MESSAGE_GENERATION,)),
    hash_from_data=hash_data,
    data_from_event=get_stopped_thread_in_chat,
)
MESSAGE_GENERATION_STOPPED_IN_CHAT_THREAD_FOR_DRAFT: typing.Final = Hasher(
    update_types=frozenset((UpdateType.STOPPED_MESSAGE_GENERATION,)),
    hash_from_data=hash_data,
    data_from_event=get_stopped_draft_in_chat_thread,
)


__all__ = (
    "BOT_SUBSCRIPTION",
    "BOT_SUBSCRIPTION_FOR_PAYLOAD_FROM_USER",
    "BOT_SUBSCRIPTION_FROM_USER",
    "MANAGED_BOT",
    "MANAGED_BOT_FROM_USER",
    "MANAGED_BOT_FROM_USER_FOR_BOT",
    "MESSAGE_GENERATION_STOPPED",
    "MESSAGE_GENERATION_STOPPED_IN_CHAT",
    "MESSAGE_GENERATION_STOPPED_IN_CHAT_FOR_DRAFT",
    "MESSAGE_GENERATION_STOPPED_IN_CHAT_THREAD",
    "MESSAGE_GENERATION_STOPPED_IN_CHAT_THREAD_FOR_DRAFT",
)
