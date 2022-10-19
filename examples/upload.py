from telegrinder import Telegrinder, API, Token, Keyboard, Button, Message
from telegrinder.rules import Text
import logging
import pathlib

api = API(token=Token.from_env())
bot = Telegrinder(api)
logging.basicConfig(level=logging.DEBUG)

kb = (Keyboard().add(Button("Button 1")).add(Button("Button 2"))).get_markup()
cool_bytes = pathlib.Path("assets/satie.jpeg").read_bytes()


@bot.on.message(Text("/photo"))
async def start(message: Message):
    await api.send_photo(
        message.chat.id, caption="Erik", photo=("satie.jpeg", cool_bytes)
    )


bot.run_forever()
