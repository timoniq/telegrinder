import typing

from telegrinder.bot.cute_types import CallbackQueryCute

from .base import ComposeError, ScalarNode
from .update import UpdateNode


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
