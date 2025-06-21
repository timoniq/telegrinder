import typing

from fntypes.result import Error, Ok

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.modules import logger
from telegrinder.node.base import ComposeError, FactoryNode, IsNode
from telegrinder.node.composer import (
    CONTEXT_STORE_NODES_KEY,
    compose_nodes,
    get_scope,
)
from telegrinder.node.context import get_global_session
from telegrinder.node.scope import NodeScope, per_call
from telegrinder.tools.fullname import fullname
from telegrinder.types.objects import Update


@per_call
class _Either(FactoryNode):
    """Represents a node that either to compose `left` or `right` nodes.

    For example:
    ```python
    # ScalarNode `Integer` -> int
    # ScalarNode `Float` -> float

    Number = Either[Integer, Float]  # using a type alias just as an example

    def number_to_int(number: Number) -> int:
        return int(number)
    ```
    """

    nodes: tuple[IsNode, IsNode | None]

    def __class_getitem__(cls, node: IsNode | tuple[IsNode, IsNode], /) -> typing.Any:
        nodes = (node, None) if not isinstance(node, tuple) else node
        assert len(nodes) == 2, "Node `Either` must have at least two nodes."
        return cls(nodes=nodes)

    @classmethod
    async def compose(cls, api: API, update: Update, context: Context) -> typing.Any | None:
        node_ctx = context.get_or_set(CONTEXT_STORE_NODES_KEY, {})

        for node in cls.nodes:
            if node is None:
                return None

            if get_scope(node) is NodeScope.PER_EVENT and node in node_ctx:
                return node_ctx[node].value
            elif get_scope(node) is NodeScope.GLOBAL and (global_session := get_global_session(node)) is not None:
                return global_session.value

            match await compose_nodes({"_either_node": node}, context, {API: api, Update: update}):
                case Ok(col):
                    return col.values["_either_node"]
                case Error(compose_error):
                    logger.debug(
                        "Failed to compose either node `{}` with error: {!r}.",
                        fullname(node),
                        compose_error.message,
                    )

        raise ComposeError("Cannot compose either nodes: {}.".format(", ".join(fullname(n) for n in cls.nodes)))


if typing.TYPE_CHECKING:
    type Either[Left, Right: typing.Any | None] = Left | Right
    type Optional[Left] = Either[Left, None]
else:
    Either = type("Either", (_Either,), {"__module__": __name__})
    Optional = type("Optional", (_Either,), {"__module__": __name__})


__all__ = ("Either", "Optional")
