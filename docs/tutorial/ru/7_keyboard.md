# Клавиатура, обработка полезной нагрузки

Клавиатуры являются неотъемлемой частью ботов, ведь при помощи них можно создавать красивое меню, пагинацию и т. д. В этой статье мы рассмотрим способы создания клавиатур, а также научимся обрабатывать полезную нагрузку.

Существует два типа клавиауры: обычная (`Keyboard`) и инлайн (`InlineKeyboard`). Начнем с обычной:

```python
from telegrinder.tools import Button, Keyboard

keyboard = (
    Keyboard()
    .add(Button("1"))
    .add(Button("2"))
)
```

Супер, при помощи класса `Keyboard` мы создали объект клавиатуры, а также добавили в нее кнопки, которые были созданы через объект `Button`. Мы также можем задавать кнопки на других рядах:

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

Клавиатура выглядит следующим образом: кнопки `1` и `2` будут на первом ряду, кнопки `3` и `4` на втором ряду, а кнопка `5` будет на третьем ряду. Теперь ее можно отправить пользователю:

```python
@bot.on.message(Text("/keyboard"))
async def handle_keyboard_command(message: Message):
    await message.answer("Okay, here's your keyboard!", reply_markup=keyboard.get_markup())
```

Отлично, теперь если отравить команду "/keyboard", то бот отправит сообщений с нашей клавиатурой! Как ты мог заметить, у `keyboard` вызывается метод `.get_markup()`, он необходим для того, чтобы объект клавиатуры получить в виде объекта `ReplyKeyboardMarkup`, который ожидает telegram API.

Мы можем обработать нажатие кнопки с помощью правила `Text`:

```python
@bot.on.message(Text("1"))
async def handle_press_button(message: Message):
    await message.answer("Wow, you pressed the '1' button!")
```

Достаточно просто и красиво, правда? Давай научимся создавать инлайн клавиатуры:

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

Код сильно похож на тот, что с обычной клавиатурой, но только здесь используются классы с префиксом `Inline`, а также параметр `callback_data` конструктора `InlineButton` — да, это та самая полезная нагрузка, которая упоминается в начале этой статьи. После того, как мы создали инлайн клавиаутуру, ее можно отправить таким же способом, как и обычную:


```python
@bot.on.message(Text("/inline_keyboard"))
async def handle_inline_keyboard_command(message: Message):
    await message.answer("Okay, here's your inline keyboard!", reply_markup=inline.get_markup())
```

Как и с обычной клавиатурой, метод `.get_markup()` возвращает инлайн клавиатуру в виде объекта `InlineKeyboardMarkup`, который ожидает telegram API.

Перейдем к обработке полезной нагрузки, используя правило `CallbackDataEq`:

```python
from telegrinder import CallbackQuery
from telegrinder.rules import CallbackDataEq

@bot.on.callback_query(CallbackDataEq("button/1"))
async def handle_press_inline_button(cb: CallbackQuery):
    await cb.answer("Wow, you pressed '1' inline button!")
```

Хорошо, давай разбрем код!

Как ты, наверное, уже заметил, здесь используется другое событие, которое называется `callback_query`. Для его обработки используется представление (view) `callback_query`, на которое мы можем зарегистрировать наши обработчики. В этих обработчиках мы можем получить объект `CallbackQuery`, который описывает событие `callback_query`. У этого объекта, как и у объекта `Message` есть полезные сокращения. Например, одно из них — `answer`. По названию оно схоже с тем, которое есть в `Message`, однако это сокращение используется для метода `answer_callback_query`, а не для отправки сообщения. В нашем примере, если пользователь нажмет на кнопку `1`, то всплывет сообщение: "Wow, you pressed '1' inline button!".

Круто, правда? Теперь мы можем рассмотреть обработку различных полезных нагрузок на нашей клавиатуре:

```python
from telegrinder.rules import CallbackDataMarkup

@bot.on.callback_query(CallbackDataMarkup("button/<index:int>"))
async def handle_press_inline_button(cb: CallbackQuery, index: int):
    await cb.answer(f"Wow, you pressed '{index}' inline button!")
```

Здесь мы обрабатываем сразу все наши полезные нагрузки с помощью правила `CallbackDataMarkup`, которые мы указали при создании клавиатуры. Это правило похоже на правило `Markup` из статьи про [Правила](2_rules.md). Наш обработчик принимает параметр `index` типа `int`, который указан в шаблоне `button/<index:int>`. Таким образом, мы обработали все наши полезные нагрузки и при нажатии на кнопки, будет всплывать сообщение с индексом нажатой пользователем кнопки.

---

Полезная нагрузка может быть одной из нескольких типов:
- `str`
- `dict`
- `dataclasses.dataclass`
- `msgspec.Struct`

Рассмотрим несколько на примере:

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

По умолчанию наши классы `Item` и `Point` будут конвертированы в словари, а словари уже в сырой объект `JSON`. Такую полезную нагрузку можно обработать сразу через несколько правил:

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

