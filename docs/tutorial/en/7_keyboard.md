# Keyboard, payload handling

Keyboards are usually the first thing that makes a bot feel friendlier.

Without keyboards, a bot often feels like this:

- the user has to remember commands
- the user has to type choices manually
- you keep checking raw text by hand

With keyboards, the interaction becomes much nicer.

Telegrinder has two main keyboard types:

- regular `Keyboard`
- inline `InlineKeyboard`

## Regular keyboard

This is the keyboard that replaces the user's system keyboard inside Telegram.

A very small example:

```python
from telegrinder.tools import Button, Keyboard

keyboard = (
    Keyboard()
    .add(Button("1"))
    .add(Button("2"))
    .row()
    .add(Button("3"))
)
```

What is happening here:

- `Keyboard()` creates the keyboard object
- `.add(...)` adds a button to the current row
- `.row()` starts a new row

Send it like this:

```python
@bot.on.message(Text("/keyboard"))
async def handle_keyboard_command(message: Message) -> None:
    await message.answer(
        "Here is your keyboard",
        reply_markup=keyboard.get_markup(),
    )
```

`get_markup()` converts the telegrinder keyboard object into the Telegram API markup object.

---

## Handling a regular button press

For a regular keyboard, pressing a button is just a new incoming message.

So the simplest handler is usually a `Text(...)` rule:

```python
@bot.on.message(Text("1"))
async def handle_press_button(message: Message) -> None:
    await message.answer("You pressed button 1")
```

That makes regular keyboards a very nice starting point, because you do not have to think about callback data yet.

> [!TIP]
> If the bot is still simple, regular keyboards are often easier than inline ones. Especially for menus with just a few actions.

---

## Static keyboards

When a keyboard is reused often and does not change much, defining it as a class is usually cleaner.

```python
from telegrinder.tools.keyboard import Button, Keyboard


class FruitsKeyboard(Keyboard, max_in_row=2, one_time_keyboard=True):
    APPLE = Button("Apple")
    BANANA = Button("Banana")
    KIWI = Button("Kiwi")
```

Why this feels nice:

- the keyboard is described in one place
- you do not rebuild it in every handler
- buttons can also be used as rules

Sending it:

```python
@bot.on.message(Text("/eat"))
async def eat(message: Message) -> None:
    await message.answer(
        "What do you want to eat?",
        reply_markup=FruitsKeyboard.get_markup(),
    )
```

And now the fun part:

```python
@bot.on.message(FruitsKeyboard.APPLE)
async def eat_apple(message: Message) -> None:
    await message.answer(
        "Good choice",
        reply_markup=FruitsKeyboard.get_keyboard_remove(),
    )
```

Here `FruitsKeyboard.APPLE` acts both as a button and as a rule.

That is a very pleasant pattern for menus.

> [!TIP]
> If the same keyboard is used in more than one place, it is usually worth turning it into a class.

---

## Button styles

Telegrinder also has styled buttons:

- `DangerButton` and `DangerInlineButton`
- `PrimaryButton` and `PrimaryInlineButton`
- `SuccessButton` and `SuccessInlineButton`

These are useful because they visually hint what kind of action the user is about to trigger.

For example:

```python
from telegrinder import DangerButton, Keyboard, PrimaryButton, SuccessButton


class MenuKeyboard(Keyboard, max_in_row=2):
    PROFILE = SuccessButton("Profile")
    BALANCE = PrimaryButton("Balance")
    EXIT = DangerButton("Exit")
```

A practical rule of thumb:

- `Success` for confirmation
- `Primary` for the main action
- `Danger` for cancel, delete, or exit

Not required, but helpful for UX.

---

## Inline keyboards

Inline buttons live directly under a message and usually work together with `callback_data`.

Example:

```python
from telegrinder.tools.keyboard import InlineButton, InlineKeyboard

inline_keyboard = (
    InlineKeyboard()
    .add(InlineButton("1", callback_data="button/1"))
    .add(InlineButton("2", callback_data="button/2"))
    .row()
    .add(InlineButton("3", callback_data="button/3"))
)
```

Sending it:

```python
@bot.on.message(Text("/inline_keyboard"))
async def handle_inline_keyboard_command(message: Message) -> None:
    await message.answer(
        "Here is your inline keyboard",
        reply_markup=inline_keyboard.get_markup(),
    )
```

Inline buttons are especially good when:

- you do not want extra messages in chat
- you want to edit the current message
- the action should be encoded in `callback_data`

---

## What payload means here

