import logging
import pathlib

from telegrinder import API, Button, Keyboard, Message, Telegrinder, Token
from telegrinder.rules import Text
from telegrinder.types import InputFile

api = API(token=Token.from_env())
bot = Telegrinder(api)
logging.basicConfig(level=logging.DEBUG)

kb = (Keyboard().add(Button("Button 1")).add(Button("Button 2"))).get_markup()
cool_bytes = pathlib.Path("assets/satie.jpeg").read_bytes()


@bot.on.message(Text("/photo"))
async def start(message: Message):
    await api.send_photo(
        message.chat.id, caption="Erik", photo=InputFile("satie.jpeg", cool_bytes)
    )


bot.run_forever()
