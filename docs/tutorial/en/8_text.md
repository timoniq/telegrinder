# Working with text: formatting, localization

Almost every bot eventually becomes text-heavy.

At first it feels simple:

- reply to `/start`
- show a couple of buttons
- send a short message

And then suddenly you need:

- formatting
- links
- code blocks
- user mentions
- many repeated texts
- a second language

Telegrinder has good tools for this, and they are fairly pleasant to use.

## Formatting

The most comfortable path in telegrinder is the HTML formatting helper set.

```python
import datetime

from telegrinder import Message
from telegrinder.tools.formatting.html import HTML, bold, date_time, italic, mention


@bot.on.message(Text("/formatting"))
async def formatting(message: Message) -> None:
    # Compose helpers like building blocks.
    await message.answer(bold(italic("Bold and italic text")))

    await message.answer(
        HTML
        << "Hello, "
        << mention(message.from_user.first_name, user_id=message.from_user.id)
        << "!"
    )

    await message.answer(
        # Telegram will render this as a proper date/time entity.
        date_time("Tomorrow", datetime.datetime.now() + datetime.timedelta(days=1))
    )
```

To make Telegram interpret the markup correctly, you usually set the default parse mode once:

```python
from telegrinder.tools.formatting.html import HTML

api.default_params["parse_mode"] = HTML.PARSE_MODE
```

Then you do not need to pass `parse_mode` in every single message.

> [!TIP]
> Life hack:
> If your bot mostly sends HTML-formatted text, set `api.default_params["parse_mode"] = HTML.PARSE_MODE` once during initialization. It removes a lot of repetitive noise.

---

## The most useful helpers

In practice these are the ones you will use most often:

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

A tiny real-looking snippet:

```python
from telegrinder.tools.formatting import HTML, bold, code_inline, link, spoiler


text = (
    HTML
    << "Documentation: "
    << link("https://docs.python.org/3/", text="Python docs")
    << "\n"
    << "Token: "
    << spoiler(code_inline("123:secret-token"))
    << "\n"
    << bold("Do not share this with anyone.")
)
```

This tends to stay much easier to read than hand-written HTML strings.

---

## Why writing raw HTML by hand gets annoying

Yes, you can do this:

```python
text = "<b>Hello</b> <i>world</i>"
```

But small problems appear quickly:

- user input was not escaped
- a closing tag is easy to miss
- it becomes harder to see what each piece of the string is doing

That is why helpers are usually worth it.

---

## `escape(...)` is your friend

If user-controlled text goes into formatted output, escaping is a very good habit.

```python
from telegrinder.tools.formatting import HTML, bold, escape


@bot.on.message()
async def echo_name(message: Message) -> None:
    unsafe_name = message.from_user.first_name

    await message.answer(
        HTML << "Your nickname: " << bold(escape(unsafe_name))
    )
```

This becomes especially important when user names contain symbols that Telegram could interpret as markup.

> [!TIP]
> Treat all user-provided text as unsafe by default if you place it inside formatted output.

---

## Example with code blocks

If you need to show code to the user, `pre_code(...)` is usually the nicest choice.

```python
from telegrinder.tools.formatting import pre_code


snippet = pre_code(
    "print('Hello from telegrinder')",
    lang="python",
)
```

This gives you a proper block of code instead of just a plain string that happens to contain indentation.

---

## Localization

Once there are many texts, and especially once a second language appears, translator nodes become useful.

A basic example:

```python
from telegrinder import API, Telegrinder, Token
from telegrinder.node import BaseTranslator, I18NConfig, KeySeparator, UserSource
from telegrinder.rules import Text

bot = Telegrinder(API(Token.from_env()))

# Point telegrinder at your translation directory.
BaseTranslator.configure(I18NConfig(domain="messages", folder="examples/assets/i18n"))

# Separator for nested keys.
KeySeparator.set(" ")


@bot.on.message(Text("hi"))
async def hi(_: BaseTranslator) -> str:
    # Translate by key.
    return _.hi()


@bot.on.message(Text("hello"))
async def hello(_: BaseTranslator, user: UserSource) -> str:
    # Or translate with parameters.
    return _("Hello, {name}!", name=user.full_name)
```

What matters here:

- `BaseTranslator` is just another node you can inject
- translations can be used by key or as templates
- localization becomes part of normal handler code instead of a separate special subsystem

---

## Two useful translation styles

### By key

```python
return _.im.fine()
```

This is nice when translations are stored in a structured way.

### By template

```python
return _("Hello, {name}!", name=user.full_name)
```

This is convenient when you want a quick phrase with parameters.

In real projects, both styles are often used together.

---

## How not to drown in text

Very practical beginner advice:

do not keep every text directly inside handlers for too long.

A minimal useful separation is:

- `messages/` or `locales/` for translations
- `keyboards/` for button text
- constants or helpers for system messages

At first that can feel unnecessary, but after a few dozen messages it starts paying off quickly.

---

## A small practical path

If you are just getting started, a good progression is:

1. Use formatting helpers for one-language text.
2. Once texts grow in number, move them out of handlers.
3. Once you need another language, bring in translator nodes.

That is a perfectly normal evolution. You do not need a heavy i18n setup on day one.

[>> Next: States: waiters, long states](9_states.md)
