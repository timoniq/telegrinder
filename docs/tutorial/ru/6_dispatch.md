# Dispatch

`Dispatch` в telegrinder отвечает за маршрутизацию событий. Если ноды отвечают за зависимости, то dispatch отвечает за то, куда вообще попадёт событие и какой набор обработчиков будет проверяться.

Раньше достаточно было думать о dispatch как о контейнере с `message`, `callback_query` и другими views. Это по-прежнему верно, но сейчас важно понимать ещё один слой: внутри dispatch живут роутеры.

## Из чего состоит Dispatch

У dispatch есть несколько ключевых частей:

- `main_router` — основной роутер
- `routers` — очередь всех загруженных роутеров
- views вроде `message`, `callback_query`, `inline_query`, `media_group`, `event_error`, `raw`
- `middlewares`
- `error_handler`
- методы загрузки: `load`, `load_many`, `load_from_dir`

Когда вы пишете:

```python
@bot.on.message(...)
async def handler(...): ...
```

вы на самом деле регистрируете обработчик во `view` `message` основного роутера `bot.on.main_router`.

То есть концептуально:

- `bot.on` — это `Dispatch`
- `bot.on.message` — это `bot.on.main_router.message`
- `bot.on.callback_query` — это `bot.on.main_router.callback_query`

---

## Что такое Router

`Router` хранит набор views и умеет попытаться обработать один апдейт.

Схема обработки такая:

1. `Dispatch.feed()` получает `API` и `Update`
2. dispatch создаёт `Context` и запускает middleware
3. dispatch проходит по своим роутерам
4. каждый `Router` проверяет подходящие event views
5. подходящий `View` запускает свои хендлеры
6. если в роутере возникла ошибка, её можно обработать через `event_error`

Важно: dispatch загружает и запускает не “голые функции”, а именно роутеры со views внутри.

---

## Views

View — это объект, на котором вы регистрируете обработчики для конкретного типа события.

Чаще всего используются:

- `message`
- `callback_query`
- `inline_query`
- `media_group`
- `event_error`
- `raw`

У каждого view есть:

- фильтр уровня view
- список хендлеров
- waiter machine
- middleware уровня view

Именно поэтому удобно мыслить так: router хранит views, а view хранит хендлеры.

---

## Базовый dispatch

```python
from telegrinder import Dispatch, Message
from telegrinder.rules import Argument, Command, IsBot

dp = Dispatch(name="chat-utilities")


@dp.message(IsBot())
async def bot_message_handler(message: Message) -> None:
    await message.answer("Hey bot!")


@dp.message(
    Command(
        "repeat",
        Argument("text"),
        Argument("times", validators=[lambda s: int(s) if s.isdigit() else None], optional=True),
    )
)
async def command_handler(message: Message, text: str, times: int = 5) -> None:
    await message.answer(", ".join([text] * times))
```

Такой код уже готов к подключению в основной бот.

---

## Подключение dispatch к боту

Пусть этот код лежит в `handlers/chat_utilities.py`. Тогда основной бот может собрать всё так:

```python
from handlers import chat_utilities
from telegrinder import API, Telegrinder, Token

api = API(Token("your-token-here"))
bot = Telegrinder(api)

bot.on.load(chat_utilities.dp)
bot.run_forever()
```

`load()` делает не копирование текста и не импорт обработчиков по одному. Он добавляет роутеры внешнего dispatch в очередь роутеров текущего dispatch, а ещё объединяет error views.

---

## Когда нужен Router отдельно

Если вы хотите явно отделять логические зоны, можно создавать роутеры самостоятельно:

```python
from telegrinder import Dispatch, Message, Router
from telegrinder.rules import Text

admin_router = Router(name="admin")


@admin_router.message(Text("/ban"))
async def ban_handler(message: Message) -> None:
    await message.answer("Admin action")


admin = Dispatch(router=admin_router, name="admin-dispatch")
```

После этого `admin` можно загрузить так же через `bot.on.load(admin)`.

Это удобно, когда вы хотите отдельно именовать и группировать куски маршрутизации: например, `admin`, `payments`, `moderation`, `games`.

---

## load_many и load_from_dir

Если dispatch много, есть два удобных способа собрать приложение.

### Загрузить несколько dispatch сразу

```python
bot.on.load_many(users.dp, payments.dp, admin.dp)
```

### Загрузить все dispatch из директории

```python
bot.on.load_from_dir("handlers", recursive=True)
```

`load_from_dir()` импортирует Python-модули из папки, ищет в них глобальные переменные с экземплярами `Dispatch` и загружает их.

Пример есть в [examples/blueprint_bot/__main__.py](https://github.com/timoniq/telegrinder/blob/dev/examples/blueprint_bot/__main__.py).

---

## Как лучше делить код

Рабочий минимальный вариант структуры:

- `bot.py` или `main.py` — сборка приложения
- `handlers/` — dispatch по доменам
- `keyboards/` — клавиатуры
- `rules/` — кастомные правила
- `nodes/` — кастомные ноды

Например:

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

Такую структуру проще масштабировать, чем один большой файл с десятками обработчиков.

---

## Что запомнить

- `Dispatch` маршрутизирует события
- внутри dispatch теперь важны не только views, но и `Router`
- views принадлежат роутеру, а хендлеры принадлежат views
- `bot.on.message(...)` регистрирует обработчик в `main_router.message`
- `load`, `load_many`, `load_from_dir` собирают приложение из нескольких dispatch

[>> Next: Клавиатура, обработка полезной нагрузки](7_keyboard.md)
