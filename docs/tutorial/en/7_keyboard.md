# Keyboard, payload handling

Telegrinder keyboards come in two main forms:

- regular `Keyboard`
- inline `InlineKeyboard`

Both can be built dynamically, and static keyboards are often easier to maintain as classes.

## Regular keyboard

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

Send it like this:

```python
@bot.on.message(Text("/keyboard"))
async def handle_keyboard_command(message: Message) -> None:
    await message.answer(
        "Here is your keyboard",
        reply_markup=keyboard.get_markup(),
    )
```

Regular keyboard presses are just regular messages, so handling them is usually a `Text` rule:

```python
@bot.on.message(Text("1"))
async def handle_press_button(message: Message) -> None:
    await message.answer("Button 1 pressed")
```

---

## New styled buttons

Both regular and inline buttons now have styled variants:

- `DangerButton` and `DangerInlineButton`
- `PrimaryButton` and `PrimaryInlineButton`
- `SuccessButton` and `SuccessInlineButton`

They set a `KeyboardButtonStyle` for the button.

```python
from telegrinder import DangerButton, Keyboard, PrimaryButton, SuccessButton


class MenuKeyboard(Keyboard, max_in_row=2):
    PROFILE = SuccessButton("Profile")
    BALANCE = PrimaryButton("Balance")
    EXIT = DangerButton("Exit")
```

These styles are useful when you want the UI to communicate intent:

- `Success` for confirmation
- `Primary` for the main action
- `Danger` for destructive or exit actions

---

## Static keyboards

Static keyboards are defined via inheritance:

```python
from telegrinder.tools.keyboard import Button, Keyboard


class FruitsKeyboard(Keyboard, max_in_row=2, one_time_keyboard=True):
    APPLE = Button("Apple")
    BANANA = Button("Banana")
    KIWI = Button("Kiwi")
```

Send the class directly:

```python
@bot.on.message(Text("/eat"))
async def eat(message: Message) -> None:
    await message.answer(
        "What do you want to eat?",
        reply_markup=FruitsKeyboard.get_markup(),
    )
```

And static buttons are both buttons and rules:

```python
@bot.on.message(FruitsKeyboard.APPLE)
async def eat_apple(message: Message) -> None:
    await message.answer(
        "Good choice",
        reply_markup=FruitsKeyboard.get_keyboard_remove(),
    )
```

---

## Inline keyboards

Now for `InlineKeyboard`:

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

Sending it looks the same:

```python
@bot.on.message(Text("/inline_keyboard"))
async def handle_inline_keyboard_command(message: Message) -> None:
    await message.answer(
        "Here is your inline keyboard",
        reply_markup=inline_keyboard.get_markup(),
    )
```

---

## Handling payload

Inline buttons usually work through `callback_data`. In the current API telegrinder has two rule families for this:

- older `CallbackData*`
- more direct `Payload*Rule`

For new code, `Payload*Rule` is usually easier to follow.

### Simple string payload

```python
from telegrinder import CallbackQuery
from telegrinder.rules import PayloadEqRule


@bot.on.callback_query(PayloadEqRule("button/1"))
async def handle_press_inline_button(cb: CallbackQuery) -> None:
    await cb.answer("Button 1 pressed")
```

### Markup payload

```python
from telegrinder.rules import PayloadMarkupRule


@bot.on.callback_query(PayloadMarkupRule("button/<index:int>"))
async def handle_press_inline_button(cb: CallbackQuery, index: int) -> None:
    await cb.answer(f"Button {index} pressed")
```

---

## Payload as a model

`callback_data` may be:

- `str`
- `dict`
- `dataclass`
- `msgspec.Struct`

For non-string payloads, typed models are often the cleanest choice:

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

Then process it through `PayloadModelRule`:

```python
from telegrinder.rules import PayloadModelRule


@bot.on.callback_query(PayloadModelRule(ItemModel, alias="data"))
async def buy(cb: CallbackQuery, data: ItemModel) -> None:
    await cb.edit_text(f"You bought {data.item} for {data.amount}")
```

Alternatives for dict and JSON-style payloads are still available:

- `CallbackDataJsonEq`
- `CallbackDataMap`
- `CallbackDataJsonModel`

They remain useful, especially in older codebases.

---

## Payload serializers

Telegrinder ships with two main serializers:

- `JSONSerializer`
- `MsgPackSerializer`

They are imported like this now:

```python
from telegrinder.tools import JSONSerializer, MsgPackSerializer
```

If you need to define a serializer explicitly for the button:

```python
import dataclasses

from telegrinder.tools import MsgPackSerializer
from telegrinder.tools.keyboard import InlineButton, InlineKeyboard


@dataclasses.dataclass(slots=True, frozen=True)
class StoreCallback:
    __key__ = "store"
    __serializer__ = MsgPackSerializer["StoreCallback"]

    action: str
    item: str
    price: int


keyboard = InlineKeyboard().add(
    InlineButton(
        "Coffee",
        callback_data=StoreCallback(action="buy", item="coffee", price=3),
    )
)
```

The corresponding rule must understand the same serializer when it decodes the payload.

---

## Inline button as a ready rule

Static inline buttons can also be used directly in decorators:

```python
class MainMenuKeyboard(InlineKeyboard):
    show_fact = PrimaryInlineButton("Show fact", callback_data="menu/fact", new_row=True)
    exit = DangerInlineButton("Exit", callback_data="menu/exit")


@bot.on.callback_query(MainMenuKeyboard.show_fact)
async def show_fact(cb: CallbackQuery) -> None:
    await cb.answer("Interesting fact")
```

That is especially convenient for menus where the keyboard and handlers are meant to stay close together.

---

## Useful examples

- [examples/keyboard.py](https://github.com/timoniq/telegrinder/blob/dev/examples/keyboard.py)
- [examples/inline_keyboard.py](https://github.com/timoniq/telegrinder/blob/dev/examples/inline_keyboard.py)
- [examples/callback_query.py](https://github.com/timoniq/telegrinder/blob/dev/examples/callback_query.py)
- [examples/callback_data_map.py](https://github.com/timoniq/telegrinder/blob/dev/examples/callback_data_map.py)

---

## What to remember

- `Keyboard` and `InlineKeyboard` can be built dynamically or statically
- `Danger`, `Primary`, and `Success` button variants help communicate intent
- static buttons can be used as rules
- `Payload*Rule` is the cleaner family for new payload handling
- typed payload models are usually the most maintainable option

[>> Next: Working with text: formatting, localization](8_text.md)
