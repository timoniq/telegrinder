from telegrinder import Telegrinder, API, Token, Keyboard, Button
from telegrinder.bot.rules import Text

api = API(token=Token("..."))
bot = Telegrinder(api)

kb = (Keyboard()
      .add(Button("Button 1"))
      .add(Button("Button 2"))).dict()


@bot.on_message(Text("/start"))
async def start(event: dict):
    message = event["message"]
    await api.request("sendMessage", {"chat_id": message["chat"]["id"],
                                      "reply_markup": kb,
                                      "text": "Hello!"})

bot.run_forever()
