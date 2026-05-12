# Handling errors

Errors are unavoidable in bots: network failures, user input, external services, databases, and your own business logic. Telegrinder has a built-in exception routing path through `event_error`.

## Basic example

```python
from telegrinder import Message
from telegrinder.node import Error
from telegrinder.rules import IsUser, Text


@bot.on.message(Text("oops"))
async def oops_handler(message: Message) -> None:
    await message.answer("Oh no")
    raise RuntimeError("Wow")


@bot.on.message(Text("woops"))
def woops_handler() -> None:
    raise ValueError("Wow oopsii!")


@bot.on.event_error(IsUser())
async def error_handler(err: Error[RuntimeError, ValueError], message: Message) -> None:
    await message.answer(f"Something went wrong: {err.exception}")
```

What happens:

- a regular handler raises
- dispatch catches the exception
- the event is routed into `event_error`
- the error handler can receive an `Error[...]` node

---

## The Error node

`Error[...]` is a generic node. You can restrict it to specific exception types:

```python
err: Error[RuntimeError]
err: Error[ValueError, TypeError]
err: Error[Exception]
```

If the actual exception type does not match, the node will not compose and that handler will not be considered a match.

This is useful when you want separate handling for:

- business errors
- validation errors
- unexpected failures

---

## Where to catch exceptions

A practical approach is:

- catch expected errors locally when the user-facing response is specific to that case
- use `event_error` as a central safety net and logging point
- do not silently swallow exceptions if that hides diagnosis

If the error means “the user did something wrong”, the regular handler often remains the best place to reply. If the error is systemic, routing it into `event_error` is often cleaner.

---

## Error views at router and dispatch level

It is worth remembering that errors are handled inside the same dispatch/router model:

- routers have `event_error`
- dispatch has `error_handler`
- when you load several dispatches, error views are merged too

That keeps error handling part of the same architecture rather than a completely separate side channel.

---

## Useful references

- [examples/error_catching.py](https://github.com/timoniq/telegrinder/blob/dev/examples/error_catching.py)
- [examples/action.py](https://github.com/timoniq/telegrinder/blob/dev/examples/action.py)

[>> Next: Out-of-the-box scenarios](12_out-of-box_scenarios.md)
