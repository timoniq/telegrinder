# States: waiters, long states

As soon as a bot starts having multi-step dialogues, state appears:

- the user already chose something
- the bot is waiting for the next reply
- the next step depends on the previous one

Telegrinder gives you two main tools for that:

- state storage and `State(...)` rules for long-lived state
- waiter machine for short interactive waits

## Long-lived state with storage

The simplest starting point is `MemoryStateStorage`.

```python
import enum

from telegrinder import MemoryStateStorage, Message
from telegrinder.rules import StateMeta, Text

states = MemoryStateStorage()


class StateEnum(enum.StrEnum):
    CURSED = "cursed"
    BLESSED = "blessed"


@bot.on.message(
    Text("/curse"),
    states.State(StateEnum.BLESSED) | states.State(StateMeta.NO_STATE),
)
async def curse_handler(message: Message) -> None:
    await states.set(message.from_user.id, StateEnum.CURSED, {})
    await message.answer("You are now cursed.")
```

Storage keeps `StateData`, which contains:

- `key`, the current state name
- `payload`, extra state data

You can check state through rules:

```python
states.State(StateEnum.CURSED)
states.State(StateMeta.NO_STATE)
states.State(StateMeta.ANY)
```

---

## Reading and mutating state

```python
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

State can be:

- written with `set(...)`
- read with `get(...)`
- removed with `delete(...)`

`MemoryStateStorage` is good for local development and simple cases. In production you will often want your own `ABCStateStorage` implementation backed by Redis, a database, or some other external store.

---

## Short-lived state with waiters

Not every state needs to survive for long. Sometimes the bot just needs the next message, the next callback query, or a confirmation action.

That is what waiter machine is for. It is already integrated into dispatch and views.

Practically, that means you can:

- wait for the next user message
- wait for callback queries
- attach filters, release conditions, and lifetimes

Several higher-level telegrinder scenarios are built on top of this.

---

## Ready-made Choice and Checkbox flows

If you need an interactive selection, you usually do not have to build a waiter manually.

### Choice

```python
@bot.on.message(Text("/choice"))
async def action(message: Message) -> None:
    chosen, message_id = await (
        bot.dispatch.choice(message.chat.id, message="Choose something", max_in_row=1)
        .add_option("apple", "Apple 🔴", "Apple 🟢")
        .add_option("banana", "Banana 🔴", "Banana 🟢", is_picked=True)
        .wait(message.api)
    )
    await message.edit(text=f"You chose: {chosen}", message_id=message_id)
```

### Checkbox

```python
@bot.on.message(Text("/checkbox"))
async def action(message: Message) -> None:
    picked, message_id = await (
        bot.dispatch.checkbox(message.chat_id, message="Check your checkbox", cancel_text="Cancel", max_in_row=2)
        .add_option("apple", "Apple", "Apple 🍏")
        .add_option("banana", "Banana", "Banana 🍌", is_picked=True)
        .wait(message.api)
    )
    await message.edit(text=str(picked), chat_id=message.chat.id, message_id=message_id)
```

These are very useful when you want decent UX without implementing your own callback flow from scratch.

---

## What to choose

A practical rule of thumb:

- if the state must outlive one event or survive restarts, use storage
- if you only need a short interaction inside one flow, use a waiter
- if the interaction is a standard button choice, start with `choice` or `checkbox`

---

## Useful references

- [examples/long_states.py](https://github.com/timoniq/telegrinder/blob/dev/examples/long_states.py)
- [examples/choice.py](https://github.com/timoniq/telegrinder/blob/dev/examples/choice.py)
- [examples/checkbox.py](https://github.com/timoniq/telegrinder/blob/dev/examples/checkbox.py)
- [examples/state_mutator.py](https://github.com/timoniq/telegrinder/blob/dev/examples/state_mutator.py)
- [examples/state_mutator_player.py](https://github.com/timoniq/telegrinder/blob/dev/examples/state_mutator_player.py)

[>> Next: Media](10_media.md)
