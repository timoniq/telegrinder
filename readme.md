<p align="center">
  <a href="https://github.com/timoniq/telegrinder">
    <img width="200px" height="145px" alt="Telegrinder" src="https://github.com/timoniq/telegrinder/blob/main/docs/logo.jpg">
  </a>
</p>

</p>
<h1>
  telegrinder
</h1>

<p>
— effective and reliable telegram bot building.</b></em>
</p>

<p>
  <a href="#license"><img alt="GitHub License" src="https://img.shields.io/github/license/timoniq/telegrinder.svg?color=lightGreen&labelColor=black"></img>
  <img alt="Linter" src="https://img.shields.io/badge/linter-Ruff-D7FF64?logo=ruff&logoColor=fff&style=flat-square&labelColor=black">
  <img alt="Python versions" src="https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Ftimoniq%2Ftelegrinder%2Frefs%2Fheads%2Fmain%2Fpyproject.toml&style=flat-square&logo=python&logoColor=fff&labelColor=black">
  <img alt="Telegram Bot API Version" src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Ftimoniq%2Ftelegrinder%2Frefs%2Fheads%2Fmain%2Ftypegen%2Fapi_types_version.json&query=%24.version&style=flat-square&logo=telegram&label=Telegram%20API%20v&labelColor=black&color=%23FBCA04">
</p>


Still in development.

* Type hinted
* Customizable and extensible
* Ready to use scenarios and rules
* Fast models built on [msgspec](https://github.com/jcrist/msgspec)
* Both low-level and high-level API
* Support [optional dependecies](https://github.com/timoniq/telegrinder/blob/dev/docs/guide/optional_dependencies.md)


Basic example:

```python
from telegrinder import API, Message, Telegrinder, Token
from telegrinder.modules import logger
from telegrinder.rules import Text

logger.set_level("INFO")
api = API(token=Token("123:token"))
bot = Telegrinder(api)


@bot.on.message(Text("/start"))
async def start(message: Message) -> None:
    me = (await api.get_me()).unwrap()
    await message.answer(f"Hello, {message.from_user.full_name}! I'm {me.full_name}.")


bot.run_forever()
```

# Getting started

Install using pip, uv or poetry:

  <img alt="PyPI Version" src="https://img.shields.io/pypi/v/telegrinder.svg?labelColor=black">

```console
pip install telegrinder
poetry add telegrinder
uv add telegrinder
```

Or install from source (unstable):

  <img alt="GitHub CI" src="https://img.shields.io/github/actions/workflow/status/timoniq/telegrinder/push.yml?branch=main&style=flat-square&labelColor=black&label=CI">

```console
pip install git+https://github.com/timoniq/telegrinder/archive/dev.zip
uv add "telegrinder @ git+https://github.com/timoniq/telegrinder.git@dev"
poetry add git+https://github.com/timoniq/telegrinder.git#dev
```

# Documentation

[Readthedocs](https://telegrinder.readthedocs.io)

# Community

Join our [telegram forum](https://t.me/botoforum).

# License

Telegrinder is [MIT licensed](./LICENSE)\
Copyright © 2022-2025 [timoniq](https://github.com/timoniq)\
Copyright © 2024-2025 [luwqz1](https://github.com/luwqz1)

# Contributors

[How to contribute](https://github.com/timoniq/telegrinder/blob/main/contributing.md)


<a href="https://github.com/timoniq/telegrinder/graphs/contributors">
 <img src="https://contributors-img.web.app/image?repo=timoniq/telegrinder" />
</a>
