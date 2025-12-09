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

from telegrinder.node.compose import compose, run_agent
from telegrinder.node.nodes import *
from telegrinder.node.nodes import __all__ as nodes_all
from telegrinder.node.scope import GLOBAL, PER_CALL, PER_EVENT, global_node, per_call, per_event
from telegrinder.node.utils import as_node

__all__ = nodes_all + (
    "GLOBAL",
    "PER_CALL",
    "PER_EVENT",
    "as_node",
    "compose",
    "run_agent",
    "global_node",
    "per_call",
    "per_event",
)
