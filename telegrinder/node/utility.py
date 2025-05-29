from telegrinder.node.base import ComposeError, NodeType, scalar_node
from telegrinder.node.scope import NodeScope
from telegrinder.tools.magic.annotations import get_generic_alias_args


@scalar_node(scope=NodeScope.PER_CALL)
class TypeArgs:
    @classmethod
    def compose(cls, t: NodeType) -> dict[str, type[object]]:
        return get_generic_alias_args(t).expect(ComposeError("No type args"))
