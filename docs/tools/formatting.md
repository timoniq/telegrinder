# Formatting

Telegrinder provides a built-in HTML formatting toolkit. The current entrypoint is `HTML` plus helper functions from `telegrinder.tools.formatting`.

```python
from telegrinder.tools.formatting import HTML, bold, italic, mention
```

This toolkit is designed for building Telegram-ready HTML safely and compositionally instead of concatenating raw tags by hand.

## Basic usage

```python
from telegrinder.tools.formatting import HTML, bold, italic, mention

text = HTML << "Hello, " << mention("Arseny", user_id=549019276) << "! " << bold(italic("Welcome"))
```

The result is an `HTML` string object. To send it correctly, use:

```python
parse_mode=HTML.PARSE_MODE
```

For example:

```python
@bot.on.message(Text("/formatting"))
async def formatting(message: Message) -> None:
    await message.answer(
        HTML << "Hello, " << mention(message.from_user.first_name, user_id=message.from_user.id),
        parse_mode=HTML.PARSE_MODE,
    )
```

Reference: [examples/formatting.py](https://github.com/timoniq/telegrinder/blob/dev/examples/formatting.py)

---

## Available helpers

Core formatting helpers:

- `bold(...)`
- `italic(...)`
- `underline(...)`
- `strike(...)`
- `spoiler(...)`
- `code_inline(...)`
- `monospace(...)`
- `pre_code(...)`
- `blockquote(...)`
- `date_time(...)`
- `link(...)`
- `mention(...)`
- `tg_emoji(...)`
- `escape(...)`

Notes:

- `monospace` is an alias of `code_inline`
- `blockquote(..., expandable=True)` creates an expandable quote
- `pre_code(..., lang="python")` adds a language class for code blocks

## Helper examples

```python
from telegrinder.tools.formatting import (
    HTML,
    blockquote,
    bold,
    code_inline,
    link,
    mention,
    pre_code,
    tg_emoji,
)

text = HTML << blockquote("Quoted text")
code = pre_code("print('hello')", lang="python")
user = mention("arseny", user_id=549019276)
repo = link("https://github.com/timoniq/telegrinder", text="telegrinder")
emoji = tg_emoji("👍", emoji_id=5368324170671202286)
inline = code_inline("TOKEN")
```

## Escaping

Use `escape(...)` whenever user-controlled text is inserted into formatted output.

```python
from telegrinder.tools.formatting import HTML, bold, escape

safe = HTML << "User said: " << bold(escape(user_input))
```

If you use helpers like `bold(...)` or `mention(...)`, they already operate on safely escaped content, but explicit `escape(...)` is still a good habit when mixing plain strings and external input.

## Template formatting

`HTML` also supports template-based formatting through Python template strings.

```python
from telegrinder.tools.formatting import HTML

text = HTML(t"Hello, {name:bold}!")
```

Supported format specifiers map to built-in helper names:

- `bold`
- `italic`
- `underline`
- `strike`
- `spoiler`
- `code`
- `monospace`
- `blockquote`
- `expandable_blockquote`

You can combine them with `+`:

```python
text = HTML(t"Hello, {name:bold+underline}!")
```

This is especially convenient when you want interpolation and formatting in one place.

## Date and time formatting

Telegram supports special date/time entities, and telegrinder wraps them with `date_time(...)`.

```python
import datetime

from telegrinder.tools.formatting import date_time

text = date_time("tomorrow", datetime.datetime.now() + datetime.timedelta(days=1))
```

You can pass either a `datetime` or a Unix timestamp.

## Deep links

The formatting package also exports a large set of Telegram deep-link helpers, for example:

- `tg_bot_start_link`
- `tg_bot_startgroup_link`
- `tg_public_message_link`
- `tg_private_message_link`
- `tg_share_link`
- `tg_mention_link`

These helpers return links, and you can combine them with `link(...)` or embed them into your own formatted output.

## Parse mode constants

If you need parse mode constants explicitly, you can use:

```python
from telegrinder.tools.parse_mode import ParseMode
```

Available values include:

- `ParseMode.HTML`
- `ParseMode.MARKDOWNV2`

For the HTML formatter path, `HTML.PARSE_MODE` is usually the most direct choice.
