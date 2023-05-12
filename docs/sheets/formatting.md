# Formatting

Telegrinder has one builtin formatter:

* HTMLFormatter

It can be imported as follows:

```python
from telegrinder.tools import HTMLFormatter
```

Formatter is derived from `FormatString` to work string formatting with the following formats:

* `bold(string: str)`
* `italic(string: str)`
* `underline(string: str)`
* `strike(string: str)`
* `spoiler(string: str)`
* `link(href: str, string: str | None = None)`
* `mention(string: str, user_id: int)`
* `code_block(string: str)`
* `code_inline(string: str)`
* `program_code_block(string: str, lang: str)`
* `escape(string: str)`
  
Also formatter has a `.format(self, *args, **kwargs)` method for formatting a string with `{}`, it can support specifiers whose names are the same as the format names (other than special):

```python
from telegrinder.tools import HTMLFormatter

HTMLFormatter("Hello, {:bold}!").format("world")
```

Union formats:

```python
from telegrinder.tools import HTMLFormatter, bold, italic

HTMLFormatter("Hello, {:bold+underline}!").format("world")
HTMLFormatter("Hello, {}!").format(bold(italic("world")))
```

To use special formats, you have to use special dataclasses or functions:
* `Mention(string: str, user_id: int)`
* `Link(href: str, string: str | None = None)`
* `ProgramCodeBlock(string: str, lang: str)`

```python
from telegrinder.tools import HTMLFormatter, Mention, Link, ProgramCodeBlock

PYTHON_CODE_ECHO_BOT = """
from telegrinder import API, Telegrinder, Token, Message

bot = Telegrinder(API(Token.from_env("TOKEN")))


@bot.on.message()
async def echo(message: Message):
    await message.answer(message.text)


bot.run_forever()
"""

HTMLFormatter("{:bold} very nice telegram user!").format(Mention("arseny", 549019276))
HTMLFormatter("{:italic} very nice framework!").format(Link("https://github.com/timoniq/telegrinder", "telegrinder"))
HTMLFormatter("echo bot on telegrinder:\n{}").format(ProgramCodeBlock(PYTHON_CODE_ECHO_BOT, "python"))
```

HTMLFormatter also has a property of parse mode string.

It can be accessed like this:

```python
HTMLFormatter.PARSE_MODE
#> 'HTML'
```

And you can import `ParseMode` which has two properties:
* `MARKDOWNV2`
* `HTML`

```python
from telegrinder.tools import ParseMode
```
