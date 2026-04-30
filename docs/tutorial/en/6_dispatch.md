# Dispatch

`Dispatch` is telegrinder's event routing layer. If nodes are about dependencies, dispatch is about where an event goes and which handlers get a chance to process it.

It used to be enough to think about dispatch as a container with `message`, `callback_query`, and other views. That is still true, but now there is one more important layer: routers live inside dispatch.

## What Dispatch contains

A dispatch has several core parts:

- `main_router`
- `routers`, the queue of loaded routers
- views such as `message`, `callback_query`, `inline_query`, `media_group`, `event_error`, `raw`
- `middlewares`
- `error_handler`
- loading helpers: `load`, `load_many`, `load_from_dir`

When you write:

```python
@bot.on.message(...)
async def handler(...): ...
```

you are really registering a handler on the `message` view of `bot.on.main_router`.

Conceptually:

- `bot.on` is a `Dispatch`
- `bot.on.message` is `bot.on.main_router.message`
- `bot.on.callback_query` is `bot.on.main_router.callback_query`

---

## What Router is

`Router` stores a set of views and knows how to try processing a single update.

The flow is:

1. `Dispatch.feed()` receives `API` and `Update`
2. dispatch creates `Context` and runs middleware
3. dispatch iterates over its routers
4. each `Router` checks matching event views
5. the matching `View` runs its handlers
6. if something fails inside a router, `event_error` may process it

So dispatch does not route directly to plain functions. It routes through routers, and routers route through views.

---

## Views

A view is the object where you register handlers for a specific event type.

The most common ones are:

- `message`
- `callback_query`
- `inline_query`
- `media_group`
- `event_error`
- `raw`

Each view has:

- a view-level filter
- a list of handlers
- a waiter machine
- view-level middleware

That is the right mental model: routers hold views, views hold handlers.

---

## A basic dispatch

```python
from telegrinder import Dispatch, Message
from telegrinder.rules import Argument, Command, IsBot

dp = Dispatch(name="chat-utilities")


@dp.message(IsBot())
async def bot_message_handler(message: Message) -> None:
    await message.answer("Hey bot!")


@dp.message(
    Command(
        "repeat",
        Argument("text"),
        Argument("times", validators=[lambda s: int(s) if s.isdigit() else None], optional=True),
    )
)
async def command_handler(message: Message, text: str, times: int = 5) -> None:
    await message.answer(", ".join([text] * times))
```

This is already a standalone dispatch unit that can be plugged into the main bot.

---

## Loading a dispatch into the bot

Assume the code above lives in `handlers/chat_utilities.py`. Then the main bot can assemble everything like this:

```python
from handlers import chat_utilities
from telegrinder import API, Telegrinder, Token

api = API(Token("your-token-here"))
bot = Telegrinder(api)

bot.on.load(chat_utilities.dp)
bot.run_forever()
```

`load()` does not copy source code or import handlers one by one. It appends routers from the external dispatch into the current dispatch router queue and merges error views as well.

---

## When to use Router explicitly

If you want stronger separation between logical areas, create routers directly:

```python
from telegrinder import Dispatch, Message, Router
from telegrinder.rules import Text

admin_router = Router(name="admin")


@admin_router.message(Text("/ban"))
async def ban_handler(message: Message) -> None:
    await message.answer("Admin action")


admin = Dispatch(router=admin_router, name="admin-dispatch")
```

Then you can load `admin` through `bot.on.load(admin)`.

This is useful when you want clearly named routing groups like `admin`, `payments`, `moderation`, or `games`.

---

## load_many and load_from_dir

When the project grows, two helpers become convenient.

### Load several dispatches at once

```python
bot.on.load_many(users.dp, payments.dp, admin.dp)
```

### Load dispatches from a directory

```python
bot.on.load_from_dir("handlers", recursive=True)
```

`load_from_dir()` imports Python modules from the directory, looks for global variables that are `Dispatch` instances, and loads them.

There is a working example in [examples/blueprint_bot/__main__.py](https://github.com/timoniq/telegrinder/blob/dev/examples/blueprint_bot/__main__.py).

---

## A practical project layout

A useful minimal structure is:

- `bot.py` or `main.py` for app assembly
- `handlers/` for domain dispatches
- `keyboards/` for keyboards
- `rules/` for custom rules
- `nodes/` for custom nodes

For example:

```text
mybot/
  bot.py
  handlers/
    start.py
    admin.py
    payments.py
  keyboards/
    menu.py
  nodes/
    db.py
  rules/
    is_admin.py
```

That scales much better than one large file full of handlers.

---

## What to remember

- `Dispatch` routes events
- routers are now an important part of that structure
- views belong to routers, handlers belong to views
- `bot.on.message(...)` registers on `main_router.message`
- `load`, `load_many`, and `load_from_dir` are how you assemble multi-file bots

[>> Next: Keyboard, payload handling](7_keyboard.md)
