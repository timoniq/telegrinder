# telegrinder

## Example

```python
from telegrinder import Telegrinder, API, Token
from telegrinder.bot.rules import Text

api = API(token=Token("123:token"))
bot = Telegrinder(api)

@bot.on_message(Text("/start"))
async def start(event: dict):
    await api.request("sendMessage", {"chat_id": event["message"]["chat"]["id"], "text": "Hello!"})

bot.run_forever()
```

## Community

Join our [telegram chat](https://t.me/telegrinder_en).
