# Nodes

Nodes is one of super important telegrinder building blocks. They are like very easy to create and interconnect building pieces. That's why we call them nodes.

Node is something we compose from other nodes.

For example from message we can compose text, or user.

From text we can compose integer, if the given text consists of digits.

There are root objects that are used to compose everything else, in classic telegrinder bot it is an instance of `Update`, `API` and `Context`.

`Update` is what we received into our bot. It is always bound to some `API`. And `Context` is just a useful storage, a low-level object where all the information about the event-processing path is actually stored.

---

At this point you probably have already grasped the simple idea that inspired nodes. Let's dive into the details on how to implement one.

In telegrinder we just have to write a class which implements `compose` classmethod. Compose method must return the instance of the node. And, what is of importance, it can accept any other nodes as arguments. They will be automatically bound to the node and altogether resolved in a quite optimized way when time for that comes.

There are multiple types of nodes in telegrinder:

* Scalar node - the node that is strives to just write a composition method for a value of another type. For example, node `Text` is a scalar node. Is is a `str`. And with some inner magic of telegrinder `Text` and `str` are interrecognizible by type-checkers.

* Data node - a node that is a dataclass. Just a combination that is often useful

* Polymorphic node - a node that has multiple implementations. For example, both message and callback query events have a sender, we can provide separate implementations on how to get a user from each type of event and thats it - we get a single polyporphic node which we can use very conveniently to extract user from different event types

* Any node - just any class that implements compose method. If one implements `compose` - it is a node.

---

Lets learn how to write nodes by example:

```python
# telegrinder.node.text
from telegrinder.node import scalar_node

@scalar_node
class Text:
    @classmethod
    def compose(cls, message: Message) -> str:
        if not message.text:
            raise ComposeError("Message has no text.")
        return message.text.unwrap()
```


What is going on in this piece of code?

We declare that there will be an implementation of a scalar node `Text`. It magically tells that the scalar value of `Text` will be `str` from the compose response type hint (`-> str`).

`compose` must return a string of text or raise a compose error.

Now it's ready to use!

```python
@bot.on.message()
async def text_message_handler(message: Message, text: Text):
    await message.answer(text.lower())
```

The exact same echo bot we made at the start of the tutorial, but so much nicer.

What about rules? Time for a great reveal, it works everywhere, rules included:

```python
class TextIsOfLength(ABCRule):
    def __init__(self, l: int):
        self.l = l

    async def check(self, text: Text) -> bool:
        return len(text) == self.l


@bot.on.message(TextIsOfLength(6))
async def six_handler():
    return "Love messages of this length.."
```

---

Great, now as we know some basics we can write some more nodes:

```python
@scalar_node
class TextInteger:
    @classmethod
    def compose(cls, text: Text) -> int:
        if not text.isdigit():
            raise ComposeError("Text is not digit.")
        return int(text)
```

Some chain is going on, huh?

We just made a new node that composes the node we created just before. `TextInteger` works with messages that contain text, where text is made of digits.

```python
pi = 3.141592653589793238

@bot.on.message()
async def number_handler(r: TextInteger):
    return f"Thats awesome! So if R = {r}, C = {2 * pi * r}"
```

## Scopes

As soon our nodes get a bit of compicated logic, like wrapping a database connection into a node, or some turning storage into a node we might need to control scope of the node. That is simple. In telegrinder we have 3 scopes:

* Per event - the node is composed per event, so if during the composition the node was already composed, it will be reused and won't be composed twice. IS DEFAULT BEHAVIOUR

* Per call - the node will be compose each time any node will require it to build itself or if we require it to be delivered into the handler

* Global - some nodes may need to be composed only once during runtime, and later be stored and reused when needed

Lets look at some node examples for each custom scope type.

Database connections may be handled gracefully using nodes:

```python
from telegrinder.node import scalar_node, per_call

@scalar_node
@per_call
class DB:
    @classmethod
    async def compose(cls) -> typing.AsyncGenerator[aiosqlite.Connection, None]:
        connection = await aiosqlite.connect("test.db")
        logger.info("Opening connection")
        yield connection
        logger.info("Closing connection")
        await connection.close()

@bot.on.message()
async def some_handler(text: Text, connection: DB):
    ...
```

Here we also used an awesome quality of nodes to work as a generator. We may finalize something after event processing is already done, just use `yield` keyboard to yield control over the value to the processor and after processing the control will be yielded back to you to close a database connection (for example).

```python
from telegrinder.node import DataNode, global_node

@global_node
class Settings(DataNode):
    api_url: str
    some_secret: str

    @classmethod
    def compose(cls) -> "Settings":
        return cls(api_url=env["API_URL"], some_secret=env["SOME_SECRET"])


@scalar_node
@global_node
class Secret:
    @classmethod
    def compose(cls) -> str:
        return generate_secret(16)
```

Have fun with nodes!

[>> Next: Dispatch](6_dispatch.md)
