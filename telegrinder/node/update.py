from telegrinder.api.api import API
from telegrinder.bot.cute_types import UpdateCute
from telegrinder.node.base import scalar_node
from telegrinder.types.objects import Update


@scalar_node
class UpdateNode:
    @classmethod
    def compose(cls, update: Update, api: API) -> UpdateCute:
        if isinstance(update, UpdateCute):
            return update
        return UpdateCute.from_update(update, bound_api=api)


__all__ = ("UpdateNode",)
