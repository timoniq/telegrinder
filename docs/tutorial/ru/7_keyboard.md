# Клавиатура, обработка полезной нагрузки

Клавиатуры это почти всегда первый способ сделать бота удобнее.

Без клавиатур бот обычно выглядит так:

- пользователь должен помнить команды
- пользователь должен сам вводить варианты
- вы постоянно проверяете текст руками

С клавиатурами всё становится намного дружелюбнее.

В telegrinder есть два основных типа:

- обычная `Keyboard`
- инлайн `InlineKeyboard`

## Обычная клавиатура

Это та клавиатура, которая появляется вместо системной клавиатуры Telegram.

Простейший пример:

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

Что здесь происходит:

- `Keyboard()` создаёт объект клавиатуры
- `.add(...)` добавляет кнопку в текущую строку
- `.row()` начинает новую строку

Отправить её можно так:

```python
@bot.on.message(Text("/keyboard"))
async def handle_keyboard_command(message: Message) -> None:
    await message.answer(
        "Вот клавиатура",
        reply_markup=keyboard.get_markup(),
    )
```

Метод `get_markup()` превращает объект telegrinder-клавиатуры в тот markup, который понимает Telegram API.

---

## Как обрабатывать нажатие обычной кнопки

Для обычной клавиатуры нажатие кнопки это просто новое сообщение от пользователя.

Поэтому чаще всего всё сводится к `Text(...)`:

```python
@bot.on.message(Text("1"))
async def handle_press_button(message: Message) -> None:
    await message.answer("Ты нажал кнопку 1")
```

Это очень удобно на старте: не нужно отдельно думать про callback data.

> [!TIP]
> Подсказка:
> Если бот только начинается, обычная клавиатура часто проще инлайн-кнопок. Особенно если вы делаете меню из 2-5 простых действий.

---

## Статические клавиатуры

Когда клавиатура используется часто и почти не меняется, её удобнее описывать классом.

```python
from telegrinder.tools.keyboard import Button, Keyboard


class FruitsKeyboard(Keyboard, max_in_row=2, one_time_keyboard=True):
    APPLE = Button("Apple")
    BANANA = Button("Banana")
    KIWI = Button("Kiwi")
```

Плюсы такого подхода:

- клавиатура описана в одном месте
- не нужно собирать её заново в каждом хендлере
- кнопки можно использовать как правила

Отправка:

```python
@bot.on.message(Text("/eat"))
async def eat(message: Message) -> None:
    await message.answer(
        "Что съесть?",
        reply_markup=FruitsKeyboard.get_markup(),
    )
```

А теперь приятная часть:

```python
@bot.on.message(FruitsKeyboard.APPLE)
async def eat_apple(message: Message) -> None:
    await message.answer(
        "Отличный выбор",
        reply_markup=FruitsKeyboard.get_keyboard_remove(),
    )
```

Здесь `FruitsKeyboard.APPLE` работает и как кнопка, и как правило.

Это очень удобный паттерн для меню.

> [!TIP]
> Лайфхак:
> Если одна и та же клавиатура используется больше чем в одном месте, почти всегда лучше вынести её в отдельный класс.

---

## Стили кнопок

В telegrinder есть styled-кнопки:

- `DangerButton` и `DangerInlineButton`
- `PrimaryButton` и `PrimaryInlineButton`
- `SuccessButton` и `SuccessInlineButton`

Это помогает визуально подсказать пользователю, что за действие его ждёт.

Например:

```python
from telegrinder import DangerButton, Keyboard, PrimaryButton, SuccessButton


class MenuKeyboard(Keyboard, max_in_row=2):
    PROFILE = SuccessButton("Profile")
    BALANCE = PrimaryButton("Balance")
    EXIT = DangerButton("Exit")
```

Хорошее практическое правило:

- `Success` для подтверждения
- `Primary` для главного действия
- `Danger` для отмены, удаления, выхода

Это не обязательная часть API, но для UX полезно.

---

## Инлайн-клавиатуры

Инлайн-кнопки живут прямо под сообщением и обычно используются вместе с `callback_data`.

Пример:

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

Отправка:

```python
@bot.on.message(Text("/inline_keyboard"))
async def handle_inline_keyboard_command(message: Message) -> None:
    await message.answer(
        "Вот инлайн-клавиатура",
        reply_markup=inline_keyboard.get_markup(),
    )
```

Инлайн-кнопки особенно хороши, когда:

- не хочется засорять чат новыми сообщениями
- нужно редактировать текущее сообщение
- важно хранить действие в `callback_data`

