import typing

from fntypes.result import Ok

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.node.base import ComposeError, FactoryNode, IsNode
from telegrinder.node.composer import compose_nodes
from telegrinder.node.scope import per_call
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
    async def compose(cls, api: API, update: Update, context: Context) -> typing.Any:
        composed = True

        for node in cls.nodes:
            if node is not None:
                match await compose_nodes(dict(node_result=node), context, {API: api, Update: update}):
                    case Ok(col):
                        value = col.values["node_result"]
                        yield value
                        await col.close_all(with_value=value)
                        break
                    case _:
                        composed = False
            else:
                yield None
                break

        if not composed:
            raise ComposeError(
                "Cannot compose either nodes: {}.".format(", ".join(fullname(n) for n in cls.nodes))
            )


if typing.TYPE_CHECKING:
    type Either[Left, Right: typing.Any | None] = Left | Right
    type Optional[Left] = Either[Left, None]
else:
    Either = type("Either", (_Either,), {"__module__": __name__})
    Optional = type("Optional", (_Either,), {"__module__": __name__})


__all__ = ("Either", "Optional")
