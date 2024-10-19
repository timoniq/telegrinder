import typing

from fntypes.result import Error, Ok

from telegrinder.bot.cute_types.callback_query import CallbackQueryCute
from telegrinder.msgspec_utils import msgspec_convert
from telegrinder.node.base import ComposeError, FactoryNode, Name, ScalarNode
from telegrinder.node.update import UpdateNode
from telegrinder.tools.callback_data_serilization import JSONSerializer, MsgPackSerializer
from telegrinder.tools.callback_data_serilization.abc import ABCDataSerializer


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


class CallbackDataFactory(FactoryNode):
    serializer: ABCDataSerializer[typing.Any]

    @classmethod
    def compose(cls, data: CallbackQueryData) -> typing.Any:
        match cls.serializer.deserialize(data):
            case Ok(value):
                return value
            case Error(err):
                raise ComposeError(err)


class _CallbackDataJson(CallbackDataFactory):
    serializer: JSONSerializer[typing.Any]

    def __class_getitem__(cls, json_model: type[typing.Any], /) -> typing.Self:
        return cls(serializer=JSONSerializer(json_model))


class _CallbackDataMsgPack(CallbackDataFactory):
    serializer: MsgPackSerializer[typing.Any]

    def __class_getitem__(cls, msgpack_model: type[typing.Any], /) -> typing.Self:
        return cls(serializer=MsgPackSerializer(msgpack_model))


if typing.TYPE_CHECKING:
    FieldType = typing.TypeVar("FieldType")
    Json = typing.TypeVar("Json")
    Model = typing.TypeVar("Model")

    Field = typing.Annotated[FieldType, ...]
    CallbackDataJson = typing.Annotated[Json, ...]
    CallbackDataMsgPack = typing.Annotated[Model, ...]
else:
    Field = _Field
    CallbackDataJson = _CallbackDataJson
    CallbackDataMsgPack = _CallbackDataMsgPack


__all__ = (
    "CallbackDataFactory",
    "CallbackDataJson",
    "CallbackDataMsgPack",
    "CallbackQueryData",
    "CallbackQueryDataJson",
    "CallbackQueryNode",
    "Field",
)
