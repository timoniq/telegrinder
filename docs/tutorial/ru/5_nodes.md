# Ноды

Ноды — это один из самых важных строительных блоков в telegrinder. Они — как простые, легко создаваемые и соединяемые между собой кусочки конструктора. Именно поэтому мы их так и называем — ноды.

Нода — это то, что мы составляем из других нод.

Например, из сообщения (message) мы можем составить текст (text) или пользователя (user).

Из текста можно составить целое число, если текст состоит только из цифр.

Есть корневые объекты, из которых можно составить всё остальное. В классическом боте на telegrinder это экземпляры `Update`, `API` и `Context`.

`Update` — это то, что пришло в наш бот. Оно всегда связано с каким-то `API`. `Context` — просто удобное хранилище, низкоуровневый объект, в котором хранится вся информация о пути обработки события.

---

К этому моменту вы, вероятно, уже уловили простую идею, которая лежит в основе нод. Давай разберёмся, как реализовать свою ноду.

В telegrinder нужно просто написать класс, реализующий класс-метод `compose`. Метод compose должен возвращать экземпляр ноды. И, что важно, он может принимать в качестве аргументов другие ноды. Они будут автоматически связаны с нодой и решены оптимизированным образом, когда наступит нужный момент.

В telegrinder есть несколько типов нод:

* Скалярная нода (scalar node) — нода, которая просто реализует метод compose для значения другого типа. Например, нода `Text` — это скалярная нода. Она возвращает `str`. И благодаря внутренней магии telegrinder, `Text` и возвращаемый тип `str` у метода `compose` распознаются как взаимозаменяемые типы.

* Дата-нода (data node) — нода, которая является датаклассом. Просто комбинация, которая часто бывает полезной.

* Полиморфная нода (polymorphic node) — нода с несколькими реализациями. Например, и сообщение, и callback-запрос содержат отправителя. Мы можем реализовать, как получать пользователя из каждого типа события, и получить одну полиморфную ноду, которая позволяет удобно извлекать пользователя из разных типов событий.

* Любая нода — любой класс, который реализует метод compose. Если есть `compose` — это нода.

---

Давай научимся писать ноды на примере:

```python
# telegrinder.node.text
from telegrinder.node import scalar_node

@scalar_node
class Text:
    @classmethod
    def compose(cls, message: Message) -> str:
        if not message.text:
            raise ComposeError("Message has no text.")
        return message.text.unwrap()
```

Что происходит в этом коде?

Мы объявляем реализацию скалярной ноды `Text`. Магически определяется, что скалярное значение `Text` будет `str` по типу возвращаемого значения из метода `compose` (`-> str`).

`compose` должен вернуть строку текста или выбросить ошибку `ComposeError`.

Теперь её можно использовать:

```python
@bot.on.message()
async def text_message_handler(message: Message, text: Text):
    await message.answer(text.lower())
```

Тот же самый эхо-бот, что мы сделали в начале туториала, но гораздо элегантнее.

А как насчёт правил? Время раскрыть секрет: это работает везде, включая правила:


```python
class TextIsOfLength(ABCRule):
    def __init__(self, l: int):
        self.l = l

    async def check(self, text: Text) -> bool:
        return len(text) == self.l


@bot.on.message(TextIsOfLength(6))
async def six_handler():
    return "Love messages of this length.."
```

---

Отлично, теперь, когда мы знаем основы, можем написать ещё ноды:

```python
@scalar_node
class TextInteger:
    @classmethod
    def compose(cls, text: Text) -> int:
        if not text.isdigit():
            raise ComposeError("Text is not digit.")
        return int(text)
```

Получается цепочка, правда?

Мы только что сделали новую ноду, которая композирует ноду, созданную ранее. `TextInteger` работает с сообщениями, содержащими текст, где текст состоит из цифр.

```python
pi = 3.141592653589793238

@bot.on.message()
async def number_handler(r: TextInteger):
    return f"Thats awesome! So if R = {r}, C = {2 * pi * r}"
```

## Области

Когда ноды начинают включать более сложную логику (например, подключение к базе данных или доступ к хранилищу), может понадобиться контролировать область ноды. Это просто. В telegrinder есть 3 области:

* На событие (per event) — нода создаётся для каждого события, если во время компоновки нода уже была создана, она переиспользуется и не создаётся повторно. Это поведение по умолчанию.

* На вызов (per call) — нода создаётся каждый раз, когда какая-либо нода требует её для компоновки, либо когда её нужно передать в хендлер.

* Глобальная (global) — некоторые ноды должны быть созданы только один раз на всю программу, а затем храниться и переиспользоваться при необходимости.


Посмотрим примеры нод для каждого типа области.

Подключение к базе данных можно элегантно обрабатывать с помощью нод:

```python
from telegrinder.node import scalar_node, per_call

@scalar_node
@per_call
class DB:
    @classmethod
    async def compose(cls) -> typing.AsyncGenerator[aiosqlite.Connection, None]:
        connection = await aiosqlite.connect("test.db")
        logger.info("Opening connection")
        yield connection
        logger.info("Closing connection")
        await connection.close()

@bot.on.message()
async def some_handler(text: Text, connection: DB):
    ...
```

Тут мы также используем замечательную особенность нод — возможность быть генератором. Мы можем что-то завершить после того, как обработка события завершена: просто используем `yield`, чтобы передать значение процессору, а после обработки управление вернётся обратно, и мы закроем соединение с базой данных (например).

```python
from telegrinder.node import DataNode, global_node

@global_node
class Settings(DataNode):
    api_url: str
    some_secret: str

    @classmethod
    def compose(cls) -> "Settings":
        return cls(api_url=env["API_URL"], some_secret=env["SOME_SECRET"])


@scalar_node
@global_node
class Secret:
    @classmethod
    def compose(cls) -> str:
        return generate_secret(16)
```

Удачи с нодами!

[>> Next: Dispatch](6_dispatch.md)
