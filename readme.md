# Telegrinder

Framework for effective and reliable telegram bot building.

Still in development.

* Type hinted
* Customizable and extensible
* Ready to use scenarios and rules
* Fast models built on [msgspec](https://github.com/jcrist/msgspec)
* Both low-level and high-level API
* Support [optional dependecies](https://github.com/timoniq/telegrinder/blob/dev/docs/guide/optional_dependencies.md)

# Getting started

Install using pip:

```console
pip install telegrinder
```

Using poetry:

```console
poetry add telegrinder
```

Install from github:

```console
pip install -U https://github.com/timoniq/telegrinder/archive/dev.zip
```

```console
poetry add git+https://github.com/timoniq/telegrinder.git#dev
```

Basic example:

```python
from telegrinder import API, Message, Telegrinder, Token
from telegrinder.modules import logger
from telegrinder.rules import Text

api = API(token=Token("123:token"))
bot = Telegrinder(api)
logger.set_level("INFO")


@bot.on.message(Text("/start"))
async def start(message: Message):
    me = (await api.get_me()).unwrap()
    await message.answer(f"Hello, {message.from_user.full_name}! I'm {me.full_name}.")


bot.run_forever()
```

# Documentation

[Readthedocs](https://telegrinder.readthedocs.io)

# Community

Join our [telegram forum](https://t.me/botoforum).

# [Contributing](https://github.com/timoniq/telegrinder/blob/main/contributing.md)

# License

Telegrinder is [MIT licensed](./LICENSE)\
Copyright © 2022-2024 [timoniq](https://github.com/timoniq)\
Copyright © 2024 [luwqz1](https://github.com/luwqz1)

# Contributors

<a href="https://github.com/timoniq/telegrinder/graphs/contributors">
 <img src="https://contributors-img.web.app/image?repo=timoniq/telegrinder" />
</a>
