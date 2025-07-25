from fntypes.library.monad.result import Ok

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.node.base import IsNode, is_node
from telegrinder.node.composer import compose_nodes
from telegrinder.types.objects import Update


class NodeRule(ABCRule):
    def __init__(self, *nodes: IsNode | tuple[str, IsNode]) -> None:
        self.nodes: list[IsNode] = []
        self.node_keys: list[str | None] = []

        for binding in nodes:
            node_key, node_t = binding if isinstance(binding, tuple) else (None, binding)
            if not is_node(node_t):
                continue
            self.nodes.append(node_t)
            self.node_keys.append(node_key)

    async def check(self, update: Update, api: API, context: Context) -> bool:
        result = await compose_nodes(
            nodes={f"node_{i}": node for i, node in enumerate(self.nodes)},
            ctx=context,
            data={Update: update, API: api},
        )

        match result:
            case Ok(collection):
                resolved_nodes = collection.sessions
            case _:
                return False

        for i, (node_key, node_value) in enumerate(resolved_nodes.items()):
            if (key := self.node_keys[i]) and node_key == key:
                context[key] = node_value

        await collection.close_all()
        return True


__all__ = ("NodeRule",)
