# Работа с текстом: форматирование, локализация

Почти любой бот рано или поздно начинает жить на текстах.

Сначала всё просто:

- ответил на `/start`
- показал пару кнопок
- отправил короткое сообщение

А потом вдруг появляется:

- форматирование
- ссылки
- код-блоки
- упоминания пользователя
- много одинаковых текстов
- второй язык

В telegrinder для этого есть хорошие инструменты, и они довольно дружелюбны.

## Форматирование

Самый удобный путь в telegrinder это HTML formatting helpers.

```python
import datetime

from telegrinder import Message
from telegrinder.tools.formatting.html import HTML, bold, date_time, italic, mention


@bot.on.message(Text("/formatting"))
async def formatting(message: Message) -> None:
    # Комбинируем helpers как конструктор.
    await message.answer(bold(italic("Жирный и курсивный текст")))

    await message.answer(
        HTML
        << "Привет, "
        << mention(message.from_user.first_name, user_id=message.from_user.id)
        << "!"
    )

    await message.answer(
        # tg-time entity, Telegram сам красиво покажет дату.
        date_time("Завтра", datetime.datetime.now() + datetime.timedelta(days=1))
    )
```

Чтобы Telegram правильно понял разметку, обычно один раз задают parse mode по умолчанию:

```python
from telegrinder.tools.formatting.html import HTML

api.default_params["parse_mode"] = HTML.PARSE_MODE
```

После этого можно не передавать `parse_mode` в каждом сообщении заново.

> [!TIP]
> Если вы почти всегда отправляете HTML, поставьте `api.default_params["parse_mode"] = HTML.PARSE_MODE` в одном месте при инициализации. Это заметно уменьшает шум в коде.

---

## Самые полезные helper-функции

Чаще всего хватает вот этих:

- `bold(...)`
- `italic(...)`
- `underline(...)`
- `strike(...)`
- `spoiler(...)`
- `code_inline(...)`
- `pre_code(...)`
- `mention(...)`
- `link(...)`
- `escape(...)`

Вот небольшой "живой" кусок:

```python
from telegrinder.tools.formatting import HTML, bold, code_inline, link, spoiler


text = (
    HTML
    << "Документация: "
    << link("https://docs.python.org/3/", text="Python docs")
    << "\n"
    << "Токен: "
    << spoiler(code_inline("123:secret-token"))
    << "\n"
    << bold("Не показывай это никому.")
)
```

Такой стиль обычно читается намного лучше, чем ручная сборка HTML-тегов строками.

---

## Почему не стоит писать HTML руками

Можно, конечно, сделать так:

```python
text = "<b>Hello</b> <i>world</i>"
```

Но довольно быстро начинаются мелкие неприятности:

- где-то забыли экранировать ввод пользователя
- где-то сломали закрывающий тег
- где-то трудно понять, какая часть строки за что отвечает

Поэтому helpers удобнее почти всегда.

---

## `escape(...)` это ваш друг

Если в разметку попадает пользовательский ввод, его лучше экранировать.

```python
from telegrinder.tools.formatting import HTML, bold, escape


@bot.on.message()
async def echo_name(message: Message) -> None:
    unsafe_name = message.from_user.first_name

    await message.answer(
        HTML << "Твой ник: " << bold(escape(unsafe_name))
    )
```

Это особенно полезно, если имя пользователя содержит символы, которые Telegram может интерпретировать как HTML.

> [!TIP]

> Всё, что пришло от пользователя, по умолчанию считайте "небезопасной строкой", если вставляете это в форматированный текст.

---

## Пример с кодом

Если вы показываете пользователю фрагменты кода, удобнее использовать `pre_code(...)`.

```python
from telegrinder.tools.formatting import pre_code


snippet = pre_code(
    "print('Hello from telegrinder')",
    lang="python",
)
```

Это даёт красивый block code, который выглядит заметно лучше, чем просто обернуть код в тройные кавычки внутри строки.

---

## Локализация

Когда текстов становится много, а особенно если нужен второй язык, стоит познакомиться с translator nodes.

Базовый пример:

```python
from telegrinder import API, Telegrinder, Token
from telegrinder.node import BaseTranslator, I18NConfig, KeySeparator, UserSource
from telegrinder.rules import Text

bot = Telegrinder(API(Token.from_env()))

# Подключаем каталог переводов.
BaseTranslator.configure(I18NConfig(domain="messages", folder="examples/assets/i18n"))

# Разделитель нужен для вложенных ключей.
KeySeparator.set(" ")


@bot.on.message(Text("hi"))
async def hi(_: BaseTranslator) -> str:
    # Получаем перевод по ключу.
    return _.hi()


@bot.on.message(Text("hello"))
async def hello(_: BaseTranslator, user: UserSource) -> str:
    # Можно форматировать строку с параметрами.
    return _("Hello, {name}!", name=user.full_name)
```

Что здесь важно:

- `BaseTranslator` можно получать как обычную ноду
- переводы можно вызывать как по ключам, так и как шаблоны
- локализация перестаёт быть "отдельной магией" и встраивается в хендлеры естественно

---

## Два удобных стиля работы с переводами

### По ключу

```python
return _.im.fine()
```

Это удобно, когда у вас структурированные словари переводов.

### По шаблону

```python
return _("Hello, {name}!", name=user.full_name)
```

Это удобно, когда нужно быстро отдать фразу с параметрами.

На практике обычно используются оба подхода одновременно.

---

## Как не утонуть в текстах

Очень практический совет для новичка:

не храните все строки прямо в хендлерах слишком долго.

Минимально полезное разделение:

- `messages/` или `locales/` для переводов
- `keyboards/` для текста кнопок
- константы или helpers для системных сообщений

Сначала это кажется избыточным, но после пары десятков текстов структура начинает очень помогать.

---

## Небольшой практический шаблон

Если вы только начинаете, хорошая схема такая:

1. Для одного языка используйте formatting helpers.
2. Как только текстов становится много, начните выносить их из хендлеров.
3. Как только появляется второй язык, подключайте translator nodes.

Это нормальная эволюция. Не обязательно строить сложную i18n-систему в первый же день.

[>> Next: Стейты (состояния пользователя): waiters, длинные стейты](9_states.md)
