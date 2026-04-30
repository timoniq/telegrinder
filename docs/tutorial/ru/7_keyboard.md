# Клавиатура, обработка полезной нагрузки

Клавиатуры в telegrinder делятся на два типа:

- обычные `Keyboard`
- инлайн `InlineKeyboard`

Обе можно собирать динамически, а если клавиатура статична, её удобно описывать классом.

## Обычная клавиатура

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

Клавиатуру можно отправить так:

```python
@bot.on.message(Text("/keyboard"))
async def handle_keyboard_command(message: Message) -> None:
    await message.answer(
        "Вот клавиатура",
        reply_markup=keyboard.get_markup(),
    )
```

Для обычных кнопок нажатие обрабатывается как обычное сообщение. Проще всего через `Text`:

```python
@bot.on.message(Text("1"))
async def handle_press_button(message: Message) -> None:
    await message.answer("Нажата кнопка 1")
```

---

## Новые стили кнопок

У обычных и инлайн-кнопок теперь есть styled-интерфейсы:

- `DangerButton` и `DangerInlineButton`
- `PrimaryButton` и `PrimaryInlineButton`
- `SuccessButton` и `SuccessInlineButton`

Они задают стиль кнопки через `KeyboardButtonStyle`.

```python
from telegrinder import DangerButton, Keyboard, PrimaryButton, SuccessButton


class MenuKeyboard(Keyboard, max_in_row=2):
    PROFILE = SuccessButton("Profile")
    BALANCE = PrimaryButton("Balance")
    EXIT = DangerButton("Exit")
```

Такие кнопки полезны, когда вы хотите явно показать намерение действия:

- `Success` для подтверждения
- `Primary` для основного действия
- `Danger` для выхода, удаления, отмены

---

## Статические клавиатуры

Статические клавиатуры создаются через наследование:

```python
from telegrinder.tools.keyboard import Button, Keyboard


class FruitsKeyboard(Keyboard, max_in_row=2, one_time_keyboard=True):
    APPLE = Button("Apple")
    BANANA = Button("Banana")
    KIWI = Button("Kiwi")
```

Теперь клавиатуру можно отправлять как класс:

```python
@bot.on.message(Text("/eat"))
async def eat(message: Message) -> None:
    await message.answer(
        "Что съесть?",
        reply_markup=FruitsKeyboard.get_markup(),
    )
```

И что особенно удобно, статические кнопки одновременно являются и кнопкой, и правилом:

```python
@bot.on.message(FruitsKeyboard.APPLE)
async def eat_apple(message: Message) -> None:
    await message.answer(
        "Отличный выбор",
        reply_markup=FruitsKeyboard.get_keyboard_remove(),
    )
```

---

## Инлайн-клавиатуры

Теперь перейдём к `InlineKeyboard`:

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

Отправка выглядит так же:

```python
@bot.on.message(Text("/inline_keyboard"))
async def handle_inline_keyboard_command(message: Message) -> None:
    await message.answer(
        "Вот инлайн-клавиатура",
        reply_markup=inline_keyboard.get_markup(),
    )
```

---

## Обработка payload

У инлайн-кнопок вместо текста сообщения обычно используется `callback_data`. В текущем API в telegrinder для этого есть два семейства правил:

- старые `CallbackData*`
- более прямые `Payload*Rule`

В новых примерах удобнее использовать `Payload*Rule`.

### Простое сравнение строки

```python
from telegrinder import CallbackQuery
from telegrinder.rules import PayloadEqRule


@bot.on.callback_query(PayloadEqRule("button/1"))
async def handle_press_inline_button(cb: CallbackQuery) -> None:
    await cb.answer("Нажата кнопка 1")
```

### Разбор по шаблону

```python
from telegrinder.rules import PayloadMarkupRule


@bot.on.callback_query(PayloadMarkupRule("button/<index:int>"))
async def handle_press_inline_button(cb: CallbackQuery, index: int) -> None:
    await cb.answer(f"Нажата кнопка {index}")
```

---

## Payload как модель

`callback_data` может быть:

- `str`
- `dict`
- `dataclass`
- `msgspec.Struct`

Удобный вариант для нестроковых payload — модель:

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

Обрабатывать это удобно через `PayloadModelRule`:

```python
from telegrinder.rules import PayloadModelRule


@bot.on.callback_query(PayloadModelRule(ItemModel, alias="data"))
async def buy(cb: CallbackQuery, data: ItemModel) -> None:
    await cb.edit_text(f"You bought {data.item} for {data.amount}")
```

Альтернатива для словарей и JSON payload:

- `CallbackDataJsonEq`
- `CallbackDataMap`
- `CallbackDataJsonModel`

Они по-прежнему доступны и полезны, особенно если вы уже используете старый стиль API.

---

## Сериализаторы payload

В telegrinder есть два основных сериализатора:

- `JSONSerializer`
- `MsgPackSerializer`

Импортируются они сейчас так:

```python
from telegrinder.tools import JSONSerializer, MsgPackSerializer
```

Если сериализатор нужно указать явно для кнопки:

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

Тот же сериализатор должен понимать и rule, если вы разбираете payload как модель.

---

## Inline-кнопка как готовое правило

Как и обычные статические кнопки, статические inline-кнопки можно использовать прямо в декораторе:

```python
class MainMenuKeyboard(InlineKeyboard):
    show_fact = PrimaryInlineButton("Show fact", callback_data="menu/fact", new_row=True)
    exit = DangerInlineButton("Exit", callback_data="menu/exit")


@bot.on.callback_query(MainMenuKeyboard.show_fact)
async def show_fact(cb: CallbackQuery) -> None:
    await cb.answer("Interesting fact")
```

Это особенно удобно для меню, где клавиатура и обработчики живут рядом.

---

## Где посмотреть рабочие примеры

Актуальные примеры лежат в:

- [examples/keyboard.py](https://github.com/timoniq/telegrinder/blob/dev/examples/keyboard.py)
- [examples/inline_keyboard.py](https://github.com/timoniq/telegrinder/blob/dev/examples/inline_keyboard.py)
- [examples/callback_query.py](https://github.com/timoniq/telegrinder/blob/dev/examples/callback_query.py)
- [examples/callback_data_map.py](https://github.com/timoniq/telegrinder/blob/dev/examples/callback_data_map.py)

---

## Что запомнить

- `Keyboard` и `InlineKeyboard` можно собирать динамически и статически
- styled-кнопки `Danger`, `Primary`, `Success` помогают явно обозначать действие
- статические кнопки можно передавать в декораторы как правила
- для новых payload-сценариев удобнее использовать `Payload*Rule`
- для сложных данных лучше сразу использовать модели

[>> Next: Работа с текстом: форматирование, локализация](8_text.md)
