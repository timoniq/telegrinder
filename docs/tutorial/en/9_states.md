# States: waiters, long states

This is one of the most important sections for real bots.

Almost every bot eventually runs into situations like these:

- the user starts a flow but does not finish it in one message
- the bot is waiting for the next reply
- the user has a current "mode"
- the interface depends on previous actions

That is where state enters the picture.

Telegrinder gives you several levels of tools for it:

- `State(...)` plus storage for long-lived state
- waiter machine for short waits
- `choice` and `checkbox` for ready interactive steps
- `state_mutator` for a more structured and typed state model

In short:

- storage is "the user is currently in this state"
- a waiter is "I am waiting for the next step"
- state mutator is "I want state transitions to look like a real model"

## The simplest start: storage

If you are just starting, `MemoryStateStorage` is the easiest entry point.

```python
import enum

from telegrinder import MemoryStateStorage, Message, StateData
from telegrinder.rules import StateMeta, Text

states = MemoryStateStorage()


class StateEnum(enum.StrEnum):
    CURSED = "cursed"
    BLESSED = "blessed"


@bot.on.message(
    Text("/curse"),
    # /curse is allowed if the user is blessed
    # or if they do not have any state yet.
    states.State(StateEnum.BLESSED) | states.State(StateMeta.NO_STATE),
)
async def curse_handler(message: Message) -> None:
    await states.set(message.from_user.id, StateEnum.CURSED, {})
    await message.answer("You are now cursed.")


@bot.on.message(Text("/bless"), states.State(StateMeta.NO_STATE))
async def bless_handler(message: Message) -> None:
    await states.set(message.from_user.id, StateEnum.BLESSED, {})
    await message.answer("You are now blessed.")


@bot.on.message()
async def any_message_handler(message: Message) -> None:
    state = await states.get(message.from_user.id)
    vibe = state.unwrap_or(StateData("normal", {})).key
    await message.answer(f"You are currently {vibe}.")
```

### What matters here

Storage keeps `StateData`, which contains:

- `key`, the state name
- `payload`, extra state data

You can check state through rules:

```python
states.State(StateEnum.CURSED)
states.State(StateMeta.NO_STATE)
states.State(StateMeta.ANY)
```

This already solves a lot of practical bot problems.

For example:

- the user is currently in a checkout flow
- the user is in onboarding
- the user is already authorized
- the user is editing profile data

> [!TIP]
> Life hack:
> If all you need is "remember the user's current mode", do not jump to `state_mutator` too early. Plain storage is simpler and often enough.

---

## Reading, writing, and deleting state

The most common three operations are:

- `set(...)`
- `get(...)`
- `delete(...)`

```python
await states.set(user_id, StateEnum.BLESSED, {"source": "admin"})
state = await states.get(user_id)
await states.delete(user_id)
```

`MemoryStateStorage` is good for:

- local development
- tests
- small bots

But it does not survive process restarts.

If state needs to live longer, people usually implement `ABCStateStorage` on top of Redis, a database, or some other external storage.

> [!TIP]
> If state disappears after a restart and that breaks the UX, it is probably time to move from `MemoryStateStorage` to external storage.

---

## When storage is the best fit

Storage is especially good when the state behaves like a mode or flag:

- the user is in a wizard
- the user is blocked
- the user selected a language
- the user is on step 3 of 5

If you mostly want to check state before a handler runs, storage is often the clearest solution.

---

## Waiters: when the bot is waiting for the next step

Not every situation needs long-lived state.

Sometimes the bot is doing something much simpler:

- ask a question
- wait for one next reply
- continue the flow

That is what waiter machine is for.

It is already built into dispatch and views, so you usually do not need to wire it up manually.

Practically, it gives you the ability to:

- wait for the next message
- wait for an inline button press
- limit waiting time
- apply filters to what counts as a valid next step

This is very useful for short funnels and interactive steps.

---

## Ready-made `Choice` and `Checkbox`

