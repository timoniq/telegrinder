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
        logger.debug(f"Composing polymorphic node {cls.__name__!r}...")
        scope = getattr(cls, "scope", None)
        node_ctx = context.get_or_set(CONTEXT_STORE_NODES_KEY, {})

        for i, impl_ in enumerate(get_impls(cls)):
            logger.debug("Checking impl {!r}...", impl_.__name__)
            composition = Composition(impl_, True)
            node_collection = await composition.compose_nodes(update, context)
            if node_collection is None:
                logger.debug("Impl {!r} composition failed!", impl_.__name__)
                continue

            # To determine whether this is a right morph, all subnodes must be resolved
            if scope is NodeScope.PER_EVENT and (cls, i) in node_ctx:
                logger.debug(
                    "Morph is already cached as per_event node, using its value. Impl {!r} succeeded!",
                    impl_.__name__,
                )
                res: NodeSession = node_ctx[(cls, i)]
                await node_collection.close_all()
                return res.value

            result = await composition(cls, **node_collection.values)
            if scope is NodeScope.PER_EVENT:
                node_ctx[(cls, i)] = NodeSession(cls, result, {})

            await node_collection.close_all(with_value=result)
            logger.debug("Impl {!r} succeeded with value: {!r}", impl_.__name__, result)
            return result

        raise ComposeError("No implementation found.")


__all__ = ("Polymorphic", "impl")
