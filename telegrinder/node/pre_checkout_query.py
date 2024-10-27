from telegrinder.bot.cute_types.pre_checkout_query import PreCheckoutQueryCute
from telegrinder.node.base import ScalarNode
from telegrinder.node.update import UpdateNode


class PreCheckoutQueryNode(ScalarNode, PreCheckoutQueryCute):
    @classmethod
    def compose(cls, update: UpdateNode) -> PreCheckoutQueryCute:
        return update.pre_checkout_query.expect("Update is not a pre_checkout_query.")


__all__ = ("PreCheckoutQueryNode",)
