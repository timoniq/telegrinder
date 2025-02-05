import typing

from telegrinder.bot.dispatch.context import Context
from telegrinder.node.base import Node, is_node
from telegrinder.tools.adapter.node import NodeAdapter

from .abc import ABCRule


class NodeRule(ABCRule):
    def __init__(self, *nodes: type[typing.Any] | tuple[str, type[typing.Any]]) -> None:
        self.nodes: list[type[Node]] = []
        self.node_keys: list[str | None] = []

        for binding in nodes:
            node_key, node_t = binding if isinstance(binding, tuple) else (None, binding)
            if not is_node(node_t):
                continue
            self.nodes.append(node_t)
            self.node_keys.append(node_key)

    @property
    def adapter(self) -> NodeAdapter:
        return NodeAdapter(*self.nodes)

    def check(self, resolved_nodes: tuple[Node, ...], ctx: Context) -> typing.Literal[True]:
        for i, node in enumerate(resolved_nodes):
            if key := self.node_keys[i]:
                ctx[key] = node
        return True


__all__ = ("NodeRule",)
