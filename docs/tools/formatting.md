# Formatting

Telegrinder has builtin formatter `HTMLFormatter`.
It can be imported as follows:

```python
from telegrinder.tools.formatting import HTMLFormatter
```

Formatter is derived from `FormatString` to work string formatting with the following formats:

* `block_quote(string: str) -> TagFormat` | `quote text`
* `bold(string: str) -> TagFormat` | **bold text**
* `channel_boost_link(channel_id: str | int, string: str | None = None) -> TagFormat` | tg://resolve?domain=channel123&boost
* `code_inline` | `inline text`
* `escape(string: str) -> EscapedString` | escaping string
* `italic(string: str) -> TagFormat` | __italic text__
* `link(href: str, string: str | None = None) -> TagFormat` | https://link
* `mention(string: str, user_id: int) -> TagFormat` | mention entity 
* `pre_code(string: str, lang: str | ProgrammingLanguage | None = None) -> TagFormat` | ```pre code```
* `resolve_domain(username: str, string: str | None = None) -> TagFormat` | tg://resolve?domain=username
* `spoiler(string: str) -> TagFormat` -> ||spoiler text||
* `start_bot_link(bot_id: str | int, data: str, string: str | None = None) -> TagFormat` | tg://resolve?domain=bot123&start=data
* `start_group_link(bot_id: str | int, data: str, string: str | None = None) -> TagFormat` | tg://resolve?domain=bot123&startgroup=data
* `strike(string: str) -> TagFormat` -> ~~strikethrough text~~
* `tg_emoji(string: str, emoji_id: int) -> TagFormat` | telegram emoji by emoji id
* `underline(string: str) -> TagFormat` -> <u>underline text</u>

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

To use special formats, you have to use special dataclasses:
* `BaseSpecFormat` -> This class is inherited into other dataclasses to implement special formats.
* `ChannelBoostLink(channel_id: str | int, string: str | None = None)` -> `channel_boost_link`
* `InviteChatLink(invite_link: str, string: str | None = None)` -> `invite_chat_link`
* `Link(href: str, string: str | None = None)` -> `link`
* `Mention(string: str, user_id: int)` -> `mention`
* `PreCode(string: str, lang: str | ProgrammingLanguage | None = None)` -> `pre_code`
* `ResolveDomain(username: str, string: str | None = None)` -> `resolve_domain`
* `StartBotLink(bot_id: str | int, data: str, string: str | None = None)` -> `start_bot_link`
* `StartGroupLink(bot_id: str | int, data: str, string: str | None = None)` -> `start_group_link`
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

HTMLFormatter("Cool telegram chat: {:bold+underline}").format(ResolveDomain("botoforum", "botoforum chat"))

HTMLFormatter("Please, boost {:bold+italic+underline} ^_^").format(ChannelBoostLink("hurricaneivykiosk", "Arseny's channel"))

HTMLFormatter("start game in the {:spoiler}").format(StartBotLink("telegrinder_bot", "game", "bot ^_^"))

HTMLFormatter("Get a bonus from the {:italic} in the chosen group").format(StartGroupLink("nice123_bot", "get_bonus", "nice cool bot"))

HTMLFormatter("Join our {:bold+underline}").format(InviteChatLink("+kMj2234KklsSka2-", "chat"))
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
