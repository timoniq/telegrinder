# Ноды

Если совсем по-простому, ноды в telegrinder это способ не таскать одну и ту же подготовительную логику по всем хендлерам вручную.

Вместо такого мышления:

- "сначала достань текст из сообщения"
- "потом попробуй превратить его в число"
- "потом достань пользователя"

можно мыслить так:

- "мне здесь нужен `Text`"
- "а здесь нужен `TextInteger`"
- "а тут нужен `UserSource`"

И telegrinder сам поймёт, как это собрать.

## Первая интуиция

Нода это просто описание: "вот так из одного значения получается другое".

Например:

- из `Message` можно получить `Text`
- из `Text` можно получить `int`
- из `CallbackQuery` можно получить `Payload`
- из `Source` можно получить пользователя или чат

Хороший ориентир для новичка такой:

если в хендлере вы раз за разом пишете одну и ту же подготовку данных, почти наверняка это кандидат в ноду.

## Что telegrinder уже даёт сам

Во время обработки события в граф зависимостей уже попадают корневые объекты:

- `API`
- `Update`
- `Context`

Из них дальше можно собрать всё остальное.

Во встроенных нодах уже есть много полезного:

- `Text`
- `TextInteger`
- `Source`
- `UserSource`
- `ChatSource`
- `ChatId`
- `Payload`
- `File`
- `Photo`
- `Caption`
- `Error`

Это значит, что свои ноды часто вообще не нужны на старте. Сначала стоит попробовать built-in варианты.

> [!TIP]
> Подсказка:
> Прежде чем писать свою ноду, загляните в `telegrinder.node`. Часто нужная уже существует.

---

## Первая собственная нода

Нода определяется через класс и метод `__compose__`.

```python
from nodnod import NodeError

from telegrinder import Message
from telegrinder.node import scalar_node


@scalar_node
class Text:
    @classmethod
    def __compose__(cls, message: Message) -> str:
        # Если в сообщении нет текста, ноду собрать нельзя.
        if not message.text:
            raise NodeError("Message has no text.")

        # unwrap() безопасен здесь, потому что выше мы уже проверили наличие текста.
        return message.text.unwrap()
```

Здесь происходит вот что:

- `@scalar_node` говорит telegrinder, что это скалярная нода
- параметр `message: Message` означает "для сборки нужен `Message`"
- `-> str` означает, что итоговое значение ноды это строка
- `NodeError` говорит "эту ноду сейчас собрать нельзя"

После этого нода используется как обычный параметр:

```python
@bot.on.message()
async def text_message_handler(message: Message, text: Text) -> None:
    # В хендлер уже приходит готовый текст.
    await message.answer(text.lower())
```

Для новичка это обычно самый приятный момент: хендлер становится короче и читается как "что делать", а не "как добыть входные данные".

---

## Ноды работают и в правилах

Это особенно удобно.

```python
from telegrinder.bot.rules import ABCRule


class TextIsOfLength(ABCRule):
    def __init__(self, length: int) -> None:
        self.length = length

    async def check(self, text: Text) -> bool:
        # Правило получает уже готовый Text.
        return len(text) == self.length


@bot.on.message(TextIsOfLength(6))
async def six_handler() -> str:
    return "Люблю сообщения такой длины."
```

То есть ноды полезны не только в хендлерах. Они также отлично разгружают кастомные правила.

> [!TIP]
> Лайфхак:
> Если правило начинает вручную лезть в `message.text`, `message.from_user`, `callback_query.data` и так далее, попробуйте сначала вынести это в ноду.

---

## Цепочки нод

Самое приятное начинается, когда ноды собираются друг из друга.

```python
from nodnod import NodeError

from telegrinder.node import scalar_node


@scalar_node
class TextInteger:
    @classmethod
    def __compose__(cls, text: Text) -> int:
        # Для этой ноды нужен уже готовый Text.
        if not text.isdigit():
            raise NodeError("Text is not a digit.")

        return int(text)
```

Теперь хендлер можно писать так:

