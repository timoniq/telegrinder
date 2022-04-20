from telegrinder import Telegrinder, API, Token, Keyboard, Button
from telegrinder.bot.rules import Text, IsMessage
from telegrinder.types import Update

api = API(token=Token("..."))
bot = Telegrinder(api)

kb = (Keyboard().add(Button("Button 1")).add(Button("Button 2"))).dict()


@bot.dispatch.handle(IsMessage(), Text("/start"))
async def start(update: Update):
    await api.send_message(
        chat_id=update.message.chat.id, reply_markup=kb, text="Hello!"
    )


bot.run_forever()
