from abc import ABC
from functools import cached_property

import typing_extensions as typing
from fntypes.result import Error, Ok

from telegrinder.api.api import API
from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.modules import logger
from telegrinder.node.base import IsNode, get_nodes
from telegrinder.node.composer import compose_nodes
from telegrinder.tools.aio import maybe_awaitable
from telegrinder.tools.lifespan import Lifespan
from telegrinder.tools.magic.function import bundle
from telegrinder.types.objects import Update

type Event = Update | BaseCute[typing.Any]
type MiddlewareResult = bool | None | typing.Coroutine[typing.Any, typing.Any, bool | None]


async def run_middleware(
    method: typing.Callable[..., MiddlewareResult],
    api: API,
    event: Update,
    ctx: Context,
    required_nodes: typing.Mapping[str, IsNode] | None = None,
) -> bool | None:
    node_col = None
    data = {API: api, Update: event, Context: ctx}

    if required_nodes:
        match await compose_nodes(required_nodes, ctx, data=data):
            case Ok(value):
                node_col = value
            case Error(compose_error):
                logger.debug(
                    "Cannot compose nodes for `{}`, error: {!r}",
                    method.__qualname__,
                    compose_error.message,
                )
                return False

    try:
        bundle_method = bundle(method, ctx | ({} if node_col is None else node_col.values))
        bundle_method &= bundle(method, data, typebundle=True)
        return await maybe_awaitable(bundle_method())
    finally:
        if node_col is not None:
            await node_col.close_all()


class ABCMiddleware(ABC):
    def __repr__(self) -> str:
        name = f"middleware {type(self).__name__!r}"
        middleware_class = type(self)

        if middleware_class.post is not ABCMiddleware.post:
            name = "post-" + name

        if middleware_class.pre is not ABCMiddleware.pre:
            name = "pre-" + name

        return f"<{name}>"

    if typing.TYPE_CHECKING:

        def pre(self, *args: typing.Any, **kwargs: typing.Any) -> MiddlewareResult: ...

        def post(self, *args: typing.Any, **kwargs: typing.Any) -> MiddlewareResult: ...

    else:

        def pre(self, *args, **kwargs): ...

        def post(self, *args, **kwargs): ...

    @cached_property
    def pre_required_nodes(self) -> dict[str, IsNode]:
        return get_nodes(self.pre)

    @cached_property
    def post_pre_required_nodes(self) -> dict[str, IsNode]:
        return get_nodes(self.post)

    def to_lifespan(
        self,
        event: Event,
        ctx: Context,
        *,
        api: API | None = None,
    ) -> Lifespan:
        if isinstance(event, BaseCute):
            event, api = event.raw_update, event.api

        if api is None:
            raise LookupError("Cannot get api, please pass as kwarg or provide BaseCute api-bound event.")

        return Lifespan(
            startup_tasks=[
                run_middleware(
                    self.pre,
                    api,
                    event,
                    ctx,
                    required_nodes=self.pre_required_nodes,
                ),
            ],
            shutdown_tasks=[
                run_middleware(
                    self.post,
                    api,
                    event,
                    ctx,
                    required_nodes=self.post_pre_required_nodes,
                ),
            ],
        )


__all__ = ("ABCMiddleware", "run_middleware")
