# Dispatch

Если ноды помогают подготовить данные, то `Dispatch` отвечает на другой вопрос: "куда вообще пойдёт событие и кто будет его обрабатывать?"

Когда бот маленький, об этом почти не думаешь. Есть `@bot.on.message(...)`, есть хендлеры, всё работает. Но как только файлов становится больше одного, dispatch становится очень важным.

## Самая короткая ментальная модель

Можно держать в голове вот такую схему:

- `Dispatch` собирает маршрутизацию
- внутри него живут `Router`
- внутри роутеров живут `View`
- внутри view живут хендлеры

То есть путь примерно такой:

`Dispatch -> Router -> View -> Handler`

Этой модели достаточно, чтобы не путаться дальше.

## Что такое `bot.on`

Когда вы пишете:

```python
@bot.on.message(...)
async def handler(...): ...
```

`bot.on` это и есть dispatch.

А `bot.on.message` это message-view основного роутера этого dispatch.

Проще говоря:

- `bot.on` — главный диспетчер вашего бота
- `bot.on.message` — место, куда вы складываете обработчики сообщений
- `bot.on.callback_query` — место для callback query

Для старта этого понимания более чем достаточно.

---

## Зачем вообще нужен Dispatch

Чтобы не держать весь бот в одном файле.

Почти любой бот быстро дорастает до такого состояния:

- отдельные хендлеры для старта
- отдельные для админки
- отдельные для платежей
- отдельные для inline-кнопок

Если всё это держать в одном `bot.py`, через какое-то время в файле становится просто тяжело ориентироваться.

Dispatch решает это очень просто: вы делите бота на логические куски и потом собираете их вместе.

---

## Минимальный dispatch

```python
from telegrinder import Dispatch, Message
from telegrinder.rules import Argument, Command, IsBot

dp = Dispatch(name="chat-utilities")


@dp.message(IsBot())
async def bot_message_handler(message: Message) -> None:
    # Обычный обработчик, только регистрируем его не в bot.on, а в локальном dispatch.
    await message.answer("Hey bot!")


@dp.message(
    Command(
        "repeat",
        Argument("text"),
        Argument("times", validators=[lambda s: int(s) if s.isdigit() else None], optional=True),
    )
)
async def command_handler(message: Message, text: str, times: int = 5) -> None:
    # В times попадёт либо число из команды, либо значение по умолчанию.
    await message.answer(", ".join([text] * times))
```

Такой `dp` уже можно вынести в отдельный файл и подключить к основному боту.

---

## Как подключить dispatch к боту

Например, пусть этот код лежит в `handlers/chat_utilities.py`.

Тогда сборка бота может выглядеть так:

```python
from handlers import chat_utilities
from telegrinder import API, Telegrinder, Token

api = API(Token("your-token-here"))
bot = Telegrinder(api)

# Подгружаем все роутеры и error-handlers из внешнего dispatch.
bot.on.load(chat_utilities.dp)

bot.run_forever()
```

На этом месте обычно приходит очень полезное ощущение: бот можно собирать из кусочков, а не писать как один длинный скрипт.

> [!TIP]
> Даже если у вас пока маленький бот, полезно рано вынести хотя бы `start`, `admin` и `callback_query` в разные файлы. Потом спасибо скажете сами себе.

---

## Где здесь роутеры

Сейчас в telegrinder важно понимать, что dispatch работает не "напрямую с хендлерами", а через роутеры.

У dispatch есть:

- `main_router`
- `routers` — очередь загруженных роутеров
- views вроде `message`, `callback_query`, `inline_query`, `media_group`, `event_error`, `raw`

Когда вы пишете:

```python
@bot.on.message(Text("/start"))
async def start(...): ...
```

по сути это регистрация в:

```python
bot.on.main_router.message
```

То есть основной роутер у вас уже есть, просто в обычной разработке его не всегда нужно трогать руками.

---

## Что такое View

View это объект для конкретного типа события.

Чаще всего вы будете видеть:

- `message`
- `callback_query`
- `inline_query`
- `media_group`
- `event_error`
- `raw`

У view внутри есть:

- фильтр уровня view
- список хендлеров
- middleware
- waiter machine

Для новичка полезно воспринимать view как "полку, на которую я складываю обработчики одного типа".

---

## Когда Router полезен отдельно

Иногда хочется явно выделить отдельную логическую зону. Например, админку.

Тогда можно создать роутер руками:

```python
from telegrinder import Dispatch, Message, Router
from telegrinder.rules import Text

admin_router = Router(name="admin")


@admin_router.message(Text("/ban"))
async def ban_handler(message: Message) -> None:
    # Весь admin-related код можно держать в отдельном роутере.
    await message.answer("Admin action")


admin = Dispatch(router=admin_router, name="admin-dispatch")
```

А потом подключить его как обычный dispatch:

```python
bot.on.load(admin)
```

Такой подход особенно приятен, когда в проекте есть чёткие домены:

- админка
- платежи
- onboarding
- игры
- модерация

---

## `load_many` и `load_from_dir`

Когда частей становится больше, собирать бот можно ещё удобнее.

### Несколько dispatch сразу

```python
bot.on.load_many(users.dp, payments.dp, admin.dp)
```

Это полезно, когда вы уже импортировали нужные модули вручную и хотите собрать всё в одном месте.

### Автозагрузка из директории

```python
bot.on.load_from_dir("handlers", recursive=True)
```

Здесь telegrinder:

- проходит по Python-файлам
- импортирует их
- ищет глобальные переменные с экземплярами `Dispatch`
- подгружает их в основной dispatch

Это удобно для "blueprint-style" структуры проекта.

Вот минимальная идея:

```python
# handlers/start.py
from telegrinder import Dispatch

dp = Dispatch(name="start")
```

```python
# bot.py
bot.on.load_from_dir("handlers", recursive=True)
```

> [!TIP]

> `load_from_dir()` удобен, когда структура проекта уже устоялась. На старте многим проще и понятнее сначала использовать обычный `load_many(...)`.

---

## Как dispatch обрабатывает событие

Без лишних деталей процесс примерно такой:

1. `Dispatch.feed()` получает `API` и `Update`
2. создаётся `Context`
3. запускаются middleware dispatch уровня
4. dispatch проходит по своим роутерам
5. каждый роутер проверяет подходящие views
6. подходящий view запускает хендлеры
7. если что-то падает, это можно обработать через `event_error`

Новичку не нужно помнить все внутренности. Достаточно понимать, что dispatch это не просто "список функций", а довольно аккуратный конвейер.

---

## Пример структуры проекта

Вот хороший минимальный старт:

```text
mybot/
  bot.py
  handlers/
    start.py
    admin.py
    payments.py
  keyboards/
    menu.py
  nodes/
    db.py
  rules/
    is_admin.py
```

Такой проект растёт заметно спокойнее, чем один огромный файл на сотни строк.

---

## Что запомнить

- `Dispatch` нужен для маршрутизации и разделения кода
- внутри dispatch живут роутеры, а внутри роутеров живут views
- `bot.on.message(...)` это по сути регистрация в `main_router.message`
- `load`, `load_many` и `load_from_dir` помогают собирать проект из нескольких частей
- если бот начал расти, лучше разделять его раньше, а не позже

[>> Next: Клавиатура, обработка полезной нагрузки](7_keyboard.md)
