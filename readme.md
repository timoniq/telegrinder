<p align="center">
  <a href="https://github.com/timoniq/telegrinder">
    <img width="200px" height="145px" alt="Telegrinder" src="docs/logo.jpg">
  </a>
</p>

</p>
<h1 align="center">
  Telegrinder
</h1>

<p align="center">
    <em><b>Framework for effective and reliable telegram bot building.</b></em>
</p>

<p align="center">
  <a href="https://github.com/timoniq/telegrinder/actions/workflows/ci.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/timoniq/telegrinder/ci.yml?branch=dev&style=flat-square&labelColor=black
    ">
  </a>
  <a href="https://github.com/timoniq/telegrinderblob/main/LICENSE">
    <img src="https://img.shields.io/github/license/timoniq/telegrinder.svg?color=lightGreen&labelColor=black">
  </a>
  <a href="https://pypi.org/project/telegrinder/">
    <img src="https://img.shields.io/pypi/v/telegrinder.svg?labelColor=black">
  </a>
  <a href="https://docs.astral.sh/ruff/">
    <img src="https://img.shields.io/badge/linter-Ruff-D7FF64?logo=ruff&logoColor=fff&style=flat-square&labelColor=black">
  </a>
  <a href="https://pypi.org/project/telegrinder/">
    <img src="https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Ftimoniq%2Ftelegrinder%2Frefs%2Fheads%2Fmain%2Fpyproject.toml&style=flat-square&logo=python&logoColor=fff&labelColor=black">
  </a>
  <a href="https://core.telegram.org/bots/api">
    <img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Ftimoniq%2Ftelegrinder%2Frefs%2Fheads%2Fdev%2Ftypegen%2Fapi_types_version.json&query=%24.version&style=flat-square&logo=telegram&label=API%20types&labelColor=black&color=%23FBCA04">
  </a>
</p>


_Still in development._

* Type hinted
* Customizable and extensible
* Ready to use scenarios and rules
* Fast models built on [msgspec](https://github.com/jcrist/msgspec)
* Both low-level and high-level API
* Support [optional dependecies](https://github.com/timoniq/telegrinder/blob/dev/docs/guide/optional_dependencies.md)


# Getting started

Install using pip, uv and poetry:

```console
pip install telegrinder
```

```console
poetry add telegrinder
```

```console
uv add telegrinder
```

Install from [source](https://github.com/timoniq/telegrinder):

```console
pip install git+https://github.com/timoniq/telegrinder/archive/dev.zip
```

```console
uv add "telegrinder @ git+https://github.com/timoniq/telegrinder.git@dev"
```

```console
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
async def start(message: Message) -> None:
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
Copyright © 2022-2025 [timoniq](https://github.com/timoniq)\
Copyright © 2024-2025 [luwqz1](https://github.com/luwqz1)

# Contributors


<a href="https://github.com/timoniq/telegrinder/graphs/contributors">
 <img src="https://contributors-img.web.app/image?repo=timoniq/telegrinder" />
</a>