Very often, you do not need to build a waiter manually at all.

### `Choice`

This is a good fit when the user should end up with exactly one selected option.

```python
@bot.on.message(Text("/choice"))
async def action(message: Message) -> None:
    chosen, message_id = await (
        bot.dispatch.choice(message.chat.id, message="Choose something", max_in_row=1)
        # First text is the normal option, second text is the selected version.
        .add_option("apple", "Apple 🔴", "Apple 🟢")
        .add_option("banana", "Banana 🔴", "Banana 🟢", is_picked=True)
        .add_option("pear", "Pear 🔴", "Pear 🟢")
        .wait(message.api)
    )

    await message.edit(
        text=f"You chose: {chosen}",
        message_id=message_id,
    )
```

### `Checkbox`

This is for multi-select flows.

```python
@bot.on.message(Text("/checkbox"))
async def action(message: Message) -> None:
    picked, message_id = await (
        bot.dispatch.checkbox(
            message.chat_id,
            message="Check your checkbox",
            cancel_text="Cancel",
            max_in_row=2,
        )
        .add_option("apple", "Apple", "Apple 🍏")
        .add_option("banana", "Banana", "Banana 🍌", is_picked=True)
        .add_option("pear", "Pear", "Pear 🍐")
        .wait(message.api)
    )

    await message.edit(
        text="You picked: {}".format(", ".join(key for key, value in picked.items() if value)),
        chat_id=message.chat.id,
        message_id=message_id,
    )
```

This is a very friendly path for beginners:

- no need to manually design callback flow
- no need to keep keyboard state by hand
- no need to manage a short-lived step state yourself

---

## Where `state_mutator` fits

This is where things move to the next level.

If storage answers:

"what is the user's current state?"

then `state_mutator` answers:

"what does the state model itself look like, and how do transitions work?"

This becomes useful when you do not just have "one string in storage", but a real state machine with meaningful transitions.

Examples:

- player: `Stopped -> Playing -> Paused`
- game character: `Alive -> Dead -> Alive`
- order: `Draft -> WaitingPayment -> Paid -> Shipped`

In those cases, `state_mutator` makes the model much nicer and safer.

---

## A first `state_mutator` model

Let us start with a friendly "alive / dead" example.

```python
import dataclasses
import datetime

from telegrinder.tools.state_mutator import State, StateMutator, mutation


@dataclasses.dataclass
class AliveState(State):
    __description__ = "alive"

    # State can store useful data directly.
    since: datetime.datetime = dataclasses.field(default_factory=datetime.datetime.now)

    @mutation
    def die(self, reason: str) -> "DeadState":
        # Alive -> Dead transition
        return DeadState(reason)


@dataclasses.dataclass
class DeadState(State):
    reason: str

    @mutation
    def resurrect(self) -> "AliveState":
        # Dead -> Alive transition
        return AliveState()

    @property
    def __description__(self) -> str:
        return f"dead because of {self.reason}"
```

You can already see the important part:

- state is described as a class
- transitions are described as methods with `@mutation`
- the return type shows which state comes next

So the code starts reading like a real domain model.

---

## Using `StateMutator` in handlers

Here is how that looks in bot code:

```python
@bot.on.message(Text("/die"))
async def die_handler(alive: AliveState) -> str:
    # If this handler ran, the current state is already AliveState.
    new_state = await alive.die("sadness")
    return f"You are now {new_state.__description__}"


@bot.on.message(Text("/resurrect"))
async def resurrect_handler(dead: DeadState) -> str:
    await dead.resurrect()
    return "You resurrected"


@bot.on.message()
async def in_state_handler(state: AliveState | DeadState) -> str:
    # You can accept a union if several states are valid here.
    return f"You are currently {state.__description__}"
```

What feels especially good here:

- if a handler takes `alive: AliveState`, it only runs when that is really the current state
- transitions are called like methods on the current state object
- the code becomes close to the language of the problem domain

