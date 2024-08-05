from telegrinder.bot.cute_types import CallbackQueryCute
from telegrinder.node.base import ComposeError, ScalarNode
from telegrinder.node.update import UpdateNode


class CallbackQueryNode(ScalarNode, CallbackQueryCute):
    @classmethod
    async def compose(cls, update: UpdateNode) -> CallbackQueryCute:
        if not update.callback_query:
            raise ComposeError
        return CallbackQueryCute(
            **update.callback_query.unwrap().to_dict(),
            api=update.api,
        )


__all__ = ("CallbackQueryNode",)
