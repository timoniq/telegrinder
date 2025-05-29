import typing

from telegrinder.node.base import ComposeError, NodeClass, scalar_node
from telegrinder.node.scope import per_call
from telegrinder.tools.magic.annotations import get_generic_alias_args


@scalar_node
@per_call
class TypeArgs:
    @classmethod
    def compose(cls, node_cls: NodeClass) -> dict[str, typing.Any]:
        return get_generic_alias_args(node_cls).expect(ComposeError("No type args"))


__all__ = ("TypeArgs",)
