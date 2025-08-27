# Keyboard, payload handling

Keyboards are an integral part of bots, as they can be used to create beautiful menus, pagination, and so on. In this article, we'll look at ways to create keyboards and learn how to handle payloads.

There are two types of keyboards: regular (`Keyboard`) and inline (`InlineKeyboard`). Let's start with the regular one:

```python
from telegrinder.tools import Button, Keyboard

keyboard = (
    Keyboard()
    .add(Button("1"))
    .add(Button("2"))
)
```

Great! Using the `Keyboard` class, we created a keyboard object and also added buttons to it that were created through the `Button` object. We can also set buttons on other rows:

```python
from telegrinder.tools.keyboard import Button, Keyboard

keyboard = (
    Keyboard()
    .add(Button("1"))
    .add(Button("2"))
    .row()
    .add(Button("3"))
    .add(Button("4"))
    .row()
    .add(Button("5"))
)
```

The keyboard looks like this: buttons `1` and `2` will be on the first row, buttons `3` and `4` on the second row, and button `5` will be on the third row. Now it can be sent to the user:

```python
@bot.on.message(Text("/keyboard"))
async def handle_keyboard_command(message: Message):
    await message.answer("Okay, here's your keyboard!", reply_markup=keyboard.get_markup())
```

Great! Now if you send the "/keyboard" command, the bot will send a message with our keyboard! As you may have noticed, the `keyboard` calls the `.get_markup()` method, which is necessary to get the keyboard object as a `ReplyKeyboardMarkup` object, which the telegram API expects.

We can handle button presses using the `Text` rule:

```python
@bot.on.message(Text("1"))
async def handle_press_button(message: Message):
    await message.answer("Wow, you pressed the '1' button!")
```

Pretty simple and beautiful, right? Let's learn to create inline keyboards:

```python
from telegrinder.tools.keyboard import InlineButton, InlineKeyboard

inline_keyboard = (
    InlineKeyboard()
    .add(InlineButton("1", callback_data="button/1"))
    .add(InlineButton("2", callback_data="button/2"))
    .row()
    .add(InlineButton("3", callback_data="button/3"))
    .add(InlineButton("4", callback_data="button/4"))
    .row()
    .add(InlineButton("5", callback_data="button/5"))
)
```

The code is very similar to the one with a regular keyboard, but here classes with the `Inline` prefix are used, as well as the `callback_data` parameter of the `InlineButton` constructor — yes, this is the very payload mentioned at the beginning of this article. After we create an inline keyboard, it can be sent in the same way as a regular one:


```python
@bot.on.message(Text("/inline_keyboard"))
async def handle_inline_keyboard_command(message: Message):
    await message.answer("Okay, here's your inline keyboard!", reply_markup=inline_keyboard.get_markup())
```

As with a regular keyboard, the `.get_markup()` method returns an inline keyboard as an `InlineKeyboardMarkup` object, which the telegram API expects.

Let's move on to payload handling using the `CallbackDataEq` rule:

```python
from telegrinder import CallbackQuery
from telegrinder.rules import CallbackDataEq

@bot.on.callback_query(CallbackDataEq("button/1"))
async def handle_press_inline_button(cb: CallbackQuery):
    await cb.answer("Wow, you pressed '1' inline button!")
```

Good, let's break down the code!

As you probably already noticed, a different event called `callback_query` is used here. To handle it, we use the `callback_query` view, on which we can register our handlers. In these handlers, we can get a `CallbackQuery` object that describes the `callback_query` event. This object, like the `Message` object, has useful shortcuts. For example, one of them is `answer`. By name, it's similar to the one in `Message`, but this shortcut is used for the `answer_callback_query` method, not for sending a message. In our example, if the user presses button `1`, a message will pop up: "Wow, you pressed '1' inline button!".

Cool, right? Now we can look at handling various payloads on our keyboard:

```python
from telegrinder.rules import CallbackDataMarkup

@bot.on.callback_query(CallbackDataMarkup("button/<index:int>"))
async def handle_press_inline_button(cb: CallbackQuery, index: int):
    await cb.answer(f"Wow, you pressed '{index}' inline button!")
```

