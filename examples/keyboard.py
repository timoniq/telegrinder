from telegrinder import API, Button, Keyboard, Message, Telegrinder, Token
from telegrinder.rules import Text

api = API(token=Token.from_env())
bot = Telegrinder(api)

kb = (Keyboard().add(Button("Button 1")).add(Button("Button 2"))).get_markup()


@bot.on.message(Text("/start"))
async def start(message: Message):
    await api.send_message(chat_id=message.chat.id, reply_markup=kb, text="Hello!")


bot.run_forever()
