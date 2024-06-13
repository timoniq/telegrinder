import inspect
import typing

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.cute_types import UpdateCute
from telegrinder.bot.dispatch.abc import ABCDispatch
from telegrinder.node import Composition, ContainerNode, Node
from telegrinder.tools import magic_bundle
from telegrinder.types import Update


class CompositionDispatch(ABCDispatch):
    def __init__(self) -> None:
        self.compositions: list[Composition] = []

    def __repr__(self) -> str:
        return "<{}: with compositions={!r}>".format(
            self.__class__.__name__,
            self.compositions,
        )

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

    def __call__(self, *container_nodes: type[Node], is_blocking: bool = True):
        def wrapper(func: typing.Callable):
            composition = Composition(func, is_blocking)
            if container_nodes:
                composition.nodes["container"] = ContainerNode.link_nodes(list(container_nodes))
            self.compositions.append(composition)
            return func

        return wrapper


__all__ = ("Composition", "CompositionDispatch")