---

## Что такое payload

Когда пользователь нажимает инлайн-кнопку, обычно вы не получаете "текст кнопки" как новое сообщение.

Вместо этого Telegram присылает `callback_query`, а в ней лежит `callback_data`.

Именно это в tutorial часто называют payload.

В telegrinder для этого есть два семейства правил:

- старые `CallbackData*`
- более новые и прямые `Payload*Rule`

Для нового кода обычно проще использовать `Payload*Rule`.

---

## Самый простой payload

Строка.

```python
from telegrinder import CallbackQuery
from telegrinder.rules import PayloadEqRule


@bot.on.callback_query(PayloadEqRule("button/1"))
async def handle_press_inline_button(cb: CallbackQuery) -> None:
    await cb.answer("Нажата кнопка 1")
```

Это лучший способ начать.

Вы даёте кнопке строку:

```python
InlineButton("1", callback_data="button/1")
```

и ловите ту же строку правилом.

---

## Payload по шаблону

Если кнопок много и они отличаются только параметром, удобнее использовать шаблон.

```python
from telegrinder.rules import PayloadMarkupRule


@bot.on.callback_query(PayloadMarkupRule("button/<index:int>"))
async def handle_press_inline_button(cb: CallbackQuery, index: int) -> None:
    # index сюда придёт уже как int.
    await cb.answer(f"Нажата кнопка {index}")
```

Это особенно удобно для:

- пагинации
- списков товаров
- меню с id-шниками

> [!TIP]
> Лайфхак:
> Если вы видите, что начинаете вручную парсить строки вроде `"page/12"` через `.split("/")`, скорее всего вам уже пора на `PayloadMarkupRule`.

---

## Payload как модель

Очень приятный вариант для более серьёзных меню это не строка, а модель.

`callback_data` может быть:

- `str`
- `dict`
- `dataclass`
- `msgspec.Struct`

Например:

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

Обработка:

```python
from telegrinder.rules import PayloadModelRule


@bot.on.callback_query(PayloadModelRule(ItemModel, alias="data"))
async def buy(cb: CallbackQuery, data: ItemModel) -> None:
    # data уже готовый объект модели.
    await cb.edit_text(f"You bought {data.item} for {data.amount}")
```

Почему это приятно:

- не нужно руками сериализовать поля в строку
- нет ручного парсинга обратно
- типы помогают не запутаться

На маленьком боте можно обойтись строками, но для магазинов, сложных меню и админок модели обычно намного удобнее.

---

## Сериализаторы payload

В telegrinder есть два основных сериализатора:

- `JSONSerializer`
- `MsgPackSerializer`

Импорт:

```python
from telegrinder.tools import JSONSerializer, MsgPackSerializer
```

Иногда модель сама знает, каким сериализатором пользоваться:

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

Это полезно, когда вы хотите централизовать способ сериализации прямо рядом с моделью.

---

## Inline-кнопка как готовое правило

Статические inline-кнопки можно использовать прямо в декораторе.

```python
class MainMenuKeyboard(InlineKeyboard):
    show_fact = PrimaryInlineButton("Show fact", callback_data="menu/fact", new_row=True)
    exit = DangerInlineButton("Exit", callback_data="menu/exit")


@bot.on.callback_query(MainMenuKeyboard.show_fact)
async def show_fact(cb: CallbackQuery) -> None:
    await cb.answer("Interesting fact")
```

Это один из самых приятных приёмов в telegrinder:

- кнопка объявлена рядом с меню
- обработчик использует саму кнопку
- меньше риска опечататься в строковом payload

---

## Мини-шаблон для новичка

Если не хочется переусложнять, можно двигаться так:

1. Для обычных меню начните с `Keyboard`.
2. Для действий под сообщением переходите на `InlineKeyboard`.
3. Для простых callback используйте строки и `PayloadEqRule`.
4. Для параметризованных callback переходите на `PayloadMarkupRule`.
5. Для сложных меню и админок используйте модели и `PayloadModelRule`.

Это очень спокойная траектория. Не нужно сразу использовать все возможности API.

---

## Что запомнить

- `Keyboard` хороша для простых пользовательских меню
- `InlineKeyboard` хороша для действий под сообщением
- статические клавиатуры удобно описывать классами
- styled-кнопки помогают сделать интерфейс понятнее
- для payload лучше начинать со строк, а потом при необходимости переходить на шаблоны и модели

[>> Next: Работа с текстом: форматирование, локализация](8_text.md)
