import pathlib

from telegrinder import API, Button, Keyboard, Message, Telegrinder, Token
from telegrinder.rules import Text
from telegrinder.types import InputFile
from telegrinder.modules import logger

api = API(token=Token.from_env())
bot = Telegrinder(api)
kb = (Keyboard().add(Button("Button 1")).add(Button("Button 2"))).get_markup()
cool_bytes = pathlib.Path("assets/satie.jpeg").read_bytes()

logger.set_level("INFO")


@bot.on.message(Text("/photo"))
async def start(message: Message):
    await message.answer_photo(
        InputFile("satie.jpeg", cool_bytes),
        caption="Erik",
    )


bot.run_forever()
