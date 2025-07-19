import typing

from telegrinder.node.base import ComposeError, NodeClass, scalar_node
from telegrinder.node.scope import per_call
from telegrinder.tools.magic.annotations import TypeParameter, get_generic_parameters


@per_call
@scalar_node
class TypeArgs:
    @classmethod
    def compose(cls, node_cls: NodeClass) -> dict[TypeParameter, typing.Any]:
        return get_generic_parameters(node_cls).expect(ComposeError("No generic alias."))


__all__ = ("TypeArgs",)
