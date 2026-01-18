"""Compose nodes with specific agent and context.

This module provides the `compose` function for executing nodes with dependency injection.

Key features:
- Execute functions as nodes with automatic dependency resolution
- Work with Node classes and ready-made Composable objects
- Integration with `Context` for access to API, events, data, and other nodes

```python
# Executing a function node
async def process_data(user_id: int, api: API) -> str:
    user = await api.get_chat(user_id)
    return f"Hello, {user.first_name}!"

async def handler(context: Context):
    async with compose(process_data, context) as result:
        match result:
            case Ok(value):
                print(value)  # "Hello, John!"
            case Error(error):
                print(f"Error: {error}")

# Executing a node with additional dependencies
from telegrinder.node import per_call, scalar_node

@per_call
@scalar_node
class Database:
    @classmethod
    def __compose__(cls) -> "Database":
        return cls()

async def get_user_data(db: Database, user_id: int) -> dict[str, Any]:
    # Use db to fetch data
    return {"id": user_id, "name": "User"}

async def handler(context: Context):
    async with compose(get_user_data, context) as result:
        user_data = result.unwrap()

# Passing additional root dependencies
async def handler(context: Context):
    custom_data = {"custom_key": "custom_value"}

    async with compose(
        my_node,
        context,
        roots={CustomType: custom_data}
    ) as result:
        # roots allows injecting additional dependencies
        pass
```

The `compose` function returns an async context manager that:

- Creates a local scope for node composing
- Automatically resolves all node dependencies
- Returns `Result[T, NodeError]` with the composed result
"""

import dataclasses
import typing
from contextlib import asynccontextmanager
from functools import lru_cache

from kungfu.library.monad.result import Error, Ok, Result
from nodnod.agent.base import Agent
from nodnod.agent.event_loop.agent import EventLoopAgent
from nodnod.error import NodeError
from nodnod.interface import create_agent_from_node, create_node_from_function, inject_externals, inject_internals
from nodnod.node import Node
from nodnod.scope import Scope
from nodnod.utils.is_type import is_type

from telegrinder.node.scope import TELEGRINDER_CONTEXT, MappedScopes, NodeScope
from telegrinder.tools.aio import maybe_awaitable
from telegrinder.tools.magic.function import Function

if typing.TYPE_CHECKING:
    from telegrinder.bot.dispatch.context import Context

type _Composable[T: Agent] = Function[..., typing.Any] | type[Node[typing.Any, typing.Any]] | Composable[T]


@lru_cache(maxsize=1024 * 4)
def create_composable[T: Agent](
    node_or_function: type[Node[typing.Any, typing.Any]] | Function[..., typing.Any],
    /,
    *,
    agent_cls: type[T] = EventLoopAgent,
) -> Composable[T]:
    if not isinstance(node_or_function, type):
        node_or_function = create_node_from_function(node_or_function)
    return Composable(node_or_function, create_agent_from_node(node_or_function, agent_cls=agent_cls))


@asynccontextmanager
async def run_agent(
    agent: Agent,
    context: Context,
    *,
    roots: dict[type[typing.Any], typing.Any] | None = None,
    per_event_scope: Scope | None = None,
) -> typing.AsyncGenerator[Result[Scope, NodeError]]:
    event_scope = (
        per_event_scope
        if per_event_scope is not None
        else context.per_event_scope.expect(ValueError("Per event scope is not found in context."))
    )
    mapped_scopes = MappedScopes(
        global_scope=TELEGRINDER_CONTEXT.node_global_scope,
        per_event_scope=event_scope,
    )

    async with event_scope.create_child(detail=NodeScope.PER_CALL) as local_scope:
        try:
            inject_internals(local_scope, {type(context): context} | (roots or {}))
            inject_externals(local_scope, context)
            await maybe_awaitable(agent.run(local_scope, mapped_scopes))
            yield Ok(local_scope.merge())
        except NodeError as error:
            yield Error(error)


@typing.overload
def compose[R](
    function: Function[..., R],
    /,
    context: Context,
    *,
    per_event_scope: Scope | None = None,
    agent_cls: type[Agent] | None = None,
    roots: dict[type[typing.Any], typing.Any] | None = None,
) -> typing.AsyncContextManager[Result[R, NodeError], None]: ...


@typing.overload
def compose[T: Agent](
    composable: Composable[T],
    /,
    context: Context,
    *,
    per_event_scope: Scope | None = None,
    roots: dict[type[typing.Any], typing.Any] | None = None,
) -> typing.AsyncContextManager[Result[typing.Any, NodeError], None]: ...


@typing.overload
def compose[T](
    node: type[Node[T, typing.Any]],
    /,
    context: Context,
    agent: Agent,
    *,
    per_event_scope: Scope | None = None,
    roots: dict[type[typing.Any], typing.Any] | None = None,
) -> typing.AsyncContextManager[Result[T, NodeError], None]: ...


@asynccontextmanager
async def compose[T = typing.Any](
    node: _Composable[Agent],
    context: Context,
    *,
    per_event_scope: Scope | None = None,
    agent: Agent | None = None,
    agent_cls: type[Agent] | None = None,
    roots: dict[type[typing.Any], typing.Any] | None = None,
) -> typing.AsyncGenerator[Result[T, NodeError], None]:
    composable = None

    if isinstance(node, Composable):
        composable = node
    elif callable(node):
        composable = create_composable(node, agent_cls=agent_cls or EventLoopAgent)

    if composable is not None:
        node, agent = composable.node, typing.cast("Agent", composable.agent)
    elif not is_type(node, Node):
        raise TypeError("Compose requires function, node, or composable.")

    if agent is None:
        raise ValueError("Agent is required.")

    async with run_agent(agent, context, roots=roots, per_event_scope=per_event_scope) as result:
        yield result.map(lambda scope: scope[node].value)


@dataclasses.dataclass(frozen=True, slots=True)
class Composable[T: Agent = Agent]:
    node: type[Node[typing.Any, typing.Any]]
    agent: T


__all__ = (
    "Composable",
    "compose",
    "create_composable",
    "run_agent",
)