Прекрасно! Пройдемся по примеру:

В первом обработчике `handle_dict` мы используем правило `CallbackDataJsonEq`, которое просто сравнивает наш словарь с `callback_data`, и, если они совпадают, правило срабатывает. Стоит отметить, что здесь использован метод `.decode_data()`, который декодирует полезную нагрузку в нужный нам тип данных. Поскольку мы ничего не передали в этот метод, по умолчанию он декодирует сырую полезную нагрузку типа `str` в `dict`.

Во втором обработчике `handle_item` используется правило `CallbackDataMap`, в которое также передаётся `dict`. Однако, как мы можем заметить, в качестве значений этого словаря используются валидаторы. С помощью этого правила можно сравнивать ключи словаря и их значения с `callback_data`. Валидатором может быть любой тип или функция, принимающая один параметр — значение из словаря полезной нагрузки — и возвращающая `bool`. В этом примере значение под ключом `name` проверяется на соответствие типу `str`, а amount проверяется с помощью лямбда-функции, внутри которой происходят две проверки: является ли значение типом `int`, и удовлетворяет ли оно условию `amount >= 3`. Таким образом, если правило сработало, обработчик сможет получить значения `name` и `amount`.

В третьем обработчике `handle_point` используется правило `CallbackDataJsonModel`, которому передаётся класс модели `Point`. Это правило принимает либо `dataclasses.dataclass`, либо `msgspec.Struct`. Оно пытается преобразовать полезную нагрузку в экземпляр модели, и, если преобразование прошло успешно, помещает объект модели в контекст под ключом `data`. В нашем примере мы как раз получаем объект `Point`, ожидая параметр `data: Point` в обработчике. В статье про [Правила](2_rules.md) описано, как правило может передавать данные в контекст. Кроме того, в этом примере обработчик возвращает строку, которая будет передана в `cb.answer()` — это "ленивый" способ ответа на нажатие кнопки ^_^

---

Поговорим о наиболее важной части обработки полезной нагрузки — о сериализаторах. В telegrinder их два:
- `JSONSerializer`
- `MsgPackSerializer`

`JSONSerializer` необходим, чтобы сериализовать объекты `dict`, `dataclasses.dataclass`, `msgspec.Struct` в `JSON`, а `MsgPackSerializer` для сериализации тех же объектов, что и `JSONSerializer`, но в [MessagePack](https://msgpack.org/).

> [!TIP]
> Если установить зависимость [brotli](https://github.com/google/brotli), то `MsgPackSerializer` будет сериализовать еще компактнее и быстрее!

Рассмотрим на примере использования:

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

По умолчанию, если не передать `callback_data_serializer`, то будет использоваться `JSONSerializer`. Сериализация `callback_data` происходит сразу же при инициализации `InlineButton`.

Правила не знают, какой мы использовали сериализатор при определении `callback_data`, поэтому его также необходимо передавать:

```python
@bot.on.callback_query(CallbackDataJsonModel(Item, serializer=MsgPackSerializer))
async def handle_item(cb: CallbackQuery, data: Item):
    await cb.answer(f"Picked item {data.name!r}, amount: {data.amount}")
```

Теперь правило `CallbackDataJsonModel` будет знать, как сериализовать полезную нагрузку в `Item`.

Кастомизация — очень приятная вещь: при желании можно реализовать свой собственный сериализатор, унаследовав `ABCDataSerializer`.

---

Специально для обработки полезной нагрузки в telegrinder есть ноды.

Например, глобальная нода `PayloadSerializer`, с помощью которой можно установить и получить сериализатор для сериализации полезной нагрузки.

```python
from telegrinder.tools.callback_data_serialization import MsgPackSerializer

PayloadSerializer.set(MsgPackSerializer)
```

По умолчанию установлен `JSONSerializer`.


Давай рассмотрим несколько нод на примере:

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

Довольно удобно, а главное - просто!

---

Зачастую статические клавиатуры используются чаще, чем динамические. Статические отличаются от динамических тем, что ты клавиатура создается один раз и она больше никак не изменится. Способ создания несколько отличается от динамического.

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


Получился класс, который представляет из себя обычную клавиатуру с 3-мя кнопками. По мимо параметра `max_in_row`, можно передать и другие параметры, которые принимает класс `Keyboard`. Статические кнопки являются и кнопкой и правилом. Да, это прикольно, по скольку эти кнопки можно передавать в обработчик и тем самым элегантно обрабатывать их нажатие.


```python
@bot.on.message(MenuKeyboard.EXIT)
async def handle_exit(message: Message):
    await message.answer("Okay, exit!", reply_markup=MenuKeyboard.get_keyboard_remove())
```


Такие клавиатуры можно хранить в файла для удобства в папке, назвав ее, к примеру, `keyboards`:

`keyboards`
 - `start_keyboard.py`
 - `buymenu_keyboard.py`
 - `game_keyboard.py`


Удачи в создании красивых клавиатур!

[>> Next: Работа с текстом: форматирование, локализация](8_text.md)
