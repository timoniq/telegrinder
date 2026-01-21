import dataclasses
import typing

from kungfu.library.monad.result import Error, Ok
from nodnod.error import NodeError
from nodnod.interface.generic import generic_node
from nodnod.interface.polymorphic import case, polymorphic
from nodnod.interface.scalar import scalar_node

from telegrinder.bot.cute_types.callback_query import CallbackQueryCute
from telegrinder.bot.cute_types.message import MessageCute
from telegrinder.bot.cute_types.pre_checkout_query import PreCheckoutQueryCute
from telegrinder.bot.cute_types.shipping_query import ShippingQueryCute
from telegrinder.node.nodes.global_node import GlobalNode
from telegrinder.tools.serialization.abc import ABCDataSerializer
from telegrinder.tools.serialization.json_ser import JSONSerializer

type _UndefinedSerializer = typing.Any


@scalar_node
@polymorphic[str]
class Payload:
    @case
    def compose_callback_query(cls, event: CallbackQueryCute) -> str:
        return event.data.expect(NodeError("CallbackQuery has no data."))

    @case
    def compose_pre_checkout_query(cls, event: PreCheckoutQueryCute) -> str:
        return event.invoice_payload

    @case
    def compose_shipping_query(cls, event: ShippingQueryCute) -> str:
        return event.invoice_payload

    @case
    def compose_message(cls, event: MessageCute) -> str:
        return event.successful_payment.map(
            lambda payment: payment.invoice_payload,
        ).expect(NodeError("Message has no successful payment."))


@dataclasses.dataclass(frozen=True)
class PayloadSerializer[T: type[ABCDataSerializer] = typing.Any](GlobalNode[T]):
    serializer: type[ABCDataSerializer[typing.Any]]

    @classmethod
    def __compose__(cls) -> typing.Self:
        return cls(serializer=JSONSerializer)


@generic_node
class _PayloadData[Data, Serializer: ABCDataSerializer = _UndefinedSerializer]:
    @classmethod
    def __compose__(
        cls,
        payload: Payload,
        data: type[Data],
        payload_serializer: type[Serializer],
        global_serializer: PayloadSerializer,
    ) -> typing.Any:
        if payload_serializer is _UndefinedSerializer:
            serializer = getattr(data, "__serializer__", global_serializer.serializer)
        else:
            serializer = payload_serializer

        match serializer(data).deserialize(payload):
            case Ok(value):
                return value
            case Error(err):
                raise NodeError(err)


if typing.TYPE_CHECKING:
    type PayloadData[
        DataType = typing.Any,
        Serializer: ABCDataSerializer = _UndefinedSerializer,
    ] = typing.Annotated[DataType, Serializer]

else:
    PayloadData = _PayloadData


__all__ = ("Payload", "PayloadData", "PayloadSerializer")
