<p>
  <a href="https://github.com/timoniq/telegrinder">
    <img width="200px" height="145px" alt="Telegrinder" src="https://github.com/timoniq/telegrinder/blob/main/docs/logo.jpg">
  </a>
</p>

</p>
<h1>
  telegrinder
</h1>

<p>
— effective and reliable telegram bot building.
</p>

<p>
  <a href="#contributors"><img alt="Still in development" src="https://img.shields.io/badge/Still_in_development-E3956B?logo=textpattern&logoColor=fff&style=flat-square&color=black"></img></a>
  <a href="#license"><img alt="GitHub License" src="https://img.shields.io/github/license/timoniq/telegrinder.svg?color=lightGreen&labelColor=black&style=flat-square"></img></a>
  <a href="https://docs.astral.sh/ruff/"><img alt="Code Style" src="https://img.shields.io/badge/code_style-Ruff-D7FF64?logo=ruff&logoColor=fff&style=flat-square&labelColor=black"></img></a>
  <a href="https://docs.basedpyright.com/latest/"><img alt="Type Checker" src="https://img.shields.io/badge/types-basedpyright-black?logo=python&color=%23FBCA04&logoColor=edb641&labelColor=black&style=flat-square"></img></a>
  <a href="https://pypi.org/project/telegrinder/"><img alt="Python versions" src="https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Ftimoniq%2Ftelegrinder%2Frefs%2Fheads%2Fmain%2Fpyproject.toml&style=flat-square&logo=python&logoColor=fff&labelColor=black"></img></a>
  <a href="https://core.telegram.org/bots/api"><img alt="Telegram Bot API Version" src="https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2Ftimoniq%2Ftelegrinder%2Frefs%2Fheads%2Fmain%2Ftypegen%2Fconfig.toml&query=%24.telegram-bot-api.version&style=flat-square&logo=telegram&label=Telegram%20API&labelColor=black&color=%23FBCA04"></img></a>
</p>


* Type hinted & [type functional](https://github.com/timoniq/telegrinder/blob/dev/docs/tutorial/en/3_functional_bits.md)
* Customizable and extensible
* Ready to use scenarios, rules and [nodes](https://github.com/timoniq/telegrinder/blob/dev/docs/tutorial/en/5_nodes.md)
* Fast models built on [msgspec](https://github.com/jcrist/msgspec)
* Both low-level and high-level API


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

  <a href="https://pypi.org/project/telegrinder/"><img alt="PyPI Version" src="https://img.shields.io/pypi/v/telegrinder.svg?labelColor=black&style=flat-square&logo=pypi"></img></a>

```console
uv add telegrinder
poetry add telegrinder
pip install telegrinder
```

Or install from source (unstable):

  <a href="https://github.com/timoniq/telegrinder/actions/workflows/push.yml"><img alt="GitHub CI" src="https://img.shields.io/github/actions/workflow/status/timoniq/telegrinder/push.yml?branch=main&style=flat-square&labelColor=black&label=CI&logo=github"></img></a>

```console
uv add "telegrinder @ git+https://github.com/timoniq/telegrinder@dev"
poetry add git+https://github.com/timoniq/telegrinder.git#dev
pip install git+https://github.com/timoniq/telegrinder/archive/dev.zip
```

# Documentation

[Tutorial](/docs/tutorial/en/0_tutorial.md)

# Community

Join our [telegram forum](https://t.me/botoforum).

# License

Telegrinder is [MIT licensed](./LICENSE)\
Copyright © 2022 [timoniq](https://github.com/timoniq)\
Copyright © 2024 [luwqz1](https://github.com/luwqz1)

# Contributors

[How to contribute](https://github.com/timoniq/telegrinder/blob/main/contributing.md)


<a href="https://github.com/timoniq/telegrinder/graphs/contributors">
 <img src="https://contributors-img.web.app/image?repo=timoniq/telegrinder" />
</a>
