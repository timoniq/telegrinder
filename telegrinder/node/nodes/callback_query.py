import typing

from nodnod.error import NodeError
from nodnod.interface.scalar import scalar_node

from telegrinder.bot.cute_types.callback_query import CallbackQueryCute


@scalar_node
class CallbackQueryData:
    @classmethod
    def __compose__(cls, callback_query: CallbackQueryCute) -> str:
        return callback_query.data.expect(NodeError("Cannot complete decode callback query data."))


@scalar_node
class CallbackQueryDataJson:
    @classmethod
    def __compose__(cls, callback_query: CallbackQueryCute) -> dict[str, typing.Any]:
        return callback_query.decode_data().expect(
            NodeError("Cannot complete decode callback query data."),
        )


__all__ = ("CallbackQueryData", "CallbackQueryDataJson")
