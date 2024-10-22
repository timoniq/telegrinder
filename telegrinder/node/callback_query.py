import dataclasses
import typing

from fntypes.result import Error, Ok

from telegrinder.bot.cute_types.callback_query import CallbackQueryCute
from telegrinder.msgspec_utils import msgspec_convert
from telegrinder.node.base import ComposeError, DataNode, FactoryNode, GlobalNode, Name, ScalarNode
from telegrinder.node.update import UpdateNode
from telegrinder.tools.callback_data_serilization.abc import ABCDataSerializer
from telegrinder.tools.callback_data_serilization.json_ser import JSONSerializer


class CallbackQueryNode(ScalarNode, CallbackQueryCute):
    @classmethod
    def compose(cls, update: UpdateNode) -> CallbackQueryCute:
        if not update.callback_query:
            raise ComposeError("Update is not a callback_query.")
        return update.callback_query.unwrap()


class CallbackQueryData(ScalarNode, str):
    @classmethod
    def compose(cls, callback_query: CallbackQueryNode) -> str:
        return callback_query.data.expect(ComposeError("Cannot complete decode callback query data."))


class CallbackQueryDataJson(ScalarNode, dict[str, typing.Any]):
    @classmethod
    def compose(cls, callback_query: CallbackQueryNode) -> dict[str, typing.Any]:
        return callback_query.decode_data().expect(
            ComposeError("Cannot complete decode callback query data."),
        )


class _Field(FactoryNode):
    field_type: type[typing.Any]

    def __class_getitem__(cls, field_type: type[typing.Any], /) -> typing.Self:
        return cls(field_type=field_type)

    @classmethod
    def compose(cls, callback_query_data: CallbackQueryDataJson, data_name: Name) -> typing.Any:
        if data := callback_query_data.get(data_name):
            match msgspec_convert(data, cls.field_type):
                case Ok(value):
                    return value
                case Error(err):
                    raise ComposeError(err)

        raise ComposeError(f"Cannot find callback data with name {data_name!r}.")


@dataclasses.dataclass(slots=True)
class CallbackDataSerializer(DataNode, GlobalNode):
    serializer: type[ABCDataSerializer[typing.Any]]

    @classmethod
    def compose(cls) -> typing.Self:
        return cls(serializer=JSONSerializer)


class _CallbackDataModel(FactoryNode):
    data_type: type[typing.Any]
    serializer: type[ABCDataSerializer[typing.Any]] | None = None

    def __class_getitem__(
        cls,
        data_type: type[typing.Any] | tuple[type[typing.Any], type[ABCDataSerializer[typing.Any]]],
        /,
    ) -> typing.Self:
        data_type, serializer = (data_type, None) if not isinstance(data_type, tuple) else data_type
        return cls(data_type=data_type, serializer=serializer)

    @classmethod
    def compose(cls, data: CallbackQueryData, serializer_info: CallbackDataSerializer) -> typing.Any:
        serializer = cls.serializer or serializer_info.serializer
        match serializer(cls.data_type).deserialize(data):
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

    type Field[FieldType] = typing.Annotated[FieldType, ...]
    type CallbackDataModelType[DataType, Serializer] = typing.Annotated[DataType, Serializer]

    CallbackDataModel: typing.TypeAlias = CallbackDataModelType[DataType, Serializer]
else:
    Field = _Field
    CallbackDataModel = _CallbackDataModel


__all__ = (
    "CallbackDataModel",
    "CallbackDataSerializer",
    "CallbackQueryData",
    "CallbackQueryDataJson",
    "CallbackQueryNode",
    "Field",
)
