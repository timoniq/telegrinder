# Nodes

If you want the short version, nodes in telegrinder are a way to stop repeating the same preparation logic in every handler.

Instead of thinking like this:

- "first get text from the message"
- "then try to convert it to an integer"
- "then get the user"

you can think like this:

- "I need `Text` here"
- "I need `TextInteger` here"
- "I need `UserSource` here"

and telegrinder figures out how to build those values.

## First intuition

A node is just a description of how one value can be obtained from other values.

For example:

- from `Message` we can get `Text`
- from `Text` we can get `int`
- from `CallbackQuery` we can get `Payload`
- from `Source` we can get a user or a chat

A good beginner rule of thumb:

if you keep repeating the same data preparation code in handlers, that is probably a candidate for a node.

## What telegrinder already gives you

During update processing these root objects are already available:

- `API`
- `Update`
- `Context`

Everything else can be composed from there.

There are already many built-in nodes:

- `Text`
- `TextInteger`
- `Source`
- `UserSource`
- `ChatSource`
- `ChatId`
- `Payload`
- `File`
- `Photo`
- `Caption`
- `Error`

So on day one you often do not need to write your own nodes at all.

> [!TIP]
> Before creating a custom node, check `telegrinder.node`. There is a good chance the one you need already exists.

---

## Your first custom node

A node is defined as a class with a `__compose__` method.

```python
from nodnod import NodeError

from telegrinder import Message
from telegrinder.node import scalar_node


@scalar_node
class Text:
    @classmethod
    def __compose__(cls, message: Message) -> str:
        # If the message has no text, this node cannot be composed.
        if not message.text:
            raise NodeError("Message has no text.")

        # unwrap() is safe here because we already checked the condition above.
        return message.text.unwrap()
```

What is happening here:

- `@scalar_node` tells telegrinder this is a scalar node
- `message: Message` means the node needs a `Message`
- `-> str` means the final result is a string
- `NodeError` means "this node cannot be built right now"

Then you use it as a normal handler argument:

```python
@bot.on.message()
async def text_message_handler(message: Message, text: Text) -> None:
    # The handler receives ready-to-use text.
    await message.answer(text.lower())
```

That is usually the moment when nodes start feeling nice: the handler becomes about what to do, not how to obtain the inputs.

---

## Nodes also work in rules

This is one of the nicest parts.

```python
from telegrinder.bot.rules import ABCRule


class TextIsOfLength(ABCRule):
    def __init__(self, length: int) -> None:
        self.length = length

    async def check(self, text: Text) -> bool:
        # The rule receives a ready Text node.
        return len(text) == self.length


@bot.on.message(TextIsOfLength(6))
async def six_handler() -> str:
    return "I like messages of that length."
```

So nodes are not only useful in handlers. They are also great for keeping custom rules clean.

> [!TIP]
> Life hack:
> If a rule keeps digging into `message.text`, `message.from_user`, `callback_query.data`, and so on, it is often cleaner to move that part into a node first.

---

## Node chains

This is where things start feeling powerful.

```python
from nodnod import NodeError

from telegrinder.node import scalar_node


@scalar_node
class TextInteger:
    @classmethod
    def __compose__(cls, text: Text) -> int:
        # This node depends on an already composed Text node.
        if not text.isdigit():
            raise NodeError("Text is not a digit.")

        return int(text)
```

Now your handler can simply ask for the final value:

```python
@bot.on.message()
async def number_handler(message: Message, value: TextInteger) -> None:
    await message.answer(f"{value} + 3 = {value + 3}")
```

Internally the chain is:

`Message -> Text -> TextInteger`

That is the real benefit of nodes.

The handler does not care how the integer appeared. It just works with an integer.

---

## A slightly more practical example

Suppose you often need the incoming message id.

```python
from nodnod.interface.scalar import scalar_node

from telegrinder import Message

MessageId = type("MessageId", (int,), {})


@scalar_node
class IncomingMessageId:
    @classmethod
    def __compose__(cls, message: Message) -> MessageId:
        # Tiny wrapper types can make code more expressive.
        return MessageId(message.message_id)


@bot.on.message()
async def show_id(message: Message, message_id: IncomingMessageId) -> None:
    await message.answer(f"Your message id is {message_id}")
```

At first this can look a bit abstract, but on larger bots these tiny nodes are very good at removing duplication.

---

## Common node shapes

In practice you will mostly see:

- `scalar_node` for one typed value
- `DataNode` for dataclass-style containers
- `generic_node` for generic nodes
- `polymorphic` for nodes that can be built from multiple event types

For example, telegrinder's `Payload` node is polymorphic. It can extract payload not only from `CallbackQuery`, but from other relevant events too.

For most beginner use cases, `scalar_node` is enough.

---

## Lifetimes

Sometimes the important question is not only "how do I build this node?" but also "how long should it live?"

Telegrinder has three scopes:

- `PER_EVENT` for one update, this is the default
- `PER_CALL` for a fresh value every time
- `GLOBAL` for one value for the whole application

### PER_EVENT

This is the default.

If the same node is needed twice during one update, telegrinder does not rebuild it from scratch.

That is usually what you want.

### PER_CALL

Useful when you want a fresh object every time.

```python
import aiosqlite
import typing

from telegrinder.node import per_call, scalar_node


@per_call
@scalar_node
class DB:
    @classmethod
    async def __compose__(cls) -> typing.AsyncGenerator[aiosqlite.Connection, None]:
        # Create the resource before use.
        connection = await aiosqlite.connect("test.db")

        # Yield it to the handler or another node.
        yield connection

        # Cleanup happens after processing is done.
        await connection.close()
```

This also shows another very nice feature: a node may be a generator.

That means a node can:

- prepare a resource
- yield it for processing
- clean it up afterwards

> [!TIP]
> Life hack:
> If you have an "open / use / close" resource like a DB connection, session, or temporary file, a generator node is often the cleanest solution.

### GLOBAL

Global nodes are good for configuration, clients, and values that almost never change.

```python
from telegrinder.node import DataNode, global_node, scalar_node


@global_node
class Settings(DataNode):
    api_url: str
    secret: str

    @classmethod
    def __compose__(cls) -> "Settings":
        # No need to rebuild this on every update.
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

---

## When you do not need a node

This matters too.

You probably do not need a node if:

- the logic is used only once
- the code is already short and obvious
- you are hiding too much simple logic behind "magic wrappers"

The healthy balance is important. Nodes are there to simplify code, not to make it mysterious.

---

## What to remember

- a node is a way to describe how one value is obtained from another
- the main method in the current API is `__compose__`
- nodes work in both handlers and rules
- the default lifetime is per event
- if you repeat the same preparation code often, try turning it into a node

[>> Next: Dispatch](6_dispatch.md)
