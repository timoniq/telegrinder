# Formatting

A built-in formatter:
```python
from telegrinder.tools.formatting import HTMLFormatter
```

`HTMLFormatter` is derived from `FormatString` to work string formatting with the following formats:
* `bold(string: str) -> TagFormat` | **bold text**
* `block_quote(string: str, expandable: bool = False) -> TagFormat` | quoted text
* `code_inline(string: str) -> TagFormat` | `inline text`
* `escape(string: str) -> EscapedString` | escaped string for HTML
* `italic(string: str) -> TagFormat` | __italic text__
* `link(href: str, string: str | None = None) -> TagFormat` | https://link
* `mention(string: str, user_id: int) -> TagFormat` | text url `tg://user?id=user_id` by `string`
* `pre_code(string: str, lang: str | ProgrammingLanguage | None = None) -> TagFormat` | ```pre code```
* `spoiler(string: str) -> TagFormat` -> ||spoiler text||
* `strike(string: str) -> TagFormat` -> ~~strikethrough text~~
* `tg_emoji(string: str, emoji_id: int) -> TagFormat` | telegram emoji by emoji id
* `underline(string: str) -> TagFormat` -> <u>underline text</u>

```python
from telegrinder.tools.formatting import HTMLFormatter, bold, spoiler

HTMLFormatter(spoiler("I want tea."))  # if you want use only formatting functions
"Just string | " + bold("bold string")  # if you want concat str with formatting functions or HTMLFormatter instance (there's no difference between right or left)
```

`HTMLFormatter` has a `.format(self, *args, **kwargs)` method for formatting a string with `{}`, it can support specifiers whose names are the same as the format names (other than special):

```python
from telegrinder.tools.formatting import HTMLFormatter

HTMLFormatter("Hello, {:bold}!").format("world")
```

Union formats by `+` separator:

```python
from telegrinder.tools.formatting import HTMLFormatter, bold, italic

HTMLFormatter("Hello, {:bold+underline}!").format("world")
HTMLFormatter("Hello, {}!").format(bold(italic("world")))
```

Special formats:
* `Base` -> This class is inherited into other dataclasses to implement special formats.
* `Link(href: str, string: str | None = None)` -> `link`
* `Mention(string: str, user_id: int)` -> `mention`
* `PreCode(string: str, lang: str | ProgrammingLanguage | None = None)` -> `pre_code`
* `BlockQuote(string: str, expandable: bool = False)` -> `block_quote`
* `TgEmoji(string: str, emoji_id: int)` -> `tg_emoji`

```python
from telegrinder.tools.formatting import HTMLFormatter, Mention, Link, CodeBlock
from telegrinder.types.enums import ProgrammingLanguage

PYTHON_CODE_ECHO_BOT = """
from telegrinder import API, Telegrinder, Token, Message
from telegrinder.tools.formatting import HTMLFormatter, bold

bot = Telegrinder(API(Token.from_env("TOKEN")))


@bot.on.message()
async def echo(message: Message):
    await message.answer(
        HTMLFormatter(bold(message.text)),
        parse_mode=HTMLFormatter.PARSE_MODE,
    )


bot.run_forever()
"""

HTMLFormatter("{:bold} very nice telegram user!").format(Mention("arseny", 549019276))

HTMLFormatter("{:italic} very nice framework!").format(Link("https://github.com/timoniq/telegrinder", "telegrinder"))

HTMLFormatter("Echo bot on python framework telegrinder:\n{}").format(PreCode(PYTHON_CODE_ECHO_BOT, ProgrammingLanguage.PYTHON))

HTMLFormatter("I {} telegrinder!").format(TgEmoji("👍", 5368324170671202286))
```

`HTMLFormatter` also has a property of parse mode string:

```python
HTMLFormatter.PARSE_MODE
#> 'HTML'
```

`ParseMode` which has two properties:
* `MARKDOWNV2`
* `HTML`

```python
from telegrinder.tools.parse_mode import ParseMode
```
