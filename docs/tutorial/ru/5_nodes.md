# Ноды

Ноды в telegrinder отвечают за dependency injection. Они позволяют описывать, как получить одно значение из другого, а затем использовать это и в хендлерах, и в правилах, и во внутренних механизмах фреймворка.

Например:

- из `Message` можно получить `Text`
- из `Text` можно получить `int`
- из `CallbackQuery` можно получить `Payload`
- из `Source` можно получить пользователя, чат или их идентификаторы

Идея простая: вы описываете зависимости декларативно, а telegrinder сам строит цепочку композиции.

## Корневые значения

Во время обработки события в граф зависимостей уже попадают несколько корневых объектов:

- `API`
- `Update`
- `Context`

Они появляются автоматически, а уже от них строятся все остальные ноды.

Встроенных нод в пакете много. Их удобно смотреть в `telegrinder.node`. Например, там уже есть `Text`, `TextInteger`, `Source`, `UserSource`, `ChatSource`, `ChatId`, `Payload`, `File`, `Photo`, `Caption`, `Error` и другие.

---

## Как написать свою ноду

Нода определяется через класс и метод `__compose__`. Именно этот метод telegrinder вызывает, когда нужно получить значение.

Простейший вариант выглядит так:

```python
from nodnod import NodeError

from telegrinder import Message
from telegrinder.node import scalar_node


@scalar_node
class Text:
    @classmethod
    def __compose__(cls, message: Message) -> str:
        if not message.text:
            raise NodeError("Message has no text.")
        return message.text.unwrap()
```

Что здесь важно:

- `@scalar_node` говорит, что это скалярная нода
- telegrinder берёт зависимости из параметров `__compose__`
- если ноду собрать нельзя, нужно выбросить `NodeError`
- тип результата берётся из аннотации `-> str`

После этого ноду можно использовать в обработчике как обычный параметр:

```python
@bot.on.message()
async def text_message_handler(message: Message, text: Text) -> None:
    await message.answer(text.lower())
```

Точно так же ноды работают и в правилах:

```python
from telegrinder.bot.rules import ABCRule


class TextIsOfLength(ABCRule):
    def __init__(self, length: int) -> None:
        self.length = length

    async def check(self, text: Text) -> bool:
        return len(text) == self.length


@bot.on.message(TextIsOfLength(6))
async def six_handler() -> str:
    return "Люблю сообщения такой длины."
```

---

## Цепочки нод

Самое удобное в нодах то, что они естественно собираются друг из друга:

```python
from nodnod import NodeError

from telegrinder.node import scalar_node


@scalar_node
class TextInteger:
    @classmethod
    def __compose__(cls, text: Text) -> int:
        if not text.isdigit():
            raise NodeError("Text is not a digit.")
        return int(text)
```

Теперь можно писать хендлеры, которые вообще не знают, откуда появилось число:

```python
@bot.on.message()
async def number_handler(message: Message, value: TextInteger) -> None:
    await message.answer(f"{value} + 3 = {value + 3}")
```

Путь будет таким:

`Message -> Text -> TextInteger`

---

## Типы нод

На практике вам пригодятся несколько форм:

- `scalar_node` для “одного значения одного типа”
- `DataNode` для дата-классовых контейнеров
- `generic_node` для обобщённых нод
- `polymorphic` для нод, которые умеют собираться из разных событий

Например, `Payload` в telegrinder полиморфный: он умеет извлекать payload из `CallbackQuery`, `PreCheckoutQuery`, `ShippingQuery` и даже из сообщения с успешной оплатой.

---

## Области видимости

У нод есть области жизни. Это важно, когда внутри ноды есть дорогая операция или ресурс с очисткой.

В telegrinder доступны три области:

- `PER_EVENT` или “на событие” — значение создаётся один раз на апдейт и переиспользуется в рамках обработки. Это поведение по умолчанию.
- `PER_CALL` или “на вызов” — нода создаётся каждый раз, когда кто-то её запрашивает.
- `GLOBAL` или “глобально” — нода создаётся один раз на всё приложение.

### Per call

```python
import aiosqlite
import typing

from telegrinder.node import per_call, scalar_node


@per_call
@scalar_node
class DB:
    @classmethod
    async def __compose__(cls) -> typing.AsyncGenerator[aiosqlite.Connection, None]:
        connection = await aiosqlite.connect("test.db")
        yield connection
        await connection.close()
```

Здесь есть ещё одна важная возможность: ноды могут быть генераторами. Значение отдаётся через `yield`, а код после `yield` используется как финализация ресурса.

### Global

```python
from telegrinder.node import DataNode, global_node, scalar_node


@global_node
class Settings(DataNode):
    api_url: str
    secret: str

    @classmethod
    def __compose__(cls) -> "Settings":
        return cls(
            api_url=env["API_URL"],
            secret=env["APP_SECRET"],
        )


@global_node
@scalar_node
class Secret:
    @classmethod
    def __compose__(cls) -> str:
        return generate_secret(16)
```

Глобальные ноды хороши для конфигурации, клиентов и редко меняющихся объектов.

---

## Практический пример

В [examples/with_nodes.py](https://github.com/timoniq/telegrinder/blob/dev/examples/with_nodes.py) можно посмотреть на более реалистичное использование:

- кастомные правила получают ноды как аргументы
- ноды используются в обычных сообщениях
- `DB` переиспользуется между несколькими хендлерами
- built-in ноды вроде `Photo`, `File`, `ChatSource` и `TextInteger` работают без ручной склейки

Именно в этом месте обычно становится заметно, что ноды полезны не ради “магии”, а ради уменьшения дублирования и нормальной композиции логики.

---

## Что запомнить

- нода описывает, как получить одно значение из других
- основной метод ноды в текущем API называется `__compose__`
- ноды работают и в хендлерах, и в правилах
- по умолчанию ноды живут в пределах одного события
- сложные зависимости удобно выносить в ноды, а не копировать по хендлерам

[>> Next: Dispatch](6_dispatch.md)
