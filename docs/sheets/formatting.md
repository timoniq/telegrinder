# Formatting

Telegrinder has two builtin formatters:

* HTMLFormatter
* MarkdownFormatter

They can be imported as follows:

```python
from telegrinder.tools import HTMLFormatter, MarkdownFormatter
```

Formatter is derived from `str` and always implements these methods:

* `.bold()`
* `.italic()`
* `.underline()`
* `.strike()`
* `.link(href: str)`
* `.mention(user_id: int)`
* `.code_block()`
* `.code_block_with_lang()`
* `.code_inline()`
* `.escape()`

Formatter also has a property of parse mode string.

It can be accessed like this:

```python
HTMLFormatter.PARSE_MODE
```