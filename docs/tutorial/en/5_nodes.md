# Nodes

Nodes are telegrinder's dependency injection building blocks. A node describes how to get one value from other values, and telegrinder can use that description in handlers, rules, and internal processing.

For example:

- from `Message` we can get `Text`
- from `Text` we can get `int`
- from `CallbackQuery` we can get `Payload`
- from `Source` we can get a user, chat, or their ids

That is the core idea: you describe dependencies declaratively and telegrinder builds the composition chain for you.

## Root values

During update processing a few root objects are already injected into the graph:

- `API`
- `Update`
- `Context`

Everything else can be composed from there.

There are many built-in nodes in `telegrinder.node`: `Text`, `TextInteger`, `Source`, `UserSource`, `ChatSource`, `ChatId`, `Payload`, `File`, `Photo`, `Caption`, `Error`, and more.

---

## Writing your own node

In the current API a node is defined through a class and a `__compose__` method.

```python
from nodnod import NodeError

from telegrinder import Message
from telegrinder.node import scalar_node


@scalar_node
class Text:
    @classmethod
    def __compose__(cls, message: Message) -> str:
        if not message.text:
            raise NodeError("Message has no text.")
        return message.text.unwrap()
```

Important details:

- `@scalar_node` declares a scalar node
- telegrinder takes dependencies from `__compose__` parameters
- if composition fails, raise `NodeError`
- the result type comes from the return annotation

Then the node is available in handlers like a regular argument:

```python
@bot.on.message()
async def text_message_handler(message: Message, text: Text) -> None:
    await message.answer(text.lower())
```

Nodes work in rules as well:

```python
from telegrinder.bot.rules import ABCRule


class TextIsOfLength(ABCRule):
    def __init__(self, length: int) -> None:
        self.length = length

    async def check(self, text: Text) -> bool:
        return len(text) == self.length


@bot.on.message(TextIsOfLength(6))
async def six_handler() -> str:
    return "I like messages of that length."
```

---

## Chaining nodes

The nice part is that nodes naturally compose from each other:

```python
from nodnod import NodeError

from telegrinder.node import scalar_node


@scalar_node
class TextInteger:
    @classmethod
    def __compose__(cls, text: Text) -> int:
        if not text.isdigit():
            raise NodeError("Text is not a digit.")
        return int(text)
```

Now handlers can just ask for the final value:

```python
@bot.on.message()
async def number_handler(message: Message, value: TextInteger) -> None:
    await message.answer(f"{value} + 3 = {value + 3}")
```

The chain is:

`Message -> Text -> TextInteger`

---

## Node shapes

In practice you will mostly meet these forms:

- `scalar_node` for a single typed value
- `DataNode` for dataclass-like containers
- `generic_node` for generic nodes
- `polymorphic` for nodes that can compose from different event types

For example, telegrinder's `Payload` node is polymorphic and can extract payload from multiple event types.

---

## Scopes

Nodes also have a lifetime. That matters when a node wraps expensive logic or a resource that must be cleaned up.

Telegrinder provides three scopes:

- `PER_EVENT` meaning once per update. This is the default.
- `PER_CALL` meaning compose every time someone asks for it.
- `GLOBAL` meaning compose once for the whole application.

### Per call

```python
import aiosqlite
import typing

from telegrinder.node import per_call, scalar_node


@per_call
@scalar_node
class DB:
    @classmethod
    async def __compose__(cls) -> typing.AsyncGenerator[aiosqlite.Connection, None]:
        connection = await aiosqlite.connect("test.db")
        yield connection
        await connection.close()
```

This also shows another useful feature: nodes may be generators. The value is yielded to the processor, and code after `yield` works as finalization.

### Global

```python
from telegrinder.node import DataNode, global_node, scalar_node


@global_node
class Settings(DataNode):
    api_url: str
    secret: str

    @classmethod
    def __compose__(cls) -> "Settings":
        return cls(
            api_url=env["API_URL"],
            secret=env["APP_SECRET"],
        )


@global_node
@scalar_node
class Secret:
    @classmethod
    def __compose__(cls) -> str:
        return generate_secret(16)
```

Global nodes are a good fit for configuration, clients, and rarely changing values.

---

## Practical example

Take a look at [examples/with_nodes.py](https://github.com/timoniq/telegrinder/blob/dev/examples/with_nodes.py).

It shows:

- custom rules receiving nodes as arguments
- built-in nodes in regular message handlers
- a reusable `DB` node
- nodes such as `Photo`, `File`, `ChatSource`, and `TextInteger`

That is usually where nodes stop looking magical and start looking practical.

---

## What to remember

- a node describes how to get one value from other values
- in the current API the main method is `__compose__`
- nodes work in both handlers and rules
- the default lifetime is per event
- complex dependency logic is usually better inside nodes than duplicated in handlers

[>> Next: Dispatch](6_dispatch.md)
