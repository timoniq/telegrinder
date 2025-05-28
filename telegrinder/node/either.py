import typing

from fntypes.result import Error, Ok

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.modules import logger
from telegrinder.node.base import ComposeError, FactoryNode, Node
from telegrinder.node.composer import CONTEXT_STORE_NODES_KEY, GLOBAL_VALUE_KEY, compose_node, compose_nodes
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

    nodes: tuple[type[Node], type[Node] | None]

    def __class_getitem__(cls, node: type[Node] | tuple[type[Node], type[Node]], /):
        nodes = (node, None) if not isinstance(node, tuple) else node
        assert len(nodes) == 2, "Node `Either` must have at least two nodes."
        return cls(nodes=nodes)

    @classmethod
    async def compose(cls, api: API, update: Update, context: Context) -> typing.Any | None:
        data = {API: api, Update: update, Context: context}
        node_ctx = context.get_or_set(CONTEXT_STORE_NODES_KEY, {})

        for node in cls.nodes:
            if node is None:
                return None

            if node.scope is NodeScope.PER_EVENT and node in node_ctx:
                return node_ctx[node].value
            elif node.scope is NodeScope.GLOBAL and hasattr(node, GLOBAL_VALUE_KEY):
                return getattr(node, GLOBAL_VALUE_KEY)

            subnodes = node.as_node().get_subnodes()
            match await compose_nodes(subnodes, context, data):
                case Ok(col):
                    try:
                        session = await compose_node(
                            node=node,
                            linked={
                                typing.cast("type[typing.Any]", n): col.sessions[name].value
                                for name, n in subnodes.items()
                            },
                            data=data,
                        )
                    except ComposeError:
                        continue

                    if node.scope is NodeScope.PER_EVENT:
                        node_ctx[node] = session
                    elif node.scope is NodeScope.GLOBAL:
                        setattr(node, GLOBAL_VALUE_KEY, session.value)

                    return session.value
                case Error(compose_error):
                    logger.info(
                        "Failed to compose either node {} with error: {!r}.",
                        fullname(node),
                        compose_error.message,
                    )

        raise ComposeError("Cannot compose either nodes: {}.".format(", ".join(repr(n) for n in cls.nodes)))


if typing.TYPE_CHECKING:
    type Either[Left, Right: typing.Any | None] = Left | Right
    type Optional[Left] = Either[Left, None]
else:
    Either = _Either
    Optional = type("Optional", (Either,), {})


__all__ = ("Either", "Optional")