When the user presses an inline button, Telegram usually does not send you the button text as a new message.

Instead, it sends a `callback_query`, and inside it there is `callback_data`.

That is what people usually mean by payload in this context.

Telegrinder has two rule families for this:

- older `CallbackData*`
- newer and more direct `Payload*Rule`

For new code, `Payload*Rule` is usually the easier path.

---

## The simplest payload

A plain string.

```python
from telegrinder import CallbackQuery
from telegrinder.rules import PayloadEqRule


@bot.on.callback_query(PayloadEqRule("button/1"))
async def handle_press_inline_button(cb: CallbackQuery) -> None:
    await cb.answer("Button 1 pressed")
```

This is the best place to begin.

You give the button a string:

```python
InlineButton("1", callback_data="button/1")
```

and catch the same string in the rule.

---

## Payload by template

If you have many buttons and only one part changes, a template is cleaner.

```python
from telegrinder.rules import PayloadMarkupRule


@bot.on.callback_query(PayloadMarkupRule("button/<index:int>"))
async def handle_press_inline_button(cb: CallbackQuery, index: int) -> None:
    # index arrives as an int automatically.
    await cb.answer(f"Button {index} pressed")
```

This is especially useful for:

- pagination
- item lists
- menu entries with ids

> [!TIP]
> If you catch yourself splitting strings like `"page/12"` manually, it is probably time to switch to `PayloadMarkupRule`.

---

## Payload as a model

For more serious menus, models are often much nicer than raw strings.

`callback_data` may be:

- `str`
- `dict`
- `dataclass`
- `msgspec.Struct`

Example:

```python
import msgspec

from telegrinder.tools.keyboard import InlineButton, InlineKeyboard


class ItemModel(msgspec.Struct):
    item: str
    amount: int
    action: str


keyboard = (
    InlineKeyboard()
    .add(
        InlineButton(
            "Buy doughnut",
            callback_data=ItemModel(item="doughnut", amount=100, action="buy"),
        )
    )
)
```

Handling it:

```python
from telegrinder.rules import PayloadModelRule


@bot.on.callback_query(PayloadModelRule(ItemModel, alias="data"))
async def buy(cb: CallbackQuery, data: ItemModel) -> None:
    # data is already a ready model object.
    await cb.edit_text(f"You bought {data.item} for {data.amount}")
```

Why this feels good:

- no need to manually pack fields into a string
- no manual parsing on the way back
- types help keep things straight

For small bots strings are fine. For shops, admin panels, and more complex menus, models are usually much nicer.

---

## Payload serializers

Telegrinder has two main serializers:

- `JSONSerializer`
- `MsgPackSerializer`

Import:

```python
from telegrinder.tools import JSONSerializer, MsgPackSerializer
```

Sometimes the model itself can declare which serializer it prefers:

```python
import dataclasses

from telegrinder.tools import MsgPackSerializer


@dataclasses.dataclass(slots=True, frozen=True)
class StoreCallback:
    __key__ = "store"
    __serializer__ = MsgPackSerializer["StoreCallback"]

    action: str
    item: str
    price: int
```

That is useful when you want the serialization logic to stay close to the payload model itself.

---

## Using an inline button directly as a rule

Static inline buttons can be used directly in decorators.

```python
class MainMenuKeyboard(InlineKeyboard):
    show_fact = PrimaryInlineButton("Show fact", callback_data="menu/fact", new_row=True)
    exit = DangerInlineButton("Exit", callback_data="menu/exit")


@bot.on.callback_query(MainMenuKeyboard.show_fact)
async def show_fact(cb: CallbackQuery) -> None:
    await cb.answer("Interesting fact")
```

This is one of the nicest telegrinder patterns:

- the button is defined next to the menu
- the handler uses the button itself
- fewer chances to mistype a payload string

---

## A practical beginner path

If you do not want to overcomplicate things, a good path is:

1. Start with `Keyboard` for simple menus.
2. Move to `InlineKeyboard` for actions under a message.
3. Use plain strings and `PayloadEqRule` for simple callback handling.
4. Use `PayloadMarkupRule` when callback strings become structured.
5. Use models and `PayloadModelRule` when the menu starts becoming complex.

You do not need every part of the API at once.

---

## What to remember

- `Keyboard` is great for simple user-facing menus
- `InlineKeyboard` is great for actions under a message
- static keyboards are often best expressed as classes
- styled buttons help make the interface clearer
- for payload handling, starting with strings is fine, and moving to templates or models later is perfectly normal

[>> Next: Working with text: formatting, localization](8_text.md)
