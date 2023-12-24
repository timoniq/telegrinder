import inspect
import typing

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.cute_types import UpdateCute
from telegrinder.bot.dispatch.abc import ABCDispatch
from telegrinder.node import ComposeError, Node, NodeCollection, NodeSession, compose_node
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
                return None
        return NodeCollection(nodes)
    
    async def __call__(self, **kwargs) -> typing.Any:
        return await self.func(**kwargs)


class CompositionDispatch(ABCDispatch):
    def __init__(self) -> None:
        self.compositions: list[Composition] = []
    
    async def feed(self, event: Update, api: ABCAPI) -> bool:
        update = UpdateCute(**event.to_dict(), api=api)
        is_found = False
        for composition in self.compositions:
            nodes = await composition.compose_nodes(update)
            if nodes is not None:
                await composition(**nodes.values())
                await nodes.close_all()
                if composition.is_blocking:
                    return True
                is_found = True
        return is_found
    
    def load(self, external: typing.Self):
        self.compositions.extend(external.compositions)

    def __call__(self, is_blocking: bool = True):
        def wrapper(func: typing.Callable):
            self.compositions.append(Composition(func, is_blocking))
            return func
        return wrapper
