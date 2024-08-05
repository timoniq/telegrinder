from telegrinder.bot.cute_types import UpdateCute
from telegrinder.node.base import ScalarNode


class UpdateNode(ScalarNode, UpdateCute):
    @classmethod
    async def compose(cls, update: UpdateCute) -> UpdateCute:
        return update


__all__ = ("UpdateNode",)
