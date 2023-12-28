import inspect
import typing

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.cute_types import UpdateCute
from telegrinder.bot.dispatch.abc import ABCDispatch
from telegrinder.node import (
    ComposeError,
    ContainerNode,
    Node,
    NodeCollection,
    NodeSession,
    compose_node,
)
from telegrinder.tools import magic_bundle
from telegrinder.types import Update


class Composition:
    nodes: dict[str, type[Node]]

    def __init__(self, func: typing.Callable, is_blocking: bool) -> None:
        self.func = func
        self.nodes = {
            name: parameter.annotation
            for name, parameter in inspect.signature(func).parameters.items()
        }
        self.is_blocking = is_blocking
    
    async def compose_nodes(self, update: UpdateCute) -> NodeCollection | None:
        nodes: dict[str, NodeSession] = {}
        for name, node_t in self.nodes.items():
            try:
                nodes[name] = await compose_node(node_t, update)
            except ComposeError as err:
                await NodeCollection(nodes).close_all()
                return None
        return NodeCollection(nodes)
    
    async def __call__(self, **kwargs) -> typing.Any:
        return await self.func(**magic_bundle(self.func, kwargs, start_idx=0, bundle_ctx=False))  # type: ignore


class CompositionDispatch(ABCDispatch):
    def __init__(self) -> None:
        self.compositions: list[Composition] = []
    
    async def feed(self, event: Update, api: ABCAPI) -> bool:
        update = UpdateCute(**event.to_dict(), api=api)
        is_found = False
        for composition in self.compositions:
            nodes = await composition.compose_nodes(update)
            if nodes is not None:
                result = await composition(**nodes.values())
                await nodes.close_all(with_value=result)
                if composition.is_blocking:
                    return True
                is_found = True
        return is_found
    
    def load(self, external: typing.Self):
        self.compositions.extend(external.compositions)

    def __call__(self, *, is_blocking: bool = True, container: typing.Iterable[type[Node]] | None = None):
        def wrapper(func: typing.Callable):
            composition = Composition(func, is_blocking)
            if container is not None:
                composition.nodes["container"] = ContainerNode.link_nodes(list(container))
            self.compositions.append(composition)
            return func
        return wrapper
