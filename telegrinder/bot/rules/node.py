import typing

from telegrinder.bot.dispatch.context import Context
from telegrinder.node.base import Node

from .abc import ABCRule
from .adapter.node import NodeAdapter


class NodeRule(ABCRule[tuple[Node, ...]]):
    def __init__(self, *nodes: type[Node] | tuple[str, type[Node]]) -> None:
        bindings = [binding if isinstance(binding, tuple) else (None, binding) for binding in nodes]
        self.nodes = [binding[1] for binding in bindings]
        self.node_keys = [binding[0] for binding in bindings]

    @property
    def adapter(self) -> NodeAdapter:
        return NodeAdapter(*self.nodes)  # type: ignore

    async def check(self, resolved_nodes: tuple[Node, ...], ctx: Context) -> typing.Literal[True]:
        for i, node in enumerate(resolved_nodes):
            if key := self.node_keys[i]:
                ctx[key] = node
        return True


__all__ = ("NodeRule",)
