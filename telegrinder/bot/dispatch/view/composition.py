import inspect
import typing

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.cute_types import UpdateCute
from telegrinder.node import ComposeError, Node, compose_node
from telegrinder.types import Update

from .abc import ABCView


class Composition:
    def __init__(self, func: typing.Callable, is_blocking: bool) -> None:
        self.func = func
        self.nodes: dict[str, type[Node]] = {name: parameter.annotation for name, parameter in inspect.signature(func).parameters.items()}
        self.is_blocking = is_blocking
    
    async def compose_nodes(self, update: UpdateCute) -> dict[str, Node] | None:
        nodes: dict[str, Node] = {}
        for name, node_t in self.nodes.items():
            try:
                nodes[name] = await compose_node(node_t, update)
            except ComposeError as err:
                return None
        return nodes
    
    async def __call__(self, **kwargs) -> typing.Any:
        return await self.func(**kwargs)


class CompositionView(ABCView):
    def __init__(self):
        self.compositions: list[Composition] = []

    def __call__(self, is_blocking: bool = True):
        def wrapper(
            func: typing.Callable,
        ):
            self.compositions.append(
                Composition(func, is_blocking),
            )
            return func

        return wrapper

    async def check(self, event: Update) -> bool:
        return bool(self.compositions)

    async def process(self, event: Update, api: ABCAPI):
        update = UpdateCute(**event.to_dict(), api=api)
        for composition in self.compositions:
            nodes = await composition.compose_nodes(update)
            if nodes is not None:
                await composition(**nodes)
                if composition.is_blocking:
                    break

    def load(self, external: typing.Self):
        self.compositions.extend(external.compositions)
