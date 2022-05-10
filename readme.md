# telegrinder

# Getting started

## Example

```python
from telegrinder import Telegrinder, API, Token, Message
from telegrinder.bot.rules import Text
import logging

api = API(token=Token("123:token")) # recommended to use Token.from_env()
bot = Telegrinder(api)
logging.basicConfig(level=logging.INFO)

@bot.on.message(Text("/start"))
async def start(message: Message):
    me = (await api.get_me()).unwrap().first_name
    await message.answer(
        "Hello, {}! It's {}. How are you today?".format(message.from_.first_name, me),
    )
    m, _ = await bot.on.message.wait_for_message(message.chat.id)
    if m.text.lower() == "fine":
        await m.reply("Cool!")
    elif m.text.lower() == "bad":
        await m.reply("Oh, i wish i could help you with that. May be some sleep will help")

bot.run_forever()
```

# Community

Join our [telegram chat](https://t.me/telegrinder_en).

# [Contributing](https://github.com/timoniq/telegrinder/blob/main/contributing.md)

# License

Telegrinder is [MIT licensed](./LICENSE)  
Copyright © 2022 [timoniq](https://github.com/timoniq)