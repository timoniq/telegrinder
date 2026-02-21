"""Compose nodes with specific agent and context.

Key features:
- Computes functions as nodes with automatic dependency composition
- Work with `Node` classes and ready-made `Composable` objects
- Integration with `Context` for access to API, update and externals

```python
# Compose a function node
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

# Compose a node with additional dependencies
from telegrinder.node import per_call, scalar_node

@per_call
@scalar_node
class Database:
    @classmethod
    def __compose__(cls) -> "Database":
        return cls()

async def get_user_data(db: Database, user_id: int) -> dict[str, Any]:
    # Use `db` to fetch data
    return {"id": user_id, "name": "User"}

async def handler(context: Context):
    async with compose(get_user_data, context) as result:
        user_data = result.unwrap()

# Inject additional dependencies
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
- Automatically runs an agent with the specified node
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
from nodnod.interface import create_agent_from_node, create_node_from_function, inject_internals
from nodnod.interface.node_from_function import Externals
from nodnod.node import Node
from nodnod.scope import Scope

from telegrinder.node.scope import NODE_GLOBAL_SCOPE, MappedScopes, create_per_call_scope
from telegrinder.tools.aio import maybe_awaitable
from telegrinder.tools.magic.function import Function, FunctionGenerator

if typing.TYPE_CHECKING:
    from telegrinder.bot.dispatch.context import Context

type _Composable[T: Agent] = Function[..., typing.Any] | type[Node[typing.Any, typing.Any]] | Composable[T]
type AnyType = typing.Any


@asynccontextmanager
async def _compose_node(
    node: _Composable[Agent],
    context: Context | None = None,
    per_event_scope: Scope | None = None,
    agent: Agent | None = None,
    agent_cls: type[Agent] = EventLoopAgent,
    roots: dict[AnyType, typing.Any] | None = None,
) -> typing.AsyncGenerator[Result[typing.Any, NodeError], None]:
    composable = (
        typing.cast("Composable[Agent]", node)
        if isinstance(node, Composable)
        else create_composable(
            node,
            agent=agent,
            agent_cls=agent_cls,
        )
    )

    async with run_agent(
        composable.agent,
        context,
        roots=roots,
        per_event_scope=per_event_scope,
    ) as result:
        yield result.map(lambda scope: scope[composable.node].value)


@lru_cache(maxsize=1024 * 4)
def create_composable[T: Agent](
    node_or_function: type[Node[typing.Any, typing.Any]] | Function[..., typing.Any],
    /,
    *,
    agent: T | None = None,
    agent_cls: type[T] = EventLoopAgent,
) -> Composable[T]:
    if not isinstance(node_or_function, type):
        node_or_function = create_node_from_function(node_or_function)

    if agent is None:
        agent = create_agent_from_node(node_or_function, agent_cls=agent_cls)

    return Composable(node_or_function, agent)


@asynccontextmanager
async def run_agent(
    agent: Agent,
    context: Context | None = None,
    *,
    roots: dict[AnyType, typing.Any] | None = None,
    per_event_scope: Scope | None = None,
) -> typing.AsyncGenerator[Result[Scope, NodeError]]:
    internals: dict[typing.Any, typing.Any] = (
        {type(context): context, Externals: context} if context is not None else {Externals: Externals()}
    )
    mapped_scopes = MappedScopes(global_scope=NODE_GLOBAL_SCOPE, per_event_scope=per_event_scope)
    scope = create_per_call_scope(NODE_GLOBAL_SCOPE if per_event_scope is None else per_event_scope)

    async with scope:
        try:
            inject_internals(scope, internals if not roots else (internals | roots))
            await maybe_awaitable(agent.run(scope, mapped_scopes))
            yield Ok(scope.merge())
        except NodeError as error:
            yield Error(error)


@typing.overload
def compose[R](
    function: FunctionGenerator[..., typing.Any, R] | Function[..., R],
    /,
    context: Context,
    *,
    per_event_scope: Scope | None = None,
    agent_cls: type[Agent] = EventLoopAgent,
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
    *,
    agent: Agent,
    per_event_scope: Scope | None = None,
    roots: dict[type[typing.Any], typing.Any] | None = None,
) -> typing.AsyncContextManager[Result[T, NodeError], None]: ...


def compose(
    node: _Composable[Agent],
    context: Context,
    *,
    per_event_scope: Scope | None = None,
    agent: Agent | None = None,
    agent_cls: type[Agent] = EventLoopAgent,
    roots: dict[type[typing.Any], typing.Any] | None = None,
) -> typing.AsyncContextManager[Result[typing.Any, NodeError], None]:
    if per_event_scope is None:
        per_event_scope = context.per_event_scope
    return _compose_node(node, context, per_event_scope, agent, agent_cls, roots)  # type: ignore


@typing.overload
def compose_once[R](
    function: FunctionGenerator[..., typing.Any, R] | Function[..., R],
    /,
    *,
    context: Context | None = None,
    agent_cls: type[Agent] = EventLoopAgent,
    roots: dict[AnyType, typing.Any] | None = None,
) -> typing.AsyncContextManager[Result[R, NodeError], None]: ...


@typing.overload
def compose_once(
    composable: Composable[Agent],
    /,
    *,
    context: Context | None = None,
    roots: dict[AnyType, typing.Any] | None = None,
) -> typing.AsyncContextManager[Result[typing.Any, NodeError], None]: ...


@typing.overload
def compose_once[R](
    node: type[Node[R, typing.Any]],
    /,
    *,
    context: Context | None = None,
    agent: Agent | None = None,
    agent_cls: type[Agent] = EventLoopAgent,
    roots: dict[AnyType, typing.Any] | None = None,
) -> typing.AsyncContextManager[Result[R, NodeError], None]: ...


def compose_once(
    node: _Composable[Agent],
    *,
    context: Context | None = None,
    agent: Agent | None = None,
    agent_cls: type[Agent] = EventLoopAgent,
    roots: dict[AnyType, typing.Any] | None = None,
) -> typing.AsyncContextManager[Result[typing.Any, NodeError], None]:
    return _compose_node(node, context, agent=agent, agent_cls=agent_cls, roots=roots)  # type: ignore


@dataclasses.dataclass(frozen=True, slots=True)
class Composable[T: Agent = Agent]:
    node: type[Node[typing.Any, typing.Any]]
    agent: T


__all__ = ("Composable", "compose", "compose_once", "create_composable", "run_agent")
