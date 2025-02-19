import dataclasses
import typing

from fntypes.result import Error, Ok

from telegrinder.node.base import ComposeError, DataNode, FactoryNode, GlobalNode, scalar_node
from telegrinder.node.callback_query import CallbackQueryNode
from telegrinder.node.message import MessageNode
from telegrinder.node.polymorphic import Polymorphic, impl
from telegrinder.node.pre_checkout_query import PreCheckoutQueryNode
from telegrinder.tools.callback_data_serilization import ABCDataSerializer, JSONSerializer


@scalar_node[str]
class Payload(Polymorphic):
    @impl
    def compose_pre_checkout_query(cls, event: PreCheckoutQueryNode) -> str:
        return event.invoice_payload

    @impl
    def compose_callback_query(cls, event: CallbackQueryNode) -> str:
        return event.data.expect("CallbackQuery has no data.")

    @impl
    def compose_message(cls, event: MessageNode) -> str:
        return event.successful_payment.map(
            lambda payment: payment.invoice_payload,
        ).expect("Message has no successful payment.")


@dataclasses.dataclass(frozen=True, slots=True)
class PayloadSerializer[T: type[ABCDataSerializer[typing.Any]]](DataNode, GlobalNode[T]):
    serializer: type[ABCDataSerializer[typing.Any]]

    @classmethod
    def compose(cls) -> typing.Self:
        return cls(serializer=cls.get(default=JSONSerializer))


class _PayloadData(FactoryNode):
    data_type: type[typing.Any]
    serializer: type[ABCDataSerializer[typing.Any]] | None = None

    def __class_getitem__(
        cls,
        data_type: type[typing.Any] | tuple[type[typing.Any], type[ABCDataSerializer[typing.Any]]],
        /,
    ):
        data_type, serializer = (data_type, None) if not isinstance(data_type, tuple) else data_type
        return cls(data_type=data_type, serializer=serializer)

    @classmethod
    def compose(cls, payload: Payload, payload_serializer: PayloadSerializer) -> typing.Any:
        serializer = cls.serializer or payload_serializer.serializer
        match serializer(cls.data_type).deserialize(payload):
            case Ok(value):
                return value
            case Error(err):
                raise ComposeError(err)


if typing.TYPE_CHECKING:
    import typing_extensions

    DataType = typing.TypeVar("DataType")
    Serializer = typing_extensions.TypeVar(
        "Serializer",
        bound=ABCDataSerializer,
        default=JSONSerializer[typing.Any],
    )

    type PayloadDataType[DataType, Serializer] = typing.Annotated[DataType, Serializer]
    PayloadData: typing.TypeAlias = PayloadDataType[DataType, Serializer]
else:
    PayloadData = _PayloadData


__all__ = ("Payload", "PayloadData", "PayloadSerializer")
