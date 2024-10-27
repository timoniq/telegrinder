import typing

from fntypes.result import Error, Ok

from telegrinder.bot.cute_types.callback_query import CallbackQueryCute
from telegrinder.msgspec_utils import msgspec_convert
from telegrinder.node.base import ComposeError, FactoryNode, Name, ScalarNode
from telegrinder.node.update import UpdateNode


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


if typing.TYPE_CHECKING:
    type Field[FieldType] = typing.Annotated[FieldType, ...]
else:
    Field = _Field


__all__ = (
    "CallbackQueryData",
    "CallbackQueryDataJson",
    "CallbackQueryNode",
    "Field",
)
