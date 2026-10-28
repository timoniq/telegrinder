import typing

from telegrinder.tools.waiter_machine.hasher.hasher import Hasher, hash_data, identity_hash
from telegrinder.types.enums import UpdateType

if typing.TYPE_CHECKING:
    from telegrinder.bot.cute_types.paid_media_purchased import PaidMediaPurchasedCute as PaidMediaPurchased
    from telegrinder.bot.cute_types.pre_checkout_query import PreCheckoutQueryCute as PreCheckoutQuery
    from telegrinder.bot.cute_types.shipping_query import ShippingQueryCute as ShippingQuery

    type ShippingQueryId = str
    type ShippingQueryUserId = int
    type ShippingOptionId = str
    type InvoicePayload = str
    type PaidMediaPayload = str
    type PreCheckoutQueryId = str
    type PreCheckoutQueryUserId = int
    type PaidMediaBuyerUserId = int

SHIPPING_QUERY_UPDATE_TYPES: typing.Final = frozenset((UpdateType.SHIPPING_QUERY,))
PRE_CHECKOUT_QUERY_UPDATE_TYPES: typing.Final = frozenset((UpdateType.PRE_CHECKOUT_QUERY,))
PAID_MEDIA_PURCHASED_UPDATE_TYPES: typing.Final = frozenset((UpdateType.PURCHASED_PAID_MEDIA,))


def get_shipping_query_id_from_event(event: ShippingQuery) -> ShippingQueryId:
    return event.id


def get_shipping_query_user_id_from_event(event: ShippingQuery) -> ShippingQueryUserId:
    return event.from_user.id


def get_pre_checkout_query_id_from_event(event: PreCheckoutQuery) -> PreCheckoutQueryId:
    return event.id


def get_pre_checkout_query_option_from_event(event: PreCheckoutQuery) -> InvoicePayload:
    return event.invoice_payload


def get_pre_checkout_query_user_id_from_event(event: PreCheckoutQuery) -> PreCheckoutQueryUserId:
    return event.from_user.id


def get_pre_checkout_query_option_and_user_id_from_event(
    event: PreCheckoutQuery,
) -> tuple[InvoicePayload, PreCheckoutQueryUserId]:
    return event.invoice_payload, event.from_user.id


def get_paid_media_purchased_user_id_from_event(event: PaidMediaPurchased) -> PaidMediaBuyerUserId:
    return event.from_user.id


def get_shipping_payload_from_event(event: ShippingQuery) -> InvoicePayload:
    return event.invoice_payload


def get_shipping_payload_and_user_from_event(event: ShippingQuery) -> tuple[InvoicePayload, ShippingQueryUserId]:
    return event.invoice_payload, event.from_user.id


def get_shipping_option_from_event(event: PreCheckoutQuery) -> ShippingOptionId | None:
    return event.shipping_option_id.unwrap_or_none()


def get_shipping_option_and_user_from_event(
    event: PreCheckoutQuery,
) -> tuple[ShippingOptionId, PreCheckoutQueryUserId] | None:
    option_id = get_shipping_option_from_event(event)
    return None if option_id is None else (option_id, event.from_user.id)


def get_payload_and_shipping_option_from_event(
    event: PreCheckoutQuery,
) -> tuple[InvoicePayload, ShippingOptionId] | None:
    option_id = get_shipping_option_from_event(event)
    return None if option_id is None else (event.invoice_payload, option_id)


def get_paid_media_payload_from_event(event: PaidMediaPurchased) -> PaidMediaPayload:
    return event.paid_media_payload


def get_paid_media_payload_and_user_from_event(
    event: PaidMediaPurchased,
) -> tuple[PaidMediaPayload, PaidMediaBuyerUserId]:
    return event.paid_media_payload, event.from_user.id


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
SHIPPING_QUERY_FOR_PAYLOAD: typing.Final = Hasher(
    update_types=SHIPPING_QUERY_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_shipping_payload_from_event,
)
SHIPPING_QUERY_FOR_PAYLOAD_FROM_USER: typing.Final = Hasher(
    update_types=SHIPPING_QUERY_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_shipping_payload_and_user_from_event,
)
PRE_CHECKOUT_QUERY_FOR_SHIPPING_OPTION: typing.Final = Hasher(
    update_types=PRE_CHECKOUT_QUERY_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_shipping_option_from_event,
)
PRE_CHECKOUT_QUERY_FOR_SHIPPING_OPTION_FROM_USER: typing.Final = Hasher(
    update_types=PRE_CHECKOUT_QUERY_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_shipping_option_and_user_from_event,
)
PRE_CHECKOUT_QUERY_FOR_PAYLOAD_AND_SHIPPING_OPTION: typing.Final = Hasher(
    update_types=PRE_CHECKOUT_QUERY_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_payload_and_shipping_option_from_event,
)
PAID_MEDIA_PURCHASED: typing.Final = Hasher(
    update_types=PAID_MEDIA_PURCHASED_UPDATE_TYPES,
    hash_from_data=identity_hash,
    data_from_event=get_paid_media_payload_from_event,
)
PAID_MEDIA_PURCHASED_FOR_PAYLOAD_FROM_USER: typing.Final = Hasher(
    update_types=PAID_MEDIA_PURCHASED_UPDATE_TYPES,
    hash_from_data=hash_data,
    data_from_event=get_paid_media_payload_and_user_from_event,
)


__all__ = (
    "PAID_MEDIA_PURCHASED",
    "PAID_MEDIA_PURCHASED_FOR_PAYLOAD_FROM_USER",
    "PAID_MEDIA_PURCHASED_FROM_USER",
    "PRE_CHECKOUT_QUERY",
    "PRE_CHECKOUT_QUERY_FOR_OPTION_FROM_USER",
    "PRE_CHECKOUT_QUERY_FOR_PAYLOAD_AND_SHIPPING_OPTION",
    "PRE_CHECKOUT_QUERY_FOR_SHIPPING_OPTION",
    "PRE_CHECKOUT_QUERY_FOR_SHIPPING_OPTION_FROM_USER",
    "PRE_CHECKOUT_QUERY_FROM_USER",
    "PRE_CHECKOUT_QUERY_OPTION",
    "SHIPPING_QUERY",
    "SHIPPING_QUERY_FOR_PAYLOAD",
    "SHIPPING_QUERY_FOR_PAYLOAD_FROM_USER",
    "SHIPPING_QUERY_FROM_USER",
)
