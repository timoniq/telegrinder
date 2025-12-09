"""Specific `scopes` for node scope system.

Scopes:
- `GLOBAL`: compose only once during runtime, and later be stored and reused when needed ~ `@global_node`
- `PER_EVENT`: compose once per event, so if during the composition the node was already composed, it will be reused and won't be composed twice ~ `@per_event`
- `PER_CALL`: compose each time any node will require it to build itself or if we require it to be delivered into the handler ~ `@per_call`
"""

from __future__ import annotations

import enum
import typing

from nodnod.node import Node
from nodnod.scope import Scope

from telegrinder.modules import logger
from telegrinder.node.utils import as_node
from telegrinder.tools.global_context.builtin_context import TelegrinderContext
from telegrinder.tools.global_context.global_context import GlobalContext, ctx_var

if typing.TYPE_CHECKING:
    from telegrinder.node.scope import NodeScope

    # Import members from NodeScope
    GLOBAL, PER_CALL, PER_EVENT = NodeScope.GLOBAL, NodeScope.PER_CALL, NodeScope.PER_EVENT

TELEGRINDER_CONTEXT: typing.Final = TelegrinderContext()


@TELEGRINDER_CONTEXT.loop_wrapper.lifespan.on_shutdown
async def close_node_global_scope() -> None:
    logger.debug("Closing node global scope")

    try:
        await TELEGRINDER_CONTEXT.close_global_scope()
    except Exception as error:
        logger.error("While closing node global scope, an error occurred: {!r}", error)


class NodeScopeInfo(GlobalContext, thread_safe=True):
    __ctx_name__ = "node_scope_info_context"

    scope_info: typing.Final[dict[type[Node], NodeScope]] = ctx_var(
        default_factory=dict,
        const=True,
        init=False,
    )

    def set_node_scope[T: Node[typing.Any, typing.Any]](self, node: type[T], scope: NodeScope, /) -> None:
        self.scope_info[node] = scope

    def get_node_scope[T: Node[typing.Any, typing.Any]](self, node: type[T], /) -> NodeScope | None:
        return self.scope_info.get(node, None)


NODE_SCOPE_INFO: typing.Final = NodeScopeInfo()


class MappedScopes(dict[type[Node], Scope]):
    scopes: dict[NodeScope, Scope]

    def __init__(self, global_scope: Scope, per_event_scope: Scope) -> None:
        self.scopes = {NodeScope.GLOBAL: global_scope, NodeScope.PER_EVENT: per_event_scope}

    def get(self, key: type[Node], default: Scope | None = None) -> Scope | None:
        scope = NODE_SCOPE_INFO.get_node_scope(key) or NodeScope.PER_EVENT
        return self.scopes.get(scope, default)


# Declare NodeScope members in a global scope
@enum.global_enum
class NodeScope(enum.StrEnum):
    GLOBAL = "global"
    PER_CALL = "local"
    PER_EVENT = "per_event"

    def __call__[T](self, node: type[T], /) -> type[T]:
        NODE_SCOPE_INFO.set_node_scope(as_node(node), self)
        return node


# Decorators
global_node, per_call, per_event = GLOBAL, PER_CALL, PER_EVENT


__all__ = (
    "GLOBAL",
    "NODE_SCOPE_INFO",
    "PER_CALL",
    "PER_EVENT",
    "MappedScopes",
    "NodeScope",
    "global_node",
    "per_call",
    "per_event",
)
