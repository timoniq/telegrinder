# Checkbox

`Checkbox` is a built-in scenario for quick inline multi-choice flows. It sends a message with inline buttons, tracks button presses through the waiter machine, and returns the final selection as a dictionary.

This is useful for:

- short menus with multiple toggles
- setup wizards
- confirmation flows with several options
- lightweight conversational funnels

`Checkbox` is intentionally short-lived. It keeps the interaction inside a single scenario session and is not meant to replace persistent user state.

## Recommended usage

In real bots the most convenient entrypoint is usually the `Dispatch` shortcut:

```python
from telegrinder import API, Message, Telegrinder, Token, configure_dotenv, setup_logger
from telegrinder.rules import Text

configure_dotenv()
setup_logger()

api = API(token=Token.from_env())
bot = Telegrinder(api)


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


bot.run_forever()
```

Reference: [examples/checkbox.py](https://github.com/timoniq/telegrinder/blob/dev/examples/checkbox.py)

---

## What `wait()` returns

`wait()` returns:

- `dict[Key, bool]` with option states
- `message_id` of the scenario message

The dictionary preserves your option keys, so you can use strings, enums, or other hashable values as option identifiers.

## Adding options

Each option has:

- `key` used in the resulting dictionary
- `default_text` shown when the option is not picked
- `picked_text` shown when the option is picked
- optional `is_picked` initial state
- optional `icon_id`
- optional `style`

Example:

```python
checkbox = (
    bot.dispatch.checkbox(chat_id, message="Choose toppings")
    .add_option("cheese", "Cheese", "Cheese ✅")
    .add_option("bacon", "Bacon", "Bacon ✅", is_picked=True)
)
```

## Constructor parameters

The current `Checkbox` constructor accepts:

```python
Checkbox(
    chat_id: int,
    message: str,
    *,
    parse_mode: str | None = None,
    max_in_row: int = 3,
    callback_answer: str | None = None,
    callback_answer_as_alert: bool | None = None,
    ready_text: str = "Ready",
    ready_icon_id: str | int | None = None,
    ready_style: KeyboardButtonStyle | None = None,
    cancel_text: str | None = None,
    cancel_icon_id: str | int | None = None,
    cancel_style: KeyboardButtonStyle | None = None,
    waiter_machine: WaiterMachine | None = None,
)
```

The most commonly used arguments are:

- `message` for the text above the checkbox
- `max_in_row` for layout
- `ready_text` to customize the submit button
- `cancel_text` to add a cancel button
- `parse_mode` if the scenario message uses formatting

## Button styles

Checkbox buttons use regular `InlineButton` under the hood, so style-aware buttons are supported through the scenario parameters and option styles.

That means you can visually distinguish:

- the ready action
- the cancel action
- individual options

via `KeyboardButtonStyle` values.

## Direct construction

If you do not want to use `bot.dispatch.checkbox(...)`, you can instantiate the scenario directly:

```python
from telegrinder import Checkbox

checkbox = Checkbox(
    chat_id=message.chat_id,
    message="Pick your options",
    waiter_machine=bot.dispatch.callback_query.waiter_machine,
)
```

Then call `.add_option(...)` and `.wait(api)` the same way.

The important detail is that `Checkbox` needs a `WaiterMachine`. The dispatch shortcut already provides the correct one for you, which is why it is the recommended path.

## Cancellation behavior

If `cancel_text` is provided, the checkbox renders a separate cancel button.

When the cancel action is pressed:

- the internal option list is cleared
- the wait loop ends
- the returned dictionary is empty

That makes cancellation easy to distinguish from a normal completed selection.

## When to use Checkbox vs Choice

Use `Checkbox` when multiple items may be selected.

Use `Choice` when only one item should be selected at the end of the interaction.

Both scenarios are built on the same general mechanism, but `Choice` gives a more natural API for single-select flows.
