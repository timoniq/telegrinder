# Работа с текстом: форматирование, локализация

В ботах текст почти никогда не бывает “просто строкой”. Обычно нужно:

- форматировать сообщения
- экранировать пользовательский ввод
- переиспользовать шаблоны
- локализовать ответы

В telegrinder для этого есть два удобных слоя:

- formatting helpers
- i18n через translator nodes

## Форматирование

Один из самых удобных вариантов в telegrinder это HTML-formatting helpers.

```python
import datetime

from telegrinder import Message
from telegrinder.tools.formatting.html import HTML, bold, date_time, italic, mention


@bot.on.message(Text("/formatting"))
async def formatting(message: Message) -> None:
    await message.answer(bold(italic("bold italic text")))
    await message.answer(HTML << "Hello, " << mention(message.from_user.first_name, user_id=message.from_user.id))
    await message.answer(date_time("tomorrow", datetime.datetime.now() + datetime.timedelta(days=1)))
```

Чтобы Telegram правильно интерпретировал разметку, обычно задают `parse_mode` у API:

```python
from telegrinder.tools.formatting.html import HTML

api.default_params["parse_mode"] = HTML.PARSE_MODE
```

Такой подход удобнее ручной сборки HTML-строк по двум причинам:

- меньше шанс сломать разметку
- проще комбинировать куски текста

---

## Полезные функции форматирования

Часто используются:

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

Если в сообщение попадает пользовательский текст, не забывайте про `escape(...)`.

---

## Локализация

Для локализации в telegrinder есть translator nodes. Базовый сценарий выглядит так:

```python
from telegrinder import API, Telegrinder, Token
from telegrinder.node import BaseTranslator, I18NConfig, KeySeparator, UserSource
from telegrinder.rules import Text

bot = Telegrinder(API(Token.from_env()))

BaseTranslator.configure(I18NConfig(domain="messages", folder="examples/assets/i18n"))
KeySeparator.set(" ")


@bot.on.message(Text("hi"))
async def hi(_: BaseTranslator) -> str:
    return _.hi()


@bot.on.message(Text("hello"))
async def hello(_: BaseTranslator, user: UserSource) -> str:
    return _("Hello, {name}!", name=user.full_name)
```

Что здесь происходит:

- `BaseTranslator.configure(...)` подключает каталог с переводами
- `KeySeparator` определяет, как собираются вложенные ключи
- `BaseTranslator` можно просто получить как ноду в хендлере

---

## Два стиля обращения к переводам

У translator node есть два распространённых режима работы.

### Вызов по строке-шаблону

```python
return _("Hello, {name}!", name=user.full_name)
```

### Вызов по ключу

```python
return _.im.fine()
```

Второй стиль особенно удобен, когда переводы организованы иерархически.

---

## Как хранить тексты

Практически полезно отделять:

- `messages/` или `locales/` для переводов
- `keyboards/` для текста кнопок
- константы для системных сообщений

Если бот вырастает, не стоит хранить все строки прямо в обработчиках. Даже без многоязычности это быстро начинает мешать.

---

## Что посмотреть в примерах

- [examples/formatting.py](https://github.com/timoniq/telegrinder/blob/dev/examples/formatting.py)
- [examples/i18n.py](https://github.com/timoniq/telegrinder/blob/dev/examples/i18n.py)
- [docs/tools/formatting.md](https://github.com/timoniq/telegrinder/blob/dev/docs/tools/formatting.md)

[>> Next: Стейты (состояния пользователя): waiters, длинные стейты](9_states.md)
