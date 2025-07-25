import dataclasses
import typing

from fntypes.library.monad.result import Error, Ok

from telegrinder.bot.cute_types.callback_query import CallbackQueryCute
from telegrinder.bot.cute_types.message import MessageCute
from telegrinder.bot.cute_types.pre_checkout_query import PreCheckoutQueryCute
from telegrinder.node.base import ComposeError, DataNode, FactoryNode, GlobalNode, scalar_node
from telegrinder.node.polymorphic import Polymorphic, impl
from telegrinder.tools.callback_data_serialization.abc import ABCDataSerializer
from telegrinder.tools.callback_data_serialization.json_ser import JSONSerializer
from telegrinder.tools.callback_data_serialization.utils import get_model_serializer


@scalar_node[str]
class Payload(Polymorphic):
    @impl
    def compose_pre_checkout_query(cls, event: PreCheckoutQueryCute) -> str:
        return event.invoice_payload

    @impl
    def compose_callback_query(cls, event: CallbackQueryCute) -> str:
        return event.data.expect("CallbackQuery has no data.")

    @impl
    def compose_message(cls, event: MessageCute) -> str:
        return event.successful_payment.map(
            lambda payment: payment.invoice_payload,
        ).expect("Message has no successful payment.")


@dataclasses.dataclass(frozen=True, slots=True)
class PayloadSerializer[T: type[ABCDataSerializer]](DataNode, GlobalNode[T]):
    serializer: type[ABCDataSerializer[typing.Any]]

    @classmethod
    def compose(cls) -> typing.Self:
        return cls(serializer=cls.get(default=JSONSerializer))


class _PayloadData(FactoryNode):
    data_type: type[typing.Any]
    serializer: type[ABCDataSerializer] | None = None

    def __class_getitem__(
        cls,
        data_type: type[typing.Any] | tuple[type[typing.Any], type[ABCDataSerializer]],
        /,
    ):
        data_type, serializer = (data_type, None) if not isinstance(data_type, tuple) else data_type
        return cls(data_type=data_type, serializer=get_model_serializer(data_type) or serializer)

    @classmethod
    def compose(cls, payload: Payload, payload_serializer: PayloadSerializer) -> typing.Any:
        serializer = cls.serializer or payload_serializer.serializer
        match serializer(cls.data_type).deserialize(payload):
            case Ok(value):
                return value
            case Error(err):
                raise ComposeError(err)


if typing.TYPE_CHECKING:
    type PayloadData[
        DataType,
        Serializer: ABCDataSerializer = AnySerializer,
    ] = typing.Annotated[DataType, Serializer]

    AnySerializer = typing.NewType("AnySerializer", ABCDataSerializer)
else:
    PayloadData = _PayloadData


__all__ = ("Payload", "PayloadData", "PayloadSerializer")
