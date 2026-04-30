# Working with text: formatting, localization

In bots, text is rarely just a plain string. Usually you need to:

- format messages
- escape user input
- reuse message templates
- localize responses

Telegrinder provides two comfortable layers for that:

- formatting helpers
- i18n through translator nodes

## Formatting

One of the most convenient options in telegrinder is the HTML formatting helper set.

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

To make Telegram interpret the markup correctly, it is common to set a default parse mode:

```python
from telegrinder.tools.formatting.html import HTML

api.default_params["parse_mode"] = HTML.PARSE_MODE
```

This is usually better than building raw HTML strings by hand because:

- it is harder to break the markup
- it is easier to compose text pieces

---

## Useful formatting helpers

Commonly used helpers include:

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

If user input goes into a formatted message, `escape(...)` is the one you should remember.

---

## Localization

Telegrinder has translator nodes for i18n. A basic setup looks like this:

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

What happens here:

- `BaseTranslator.configure(...)` points telegrinder at the translation files
- `KeySeparator` defines how nested keys are composed
- `BaseTranslator` is injected like a normal node

---

## Two translation styles

Translator nodes are commonly used in two ways.

### String template call

```python
return _("Hello, {name}!", name=user.full_name)
```

### Key access

```python
return _.im.fine()
```

The second style is especially nice when your translations are hierarchical.

---

## Organizing text

In practice it is useful to separate:

- `messages/` or `locales/` for translations
- `keyboards/` for button text
- constants for system messages

Once a bot grows, keeping every string inside handlers becomes painful even if you only support one language.

---

## Useful references

- [examples/formatting.py](https://github.com/timoniq/telegrinder/blob/dev/examples/formatting.py)
- [examples/i18n.py](https://github.com/timoniq/telegrinder/blob/dev/examples/i18n.py)
- [docs/tools/formatting.md](https://github.com/timoniq/telegrinder/blob/dev/docs/tools/formatting.md)

[>> Next: States: waiters, long states](9_states.md)