> [!TIP]
> Life hack:
> If you keep writing many branches like `if current_state == "...": ... elif current_state == "...": ...`, that is often a sign to consider `state_mutator`.

---

## Initial state and "external" mutations

A mutation does not have to be a method on a state class.

```python
from telegrinder.tools.state_mutator import mutation


be_born = mutation(AliveState)


@mutation
def login_as_ghost(silently: bool = False):
    if not silently:
        print("Ghost just logged in ~*_*~")
    return DeadState(reason="~*being a ghost*~")
```

This is useful when a transition:

- does not belong to one specific state
- acts as an entry point into a flow
- should be triggered from outside the current state object

Usage:

```python
@bot.on.message(Text("/be_born"))
async def be_born_handler(mutator: StateMutator) -> str:
    await be_born(mutator)
    return "You were born"


@bot.on.message(Text("Gh0$T_рa$$w0rd"))
async def ghost_handler(mutator: StateMutator) -> str:
    await login_as_ghost(mutator, silently=True)
    return "You are now a ghost"
```

Here `StateMutator` acts like the object that can apply a transition to the current user state.

---

## A more practical example: a mini player

Now let us look at something closer to a real model.

```python
import datetime
from dataclasses import dataclass

from telegrinder.tools.state_mutator import State, mutation


@dataclass
class Stopped(State):
    @mutation
    def play(self, song: str, offset: datetime.timedelta = datetime.timedelta(0)) -> "Playing":
        return Playing(song, offset, datetime.datetime.now())


@dataclass
class Playing(State):
    song: str
    offset: datetime.timedelta
    started_at: datetime.datetime

    @mutation
    def stop(self) -> "Stopped":
        return Stopped()

    @mutation
    def pause(self) -> "Paused":
        offset = datetime.datetime.now() - self.started_at
        return Paused(song=self.song, offset=offset + self.offset, stopped_at=datetime.datetime.now())


@dataclass
class Paused(State):
    song: str
    offset: datetime.timedelta
    stopped_at: datetime.datetime

    @mutation
    def stop(self) -> "Stopped":
        return Stopped()

    @mutation
    def play(self) -> "Playing":
        return Playing(self.song, self.offset, datetime.datetime.now())
```

And now the handlers:

```python
@bot.on.message(Command("play", Argument("song_name", optional=True)))
async def play_song_handler(state: Stopped | Paused | Playing, song_name: str | None = None) -> str:
    match state:
        case Stopped():
            if song_name is None:
                return "You need to provide a song name"

            await state.play(song_name)
            return f"Started {song_name}"

        case Paused():
            await state.play()
            return f"Continuing {state.song}"

        case Playing():
            return "Already playing"
```

Why this is nice:

- transitions are declared on the states themselves
- the logic becomes much easier to read
- fewer string comparisons
- types start helping for real

For more complex bots this is much nicer than manually storing strings like `"playing"` and `"paused"` and then untangling everything later.

---

## When `state_mutator` is worth it

It is especially useful when:

- there are several states with clear transitions
- the state itself carries useful data
- you want the code to read like a model of the process
- plain storage is starting to turn into a large `if/elif` grid

If you only have simple states like `"waiting_for_name"` and `"waiting_for_email"`, storage may still be simpler.

---

## How to choose the right tool

A very practical rule:

- if you only need a user mode or flag, use storage
- if the bot is waiting for the very next answer, use a waiter
- if you want quick UX with inline buttons, use `choice` or `checkbox`
- if you have a real state machine with transitions, look at `state_mutator`

You do not have to use all of them at once.

It is perfectly normal to start with storage and only move to `state_mutator` when the simpler approach genuinely stops being enough.

---

## What to remember

- telegrinder has several levels of state tools
- `MemoryStateStorage` is the easiest entry point
- waiter machine is great for short interactive steps
- `choice` and `checkbox` solve a lot of UX problems with very little manual work
- `state_mutator` is great when state is no longer "just a string", but a real transition model

[>> Next: Media](10_media.md)
