import inspect
import typing

from fntypes.result import Error, Ok

from telegrinder.api.api import API
from telegrinder.bot.cute_types.update import UpdateCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.modules import logger
from telegrinder.node.base import ComposeError, Node, get_nodes
from telegrinder.node.composer import CONTEXT_STORE_NODES_KEY, NodeSession, compose_nodes
from telegrinder.node.scope import NodeScope
from telegrinder.tools.magic import get_polymorphic_implemenations, impl, magic_bundle
from telegrinder.types.objects import Update


class Polymorphic(Node):
    @classmethod
    async def compose(cls, raw_update: Update, update: UpdateCute, context: Context) -> typing.Any:
        logger.debug(f"Composing polymorphic node {cls.__name__!r}...")
        scope = getattr(cls, "scope", None)
        node_ctx = context.get_or_set(CONTEXT_STORE_NODES_KEY, {})
        data = {
            API: update.ctx_api,
            Context: context,
            Update: raw_update,
        }

        for i, impl_ in enumerate(get_polymorphic_implemenations(cls)):
            logger.debug("Checking impl {!r}...", impl_.__name__)
            node_collection = None

            match await compose_nodes(get_nodes(impl_), context, data=data):
                case Ok(col):
                    node_collection = col
                case Error(err):
                    logger.debug(f"Composition failed with error: {err!r}")

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

            result = impl_(cls, **node_collection.values | magic_bundle(impl_, data, typebundle=True))
            if inspect.isawaitable(result):
                result = await result

            if scope is NodeScope.PER_EVENT:
                node_ctx[(cls, i)] = NodeSession(cls, result, {})

            await node_collection.close_all(with_value=result)
            logger.debug("Impl {!r} succeeded with value: {!r}", impl_.__name__, result)
            return result

        raise ComposeError("No implementation found.")


__all__ = ("Polymorphic", "impl")
