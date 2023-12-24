from telegrinder.bot.cute_types import UpdateCute
from telegrinder.node import Node


async def compose_node(_node: type[Node], update: UpdateCute, ready_context: dict[str, Node] | None = None) -> Node:
    node = _node.as_node()

    context = {}

    if ready_context:
        context.update(ready_context)

    for name, subnode in node.get_sub_nodes().items():
        if subnode is UpdateCute:
            context[name] = update
        else:
            context[name] = await compose_node(subnode, update, context)

    return await node.compose(**context)
