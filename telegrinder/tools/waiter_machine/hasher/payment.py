import typing

from telegrinder.tools.waiter_machine.hasher.hasher import Hasher, hash_data, identity_hash
from telegrinder.types.enums import UpdateType

if typing.TYPE_CHECKING:
    from telegrinder.bot.cute_types.paid_media_purchased import PaidMediaPurchasedCute as PaidMediaPurchased
    from telegrinder.bot.cute_types.pre_checkout_query import PreCheckoutQueryCute as PreCheckoutQuery
    from telegrinder.bot.cute_types.shipping_query import ShippingQueryCute as ShippingQuery

type QueryId = str
type UserId = int
type InvoicePayload = str

SHIPPING_QUERY_UPDATE_TYPES: typing.Final = frozenset((UpdateType.SHIPPING_QUERY,))
PRE_CHECKOUT_QUERY_UPDATE_TYPES: typing.Final = frozenset((UpdateType.PRE_CHECKOUT_QUERY,))
PAID_MEDIA_PURCHASED_UPDATE_TYPES: typing.Final = frozenset((UpdateType.PURCHASED_PAID_MEDIA,))


def get_shipping_query_id_from_event(event: ShippingQuery) -> QueryId:
    return event.id


def get_shipping_query_user_id_from_event(event: ShippingQuery) -> UserId:
    return event.from_user.id


def get_pre_checkout_query_id_from_event(event: PreCheckoutQuery) -> QueryId:
    return event.id


def get_pre_checkout_query_option_from_event(event: PreCheckoutQuery) -> InvoicePayload:
    return event.invoice_payload


def get_pre_checkout_query_user_id_from_event(event: PreCheckoutQuery) -> UserId:
    return event.from_user.id


def get_pre_checkout_query_option_and_user_id_from_event(
    event: PreCheckoutQuery,
) -> tuple[InvoicePayload, UserId]:
    return event.invoice_payload, event.from_user.id


def get_paid_media_purchased_user_id_from_event(event: PaidMediaPurchased) -> UserId:
    return event.from_user.id


SHIPPING_QUERY: typing.Final = Hasher(
    update_types=SHIPPING_QUERY_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_shipping_query_id_from_event,
)
SHIPPING_QUERY_FROM_USER: typing.Final = Hasher(
    update_types=SHIPPING_QUERY_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_shipping_query_user_id_from_event,
)
PRE_CHECKOUT_QUERY: typing.Final = Hasher(
    update_types=PRE_CHECKOUT_QUERY_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_pre_checkout_query_id_from_event,
)
PRE_CHECKOUT_QUERY_OPTION: typing.Final = Hasher(
    update_types=PRE_CHECKOUT_QUERY_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_pre_checkout_query_option_from_event,
)
PRE_CHECKOUT_QUERY_FROM_USER: typing.Final = Hasher(
    update_types=PRE_CHECKOUT_QUERY_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_pre_checkout_query_user_id_from_event,
)
PRE_CHECKOUT_QUERY_FOR_OPTION_FROM_USER: typing.Final = Hasher(
    update_types=PRE_CHECKOUT_QUERY_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_pre_checkout_query_option_and_user_id_from_event,
)
PAID_MEDIA_PURCHASED_FROM_USER: typing.Final = Hasher(
    update_types=PAID_MEDIA_PURCHASED_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_paid_media_purchased_user_id_from_event,
)


__all__ = (
    "PAID_MEDIA_PURCHASED_FROM_USER",
    "PRE_CHECKOUT_QUERY",
    "PRE_CHECKOUT_QUERY_FOR_OPTION_FROM_USER",
    "PRE_CHECKOUT_QUERY_FROM_USER",
    "PRE_CHECKOUT_QUERY_OPTION",
    "SHIPPING_QUERY",
    "SHIPPING_QUERY_FROM_USER",
)
