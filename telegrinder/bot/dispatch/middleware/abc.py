import typing
from abc import ABC
from functools import cached_property

from kungfu.library.monad.result import Error, Ok
from nodnod.error import NodeError
from nodnod.utils.misc import reverse_dict

from telegrinder.bot.dispatch.context import Context
from telegrinder.modules import logger
from telegrinder.node.compose import compose, create_composable_from_node, create_node_from_func
from telegrinder.tools.fullname import fullname
from telegrinder.tools.lifespan import Lifespan

if typing.TYPE_CHECKING:
    from nodnod.agent.base import Agent

    from telegrinder.node.compose import Composable

type Node = typing.Any
type MiddlewareResult = bool | None | typing.Coroutine[typing.Any, typing.Any, bool | None]


async def run_pre_middleware(
    middleware: ABCMiddleware,
    context: Context,
) -> bool | None:
    if middleware.is_pre:
        return bool(await run_middleware(middleware, context, composable=middleware.pre_composable))
    return None


async def run_post_middleware(
    middleware: ABCMiddleware,
    context: Context,
) -> None:
    if middleware.is_post:
        await run_middleware(middleware, context, composable=middleware.post_composable)


async def run_middleware(
    middleware: ABCMiddleware,
    context: Context,
    *,
    composable: Composable,
) -> bool | None:
    async with compose(composable, context) as result:
        match result:
            case Ok(response):
                return response
            case Error(error):
                await logger.adebug(
                    "Middleware `{!r}` failed with error:{}",
                    middleware_name := fullname(middleware),
                    NodeError(f"failed to compose middleware `{middleware_name}`", from_error=error),
                )


class ABCMiddleware(ABC):
    agent_cls: type[Agent] | None = None
    pre_required_nodes: typing.Mapping[str, Node] | None = None
    post_required_nodes: typing.Mapping[str, Node] | None = None

    def __repr__(self) -> str:
        return "<{}{}>".format(
            "".join(
                (
                    f"{'pre-' if self.is_pre else ''}",
                    f"{'post-' if self.is_post else ''}",
                ),
            ),
            f"middleware `{fullname(self)}`",
        )

    @property
    def is_pre(self) -> bool:
        return type(self).pre is not ABCMiddleware.pre

    @property
    def is_post(self) -> bool:
        return type(self).post is not ABCMiddleware.post

    @cached_property
    def pre_composable(self) -> Composable:
        return create_composable_from_node(
            create_node_from_func(
                self.pre,
                dependencies_names=None if self.pre_required_nodes is None else reverse_dict(self.pre_required_nodes),  # type: ignore
            ),
            agent_cls=self.agent_cls,
        )

    @cached_property
    def post_composable(self) -> Composable:
        return create_composable_from_node(
            create_node_from_func(
                self.post,
                dependencies_names=None if self.post_required_nodes is None else reverse_dict(self.post_required_nodes),  # type: ignore
            ),
            agent_cls=self.agent_cls,
        )

    def pre(self) -> MiddlewareResult: ...

    def post(self) -> MiddlewareResult: ...

    def to_lifespan(self, context: Context) -> Lifespan:
        return Lifespan(
            startup_tasks=[run_pre_middleware(self, context)],
            shutdown_tasks=[run_post_middleware(self, context)],
        )


__all__ = (
    "ABCMiddleware",
    "run_post_middleware",
    "run_pre_middleware",
)
