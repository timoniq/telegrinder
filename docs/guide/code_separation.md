# Code Separation

Telegrinder obtains a `Dispatch` class. It allows to separate code. You need to import `Dispatch` and later load it into the `Telegrinder` main dispatch.
```python
from telegrinder import Dispatch

dp = Dispatch()
```

Let's imagine a tree for our project:
```
telegram_bot
├── .env
├── __main__.py
├── handlers
│   ├── admin.py
│   ├── __init__.py
│   ├── ravioli.py
│   └── start.py
├── middlewares
│   └── chat_protect.py
└── rules
    ├── admins.py
    └── users.py
```

The `.env` file contains environment variables. Examples for `middlewares` and `handlers` folders' contents: [*Custom rule*](https://github.com/timoniq/telegrinder/blob/main/examples/custom_rule.py) and [*Middleware*](https://github.com/timoniq/telegrinder/blob/main/examples/middleware.py).

For example, let's write code in `start.py`:
```python
from telegrinder import Dispatch, Message
from telegrinder.rules import Text
from telegrinder.tools import HTMLFormatter

dp = Dispatch()


@dp.message(Text("/start"))
async def start(message: Message):
    await message.reply(
        HTMLFormatter("Hello, {:italic}!").format(message.from_.first_name),
        parse_mode=HTMLFormatter.PARSE_MODE,
    )
```

The other files are similar. Now let's gather them in the `handlers/__init__.py` file:
```python
from . import admin, ravioli, start

dps = (
    admin.dp,
    ravioli.dp,
    start.dp,
)
```

Let's upload `dps` from `handlers/__init__.py` to the Telegrinder's main dispatch in `__main__.py` file:
```python
import logging

from telegrinder import API, Telegrinder, Token
from handlers import dps

api = API(Token.from_env())
bot = Telegrinder(api)
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    for dp in dps:
        bot.dispatch.load(dp)
    bot.run_forever()
```
