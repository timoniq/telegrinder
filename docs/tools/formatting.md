# Formatting

Telegrinder has builtin formatter `HTMLFormatter`.
It can be imported as follows:

```python
from telegrinder.tools.formatting import HTMLFormatter
```

Formatter is derived from `FormatString` to work string formatting with the following formats:

* `bold(string: str) -> TagFormat`
* `italic(string: str) -> TagFormat`
* `underline(string: str) -> TagFormat`
* `strike(string: str) -> TagFormat`
* `spoiler(string: str) -> TagFormat`
* `link(href: str, string: str | None = None) -> TagFormat`
* `mention(string: str, user_id: int) -> TagFormat`
* `code_block(string: str) -> TagFormat`
* `code_inline(string: str) -> TagFormat`
* `program_code_block(string: str, lang: str) -> TagFormat`
* `escape(string: str) -> EscapedString`

```python
from telegrinder.tools.formatting import HTMLFormatter, bold, spoiler

HTMLFormatter(spoiler("I want tea."))  # if you want use only formatting functions
"Just string | " + bold("bold string")  # if you want concat str with formatting functions or HTMLFormatter instance (there's no difference between right or left)
```
  
Also formatter has a `.format(self, *args, **kwargs)` method for formatting a string with `{}`, it can support specifiers whose names are the same as the format names (other than special):

```python
from telegrinder.tools.formatting import HTMLFormatter

HTMLFormatter("Hello, {:bold}!").format("world")
```

Union formats:

```python
from telegrinder.tools.formatting import HTMLFormatter, bold, italic

HTMLFormatter("Hello, {:bold+underline}!").format("world")
HTMLFormatter("Hello, {}!").format(bold(italic("world")))
```

To use special formats, you have to use special dataclasses or functions:
* `Mention(string: str, user_id: int)`
* `Link(href: str, string: str | None = None)`
* `ProgramCodeBlock(string: str, lang: str)`

```python
from telegrinder.tools.formatting import HTMLFormatter, Mention, Link, ProgramCodeBlock

PYTHON_CODE_ECHO_BOT = """
from telegrinder import API, Telegrinder, Token, Message
from telegrinder.tools.formatting import HTMLFormatter, bold

bot = Telegrinder(API(Token.from_env("TOKEN")))


@bot.on.message()
async def echo(message: Message):
    await message.answer(HTMLFormatter(bold(message.text)))


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
