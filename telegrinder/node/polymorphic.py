import inspect
import typing

from telegrinder.bot.dispatch.context import Context
from telegrinder.modules import logger
from telegrinder.node.base import ComposeError, Node
from telegrinder.node.composer import CONTEXT_STORE_NODES_KEY, Composition, NodeSession
from telegrinder.node.scope import NodeScope
from telegrinder.node.update import UpdateNode
from telegrinder.tools.magic import get_impls, impl


class Polymorphic(Node):
    @classmethod
    async def compose(cls, update: UpdateNode, context: Context) -> typing.Any:
        logger.debug(f"Composing polimorphic node {cls.__name__}")
        scope = getattr(cls, "scope", None)
        node_ctx = context.get_or_set(CONTEXT_STORE_NODES_KEY, {})

        for i, impl in enumerate(get_impls(cls)):
            logger.debug("Checking impl {}", impl.__name__)
            composition = Composition(impl, True)
            node_collection = await composition.compose_nodes(update, context)
            if node_collection is None:
                logger.debug("Impl {!r} composition failed", impl.__name__)
                continue

            # To determine whether this is a right morph, all subnodes must be resolved
            if scope is NodeScope.PER_EVENT and (cls, i) in node_ctx:
                logger.debug("Morph is already cached as per_event node, using its value. Impl {!r} succeeded", impl.__name__)
                res: NodeSession = node_ctx[(cls, i)]
                await node_collection.close_all()
                return res.value

            result = composition.func(cls, **node_collection.values)
            if inspect.isawaitable(result):
                result = await result

            if scope is NodeScope.PER_EVENT:
                node_ctx[(cls, i)] = NodeSession(cls, result, {})

            await node_collection.close_all(with_value=result)
            logger.debug("Impl {!r} succeeded with value {}", impl.__name__, result)
            return result

        raise ComposeError("No implementation found.")


__all__ = ("Polymorphic", "impl")
