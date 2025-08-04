import pathlib

from telegrinder import API, Message, Telegrinder, Token
from telegrinder.bot.rules.is_from import IsPrivate
from telegrinder.rules import IsUser, Text
from telegrinder.types import InputFile

api = API(token=Token.from_env())
bot = Telegrinder(api)
cool_bytes = pathlib.Path("examples/assets/satie.jpeg").read_bytes()


@bot.on.message(Text("/photo"), IsPrivate() & IsUser())
async def start(message: Message):
    await message.answer_photo(
        InputFile("satie.jpeg", cool_bytes),
        caption="Erik",
    )


bot.run_forever()
