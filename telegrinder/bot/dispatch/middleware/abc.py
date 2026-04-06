import typing
from abc import ABC
from functools import cached_property

from kungfu.library.monad.result import Error, Ok
from nodnod.agent.event_loop.agent import EventLoopAgent
from nodnod.error import NodeError
from nodnod.interface.node_from_function import create_node_from_function

from telegrinder.bot.dispatch.context import Context
from telegrinder.modules import logger
from telegrinder.node.compose import compose, create_composable
from telegrinder.node.scope import NodeScope
from telegrinder.node.utils import get_globals_from_function, get_locals_from_function
from telegrinder.tools.fullname import fullname
from telegrinder.tools.lifespan import Lifespan

if typing.TYPE_CHECKING:
    from nodnod.agent.base import Agent

    from telegrinder.node.compose import Composable

type Node = typing.Any
type MiddlewareResult = bool | typing.Awaitable[bool | None] | None


async def run_pre_middleware(middleware: ABCMiddleware, context: Context) -> bool:
    if middleware.is_pre:
        return bool(await run_middleware(middleware, context, composable=middleware.pre_composable))
    return True


async def run_post_middleware(middleware: ABCMiddleware, context: Context) -> None:
    if middleware.is_post:
        await run_middleware(middleware, context, composable=middleware.post_composable)


async def run_middleware(
    middleware: ABCMiddleware,
    context: Context,
    *,
    composable: Composable[typing.Any],
) -> bool | None:
    async with compose(composable, context) as result:
        match result:
            case Ok(response):
                return response
            case Error(error):
                await logger.adebug(
                    "Middleware `{!r}` failed with error:{}\n",
                    middleware_name := fullname(middleware),
                    NodeError(f"* failed to compose middleware `{middleware_name}`", from_error=error),
                )


class ABCMiddleware(ABC):
    agent_cls: type[Agent] = EventLoopAgent
    scope: NodeScope = NodeScope.PER_CALL
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
        return self.get_composable(
            self.pre,
            self.scope,
            self.agent_cls,
            required_nodes=self.pre_required_nodes,
        )

    @cached_property
    def post_composable(self) -> Composable:
        return self.get_composable(
            self.post,
            self.scope,
            self.agent_cls,
            required_nodes=self.post_required_nodes,
        )

    @staticmethod
    def get_composable(
        method: typing.Callable[..., typing.Any],
        scope: NodeScope,
        agent_cls: type[Agent] | None,
        required_nodes: typing.Mapping[str, Node] | None,
    ) -> Composable:
        node = create_node_from_function(
            method,
            dependencies=required_nodes,
            forward_refs=get_globals_from_function(method),
            namespace=get_locals_from_function(method),
        )
        return create_composable(node, agent_cls=agent_cls, scope=scope)

    def pre(self, *args: typing.Any, **kwargs: typing.Any) -> MiddlewareResult: ...

    def post(self, *args: typing.Any, **kwargs: typing.Any) -> MiddlewareResult: ...

    def to_lifespan(self, context: Context) -> Lifespan:
        return Lifespan(
            startup_tasks=[run_pre_middleware(self, context)],
            shutdown_tasks=[run_post_middleware(self, context)],
        )


__all__ = ("ABCMiddleware", "run_post_middleware", "run_pre_middleware")
