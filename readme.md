# Telegrinder

Framework for effective and reliable telegram bot building.

Still in development.

* Type hinted
* Customizable and extensible
* Ready to use scenarios and rules
* Fast models built on msgspec
* Both low-level and high-level API

# Getting started

Install using pip:

```
pip install telegrinder
```

Using poetry:

```
poetry add telegrinder
```

Install from github:

```
pip install -U https://github.com/timoniq/telegrinder/archive/dev.zip
```

```
poetry add git+https://github.com/timoniq/telegrinder.git#dev
```

Basic example:

```python
from telegrinder import API, Message, Telegrinder, Token
from telegrinder.modules import logger
from telegrinder.rules import Text

logger.set_level("INFO")
api = API(token=Token("123:token"))
bot = Telegrinder(api)


@bot.on.message(Text("/start"))
async def start(message: Message):
    me = (await api.get_me()).unwrap()
    await message.answer(
        f"Hello, {message.from_user.full_name}! I'm {me.full_name}."
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
