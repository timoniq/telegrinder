# Dispatch

В этой статье мы рассмотрим один из основных компонентов telegrinder — `Dispatch`. Он служит контейнером и маршрутизатором для всех наших событий.

Для начинающего пользователя, который только знакомится с основами, важно знать, что `Dispatch` помогает разделять код и, таким образом, строить аккуратную архитектуру бота. Это потому, что `Dispatch` реализует логику объединения — один диспетчер можно легко загрузить в другой.

В предыдущих частях урока мы уже использовали диспетчер по умолчанию. Главный диспетчер скрыт внутри экземпляра `bot.on`. `bot.on` — это, по сути, диспетчер, в который мы будем загружать все остальные части нашего бота.

Внутри диспетчера обычно находятся:

* Представления (views): `message`, `callback_query` и другие

* Методы загрузки. С помощью `dispatch.load(another_dispatch)` мы можем легко загрузить всё из `another_dispatch` в `dispatch`.

* Метод `feed`. Этот метод принимает модель события и делает всю работу по передаче её в финальный обработчик.

Также существуют методы `load_many` и `load_from_dir` для более быстрой сборки диспетчера.

---

Теперь, когда мы знаем, что такое диспетчер, давайте напишем свой!

```python
from telegrinder import Dispatch, Message
from telegrinder.rules import IsBot, Command, Argument

dp = Dispatch()

@dp.message(IsBot())
async def bot_message_handler(m: Message):
    await m.api.send_message(
        chat_id=m.chat_id,
        text="Hey bot!",
    )

@dp.message(
    Command(
        "repeat",
        Argument("string"),
        Argument("times", [lambda s: int(s) if s.isdigit() else None], optional=True),
    ),
)
async def command_handler(m: Message, string: str, times: int = 5):
    await m.answer(", ".join([string] * times))
```

Готово! Это почти как обычный бот, но мы уже работаем через `bot.on`.

Допустим, у нас есть этот код в файле `handlers/chat_utilities.py`.

Теперь мы хотим загрузить этот диспетчер в основной диспетчер нашего бота вот так:

```python
from handlers import chat_utilities

api = API(Token("your-token-here"))
bot = Bot(api)

bot.on.load(chat_utilities.dp)

bot.run_forever()
```

Вот и всё. Только что написанный диспетчер был загружен в основной диспетчер бота. Видите, какие возможности для разделения кода открываются?

Например, можно создать папку `handlers` для диспетчеров с обработчиками, добавить папки `nodes` и `rules`. Бот можно собрать в файле `main.py` или `bot.py`. Это очень просто! Найдите подходящую структуру для себя. Это сильно поможет в удобной организации проекта.

Возможно, вам также стоит заранее зарезервировать место для папок `keyboards` и `messages`. Скоро мы к ним перейдём `>_o

[>> Next: Клавиатура, обработка полезной нагрузки](7_keyboard.md)