```python
@bot.on.message()
async def number_handler(message: Message, value: TextInteger) -> None:
    await message.answer(f"{value} + 3 = {value + 3}")
```

Хотя внутри происходит цепочка:

`Message -> Text -> TextInteger`

Это и есть главное удобство нод.

Хендлеру не важно, как именно появилось число. Он просто работает с числом.

---

## Более жизненный пример

Допустим, вы часто берёте id входящего сообщения.

```python
from nodnod.interface.scalar import scalar_node

from telegrinder import Message

MessageId = type("MessageId", (int,), {})


@scalar_node
class IncomingMessageId:
    @classmethod
    def __compose__(cls, message: Message) -> MessageId:
        # Небольшой тип-обёртка иногда помогает сделать код понятнее.
        return MessageId(message.message_id)


@bot.on.message()
async def show_id(message: Message, message_id: IncomingMessageId) -> None:
    await message.answer(f"Твой message id: {message_id}")
```

На старте это может показаться "слишком абстрактно", но на больших ботах такие маленькие ноды очень хорошо убирают дублирование.

---

## Какие ноды бывают

На практике чаще всего встречаются:

- `scalar_node` для одного значения одного типа
- `DataNode` для дата-классовых контейнеров
- `generic_node` для обобщённых нод
- `polymorphic` для нод, которые умеют собираться из разных событий

Например, `Payload` в telegrinder полиморфный. Он умеет доставать payload не только из `CallbackQuery`, но и из других событий, где это уместно.

В повседневной разработке новичку чаще всего хватает именно `scalar_node`.

---

## Области жизни

Иногда важно не только "как собрать ноду", но и "как долго она живёт".

В telegrinder есть три области:

- `PER_EVENT` — на одно событие, это поведение по умолчанию
- `PER_CALL` — каждый раз заново
- `GLOBAL` — один раз на всё приложение

### PER_EVENT

Это дефолт.

Если одна и та же нода нужна в двух местах в рамках одного апдейта, telegrinder не будет собирать её заново.

Это удобно и обычно именно то, что нужно.

### PER_CALL

Полезно, когда вы хотите каждый раз получать "свежий" объект.

```python
import aiosqlite
import typing

from telegrinder.node import per_call, scalar_node


@per_call
@scalar_node
class DB:
    @classmethod
    async def __compose__(cls) -> typing.AsyncGenerator[aiosqlite.Connection, None]:
        # Создаём соединение перед использованием.
        connection = await aiosqlite.connect("test.db")

        # Передаём значение в обработчик или в другую ноду.
        yield connection

        # А сюда вернёмся после завершения обработки.
        await connection.close()
```

Здесь видно ещё одну важную фишку: нода может быть генератором.

То есть нода умеет:

- подготовить ресурс
- отдать его в работу
- потом корректно закрыть

> [!TIP]
> Лайфхак:
> Если у вас есть ресурс "открыть/закрыть", вроде соединения с БД, сессии или временного файла, нода-генератор часто оказывается самым аккуратным решением.

### GLOBAL

Глобальные ноды хороши для конфигурации, клиентов и почти неизменяемых значений.

```python
from telegrinder.node import DataNode, global_node, scalar_node


@global_node
class Settings(DataNode):
    api_url: str
    secret: str

    @classmethod
    def __compose__(cls) -> "Settings":
        # Такой объект обычно не нужно создавать на каждый апдейт.
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

---

## Когда нода не нужна

Тоже важный вопрос.

Нода не нужна, если:

- логика используется ровно один раз
- код и так короткий и очевидный
- вы начинаете прятать слишком много простой логики в "магические" обёртки

Новичкам полезно держать баланс. Ноды это инструмент для упрощения кода, а не для усложнения.

---

## Что запомнить

- нода это способ описать, как получить одно значение из другого
- главный метод ноды в текущем API это `__compose__`
- ноды работают и в хендлерах, и в правилах
- по умолчанию ноды живут в пределах одного события
- если вы часто повторяете одну и ту же подготовку данных, попробуйте вынести её в ноду

[>> Next: Dispatch](6_dispatch.md)
