from telegrinder.api.api import API
from telegrinder.bot.cute_types import UpdateCute
from telegrinder.node.base import ScalarNode
from telegrinder.types.objects import Update


class UpdateNode(ScalarNode, UpdateCute):
    @classmethod
    def compose(cls, update: Update, api: API) -> UpdateCute:
        if isinstance(update, UpdateCute):
            return update
        return UpdateCute.from_update(update, api)


__all__ = ("UpdateNode",)
