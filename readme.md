# Telegrinder

Framework for effective and reliable telegram bot building.

Still in development.

* Type hinted
* Customizable and extensible
* Ready to use scenarios and rules
* Fast models built on msgspec
* Both low-level and high-level API

# Getting started

Install using PyPI:

```
pip install telegrinder
```

Basic example:

```python
import logging

from telegrinder import API, Telegrinder, Token, Message
from telegrinder.rules import Text
from telegrinder.tools import HTMLFormatter, bold

api = API(token=Token("123:TOKEN"))
bot = Telegrinder(api)
logging.basicConfig(level=logging.INFO)


@bot.on.message(Text("/start"))
async def start(message: Message):
    me = (await api.get_me()).unwrap()
    await message.answer(
        "Hello, I'm " + bold(me.first_name),
        parse_mode=HTMLFormatter.PARSE_MODE,
    )


bot.run_forever()
```

# Community

Join our [Telegram Chat](https://t.me/telegrinder_en).

# [Contributing](https://github.com/timoniq/telegrinder/blob/main/contributing.md)

# License

Telegrinder is [MIT licensed](./LICENSE)  
Copyright © 2022 [timoniq](https://github.com/timoniq)