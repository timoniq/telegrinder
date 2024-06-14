import inspect
import typing

from telegrinder.tools.magic import get_impls, impl

from .base import ComposeError
from .composer import Composition
from .update import UpdateNode


class Polymorphic:
    @classmethod
    async def compose(cls, update: UpdateNode) -> typing.Any:
        for impl in get_impls(cls):
            composition = Composition(impl, True)
            node_collection = await composition.compose_nodes(update)
            if node_collection is None:
                continue
            
            result = composition.func(cls, **node_collection.values())
            if inspect.isawaitable(result):
                result = await result
            
            await node_collection.close_all(with_value=result)
            return result
        
        raise ComposeError("No implementation found.")


__all__ = ("Polymorphic", "impl")
