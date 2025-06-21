from __future__ import annotations

import typing

from telegrinder.modules import logger
from telegrinder.node.scope import NodeScope
from telegrinder.tools.fullname import fullname
from telegrinder.tools.global_context import GlobalContext, ctx_var
from telegrinder.tools.global_context.builtin_context import TelegrinderContext

if typing.TYPE_CHECKING:
    from telegrinder.node.base import IsNode
    from telegrinder.node.composer import NodeSession

TELEGRINDER_CONTEXT: typing.Final[TelegrinderContext] = TelegrinderContext()


class NodeGlobalContext(GlobalContext):
    __ctx_name__ = "node_context"

    global_sessions: dict[IsNode, NodeSession] = ctx_var(
        const=True,
        init=False,
        default_factory=dict,
    )

    async def close_global_scopes(self) -> None:
        for node, session in self.global_sessions.items():
            try:
                await session.close(scopes=(NodeScope.GLOBAL,))
            except BaseException as exc:
                logger.error(
                    "Uncaught `{!r}` was occurred when closing global session for node `{}`",
                    exc,
                    fullname(node),
                )


def get_global_session(node: IsNode, /) -> NodeSession | None:
    return NODE_CONTEXT.global_sessions.get(node)


def set_global_session(node: IsNode, session: NodeSession, /) -> None:
    NODE_CONTEXT.global_sessions[node] = session


@TELEGRINDER_CONTEXT.loop_wrapper.lifespan.on_shutdown
async def close_nodes_global_scopes() -> None:
    await NODE_CONTEXT.close_global_scopes()


NODE_CONTEXT: typing.Final[NodeGlobalContext] = NodeGlobalContext()


__all__ = ("NODE_CONTEXT", "NodeGlobalContext", "get_global_session", "set_global_session")