Here we handle all our payloads at once using the `CallbackDataMarkup` rule, which we specified when creating the keyboard. This rule is similar to the `Markup` rule from the article about [Rules](2_rules.md). Our handler takes an `index` parameter of type `int`, which is specified in the template `button/<index:int>`. Thus, we handled all our payloads and when buttons are pressed, a message with the index of the button pressed by the user will pop up.

---

The payload can be one of several types:
- `str`
- `dict`
- `dataclasses.dataclass`
- `msgspec.Struct`

Let's look at several examples:

```python
import dataclasses
import msgspec


@dataclasses.dataclass
class Item:
    name: str
    amount: int

class Point(msgspec.Struct):
    x: int
    y: int


inline_keyboard = (
    InlineKeyboard()
    .add(InlineButton("apple", callback_data=Item("apple", 5)))
    .add(InlineButton("point", callback_data=Point(2, 2)))
    .add(InlineButton("dict", callback_data=dict(key="value")))
)
```

By default, our `Item` and `Point` classes will be converted to dictionaries, and dictionaries to raw `JSON` objects. Such payloads can be handled immediately through several rules:

```python
from telegrinder.rules import CallbackDataMap, CallbackDataJsonEq, CallbackDataJsonModel

@bot.on.callback_query(CallbackDataJsonEq(dict(key="value")))
async def handle_dict(cb: CallbackQuery):
    await cb.answer(f"Really nice dict: {cb.decode_data().unwrap()!r}")

@bot.on.callback_query(CallbackDataMap({"name": str, "amount": lambda amount: isinstance(amount, int) and amount >= 3}))
async def handle_item(cb: CallbackQuery, name: str, amount: int):
    await cb.answer(f"Picked item {name!r}, amount: {amount}")

@bot.on.callback_query(CallbackDataJsonModel(Point))
async def handle_point(data: Point):
    return f"Point: x={data.x} y={data.y}"
```

Excellent! Let's go through the example:

In the first handler `handle_dict`, we use the `CallbackDataJsonEq` rule, which simply compares our dictionary with `callback_data`, and if they match, the rule triggers. It's worth noting that the `.decode_data()` method is used here, which decodes the payload into the data type we need. Since we didn't pass anything to this method, by default it decodes the raw payload of type `str` to `dict`.

In the second handler `handle_item`, the `CallbackDataMap` rule is used, which also receives a `dict`. However, as we can see, validators are used as values of this dictionary. With this rule, you can compare the keys of the dictionary and their values with `callback_data`. A validator can be any type or function that takes one parameter — a value from the payload dictionary — and returns `bool`. In this example, the value under the `name` key is checked for compliance with the `str` type, and amount is checked using a lambda function, inside which two checks occur: whether the value is of type `int`, and whether it satisfies the condition `amount >= 3`. Thus, if the rule worked, the handler will be able to get the `name` and `amount` values.

In the third handler `handle_point`, the `CallbackDataJsonModel` rule is used, which is passed the `Point` model class. This rule accepts either `dataclasses.dataclass` or `msgspec.Struct`. It tries to convert the payload to an instance of the model, and if the conversion is successful, it places the model object in the context under the `data` key. In our example, we just get a `Point` object, expecting a `data: Point` parameter in the handler. The article about [Rules](2_rules.md) describes how a rule can pass data to the context. Additionally, in this example, the handler returns a string that will be passed to `cb.answer()` — this is a "lazy" way to respond to a button press ^_^

---

Let's talk about the most important part of payload handling — serializers. There are two of them in telegrinder:
- `JSONSerializer`
- `MsgPackSerializer`

