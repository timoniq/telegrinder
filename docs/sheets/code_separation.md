# Code separation

Telegrinder has a `Dispatch` class. It allows for code separation across files. From each file, you need to import the declared `Dispatch` and load it into the `Telegrinder` class.
```python
from telegrinder import Dispatch

dp = Dispatch()
# some code...
```

Let's imagine our project tree:
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

The `.env` file contains environment variables. In the `rules` and `middlewares` folders there are files with them. They are used by the handlers. Examples with them can be seen [*Custom rule*](https://github.com/timoniq/telegrinder/blob/main/examples/custom_rule.py) and [*Middleware*](https://github.com/timoniq/telegrinder/blob/main/examples/middleware.py).

For example, let's write the code in the file `start.py`:
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

The remaining files are similar. Now let's initialize them in the `__init__.py` file:
```python
import typing
import telegrinder

from . import admin, ravioli, start

dps: typing.Iterable["telegrinder.Dispatch"] = (
    admin.dp,
    ravioli.dp,
    start.dp,
)
```

Let's upload `dps` from `handlers/__init__.py` file to the Telegrinder class in `__main__.py` file:
```python
import logging

from telegrinder import API, Telegrinder, Token
from handlers import dps

api = API(Token.from_env())
bot = Telegrinder(api)
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    for dp in dps:
        bot.on.load(dp)
    bot.run_forever()
```
