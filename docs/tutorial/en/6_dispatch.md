# Dispatch

If nodes help prepare data, `Dispatch` answers a different question: "where does this event go, and who gets to handle it?"

When the bot is small, you barely think about it. You have `@bot.on.message(...)`, you have a few handlers, everything feels simple. But once the project grows beyond one file, dispatch becomes a big deal.

## The shortest mental model

This model is enough to stay oriented:

- `Dispatch` collects routing
- inside it live `Router`
- inside routers live `View`
- inside views live handlers

So the path is roughly:

`Dispatch -> Router -> View -> Handler`

You do not need more than that to get started.

## What `bot.on` really is

When you write:

```python
@bot.on.message(...)
async def handler(...): ...
```

`bot.on` is the dispatch.

And `bot.on.message` is the message view of the main router inside that dispatch.

In other words:

- `bot.on` is your bot's main dispatch
- `bot.on.message` is where message handlers go
- `bot.on.callback_query` is where callback query handlers go

That understanding is more than enough for early projects.

---

## Why Dispatch exists at all

Because keeping the whole bot in one file becomes painful very quickly.

Almost every bot eventually grows into something like:

- separate handlers for start
- separate handlers for admin tools
- separate handlers for payments
- separate handlers for inline buttons

If all of that stays in one `bot.py`, the file becomes hard to navigate. Dispatch solves that by letting you split the bot into logical pieces and then assemble them together.

---

## A minimal dispatch

```python
from telegrinder import Dispatch, Message
from telegrinder.rules import Argument, Command, IsBot

dp = Dispatch(name="chat-utilities")


@dp.message(IsBot())
async def bot_message_handler(message: Message) -> None:
    # A normal handler, just registered in a local dispatch instead of bot.on.
    await message.answer("Hey bot!")


@dp.message(
    Command(
        "repeat",
        Argument("text"),
        Argument("times", validators=[lambda s: int(s) if s.isdigit() else None], optional=True),
    )
)
async def command_handler(message: Message, text: str, times: int = 5) -> None:
    # times will contain the parsed number or the default value.
    await message.answer(", ".join([text] * times))
```

That `dp` can already live in its own file and be plugged into the main bot later.

---

## Loading a dispatch into the bot

Suppose the code above lives in `handlers/chat_utilities.py`.

Then your main bot can look like this:

```python
from handlers import chat_utilities
from telegrinder import API, Telegrinder, Token

api = API(Token("your-token-here"))
bot = Telegrinder(api)

# Load routers and error handlers from the external dispatch.
bot.on.load(chat_utilities.dp)

bot.run_forever()
```

This is usually the moment when things start feeling much more maintainable: the bot can be assembled from pieces instead of being written as one giant script.

> [!TIP]
> Life hack:
> Even if the bot is still small, it is often worth splitting at least `start`, `admin`, and `callback_query` into separate files early.

---

## Where routers fit in

In the current telegrinder API, dispatch works through routers.

A dispatch has:

- `main_router`
- `routers`, the queue of loaded routers
- views such as `message`, `callback_query`, `inline_query`, `media_group`, `event_error`, `raw`

When you write:

```python
@bot.on.message(Text("/start"))
async def start(...): ...
```

you are effectively registering on:

```python
bot.on.main_router.message
```

So the main router is already there. In day-to-day bot code you just do not always need to touch it explicitly.

---

## What a View is

A view is an object for one specific kind of event.

The most common ones are:

- `message`
- `callback_query`
- `inline_query`
- `media_group`
- `event_error`
- `raw`

Each view contains:

- a view-level filter
- a list of handlers
- middleware
- a waiter machine

A beginner-friendly way to think about it is: a view is just a shelf where you put handlers of one event type.

---

## When using Router directly is helpful

Sometimes you want to separate a clear logical area. For example, an admin zone.

Then creating a router explicitly makes sense:

```python
from telegrinder import Dispatch, Message, Router
from telegrinder.rules import Text

admin_router = Router(name="admin")


@admin_router.message(Text("/ban"))
async def ban_handler(message: Message) -> None:
    # All admin-related logic can stay inside this router.
    await message.answer("Admin action")


admin = Dispatch(router=admin_router, name="admin-dispatch")
```

Then load it like any other dispatch:

```python
bot.on.load(admin)
```

This becomes very nice when the project has clear domains:

- admin
- payments
- onboarding
- games
- moderation

---

## `load_many` and `load_from_dir`

As the number of pieces grows, bot assembly can become even cleaner.

### Load several dispatches at once

```python
bot.on.load_many(users.dp, payments.dp, admin.dp)
```

This is useful when you already imported the modules yourself and just want to combine them in one place.

### Auto-load from a directory

```python
bot.on.load_from_dir("handlers", recursive=True)
```

Here telegrinder:

- walks over Python files
- imports them
- looks for global `Dispatch` instances
- loads them into the main dispatch

This is convenient for blueprint-style project layouts.

Minimal idea:

```python
# handlers/start.py
from telegrinder import Dispatch

dp = Dispatch(name="start")
```

```python
# bot.py
bot.on.load_from_dir("handlers", recursive=True)
```

> [!TIP]
> `load_from_dir()` is great once your project structure is stable. Early on, many people find `load_many(...)` easier and more explicit.

---

## What happens when an event is processed

Without going too deep into internals, the flow is roughly:

1. `Dispatch.feed()` receives `API` and `Update`
2. a `Context` is created
3. dispatch-level middleware runs
4. dispatch iterates through its routers
5. each router checks matching views
6. the matching view runs handlers
7. if something fails, it can be processed by `event_error`

You do not need to memorize every detail. It is enough to understand that dispatch is not just "a list of functions", but a fairly structured pipeline.

---

## A practical project layout

Here is a very good minimal starting point:

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

This kind of layout scales much more calmly than one huge file with hundreds of lines.

---

## What to remember

- `Dispatch` is about routing and code separation
- routers live inside dispatch, and views live inside routers
- `bot.on.message(...)` is basically registration on `main_router.message`
- `load`, `load_many`, and `load_from_dir` help assemble multi-file bots
- if your bot starts growing, split it earlier rather than later

[>> Next: Keyboard, payload handling](7_keyboard.md)
