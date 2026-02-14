"""`Node` module which implements [nodnod](https://github.com/timoniq/nodnod)
integration for convenient dependency injection via `nodes`.


```python
from telegrinder.node import scalar_node, global_node, per_call

@global_node
@scalar_node
class Hello:
    @classmethod
    def __compose__(cls) -> str:
        return "Hello"

@global_node
@scalar_node
class World:
    @classmethod
    def __compose__(cls) -> str:
        return "World"

@per_call
@scalar_node
class Greeter:
    @classmethod
    def __compose__(cls, hello: Hello, world: World) -> str:
        return f"{hello}, {world}!"

@bot.on.message()
async def hello_world(greeter: Greeter) -> str:
    return greeter
```
"""

# pyright: reportUnusedImport=false, reportUnsupportedDunderAll=false

from nodnod import (
    DataNode,
    Injection,
    Node,
    NodeConstructor,
    NodeError,
    ResultNode,
    Scalar,
    case,
    generic_node,
    polymorphic,
    scalar_node,
)

from telegrinder.node.compose import Composable, compose, compose_once, create_composable, run_agent
from telegrinder.node.nodes import *
from telegrinder.node.nodes import __all__ as nodes_all
from telegrinder.node.scope import (
    GLOBAL,
    NODE_GLOBAL_SCOPE,
    PER_CALL,
    PER_EVENT,
    NodeScope,
    create_per_call_scope,
    create_per_event_scope,
    global_node,
    per_call,
    per_event,
)
from telegrinder.node.utils import as_node, is_node

__all__ = (
    *nodes_all,
    "GLOBAL",
    "NODE_GLOBAL_SCOPE",
    "PER_CALL",
    "PER_EVENT",
    "Composable",
    "DataNode",
    "Injection",
    "Node",
    "NodeConstructor",
    "NodeError",
    "NodeScope",
    "ResultNode",
    "Scalar",
    "as_node",
    "case",
    "compose",
    "compose_once",
    "create_composable",
    "create_per_call_scope",
    "create_per_event_scope",
    "generic_node",
    "global_node",
    "is_node",
    "per_call",
    "per_event",
    "polymorphic",
    "run_agent",
    "scalar_node",
)
