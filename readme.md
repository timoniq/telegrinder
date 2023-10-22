# telegrinder

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

api = API(token=Token("123:token"))
bot = Telegrinder(api)
logging.basicConfig(level=logging.INFO)


@bot.on.message(Text("/start"))
async def start(message: Message):
    me = (await api.get_me()).unwrap()
    await message.answer(
        f"Hello, {message.from_user.first_name}! I'm {me.first_name}"
    )


bot.run_forever()
```

# Documentation

[Readthedocs](https://telegrinder.readthedocs.io)

# Community

Join our [telegram forum](https://t.me/botoforum).

# [Contributing](https://github.com/timoniq/telegrinder/blob/main/contributing.md)

# License

Telegrinder is [MIT licensed](./LICENSE)  
Copyright © 2022-2023 [timoniq](https://github.com/timoniq)