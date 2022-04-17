# telegrinder

# Getting started

## Example

```python
from telegrinder import Telegrinder, API, Token
from telegrinder.bot.rules import Text
from telegrinder.types import Update
import logging

api = API(token=Token("123:token"))
bot = Telegrinder(api)
logging.basicConfig(level=logging.INFO)

@bot.on_message(Text("/start"))
async def start(update: Update):
    me = (await api.get_me()).unwrap()
    await api.send_message(
        chat_id=update.message.chat.id, 
        text=f"Hello, I'm {me.first_name}"
    )

bot.run_forever()
```

# Community

Join our [telegram chat](https://t.me/telegrinder_en).

# [Contributing](https://github.com/timoniq/telegrinder/blob/main/contributing.md)

# License

Telegrinder is [MIT licensed](./LICENSE)  
Copyright © 2022 [timoniq](https://github.com/timoniq)