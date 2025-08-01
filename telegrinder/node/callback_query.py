import typing

from fntypes.library.monad.result import Error, Ok

from telegrinder.bot.cute_types.callback_query import CallbackQueryCute
from telegrinder.msgspec_utils import convert
from telegrinder.node.base import ComposeError, FactoryNode, Name, scalar_node


@scalar_node
class CallbackQueryData:
    @classmethod
    def compose(cls, callback_query: CallbackQueryCute) -> str:
        return callback_query.data.expect(ComposeError("Cannot complete decode callback query data."))


@scalar_node
class CallbackQueryDataJson:
    @classmethod
    def compose(cls, callback_query: CallbackQueryCute) -> dict[str, typing.Any]:
        return callback_query.decode_data().expect(
            ComposeError("Cannot complete decode callback query data."),
        )


class _Field(FactoryNode):
    field_type: typing.Any

    def __class_getitem__(cls, field_type: typing.Any, /) -> typing.Self:
        return cls(field_type=field_type)

    @classmethod
    def compose(cls, callback_query_data: CallbackQueryDataJson, data_name: Name) -> typing.Any:
        if data := callback_query_data.get(data_name):
            match convert(data, cls.field_type):
                case Ok(value):
                    return value
                case Error(err):
                    raise ComposeError(err)

        raise ComposeError(f"Cannot find callback data with name {data_name!r}.")


if typing.TYPE_CHECKING:
    type Field[FieldType] = FieldType
else:
    Field = _Field


__all__ = (
    "CallbackQueryData",
    "CallbackQueryDataJson",
    "Field",
)
