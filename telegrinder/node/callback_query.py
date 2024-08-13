from telegrinder.bot.cute_types.callback_query import CallbackQueryCute
from telegrinder.node.base import ComposeError, ScalarNode
from telegrinder.node.update import UpdateNode


class CallbackQueryNode(ScalarNode, CallbackQueryCute):
    @classmethod
    async def compose(cls, update: UpdateNode) -> CallbackQueryCute:
        if not update.callback_query:
            raise ComposeError("Update is not a callback_query.")
        return update.callback_query.unwrap()


__all__ = ("CallbackQueryNode",)
