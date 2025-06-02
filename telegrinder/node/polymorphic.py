import typing

from fntypes.result import Error, Ok

from telegrinder.api.api import API
from telegrinder.bot.cute_types.update import UpdateCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.modules import logger
from telegrinder.node.base import ComposeError, Node, get_nodes
from telegrinder.node.composer import CONTEXT_STORE_NODES_KEY, NodeSession, compose_nodes
from telegrinder.node.scope import NodeScope
from telegrinder.tools.aio import maybe_awaitable
from telegrinder.tools.fullname import fullname
from telegrinder.tools.magic.function import bundle
from telegrinder.types.objects import Update

type Impl = type[classmethod]

MORPH_IMPLEMENTATIONS_KEY: typing.Final[str] = "__morph_implementations__"
IMPL_MARK_KEY: typing.Final[str] = "_is_impl"


@typing.cast("typing.Callable[..., Impl]", lambda f: f)
def impl(method: typing.Callable[..., typing.Any]):
    setattr(method, IMPL_MARK_KEY, True)
    return classmethod(method)


def get_polymorphic_implementations(
    cls: type["Polymorphic"],
    /,
) -> list[typing.Callable[typing.Concatenate[type["Polymorphic"], ...], typing.Any]]:
    moprh_impls = getattr(cls, MORPH_IMPLEMENTATIONS_KEY, None)
    if moprh_impls is not None:
        return moprh_impls

    impls = []
    for cls_ in cls.mro():
        impls += [
            obj.__func__
            for obj in vars(cls_).values()
            if isinstance(obj, classmethod) and getattr(obj.__func__, IMPL_MARK_KEY, False)
        ]

    setattr(cls, MORPH_IMPLEMENTATIONS_KEY, impls)
    return impls


class Polymorphic(Node):
    @classmethod
    async def compose(cls, raw_update: Update, update: UpdateCute, context: Context) -> typing.Any:
        logger.debug(f"Composing polymorphic node `{fullname(cls)}`...")
        scope = getattr(cls, "scope", None)
        node_ctx = context.get_or_set(CONTEXT_STORE_NODES_KEY, {})
        data = {
            API: update.ctx_api,
            Context: context,
            Update: raw_update,
        }

        for i, impl_ in enumerate(get_polymorphic_implementations(cls)):
            logger.debug("Checking impl {!r}...", fullname(impl_))
            node_collection = None

            match await compose_nodes(get_nodes(impl_), context, data=data):
                case Ok(col):
                    node_collection = col
                case Error(err):
                    logger.debug(f"Composition failed with error: {err!r}")

            if node_collection is None:
                logger.debug("Impl `{}` composition failed!", fullname(impl_))
                continue

            # To determine whether this is a right morph, all subnodes must be resolved
            if scope is NodeScope.PER_EVENT and (cls, i) in node_ctx:
                logger.debug(
                    "Morph is already cached as per_event node, using its value. Impl `{}` succeeded!",
                    fullname(impl_),
                )
                res: NodeSession = node_ctx[(cls, i)]
                await node_collection.close_all()
                return res.value

            impl_bundle = bundle(impl_, data, typebundle=True)

            try:
                result = await maybe_awaitable(impl_bundle(cls, **node_collection.values))
            except ComposeError as compose_error:
                logger.debug(
                    "Failed to compose morph impl `{}`, error: {!r}",
                    fullname(impl_),
                    compose_error.message,
                )

            if scope is NodeScope.PER_EVENT:
                node_ctx[(cls, i)] = NodeSession(cls, result, {})

            await node_collection.close_all(with_value=result)
            logger.debug("Impl `{}` composition succeeded", fullname(impl_), result)
            return result

        raise ComposeError("No implementation found.")


__all__ = ("Polymorphic", "impl")