`JSONSerializer` is needed to serialize `dict`, `dataclasses.dataclass`, `msgspec.Struct` objects to `JSON`, and `MsgPackSerializer` for serializing the same objects as `JSONSerializer`, but to [MessagePack](https://msgpack.org/).

> [!TIP]
> If you install the [brotli](https://github.com/google/brotli) dependency, then `MsgPackSerializer` will serialize even more compactly and faster!

Let's look at an example of usage:

```python
import dataclasses
import msgspec

from telegrinder.tools.callback_data_serialization import MsgPackSerializer


@dataclasses.dataclass
class Item:
    name: str
    amount: int

class Point(msgspec.Struct):
    x: int
    y: int


inline_keyboard = (
    InlineKeyboard()
    .add(InlineButton("item", callback_data=Item("banana", 10), callback_data_serializer=MsgPackSerializer))
    .add(InlineButton("point", callback_data=Point(2, 6)))
)
```

By default, if you don't pass `callback_data_serializer`, then `JSONSerializer` will be used. Serialization of `callback_data` occurs immediately when `InlineButton` is initialized.

Rules don't know which serializer we used when defining `callback_data`, so it also needs to be passed:

```python
@bot.on.callback_query(CallbackDataJsonModel(Item, serializer=MsgPackSerializer))
async def handle_item(cb: CallbackQuery, data: Item):
    await cb.answer(f"Picked item {data.name!r}, amount: {data.amount}")
```

Now the `CallbackDataJsonModel` rule will know how to serialize the payload to `Item`.

Customization is a very nice thing: if desired, you can implement your own serializer by inheriting `ABCDataSerializer`.

---

There are nodes specifically for handling payloads in telegrinder.

For example, the global `PayloadSerializer` node, with which you can set and get a serializer for payload serialization.

```python
from telegrinder.tools.callback_data_serialization import MsgPackSerializer

PayloadSerializer.set(MsgPackSerializer)
```

By default, `JSONSerializer` is installed.


Let's look at several nodes with an example:

```python
import dataclasses
import msgspec

from telegrinder.node import PayloadSerializer, PayloadData, Field
from telegrinder.tools.callback_data_serialization import MsgPackSerializer


@dataclasses.dataclass
class Item:
    __key__ = "item"  # Payload key to identify payload for this dataclass
    __serializer__ = MsgPackSerializer["Item"]  # "Item" in a generic is a model/dataclass type-hint for the serializer

    name: str
    amount: int

class Point(msgspec.Struct):
    x: int
    y: int


inline_keyboard = (
    InlineKeyboard()
    .add(InlineButton("item", callback_data=Item("banana", 10)))
    .add(InlineButton("point", callback_data=Point(2, 6)))
)


@bot.on.callback_query()
async def handle_field(cb: CallbackQuery, amount: Field[int]):
    await cb.answer(f"Amount of items: {amount}")


@bot.on.callback_query()
async def handle_point(cb: CallbackQuery, point: PayloadData[Point]):
    await cb.answer(f"Point x={point.x} y={point.y}")
```

Pretty convenient, and most importantly - simple!

---

Often static keyboards are used more often than dynamic ones. Static keyboards differ from dynamic ones in that the keyboard is created once and it will never change again. The creation method is somewhat different from dynamic.

```python
from telegrinder.tools.keyboard import Button, Keyboard


class MenuKeyboard(Keyboard, max_in_row=2):
    PROFILE = Button("Profile")
    BALANCE = Button("Balance")
    EXIT = Button("Exit")


@bot.on.message(Text("menu"))
async def menu(message: Message):
    await message.answer("Menu:", reply_markup=MenuKeyboard.get_markup())
```


We got a class that represents a regular keyboard with 3 buttons. In addition to the `max_in_row` parameter, you can also pass other parameters that the `Keyboard` class accepts. Static buttons are both a button and a rule. Yes, this is cool, since these buttons can be passed to the handler and thus elegantly handle their pressing.


```python
@bot.on.message(MenuKeyboard.EXIT)
async def handle_exit(message: Message):
    await message.answer("Okay, exit!", reply_markup=MenuKeyboard.get_keyboard_remove())
```


Such keyboards can be stored in files for convenience in a folder, naming it, for example, `keyboards`:

`keyboards`
 - `start_keyboard.py`
 - `buymenu_keyboard.py`
 - `game_keyboard.py`


Good luck creating beautiful keyboards!

[>> Next: Working with text: formatting, localization](8_text.md)
