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

if typing.TYPE_CHECKING:
    from telegrinder.node.scope import NodeScope

    # Import members from NodeScope
    GLOBAL, PER_CALL, PER_EVENT = NodeScope.GLOBAL, NodeScope.PER_CALL, NodeScope.PER_EVENT

TELEGRINDER_CONTEXT: typing.Final = TelegrinderContext()
NODE_GLOBAL_SCOPE: typing.Final = TELEGRINDER_CONTEXT.node_global_scope


@TELEGRINDER_CONTEXT.loop_wrapper.lifespan.on_shutdown
async def close_node_global_scope() -> None:
    logger.debug("Closing node global scope")

    try:
        await TELEGRINDER_CONTEXT.close_global_scope()
    except Exception:
        await logger.aexception("While closing node global scope, an error occurred:")
    else:
        await logger.adebug("Node global scope closed")


def create_per_event_scope() -> Scope:
    """Create a new per event scope."""

    return NODE_GLOBAL_SCOPE.create_child(detail=NodeScope.PER_EVENT)


def create_per_call_scope(scope: Scope) -> Scope:
    """Create a new per call scope."""

    return scope.create_child(detail=NodeScope.PER_CALL)


class NodeScopeInfo(dict[type[Node], "NodeScope"]):
    def set_node_scope[T: Node[typing.Any, typing.Any]](self, node: type[T], scope: NodeScope, /) -> None:
        self[node] = scope

    def get_node_scope[T: Node[typing.Any, typing.Any]](self, node: type[T], /) -> NodeScope | None:
        return self.get(node, None)


NODE_SCOPE_INFO: typing.Final = NodeScopeInfo()


class MappedScopes(dict[type[Node], Scope]):
    scopes: dict[NodeScope, Scope]

    def __init__(self, global_scope: Scope, per_event_scope: Scope | None = None) -> None:
        self.scopes = {NodeScope.GLOBAL: global_scope}

        if per_event_scope is not None:
            self.scopes[NodeScope.PER_EVENT] = per_event_scope

    def get(self, key: type[Node], default: Scope | None = None) -> Scope | None:
        scope = NODE_SCOPE_INFO.get_node_scope(key) or NodeScope.PER_EVENT
        return self.scopes.get(scope, default)


# Declare NodeScope members in a global scope
@enum.global_enum
class NodeScope(enum.StrEnum):
    """Node scope types."""

    GLOBAL = "global"
    """Compose only once during runtime, and later be stored and reused when needed ~ `@global_node`."""

    PER_CALL = "local"
    """Compose each time any node will require it to build itself or if we require it to be delivered
    into the handler ~ `@per_call`."""

    PER_EVENT = "event"
    """Compose once per event, so if during the composition the node was already composed, it will be
    reused and won't be composed twice ~ `@per_event`."""

    def __call__[T](self, node: type[T], /) -> type[T]:
        NODE_SCOPE_INFO.set_node_scope(as_node(node), self)
        return node


# Decorators
global_node, per_call, per_event = GLOBAL, PER_CALL, PER_EVENT


__all__ = (
    "GLOBAL",
    "NODE_GLOBAL_SCOPE",
    "NODE_SCOPE_INFO",
    "PER_CALL",
    "PER_EVENT",
    "MappedScopes",
    "NodeScope",
    "create_per_call_scope",
    "create_per_event_scope",
    "global_node",
    "per_call",
    "per_event",
)
