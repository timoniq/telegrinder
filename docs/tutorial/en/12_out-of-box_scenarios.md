# Out-of-the-box scenarios

Once the basic building blocks are clear, the next step is usually not “write more handlers”, but “assemble recurring bot flows from reusable parts”. Telegrinder already provides quite a few of those patterns.

This page is not a full API index. It is a short map of the ready-made pieces worth remembering first.

## Menus and selection

If you need to build menus quickly:

- use static `Keyboard` and `InlineKeyboard`
- keep them in dedicated modules
- use `choice` for single selection
- use `checkbox` for multiple selection

That covers a large part of normal bot UX without hand-writing a callback state machine.

---

## Project separation

When the bot grows:

- split code into multiple `Dispatch` instances
- group views with `Router`
- assemble the app through `load_many` or `load_from_dir`

This is one of the most useful out-of-the-box scenarios because it affects maintainability more than any single helper does.

---

## Dialogs and states

For dialog flows you have several abstraction levels:

- `State` plus storage for long-lived state
- waiter machine for short waits
- `choice` and `checkbox` as ready interactive flows
- `state_mutator` for more controlled, complex state logic

If you are not sure where to start, start with the simplest thing:

- storage for “the current user mode”
- a waiter for “I need the next answer”

---

## Payload models

For inline menus and action buttons, typed payload models are usually much better than string concatenation:

- they are typed
- they are easier to extend
- they work naturally with `PayloadModelRule`

This matters a lot in stores, admin panels, pagination, and multi-step menus.

---

## Media and attachments

Telegrinder already gives you comfortable primitives for:

- reply shortcuts on cute types
- attachment nodes
- `File[...]`
- `MediaGroup`

Because of that, a lot of media logic can stay at the level of “what do I want to receive” instead of “how do I parse the raw update shape”.

---

## What to look at next

If you want to see real usage quickly, start with these examples:

- [examples/blueprint_bot](https://github.com/timoniq/telegrinder/tree/dev/examples/blueprint_bot)
- [examples/with_nodes.py](https://github.com/timoniq/telegrinder/blob/dev/examples/with_nodes.py)
- [examples/keyboard.py](https://github.com/timoniq/telegrinder/blob/dev/examples/keyboard.py)
- [examples/inline_keyboard.py](https://github.com/timoniq/telegrinder/blob/dev/examples/inline_keyboard.py)
- [examples/state_mutator.py](https://github.com/timoniq/telegrinder/blob/dev/examples/state_mutator.py)
- [examples/webhook_bot](https://github.com/timoniq/telegrinder/tree/dev/examples/webhook_bot)

That completes the base tutorial. From here it usually makes sense to read examples and API docs in parallel with your actual bot task.
